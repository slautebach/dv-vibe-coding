"""
Dataverse Web API Client for Python

This module provides a Python client for interacting with Microsoft Dynamics 365 / Dataverse Web API.
Based on the PowerShell examples from: https://github.com/microsoft/PowerApps-Samples/tree/master/dataverse/webapi/PS

Features:
- Azure authentication (interactive and service principal)
- Persistent token caching (stored in OS keychain/keyring)
- Automatic token refresh when expired
- CRUD operations on Dataverse records
- FetchXML query support
- Metadata retrieval
- Automatic retry handling for 429 (Too Many Requests) errors
- File column support

Token Caching:
- Tokens are cached persistently using Azure Identity's TokenCachePersistenceOptions
- Interactive auth tokens are stored in the OS keychain (Windows Credential Manager, macOS Keychain, Linux Secret Service)
- Tokens are automatically reused across script invocations if still valid
- Token expiration is checked proactively (with 5-minute buffer) before each request
- No re-authentication required until token expires (typically 1 hour for Dataverse)

Usage:
    from dataverse_client import DataverseClient
    from config_loader import load_dataverse_config
    
    # Load environment config
    config = load_dataverse_config('dev')
    
    # Connect interactively (token cached for subsequent runs)
    client = DataverseClient(config['environment_url'])
    client.connect(tenant_id=config['tenant_id'])
    
    # Or connect with service principal
    client = DataverseClient(config['environment_url'])
    client.connect(
        app_id=config.get('app_id'),
        client_secret="...",
        tenant_id=config['tenant_id']
    )
    
    # Get records
    accounts = client.get_records("accounts", query="?$select=name&$top=10")
    
    # Get records with FetchXML
    results = client.get_records_with_fetchxml("accounts", "<fetch>...</fetch>")
"""

import requests
import json
import time
import urllib.parse
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from pathlib import Path
from azure.identity import InteractiveBrowserCredential, ClientSecretCredential, DefaultAzureCredential, TokenCachePersistenceOptions, AuthenticationRecord
from azure.core.credentials import AccessToken
import logging

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


