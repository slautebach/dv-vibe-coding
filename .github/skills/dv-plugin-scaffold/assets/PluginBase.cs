// ============================================================
// PluginBase.cs
// MNP base plugin pattern — copy to MNP.{Solution}.Plugins
// Targets .NET Framework 4.6.2
// NuGet: Microsoft.CrmSdk.CoreAssemblies
// ============================================================
using System;
using Microsoft.Xrm.Sdk;

namespace MNP.SOLUTION.Plugins
{
    /// <summary>
    /// Abstract base class for all MNP plugins.
    /// Implements IPlugin and exposes a strongly-typed LocalPluginContext
    /// so derived classes never need to resolve services manually.
    /// </summary>
    public abstract class PluginBase : IPlugin
    {
        private readonly string _childClassName;

        // Optional configuration strings set in the Plugin Registration Tool step.
        protected string UnsecureConfig { get; }
        protected string SecureConfig   { get; }

        protected PluginBase(Type childClassName, string unsecureConfig = null, string secureConfig = null)
        {
            _childClassName = childClassName?.ToString() ?? throw new ArgumentNullException(nameof(childClassName));
            UnsecureConfig  = unsecureConfig;
            SecureConfig    = secureConfig;
        }

        // -------------------------------------------------------
        // IPlugin.Execute — entry point called by Dataverse
        // -------------------------------------------------------
        public void Execute(IServiceProvider serviceProvider)
        {
            if (serviceProvider == null) throw new ArgumentNullException(nameof(serviceProvider));

            var localContext = new LocalPluginContext(serviceProvider);
            localContext.Trace($"Entered {_childClassName}.Execute()");

            try
            {
                ExecuteDataversePlugin(localContext);
                localContext.Trace($"Exiting {_childClassName}.Execute()");
            }
            catch (InvalidPluginExecutionException)
            {
                throw; // propagate user-visible validation errors as-is
            }
            catch (Exception ex)
            {
                localContext.Trace($"Exception in {_childClassName}: {ex}");
                throw new InvalidPluginExecutionException(
                    $"An unexpected error occurred in {_childClassName}. " +
                    $"Please contact your system administrator. Detail: {ex.Message}", ex);
            }
        }

        /// <summary>Override this method to implement plugin logic.</summary>
        protected abstract void ExecuteDataversePlugin(ILocalPluginContext localContext);

        // -------------------------------------------------------
        // ILocalPluginContext — public surface for derived classes
        // -------------------------------------------------------
        public interface ILocalPluginContext
        {
            IPluginExecutionContext     PluginExecutionContext              { get; }
            IOrganizationService        InitiatingUserOrganizationService  { get; }
            IOrganizationService        OrganizationService                { get; }
            ITracingService             TracingService                     { get; }
            void Trace(string message);
        }

        // -------------------------------------------------------
        // LocalPluginContext — concrete implementation
        // -------------------------------------------------------
        protected class LocalPluginContext : ILocalPluginContext
        {
            private readonly IOrganizationServiceFactory _serviceFactory;

            public IPluginExecutionContext  PluginExecutionContext             { get; }
            public ITracingService          TracingService                     { get; }
            public IOrganizationService     InitiatingUserOrganizationService  { get; }
            public IOrganizationService     OrganizationService                { get; }

            public LocalPluginContext(IServiceProvider serviceProvider)
            {
                if (serviceProvider == null) throw new ArgumentNullException(nameof(serviceProvider));

                PluginExecutionContext = (IPluginExecutionContext)
                    serviceProvider.GetService(typeof(IPluginExecutionContext));

                TracingService = (ITracingService)
                    serviceProvider.GetService(typeof(ITracingService));

                _serviceFactory = (IOrganizationServiceFactory)
                    serviceProvider.GetService(typeof(IOrganizationServiceFactory));

                // Service acting as the user who triggered the event
                InitiatingUserOrganizationService =
                    _serviceFactory.CreateOrganizationService(PluginExecutionContext.InitiatingUserId);

                // Service acting as the system account (SYSTEM)
                OrganizationService =
                    _serviceFactory.CreateOrganizationService(null);
            }

            public void Trace(string message)
            {
                if (string.IsNullOrWhiteSpace(message) || TracingService == null) return;
                TracingService.Trace(message);
            }

            // -------------------------------------------------------
            // Image helpers
            // -------------------------------------------------------

            /// <summary>Returns the pre-image registered as <paramref name="imageName"/> or null.</summary>
            public Entity GetPreImage(string imageName = "PreImage")
            {
                return PluginExecutionContext.PreEntityImages.Contains(imageName)
                    ? PluginExecutionContext.PreEntityImages[imageName]
                    : null;
            }

            /// <summary>Returns the post-image registered as <paramref name="imageName"/> or null.</summary>
            public Entity GetPostImage(string imageName = "PostImage")
            {
                return PluginExecutionContext.PostEntityImages.Contains(imageName)
                    ? PluginExecutionContext.PostEntityImages[imageName]
                    : null;
            }

            // -------------------------------------------------------
            // Parameter helpers
            // -------------------------------------------------------

            /// <summary>Reads a typed input parameter. Returns default(T) if not present.</summary>
            public T GetInputParameter<T>(string parameterName)
            {
                return PluginExecutionContext.InputParameters.Contains(parameterName)
                    ? (T)PluginExecutionContext.InputParameters[parameterName]
                    : default;
            }

            /// <summary>Writes a typed output parameter.</summary>
            public void SetOutputParameter(string parameterName, object value)
            {
                PluginExecutionContext.OutputParameters[parameterName] = value;
            }
        }
    }
}