class DataverseClient:
    """Client for interacting with Dataverse Web API"""
    
    DEFAULT_TENANT_ID = "fbef0798-20e3-4be7-bdc8-372032610f65"
    API_VERSION = "v9.2"
    MAX_RETRIES = 3
    AUTH_RECORD_FILE = Path.home() / ".dataverse" / "auth_record.json"
    
    def __init__(self, resource_url: str, debug: bool = False, proxy_url: Optional[str] = None):
        """
        Initialize the Dataverse client
        
        Args:
            resource_url: The Dataverse environment URL (e.g., https://yourorg.crm.dynamics.com)
            debug: Enable debug mode (uses proxy if specified)
            proxy_url: Proxy URL for debugging (e.g., http://127.0.0.1:8888 for Fiddler)
        """
        if not resource_url.endswith("/"):
            resource_url = resource_url + "/"
        
        self.resource_url = resource_url
        self.base_uri = f"{resource_url}api/data/{self.API_VERSION}/"
        self.debug = debug
        self.proxy_url = proxy_url
        self.credential = None
        self.base_headers = {}
        self._cached_token: Optional[AccessToken] = None
    
    def _get_auth_record_path(self, tenant_id: str) -> Path:
        """Get the path to the authentication record file for a specific tenant"""
        auth_dir = Path.home() / ".dataverse"
        auth_dir.mkdir(parents=True, exist_ok=True)
        # Use tenant-specific file to support multiple tenants
        return auth_dir / f"auth_record_{tenant_id}.json"
    
    def _save_auth_record(self, auth_record: AuthenticationRecord, tenant_id: str):
        """Save authentication record to file"""
        try:
            auth_file = self._get_auth_record_path(tenant_id)
            with open(auth_file, 'w') as f:
                # serialize() already returns a JSON string, write it directly
                f.write(auth_record.serialize())
            logger.info(f"Saved authentication record to {auth_file}")
        except Exception as e:
            logger.warning(f"Could not save authentication record: {e}")
    
    def _load_auth_record(self, tenant_id: str) -> Optional[AuthenticationRecord]:
        """Load authentication record from file"""
        try:
            auth_file = self._get_auth_record_path(tenant_id)
            if auth_file.exists():
                with open(auth_file, 'r') as f:
                    json_string = f.read()
                logger.info(f"Loaded cached authentication record from {auth_file}")
                return AuthenticationRecord.deserialize(json_string)
        except Exception as e:
            logger.warning(f"Could not load authentication record: {e}")
        return None
    
    def _clear_auth_record(self, tenant_id: str):
        """Clear saved authentication record to force re-authentication"""
        try:
            auth_file = self._get_auth_record_path(tenant_id)
            if auth_file.exists():
                auth_file.unlink()
                logger.info(f"Cleared authentication record from {auth_file}")
        except Exception as e:
            logger.warning(f"Could not clear authentication record: {e}")
        
    def connect(self, 
                app_id: Optional[str] = None, 
                client_secret: Optional[str] = None, 
                tenant_id: Optional[str] = None,
                use_default_credential: bool = False):
        """
        Connect to Dataverse Web API using Azure authentication
        
        Args:
            app_id: Application (client) ID for service principal authentication
            client_secret: Client secret for service principal authentication
            tenant_id: Tenant ID (defaults to DEFAULT_TENANT_ID if not specified)
            use_default_credential: Use DefaultAzureCredential (tries multiple auth methods)
        """
        logger.info(f"Connecting to Web API at: {self.resource_url}")
        
        tenant_id = tenant_id or self.DEFAULT_TENANT_ID
        
        # Determine authentication method
        if use_default_credential:
            logger.info("Using DefaultAzureCredential")
            # Enable persistent cache for token caching
            try:
                cache_options = TokenCachePersistenceOptions(allow_unencrypted_storage=True)
                self.credential = DefaultAzureCredential(cache_persistence_options=cache_options)
            except Exception as e:
                logger.warning(f"Could not enable token cache persistence: {e}")
                self.credential = DefaultAzureCredential()
        elif app_id and client_secret:
            logger.info(f"Connecting with AppId: '{app_id}', Tenant: {tenant_id}")
            # Enable persistent cache for token caching
            try:
                cache_options = TokenCachePersistenceOptions(allow_unencrypted_storage=True)
                self.credential = ClientSecretCredential(
                    tenant_id=tenant_id,
                    client_id=app_id,
                    client_secret=client_secret,
                    cache_persistence_options=cache_options
                )
            except Exception as e:
                logger.warning(f"Could not enable token cache persistence: {e}")
                self.credential = ClientSecretCredential(
                    tenant_id=tenant_id,
                    client_id=app_id,
                    client_secret=client_secret
                )
        else:
            logger.info("Connecting Interactively")
            # Enable persistent cache for token caching (stores in OS keychain/keyring)
            try:
                cache_options = TokenCachePersistenceOptions(allow_unencrypted_storage=True)
                
                # Try to load saved authentication record
                auth_record = self._load_auth_record(tenant_id)
                
                if auth_record:
                    logger.info("Using cached authentication record (no browser popup needed)")
                    self.credential = InteractiveBrowserCredential(
                        tenant_id=tenant_id,
                        cache_persistence_options=cache_options,
                        authentication_record=auth_record
                    )
                else:
                    logger.info("No cached authentication found - browser authentication required")
                    self.credential = InteractiveBrowserCredential(
                        tenant_id=tenant_id,
                        cache_persistence_options=cache_options
                    )
                    
                    # Authenticate and save the record for future use
                    logger.info("Authenticating to get authentication record...")
                    scope = self.resource_url.rstrip('/') + '/.default'
                    new_auth_record = self.credential.authenticate(scopes=[scope])
                    self._save_auth_record(new_auth_record, tenant_id)
                    logger.info("Authentication record saved - future runs will not require browser authentication")
                
                logger.info("Enabled persistent token cache (tokens stored in OS keychain)")
            except Exception as e:
                logger.warning(f"Could not enable token cache persistence: {e}")
                logger.warning("Tokens will only be cached in memory (lost on script exit)")
                self.credential = InteractiveBrowserCredential(tenant_id=tenant_id)
        
        # Get access token
        logger.info(f"Getting access token for: {self.resource_url}")
        token_obj = self._get_access_token()
        
        # Set base headers
        self.base_headers = {
            'Authorization': f'Bearer {token_obj.token}',
            'Accept': 'application/json',
            'OData-MaxVersion': '4.0',
            'OData-Version': '4.0'
        }
        
        logger.info("Connected successfully")
    
    def _get_access_token(self) -> AccessToken:
        """Get access token from Azure AD (uses cache if token is still valid)"""
        # Remove trailing slash for scope
        scope = self.resource_url.rstrip('/') + '/.default'
        
        # Azure Identity library handles caching internally
        # It will reuse cached tokens if they're still valid
        token = self.credential.get_token(scope)
        
        # Cache the token object so we can check expiration
        self._cached_token = token
        
        # Log token expiration time for debugging
        expiry_time = datetime.fromtimestamp(token.expires_on, tz=timezone.utc)
        logger.debug(f"Token expires at: {expiry_time} UTC")
        
        return token
    
    def _is_token_expired(self) -> bool:
        """Check if the cached token is expired or about to expire"""
        if not self._cached_token:
            return True
        
        # Check if token expires in the next 5 minutes (300 seconds buffer)
        current_time = datetime.now(timezone.utc).timestamp()
        time_until_expiry = self._cached_token.expires_on - current_time
        
        return time_until_expiry < 300
    
    def _refresh_token_if_needed(self):
        """Refresh the access token if expired or about to expire"""
        if self._is_token_expired():
            logger.debug("Token expired or expiring soon, refreshing...")
            token = self._get_access_token()
            self.base_headers['Authorization'] = f'Bearer {token.token}'
        else:
            logger.debug("Token still valid, using cached token")
    
    def _invoke_resilient_request(self, 
                                   method: str, 
                                   url: str, 
                                   headers: Optional[Dict[str, Any]] = None,
                                   body: Optional[Dict[str, Any]] = None,
                                   return_headers: bool = False) -> Any:
        """
        Invoke HTTP request with resilience to handle 429 errors
        
        Args:
            method: HTTP method (GET, POST, PATCH, DELETE, PUT)
            url: Request URL
            headers: Request headers
            body: Request body (will be JSON serialized)
            return_headers: Return response headers instead of body
            
        Returns:
            Response data or headers depending on return_headers
        """
        # Proactively refresh token if expired before making request
        self._refresh_token_if_needed()
        
        headers = headers or self.base_headers.copy()
        proxies = {'http': self.proxy_url, 'https': self.proxy_url} if self.debug and self.proxy_url else None
        
        retry_count = 0
        while retry_count <= self.MAX_RETRIES:
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=body,
                    proxies=proxies
                )
                
                # Handle 429 Too Many Requests
                if response.status_code == 429:
                    if retry_count < self.MAX_RETRIES:
                        retry_after = int(response.headers.get('Retry-After', 1))
                        logger.warning(f"Rate limited. Retrying after {retry_after} seconds...")
                        time.sleep(retry_after)
                        retry_count += 1
                        continue
                    else:
                        response.raise_for_status()
                
                # Handle 401 Unauthorized (token might be expired)
                if response.status_code == 401:
                    logger.info("Token expired, refreshing...")
                    self._refresh_token_if_needed()
                    headers['Authorization'] = self.base_headers['Authorization']
                    retry_count += 1
                    continue
                
                response.raise_for_status()
                
                if return_headers:
                    return response.headers
                
                # Return JSON if available
                if response.content:
                    return response.json()
                return None
                
            except requests.exceptions.HTTPError as e:
                logger.error(f"HTTP Error: {e}")
                logger.error(f"Response: {e.response.text if e.response else 'No response'}")
                raise
            except requests.exceptions.RequestException as e:
                logger.error(f"Request Exception: {e}")
                raise
        
        raise Exception(f"Max retries ({self.MAX_RETRIES}) exceeded")
    
    def get_records(self, 
                   set_name: str, 
                   query: Optional[str] = None) -> Dict[str, Any]:
        """
        Get a set of records from a Dataverse table
        
        Args:
            set_name: The entity set name (plural form, e.g., 'accounts')
            query: Optional query parameters (e.g., '?$select=name&$top=10')
            
        Returns:
            Dictionary with 'value' key containing list of records
            
        Example:
            accounts = client.get_records('accounts', '?$select=name&$top=10')
            for account in accounts['value']:
                print(account['name'])
        """
        uri = self.base_uri + set_name
        if query:
            uri = uri + query
        
        logger.info(f"GET {uri}")
        
        headers = self.base_headers.copy()
        headers['If-None-Match'] = 'null'
        headers['Prefer'] = 'odata.include-annotations="*"'
        
        return self._invoke_resilient_request('GET', uri, headers)
    
    def get_records_with_fetchxml(self, 
                                  set_name: str, 
                                  fetch_xml: str) -> Dict[str, Any]:
        """
        Get records using FetchXML query
        
        Args:
            set_name: The entity set name (plural form)
            fetch_xml: FetchXML query string
            
        Returns:
            Dictionary with 'value' key containing list of records
            
        Example:
            fetch = '''
            <fetch top="10">
                <entity name="account">
                    <attribute name="name"/>
                </entity>
            </fetch>
            '''
            accounts = client.get_records_with_fetchxml('accounts', fetch)
        """
        # Minify XML (remove all unnecessary whitespace between tags)
        import re
        fetch_xml = re.sub(r'>\s+<', '><', fetch_xml.strip())
        
        # URL encode the FetchXML
        encoded_fetch = urllib.parse.quote(fetch_xml)
        
        uri = f"{self.base_uri}{set_name}?fetchXml={encoded_fetch}"
        
        logger.info(f"GET {uri}")
        
        headers = self.base_headers.copy()
        headers['If-None-Match'] = 'null'
        headers['Prefer'] = 'odata.include-annotations="*"'
        
        return self._invoke_resilient_request('GET', uri, headers)
    
    def get_record(self, 
                   set_name: str, 
                   record_id: str, 
                   query: Optional[str] = None) -> Dict[str, Any]:
        """
        Get a single record by ID
        
        Args:
            set_name: The entity set name
            record_id: The GUID of the record
            query: Optional query parameters (e.g., '?$select=name')
            
        Returns:
            Record data dictionary
        """
        uri = f"{self.base_uri}{set_name}({record_id})"
        if query:
            uri = uri + query
        
        logger.info(f"GET {uri}")
        
        headers = self.base_headers.copy()
        headers['If-None-Match'] = 'null'
        headers['Prefer'] = 'odata.include-annotations="*"'
        
        return self._invoke_resilient_request('GET', uri, headers)
    
    def create_record(self, 
                     set_name: str, 
                     data: Dict[str, Any]) -> str:
        """
        Create a new record
        
        Args:
            set_name: The entity set name
            data: Dictionary of field values
            
        Returns:
            GUID of the created record
            
        Example:
            contact_id = client.create_record('contacts', {
                'firstname': 'John',
                'lastname': 'Doe'
            })
        """
        uri = self.base_uri + set_name
        
        logger.info(f"POST {uri}")
        
        headers = self.base_headers.copy()
        headers['Content-Type'] = 'application/json'
        
        response_headers = self._invoke_resilient_request(
            'POST', uri, headers, data, return_headers=True
        )
        
        # Extract ID from OData-EntityId header
        entity_id_url = response_headers.get('OData-EntityId', '')
        # Extract GUID from URL like: https://org.crm.dynamics.com/api/data/v9.2/contacts(guid)
        start = entity_id_url.rfind('(') + 1
        end = entity_id_url.rfind(')')
        return entity_id_url[start:end]
    
    def update_record(self, 
                     set_name: str, 
                     record_id: str, 
                     data: Dict[str, Any]) -> None:
        """
        Update an existing record
        
        Args:
            set_name: The entity set name
            record_id: The GUID of the record
            data: Dictionary of field values to update
        """
        uri = f"{self.base_uri}{set_name}({record_id})"
        
        logger.info(f"PATCH {uri}")
        
        headers = self.base_headers.copy()
        headers['Content-Type'] = 'application/json'
        headers['If-Match'] = '*'  # Prevent create if not exists
        
        self._invoke_resilient_request('PATCH', uri, headers, data)
    
    def delete_record(self, 
                     set_name: str, 
                     record_id: str) -> None:
        """
        Delete a record
        
        Args:
            set_name: The entity set name
            record_id: The GUID of the record
        """
        uri = f"{self.base_uri}{set_name}({record_id})"
        
        logger.info(f"DELETE {uri}")
        
        self._invoke_resilient_request('DELETE', uri)
    
    def get_column_value(self, 
                        set_name: str, 
                        record_id: str, 
                        property_name: str) -> Any:
        """
        Get the value of a single property
        
        Args:
            set_name: The entity set name
            record_id: The GUID of the record
            property_name: The name of the property
            
        Returns:
            The property value
        """
        uri = f"{self.base_uri}{set_name}({record_id})/{property_name}"
        
        logger.info(f"GET {uri}")
        
        headers = self.base_headers.copy()
        headers['If-None-Match'] = 'null'
        
        result = self._invoke_resilient_request('GET', uri, headers)
        return result.get('value')
    
    def set_column_value(self, 
                        set_name: str, 
                        record_id: str, 
                        property_name: str, 
                        value: Any) -> None:
        """
        Set the value of a single property
        
        Args:
            set_name: The entity set name
            record_id: The GUID of the record
            property_name: The name of the property
            value: The new value
        """
        uri = f"{self.base_uri}{set_name}({record_id})/{property_name}"
        
        logger.info(f"PUT {uri}")
        
        headers = self.base_headers.copy()
        headers['Content-Type'] = 'application/json'
        
        body = {'value': value}
        
        self._invoke_resilient_request('PUT', uri, headers, body)
    
    def get_entity_metadata(self, entity_logical_name: str) -> Dict[str, Any]:
        """
        Get metadata for a specific entity
        
        Args:
            entity_logical_name: The logical name of the entity (e.g., 'account')
            
        Returns:
            Entity metadata dictionary
        """
        uri = f"{self.base_uri}EntityDefinitions(LogicalName='{entity_logical_name}')"
        
        logger.info(f"GET {uri}")
        
        return self._invoke_resilient_request('GET', uri)
    
    def get_entity_attributes(self, entity_logical_name: str) -> List[Dict[str, Any]]:
        """
        Get attributes (fields) metadata for an entity
        
        Args:
            entity_logical_name: The logical name of the entity
            
        Returns:
            List of attribute metadata dictionaries
        """
        uri = f"{self.base_uri}EntityDefinitions(LogicalName='{entity_logical_name}')/Attributes"
        
        logger.info(f"GET {uri}")
        
        result = self._invoke_resilient_request('GET', uri)
        return result.get('value', [])
    
    def get_all_entity_metadata(self) -> List[Dict[str, Any]]:
        """
        Get metadata for all entities
        
        Returns:
            List of entity metadata dictionaries
        """
        uri = f"{self.base_uri}EntityDefinitions"
        
        logger.info(f"GET {uri}")
        
        result = self._invoke_resilient_request('GET', uri)
        return result.get('value', [])
    
    def post_action(self, 
                   action_name: str, 
                   data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a Dataverse action
        
        Args:
            action_name: The name of the action
            data: Action parameters
            
        Returns:
            Action response
        """
        uri = self.base_uri + action_name
        
        logger.info(f"POST {uri}")
        
        headers = self.base_headers.copy()
        headers['Content-Type'] = 'application/json'
        
        return self._invoke_resilient_request('POST', uri, headers, data)
    
    def who_am_i(self) -> Dict[str, Any]:
        """
        Execute WhoAmI function to get current user info
        
        Returns:
            Dictionary with UserId, BusinessUnitId, OrganizationId
        """
        uri = f"{self.base_uri}WhoAmI"
        
        logger.info(f"GET {uri}")
        
        return self._invoke_resilient_request('GET', uri)


# Convenience functions for common operations

def connect_to_dataverse(environment_url: str, 
                         app_id: Optional[str] = None,
                         client_secret: Optional[str] = None,
                         tenant_id: Optional[str] = None) -> DataverseClient:
    """
    Convenience function to connect to Dataverse
    
    Args:
        environment_url: Dataverse environment URL
        app_id: Optional app ID for service principal auth
        client_secret: Optional client secret for service principal auth
        tenant_id: Optional tenant ID
        
    Returns:
        Connected DataverseClient instance
    """
    client = DataverseClient(environment_url)
    client.connect(app_id=app_id, client_secret=client_secret, tenant_id=tenant_id)
    return client
