# North52 Business Process Activities Complete Reference

> **🔧 About this reference**: This document covers North52's Process Genie business process activities and workflow actions.  
> **📚 For formula functions**, see [north52-functions-complete.md](north52-functions-complete.md) (complete list) or [north52-functions.md](north52-functions.md) (examples and tips).

This document provides a comprehensive list of all **523 Business Process Activities (BPA)** documentation articles with direct links to official North52 documentation.

**Last Updated**: February 17, 2026  
**Source**: https://support.north52.com/knowledgebase/business-process-activities/

---

## Table of Contents

- [North52 Business Process Activities Complete Reference](#north52-business-process-activities-complete-reference)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Installation \& Configuration](#installation--configuration)
  - [General](#general)
  - [Formula Manager](#formula-manager)
  - [Decision Tables](#decision-tables)
  - [Process Genie](#process-genie)
  - [Scheduler](#scheduler)
  - [Smart Flow](#smart-flow)
  - [WebFusion](#webfusion)
  - [xCache](#xcache)
  - [Showcase Apps - Quick Button](#showcase-apps---quick-button)
  - [Showcase Apps - Quick Ribbon](#showcase-apps---quick-ribbon)
  - [Showcase Apps - Quick Tile](#showcase-apps---quick-tile)
  - [Power Pages / Dynamics Portals](#power-pages--dynamics-portals)
  - [Training Videos - Legacy](#training-videos---legacy)
  - [Troubleshooting](#troubleshooting)
  - [xRM Formula Samples](#xrm-formula-samples)
    - [AutoNumber \& ID Generation](#autonumber--id-generation)
    - [Business Process Flows](#business-process-flows)
    - [Client-Side Functionality](#client-side-functionality)
    - [Cloning \& Record Creation](#cloning--record-creation)
    - [Complex Calculations \& Decision Tables](#complex-calculations--decision-tables)
    - [Date \& Time Operations](#date--time-operations)
    - [Email \& Communication](#email--communication)
    - [GeoLocation \& Mapping](#geolocation--mapping)
    - [Integration \& Web Services](#integration--web-services)
    - [N:N Relationships](#nn-relationships)
    - [Power Pages / Portal Samples](#power-pages--portal-samples)
    - [Quick Button Samples](#quick-button-samples)
    - [Rollups \& Aggregations](#rollups--aggregations)
    - [SharePoint Integration](#sharepoint-integration)
    - [Validation \& Data Quality](#validation--data-quality)
    - [AI \& Modern Features](#ai--modern-features)
    - [Industry-Specific Examples](#industry-specific-examples)
  - [Additional Resources](#additional-resources)
  - [Usage Notes](#usage-notes)

---

## Introduction

Getting started with North52 Business Process Activities and understanding the core concepts.

| Article | Level | Reading Time | Link |
|---------|-------|--------------|------|
| Introduction to North52 BPA | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02044-dynamics-crm-365-Introduction-to-North52-BPA/en-us) |
| Anatomy of a Formula | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02046-dynamics-crm-365-Anatomy-of-a-Formula/en-us) |
| Architecture of North52 BPA | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02047-dynamics-crm-365-Architecture-of-North52-BPA/en-us) |
| Getting Started Guide - N52 Formula Manager | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02045-dynamics-crm-365-Getting-Started-Guide-N52-Formula-Manager/en-us) |
| Introduction to North52's Formula Manager | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-02166-dynamics-crm-365-Introduction-to-North52s-Formula-Manager/en-us) |
| Introduction to North52's Decision Tables | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-02128-dynamics-crm-365-Introduction-to-North52s-Decision-Tables/en-us) |
| Introduction to North52's Process Genie | Beginner | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01974-dynamics-crm-365-Introduction-to-North52s-Process-Genie/en-us) |
| Introduction to North52's Scheduler Manager | Beginner | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01976-dynamics-crm-365-Introduction-to-North52s-Scheduler-Manager/en-us) |
| Introduction to North52's SmartFlow | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-02130-dynamics-crm-365-Introduction-to-North52s-Smartflow/en-us) |
| Introduction to North52's WebFusion | Intermediate | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01970-dynamics-crm-365-Introduction-to-North52s-WebFusion/en-us) |
| Introduction to North52's xCache | Beginner | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01963-dynamics-crm-365-Introduction-to-North52s-xCache/en-us) |
| Timezones and how they work with North52 Functions | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10180-dynamics-crm-365-Timezones-and-how-they-work-with-North52-Functions/en-us) |

---

## Installation & Configuration

Installing, configuring, and upgrading North52 BPA.

| Article | Level | Reading Time | Link |
|---------|-------|--------------|------|
| Installation and Configuration | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02065-dynamics-crm-365-Install-and-Configuration/en-us) |
| How to - Accept the license agreement | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02066-dynamics-crm-365-How-to-Accept-the-license-agreement/en-us) |
| How to - Apply your license key | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02067-dynamics-crm-365-How-to-Apply-your-license-key/en-us) |
| How to - Retrieve Unique Organization ID | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02068-dynamics-crm-365-How-to-Retrieve-Unique-Organization-ID/en-us) |
| How to - Uninstall - North52 BPA | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02069-dynamics-crm-365-How-to-Uninstall-North52-BPA/en-us) |
| How to - Upgrade North52 Decision Suite | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02089-dynamics-crm-365-How-to-Upgrade-North52/en-us) |
| North52 - Bulk Delete System Jobs | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02070-dynamics-crm-365-North52-Bulk-Delete-System-Jobs/en-us) |
| How To - Publish Process | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10510-dynamics-crm-365-How-To-Publish-Process/en-us) |
| Azure DevOps - Deploying North52 Solutions from an Azure Pipeline | Intermediate | 2 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-10372-dynamics-crm-365-Azure-Devops-Deploying-North52-from-an-Azure-Pipeline/en-us) |
| Guidelines for North52 Deployment with Power Objects ALM tools | Intermediate | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10547-dynamics-crm-365-Guidelines-for-North52-Deployment-with-Power-Objects-ALM-tools/en-us) |

---

## General

General guides, FAQs, and best practices for using North52 BPA.

| Article | Level | Reading Time | Link |
|---------|-------|--------------|------|
| North52 BPA - FAQ | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02048-dynamics-crm-365-North52-BPA-FAQ/en-us) |
| North52 BPA - Upgrades | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02058-dynamics-crm-365-North52-BPA-Upgrades/en-us) |
| North52 Business Process Activities - Release History | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02049-dynamics-crm-365-North52-Business-Process-Activities-Release-History/en-us) |
| North52 Special Character Handling | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02057-dynamics-crm-365-North52-Special-Character-Handling/en-us) |
| Deprecated Features & Functions | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02056-dynamics-crm-365-Deprecated-Features-and-Functions/en-us) |
| How to - Categorize Formulas | Beginner | 2 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-10339-dynamics-crm-365-How-To-Categorize-Formulas/en-us) |
| How to - Execution Order | Beginner | 2 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-10342-dynamics-crm-365-How-To-Execution-Order/en-us) |
| How to - Formula Summary | Beginner | 2 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-10520-dynamics-crm-365-How-to-Formula-Summary/en-us) |
| How to - Formula Summary Generated by AI | Beginner | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-10597-dynamics-crm-365-How-to-Formula-Summary-Generated-by-AI/en-us) |
| How to - Handle NULL or Empty values with North52 BPA | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02054-dynamics-crm-365-How-to-Handle-NULL-or-Empty-values-with-North52-BPA/en-us) |
| How to - Set Null or Empty values | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02055-dynamics-crm-365-How-to-Set-Null-or-Empty-values/en-us) |
| How to - Using Advanced Fetch-XML with North52 | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02053-dynamics-crm-365-How-to-Using-Advanced-Fetch-XML-with-North52/en-us) |
| How to - Refresh the Entity List | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02051-dynamics-crm-365-How-to-Refresh-the-Entity-List/en-us) |
| How to - North52 BPA Deployment | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02050-dynamics-crm-365-How-to-North52-BPA-Deployment/en-us) |
| How to - Change deployment Solution | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10072-dynamics-crm-365-How-to-Change-deployment-Solution/en-us) |
| How to - Deploy Power Pages site with North52 via Power Platform Pipeline | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10555-dynamics-crm-365-How-to-Deploy-Power-Pages-site-with-North52-via-Power-Platform-Pipeline/en-us) |
| Deleting North52 Formula from a managed solution | Advanced | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10129-dynamics-crm-365-Deleting-North52-Formula-from-a-managed-solution/en-us) |
| Top 5 Productivity Tips when Using North52 | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10573-dynamics-crm-365-Top-5-Productivity-Tips-when-Using-North52/en-us) |
| Upgrading to version 1.0.0.328 | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02059-dynamics-crm-365-Upgrading-to-version-100328/en-us) |
| Upgrading to version 1.0.0.616 or higher | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10435-dynamics-crm-365-Upgrading-to-version-100616/en-us) |
| Spotlight on Insurance - Commission for Brokers/Agencies | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10238-dynamics-crm-365-Spotlight-on-Insurance-Commission-for-Brokers/en-us) |

---

## Formula Manager

Guides specific to the Formula Manager module.

| Article | Level | Reading Time | Link |
|---------|-------|--------------|------|
| Chaining - Business Logic / Rules / Formulas | Intermediate | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10337-dynamics-crm-365-Chaining-Business-Logic---Rules---Formulas/en-us) |
| North52 Performance - 500 updates using Decision Logic and 2500 fields across 5 entities | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-10386-dynamics-crm-365-North52-Performance-500-updates-using-Decision-Logic-and-2500-fields-across-5-entities/en-us) |
| Using Azure App Insights to analyse North52 Formula performance | Intermediate | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10522-dynamics-crm-365-Using-Azure-App-Insights-to-analyse-North52-Formula-performance/en-us) |

---

## Decision Tables

How-to guides and tutorials for working with Decision Tables.

| Article | Level | Reading Time | Link |
|---------|-------|--------------|------|
| DT - How to - 01 - Decision Tables Overview | Beginner | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01942-dynamics-crm-365-DT-How-to-01-Decision-Tables-Overview/en-us) |
| DT - How to - 10 - Introduction to Multi-Sheet Decision Tables | Beginner | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01949-dynamics-crm-365-DT-How-to-10-Introduction-to-Multi-Sheet-Decision-Tables/en-us) |
| DT - How to - 12 - Use Global Fetch XML Sheet | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10165-dynamics-crm-365-DT-How-to-12-Use-Global-Fetch-XML-Sheet/en-us) |
| DT - How to - 13 - Global Actions sheet | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10171-dynamics-crm-365-DT-How-to-13-Global-Actions-sheet/en-us) |
| DT - How to - 14 - Global Calculation sheet | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10166-dynamics-crm-365-DT-How-to-14-Global-Calculation-sheet/en-us) |
| DT - How to - 15 - Source tab | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10169-dynamics-crm-365-DT-How-to-15-Source-tab/en-us) |
| DT - How to - 16 - Use the Validator | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10167-dynamics-crm-365-DT-How-to-16-Use-the-Validator/en-us) |
| DT - How to - 17 - Tester (execute Formula from the editor) | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10168-dynamics-crm-365-DT-How-to-17-Tester-(execute-Formula-from-the-editor)/en-us) |

---

## Process Genie

Guides for using Process Genie with workflows.

| Article | Level | Reading Time | Link |
|---------|-------|--------------|------|
| Process Genie Sample - Managing Case Service Level Agreements (SLAs) | Beginner | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01975-dynamics-crm-365-Process-Genie-Sample-Managing-Case-Service-Level-Agreements-(SLAs)/en-us) |

---

## Scheduler

Working with the North52 Scheduler module.

| Article | Level | Reading Time | Link |
|---------|-------|--------------|------|
| Anatomy of a Schedule | Beginner | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01977-dynamics-crm-365-Anatomy-of-a-Schedule/en-us) |
| Anatomy of a Schedule - Advanced View | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-02184-dynamics-crm-365-Anatomy-of-a-Schedule-Advanced-View/en-us) |
| How To #1 - Create Your First Schedule | Beginner | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01978-dynamics-crm-365-How-To-1-Create-Your-First-Schedule/en-us) |
| How To #2 - Execute Schedule only in Working Hours | Beginner | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01979-dynamics-crm-365-How-To-2-Execute-Schedule-only-in-Working-Hours/en-us) |
| How To #3 - Deploying Schedules | Beginner | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01980-dynamics-crm-365-How-To-3-Deploying-Schedules/en-us) |
| Dynamics 365 Upgrades - North52 Scheduler | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10063-dynamics-crm-365-Dynamics-365-Upgrades-North52-Scheduler/en-us) |
| Troubleshooting #00 - Platform Limitations | Beginner | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01981-dynamics-crm-365-Troubleshooting-00-Platform-Limitations/en-us) |

---

## Smart Flow

Documentation for SmartFlow functionality.

| Article | Level | Reading Time | Link |
|---------|-------|--------------|------|
| Introduction to North52's Smartflow | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-02130-dynamics-crm-365-Introduction-to-North52s-Smartflow/en-us) |

---

## WebFusion

REST API integration and web service calling.

| Article | Level | Reading Time | Link |
|---------|-------|--------------|------|
| CallRestAPI - Scenario 1 - Send an SMS Message | Intermediate | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01971-dynamics-crm-365-CallRestAPI-Scenario-1-Send-an-SMS-Message/en-us) |
| CallRestAPI - Scenario 2 - Generate a PDF document | Intermediate | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01972-dynamics-crm-365-CallRestAPI-Scenario-2-Generate-a-PDF-document/en-us) |
| CallRestAPI - Scenario 3 - REST API Call using a JSON Object | Intermediate | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01973-dynamics-crm-365-CallRestAPI-Scenario-3-REST-API-Call-using-a-JSON-Object/en-us) |

---

## xCache

Using xCache for performance optimization.

| Article | Level | Reading Time | Link |
|---------|-------|--------------|------|
| xCache - General Information | Intermediate | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01964-dynamics-crm-365-xCache-General-Information/en-us) |
| xCache - Scenario 1 - Static Configuration Data | Intermediate | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01965-dynamics-crm-365-xCache-Scenario-1-Static-Configuration-Data/en-us) |
| xCache - Scenario 2 - Organization Name Dependence | Intermediate | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01966-dynamics-crm-365-xCache-Scenario-2-Organization-Name-Dependence/en-us) |
| xCache - Scenario 3 - Work Day Shift Patterns | Intermediate | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01967-dynamics-crm-365-xCache-Scenario-3-Work-Day-Shift-Patterns/en-us) |
| xCache - Scenario 4 - Time Dependence | Intermediate | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01968-dynamics-crm-365-xCache-Scenario-4-Time-Dependence/en-us) |
| xCache - Scenario 5 - Multi-Language | Intermediate | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01969-dynamics-crm-365-xCache-Scenario-5-Multi-Language/en-us) |

---

## Showcase Apps - Quick Button

Building and configuring Quick Buttons.

| Article | Level | Reading Time | Link |
|---------|-------|--------------|------|
| North52 App - Quick Button | Intermediate | 60 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01953-dynamics-crm-365-North52-App-Quick-Button/en-us) |
| North52 App - Quick Button Subgrid | Beginner | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02175-dynamics-crm-365-North52-App-Quick-Button-Subgrid/en-us) |
| North52 App - Quick Button UCI | Beginner | 60 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-10021-dynamics-crm-365-North52-App-Quick-Button-UCI/en-us) |
| Quick Button Unified Interface - Styles and Advanced Settings | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10030-dynamics-crm-365-Quick-Button-Unified-Interface-Styles/en-us) |

---

## Showcase Apps - Quick Ribbon

Building custom ribbon buttons.

| Article | Level | Reading Time | Link |
|---------|-------|--------------|------|
| North52 App - Quick Ribbon - Enable or Disable - Button on Form | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10263-dynamics-crm-365-North52-App-Quick-Ribbon-Enable-or-Disable-Button-on-Form/en-us) |
| North52 App - Quick Ribbon - Enable or Disable - Button on ListView | Intermediate | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10264-dynamics-crm-365-North52-App-Quick-Ribbon-Enable-or-Disable-Button-on-ListView-Unified-Interface/en-us) |
| North52 App - Quick Ribbon - Execute Formula - Button on ListView | Intermediate | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10262-dynamics-crm-365-North52-App-Quick-Ribbon-Execute-Formula-Button-on-ListView-Unified-Interface/en-us) |
| North52 App - Quick Ribbon - Execute Formula - No Selected Records | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10568-dynamics-crm-365-North52-App-Quick-Ribbon-Execute-Formula-No-Selected-Records/en-us) |
| North52 App - Quick Ribbon - Execute Formula - Selected records in a List or SubGrid - Batch Mode | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10569-dynamics-crm-365-North52-App-Quick-Ribbon-Execute-Formula-Selected-records-in-a-List-or-SubGrid-Batch-Mode/en-us) |
| North52 App - Quick Ribbon - How to update from older versions | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10266-dynamics-crm-365-Quick-Ribbon-How-to-update-to-the-latest-version-of-v9/en-us) |
| North52 App - Quick Ribbon - Opening a Custom Page | Intermediate | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10493-dynamics-crm-365-Quick-Ribbon-Opening-a-Custom-Page-Unified-Interface/en-us) |

---

## Showcase Apps - Quick Tile

Creating dynamic dashboard tiles and custom UI components.

| Article | Level | Reading Time | Link |
|---------|-------|--------------|------|
| North52 App - Quick Tile | Intermediate | 60 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01957-dynamics-crm-365-North52-App-Quick-Tile/en-us) |
| North52 App - Quick Tile - Sample formula | Intermediate | 60 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01958-dynamics-crm-365-North52-App-Quick-Tile-Sample-formula/en-us) |
| North52 App - Quick Tile - Custom Templates - 1. Overview | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10517-dynamics-crm-365-North52-App-Quick-Tile-Custom-Templates/en-us) |
| North52 App - Quick Tile - Custom Templates - 2. Configuration | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10518-dynamics-crm-365-North52-App-Quick-Tile-Custom-Templates-Configuration/en-us) |
| North52 App - Quick Tile - Custom Templates - 3. Sample Templates | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10532-dynamics-crm-365-North52-App-Quick-Tile-Custom-Templates-3-Sample-Templates/en-us) |
| North52 Apps - Overview | Intermediate | 60 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01951-dynamics-crm-365-North52-Apps-Overview/en-us) |

---

## Power Pages / Dynamics Portals

Integrating North52 with Power Pages and Dynamics Portals.

| Article | Level | Reading Time | Link |
|---------|-------|--------------|------|
| North52 BPA for Power Pages/Dynamics Portals Overview | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-10013-dynamics-crm-365-North52-BPA-for-Dynamics-Portals-Overview/en-us) |
| Installing North52 BPA for Power Pages/Dynamics Portals | Intermediate | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-10003-dynamics-crm-365-Installing-North52-BPA-for-Dynamics-Portals/en-us) |
| Installing North52 BPA - Finding Required Information | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10546-dynamics-crm-365-Installing-North52-BPA-for-Dynamics-Portals-Finding-Required-Data/en-us) |
| Upgrading North52 BPA for Power Pages/Dynamics Portals | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10563-dynamics-crm-365-Upgrading-North52-BPA-for-Power-Pages-Dynamics-Portals/en-us) |
| Uninstalling North52 BPA for Power Pages/Dynamics Portals | Intermediate | 10 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-10006-dynamics-crm-365-Uninstalling-North52-BPA-for-Dynamics-Portals/en-us) |
| Power Pages Troubleshooting #1 - Page Validation | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10534-dynamics-crm-365-Dynamics-Portals-Troubleshooting-Page-Validation/en-us) |
| Power Pages Troubleshooting #4 - Remove Duplicate North52 Records | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10564-dynamics-crm-365-Power-Pages-Troubleshooting-4-Remove-Duplicate-North52-Records/en-us) |
| Power Pages Sample: Updating form fields based on Case Type | Beginner | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-10007-dynamics-crm-365-Portal-Sample-Updating-form-fields-based-on-Case-Type-(OnLoad-OnChange-event)/en-us) |
| Power Pages Sample: Dynamic Quick Button - Escalate Case | Advanced | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-10067-dynamics-crm-365-Portal-Sample-Dynamic-Quick-Button-Escalate-Case/en-us) |
| Power Pages Sample: Using a custom parameter in the URL | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10431-dynamics-crm-365-Portal-Sample-Using-a-custom-parameter-in-the-URL/en-us) |

---

## Training Videos - Legacy

Legacy video training resources.

| Article | Level | Reading Time | Link |
|---------|-------|--------------|------|
| Training Video - Legacy - Advanced Auto Number | Beginner | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02028-dynamics-crm-365-Training-Video-Legacy-Advanced-Auto-Number/en-us) |
| Training Video - Legacy - Basic Auto Number | Beginner | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02043-dynamics-crm-365-Training-Video-Legacy-Basic-Auto-Number/en-us) |
| Training Video - Legacy - Calculate Lead Aging Days | Beginner | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02031-dynamics-crm-365-Training-Video-Legacy-Calculate-Lead-Aging-Days/en-us) |
| Training Video - Legacy - Client Side Add Custom View | Beginner | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02024-dynamics-crm-365-Training-Video-Legacy-Client-Side-Add-Custom-View/en-us) |
| Training Video - Legacy - Client Side Calculate Weighted Estimated Revenue | Beginner | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02019-dynamics-crm-365-Training-Video-Legacy-Client-Side-Calculate-Weighted-Estimated-Revenue/en-us) |
| Training Video - Legacy - Client Side Dependent Picklists | Beginner | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02020-dynamics-crm-365-Training-Video-Legacy-Client-Side-Dependent-Picklists/en-us) |
| Training Video - Legacy - Client Side Hide Tabs | Beginner | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02026-dynamics-crm-365-Training-Video-Legacy-Client-Side-Hide-Tabs/en-us) |
| Training Video - Legacy - Client Side Telephone Number Formatting | Beginner | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02021-dynamics-crm-365-Training-Video-Legacy-Client-Side-Telephone-Number-Formatting/en-us) |
| Training Video - Legacy - Clone Records | Beginner | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02032-dynamics-crm-365-Training-Video-Legacy-Clone-Records/en-us) |
| Training Video - Legacy - Debugging & Tracing | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02010-dynamics-crm-365-Training-Video-Legacy-Debugging-and-Tracing/en-us) |
| Training Video - Legacy - Performance (Formula Manager) | Beginner | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01982-dynamics-crm-365-Training-Video-Legacy-Performance/en-us) |
| Training Video - Legacy - Performance (Scheduler Manager) | Beginner | 15 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01983-dynamics-crm-365-Training-Video-Legacy-Performance/en-us) |

---

## Troubleshooting

Resolving common issues and errors.

| Article | Level | Reading Time | Link |
|---------|-------|--------------|------|
| Debug & Trace - Basics - Part 1 - What is a tracelog? | Intermediate | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10226-dynamics-crm-365-Debug-and-Trace-Basics-Part-1-What-is-a-tracelog/en-us) |
| Debug & Trace - Basics - Part 2 - Activating a Trace log | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10170-dynamics-crm-365-Debug-and-Trace-Basics-Part-2-Activating-a-Trace-log/en-us) |
| Debug & Trace - Basics - Part 3 - Locating Trace logs | Intermediate | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10140-dynamics-crm-365-Debug-and-Trace-Basics-Part-3-Locating-Trace-logs/en-us) |
| Debug & Trace - Intermediate - Part 1 - Reading a Trace log | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10442-dynamics-crm-365-Debug-and-Trace-Intermediate-Part-1-Reading-a-Trace-log/en-us) |
| Debug & Trace - Top 10 - Tips & Tricks | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10143-dynamics-crm-365-Debug-and-Trace-Top-10-Tips-and-Tricks/en-us) |
| How to - Change the name of a Form that has North52 ClientSide Formulas | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02009-dynamics-crm-365-How-to-Change-the-name-of-a-Form-that-has-North52-ClientSide-Formulas-connected-to-it/en-us) |
| How to - Handling and Setting Dates | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02011-dynamics-crm-365-How-to-Handling-and-Setting-Dates/en-us) |
| How to - Manual Publishing | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02006-dynamics-crm-365-How-to-Manual-Publishing/en-us) |
| How to - Manually change the Owner of a North52 BPA Installation | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02003-dynamics-crm-365-How-to-Manually-change-the-Owner-of-a-North52-BPA-Installation/en-us) |
| How to - Manually change the Owner of North52 BPA Formulas, Schedules, etc. | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10485-dynamics-crm-365-How-to-Manually-change-the-Owner-of-North52-BPA-Formulas%2c-Schedules%2c-Data-Packages-and-xCache-Records/en-us) |
| How to turn off Copilot in the North52 App | - | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10557-dynamics-crm-365-How-to-turn-off-Copilot-in-North52-App/en-us) |
| Known Microsoft issues - 3 - BPF Security Roles | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02014-dynamics-crm-365-Known-Microsoft-issues-3-BPF-Security-Roles/en-us) |
| Known Microsoft issues - 4 - EntitySetName | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02015-dynamics-crm-365-Known-Microsoft-issues-4-EntitySetName/en-us) |
| Known Microsoft issues - 5 - Release 9.0.2.438 | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-02177-dynamics-crm-365-Known-Microsoft-issues-5-Release-902438/en-us) |
| System Report - Missing SDK Message Processing Steps | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10229-dynamics-crm-365-System-Report-Missing-SDK-Message-Processing-Steps/en-us) |
| System Report - Missing Web Resources | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10227-dynamics-crm-365-System-Report-Missing-Web-Resources/en-us) |
| System Report - Organizational Insights | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02016-dynamics-crm-365-System-Report-Organizational-Insights/en-us) |
| Troubleshooting #01 - Insufficient Privileges | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01984-dynamics-crm-365-Troubleshooting-01-Insufficient-Privileges/en-us) |
| Troubleshooting #05 - Nested Exceptions | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01988-dynamics-crm-365-Troubleshooting-05-Nested-Exceptions/en-us) |
| Troubleshooting #06 - Enable SDK Message Processing Steps | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01989-dynamics-crm-365-Troubleshooting-06-Enable-SDK-Message-Processing-Steps/en-us) |
| Troubleshooting #07 - Refresh the Formula Cache | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01990-dynamics-crm-365-Troubleshooting-07-Refresh-the-Formula-Cache/en-us) |
| Troubleshooting #09 - Disable SDK Message Processing Steps | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01992-dynamics-crm-365-Troubleshooting-09-Disable-SDK-Message-Processing-Steps/en-us) |
| Troubleshooting #10 - Disable Auto Publishing | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01993-dynamics-crm-365-Troubleshooting-10-Disable-Auto-Publishing/en-us) |
| Troubleshooting #11 - Site Map does not appear | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01994-dynamics-crm-365-Troubleshooting-11-Site-Map-does-not-appear/en-us) |
| Troubleshooting #14 - Rebuild Configuration Record | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01997-dynamics-crm-365-Troubleshooting-14-Rebuild-Configuration-Record/en-us) |
| Troubleshooting #15 - License Configuration Failed | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01998-dynamics-crm-365-Troubleshooting-15-License-Configuration-Failed/en-us) |
| Troubleshooting #16 - Check licence is accepted | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-01999-dynamics-crm-365-Troubleshooting-16-Check-licence-is-accepted/en-us) |
| Troubleshooting #17 - Find how many active users you have | Beginner | 5 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-02000-dynamics-crm-365-Troubleshooting-17-Find-how-many-active-users-you-have/en-us) |
| Troubleshooting #19 - All permissions for North52 Formula Manager - Standard role| Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10027-dynamics-crm-365-Troubleshooting-19-All-permissions-for-the-North52-Formula-Manager-Standard-security-role/en-us) |
| Troubleshooting #22 - Checksum | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10334-dynamics-crm-365-Troubleshooting-22-Checksum/en-us) |
| Troubleshooting #25 - Use Named Server instead of IP Address in URL | Beginner | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10445-dynamics-crm-365-Troubleshooting-25-Use-Named-Server-instead-of-IP-Address-in-URL/en-us) |
| Troubleshooting #30 - Publish Settings - Disable Solution Linking | Intermediate | 1 mins | [Docs](https://support.north52.com/knowledgebase/article/KA-10556-dynamics-crm-365-Troubleshooting-30-Disable-Solution-Linking/en-us) |
| Troubleshooting #32 - Solution Import - Failed to import SDK Message Processing | - | - | [Docs](https://support.north52.com/knowledgebase/article/KA-10588-dynamics-crm-365-Troubleshooting-32-Solution-Import-Failed-to-import-SDK-Message-Processing-Steps-import/en-us) |

---

## xRM Formula Samples

Over 300 practical formula examples covering a wide range of scenarios. **Note**: Due to the large number of samples, below are key categories with select examples. Visit the [official samples page](https://support.north52.com/knowledgebase/business-process-activities/) for the complete list.

### AutoNumber & ID Generation
- [#001 - AutoNumber](https://support.north52.com/knowledgebase/article/KA-01004-dynamics-crm-365-xRM-Formula-001-AutoNumber/en-us)
- [#124 - Generate a random number using AutoNumber](https://support.north52.com/knowledgebase/article/KA-01129-dynamics-crm-365-xRM-Formula-124-Generate-a-random-number-for-the-Case-entity-using-AutoNumber/en-us)
- [#221 - Reset AutoNumber every year](https://support.north52.com/knowledgebase/article/KA-10022-dynamics-crm-365-xRM-Formula-221-Reset-AutoNumber-every-year/en-us)
- [#222 - Multiple Entities sharing an AutoNumber](https://support.north52.com/knowledgebase/article/KA-10023-dynamics-crm-365-xRM-Formula-222-Multiple-Entities-sharing-an-AutoNumber/en-us)

### Business Process Flows
- [#004 - Change Stage of a Business Process Flow](https://support.north52.com/knowledgebase/article/KA-01007-dynamics-crm-365-xRM-Formula-004-Change-Stage-of-a-Business-Process-Flow/en-us)
- [#122 - Automatically Change BPF Stage based on User Input](https://support.north52.com/knowledgebase/article/KA-01127-dynamics-crm-365-xRM-Formula-122-Automatically-Change-Business-Process-Flow-Stage-based-on-User-Input/en-us)
- [#171 - Automatically change BPF stage based on field value](https://support.north52.com/knowledgebase/article/KA-01938-dynamics-crm-365-xRM-Formula-171-Sample-Automatically-change-Business-Process-Flow-stage-based-on-field-value/en-us)
- [#290 - Set Specific Business Process Flow on Create](https://support.north52.com/knowledgebase/article/KA-10592-dynamics-crm-365-xRM-Formula-290-Set-Specific-Business-Process-Flow-on-Create-of-a-Record/en-us)

### Client-Side Functionality
- [#013 - Copy data from Account to Contact via onChange](https://support.north52.com/knowledgebase/article/KA-01017-dynamics-crm-365-xRM-Formula-013-Copy-data-from-Account-to-Contact-via-onChange-event/en-us)
- [#025 - User Actioned Form Notifications](https://support.north52.com/knowledgebase/article/KA-01029-dynamics-crm-365-xRM-Formula-025-User-Actioned-Form-Notifications/en-us)
- [#039 - Dependent Picklists](https://support.north52.com/knowledgebase/article/KA-01043-dynamics-crm-365-xRM-Formula-039-Dependent-Picklists/en-us)
- [#138 - Hide Section of a specific Form](https://support.north52.com/knowledgebase/article/KA-01143-dynamics-crm-365-xRM-Formula-138-Hide-Section-of-a-specific-Form/en-us)
- [#289 - Filter OptionSet Dynamically by Display Name](https://support.north52.com/knowledgebase/article/KA-10566-dynamics-crm-365-xRM-Formula-289-Filter-OptionSet-Dynamically-by-Display-Name/en-us)

### Cloning & Record Creation
- [#032 - Clone Records](https://support.north52.com/knowledgebase/article/KA-02032-dynamics-crm-365-Training-Video-Legacy-Clone-Records/en-us)
- [#042 - Generate Task with Notes](https://support.north52.com/knowledgebase/article/KA-01046-dynamics-crm-365-xRM-Formula-042-Generate-Task-with-Notes/en-us)
- [#268 - Multi-Level Cloning](https://support.north52.com/knowledgebase/article/KA-10265-dynamics-crm-365-xRM-Formula-268-Multi-Level-Cloning/en-us)

### Complex Calculations & Decision Tables
- [#149 - Credit Card Entitlement - Part 1](https://support.north52.com/knowledgebase/article/KA-01913-dynamics-crm-365-xRM-Formula-149-Credit-Card-Entitlement-Part-1/en-us)
- [#152 - Determine Age Group and Next Birthday](https://support.north52.com/knowledgebase/article/KA-01916-dynamics-crm-365-xRM-Formula-152-Determine-Age-Group-and-Next-Birthday/en-us)
- [#159 - US Dept. of Veterans Affairs: Health Benefits Priority Groups](https://support.north52.com/knowledgebase/article/KA-01923-dynamics-crm-365-xRM-Formula-159-US-Dept-of-Veterans-Affairs-Health-Benefits-Priority-Groups/en-us)
- [#161 - Coronary Heart Disease Risk Score](https://support.north52.com/knowledgebase/article/KA-01927-dynamics-crm-365-xRM-Formula-161-Coronary-Heart-Disease-Risk-Score/en-us)
- [#197 - Farming Cattle Sales Advice using Decision Tables](https://support.north52.com/knowledgebase/article/KA-01924-dynamics-crm-365-xRM-Formula-197-Farming-Cattle-Sales-Advice-using-Decision-Tables/en-us)

### Date & Time Operations
- [#125 - Calculate Date and Time for a specific time zone](https://support.north52.com/knowledgebase/article/KA-01130-dynamics-crm-365-xRM-Formula-125-Calculate-Date-and-Time-for-a-specific-time-zone/en-us)
- [#143 - Calculate Elapsed Business Hours](https://support.north52.com/knowledgebase/article/KA-01150-dynamics-crm-365-xRM-Formula-143-Calculate-Elapsed-Business-Hours/en-us)
- [#182 - Check for Free Time Periods](https://support.north52.com/knowledgebase/article/KA-02086-dynamics-crm-365-xRM-Formula-182-Check-for-Free-Time-Periods/en-us)

### Email & Communication
- [#015 - Sending HTML formatted Quote emails](https://support.north52.com/knowledgebase/article/KA-01019-dynamics-crm-365-xRM-Formula-015-Sending-HTML-formatted-Quote-emails-with-a-table-of-products/en-us)
- [#044 - Default the From Address of an Email](https://support.north52.com/knowledgebase/article/KA-01048-dynamics-crm-365-xRM-Formula-044-Default-the-From-Address-of-an-Email/en-us)
- [#090 - Template Emails](https://support.north52.com/knowledgebase/article/KA-01095-dynamics-crm-365-xRM-Formula-090-Template-Emails/en-us)

### GeoLocation & Mapping
- [#002 - Geo Encode Dynamics CRM Account Addresses](https://support.north52.com/knowledgebase/article/KA-01005-dynamics-crm-365-xRM-Formula-002-Geo-Encode-a-set-of-Dynamics-CRM-Account-Addresses/en-us)
- [#033 - Geo Encode the Account Address](https://support.north52.com/knowledgebase/article/KA-01037-dynamics-crm-365-xRM-Formula-033-Geo-Encode-the-Account-Address/en-us)
- [#254 - Find longitude and latitude using Google Geocoding API](https://support.north52.com/knowledgebase/article/KA-10139-dynamics-crm-365-xRM-Formula-254-Find-longitude-and-latitude-using-Google-Geocoding-API/en-us)
- [#291 - Use Azure Maps API to set Latitude and Longitude](https://support.north52.com/knowledgebase/article/KA-10594-dynamics-crm-365-xRM-Formula-291-Use-Azure-Maps-API-to-set-Latitude-and-Longitude/en-us)

### Integration & Web Services
- [#034 - Translate French to English](https://support.north52.com/knowledgebase/article/KA-01038-dynamics-crm-365-xRM-Formula-034-Translate-French-to-English/en-us)
- [#089 - Synchronize Data with external system via Rest webservices](https://support.north52.com/knowledgebase/article/KA-01094-dynamics-crm-365-xRM-Formula-089-Synchronize-Data-with-external-system-via-Rest-webservices/en-us)
- [#225 - Send Custom JSON Message to Service Bus Queue](https://support.north52.com/knowledgebase/article/KA-10026-dynamics-crm-365-xRM-Formula-225-Send-Custom-JSON-Message-to-Service-Bus-Queue/en-us)
- [#235 - Send Custom JSON Message to Azure Event Grid](https://support.north52.com/knowledgebase/article/KA-10062-dynamics-crm-365-xRM-Formula-235-Send-Custom-JSON-Message-to-Azure-Event-Grid/en-us)
- [#276 - Trigger Power Automate Flow with Quick Button](https://support.north52.com/knowledgebase/article/KA-10457-dynamics-crm-365-xRM-Formula-276-Trigger-Power-Automate-Flow-with-Quick-Button/en-us)

### N:N Relationships
- [#005 - N:N Rollup - Count Many to Many Relationships](https://support.north52.com/knowledgebase/article/KA-01008-dynamics-crm-365-xRM-Formula-005-NN-Rollup-Count-Many-to-Many-Relationships-1/en-us)
- [#006 - N:N Relationship Updates](https://support.north52.com/knowledgebase/article/KA-01009-dynamics-crm-365-xRM-Formula-006-NN-Relationship-Updates/en-us)
- [#108 - Automatically Add Competitors to Parent Accounts](https://support.north52.com/knowledgebase/article/KA-01113-dynamics-crm-365-xRM-Formula-108-Automatically-Add-Competitors-to-Parent-Accounts/en-us)

### Power Pages / Portal Samples
- [Power Pages Sample: Updating form fields based on Case Type](https://support.north52.com/knowledgebase/article/KA-10007-dynamics-crm-365-Portal-Sample-Updating-form-fields-based-on-Case-Type-(OnLoad-OnChange-event)/en-us)
- [Power Pages Sample: Dynamic Quick Button - Escalate Case](https://support.north52.com/knowledgebase/article/KA-10067-dynamics-crm-365-Portal-Sample-Dynamic-Quick-Button-Escalate-Case/en-us)
- [Power Pages Sample: Complex Forms - Hospital Admission Questionnaire](https://support.north52.com/knowledgebase/article/KA-10454-dynamics-crm-365-Portal-Sample-Complex-Power-Apps-Portal-Forms-Hospital-Admission-Questionnaire/en-us)

### Quick Button Samples
- [#066 - Quick Button - Generate Weekly Tasks](https://support.north52.com/knowledgebase/article/KA-01070-dynamics-crm-365-xRM-Formula-066-Quick-Button-Generate-Weekly-Tasks/en-us)
- [#081 - Create and open an appointment for a Lead](https://support.north52.com/knowledgebase/article/KA-01086-dynamics-crm-365-xRM-Formula-081-Create-and-open-an-appointment-for-a-Lead/en-us)
- [#133 - Quick Button Share Record with Secure Team](https://support.north52.com/knowledgebase/article/KA-01138-dynamics-crm-365-xRM-Formula-133-Quick-Button-Share-Record-with-Secure-Team/en-us)
- [#172 - Disable a Quick Button when not needed](https://support.north52.com/knowledgebase/article/KA-01939-dynamics-crm-365-xRM-Formula-172-Disable-a-Quick-Button-when-not-needed/en-us)
- [#203 - Apply a formula to every selected record in a Sub-Grid](https://support.north52.com/knowledgebase/article/KA-02173-dynamics-crm-365-xRM-Formula-203-Apply-a-formula-to-every-selected-record-in-a-Sub-Grid/en-us)

### Rollups & Aggregations
- [#020 - Rollups via Workflow - Total Open Opportunities](https://support.north52.com/knowledgebase/article/KA-01024-dynamics-crm-365-xRM-Formula-020-Rollups-via-Workflow-Total-Open-Opportunities/en-us)
- [#033 - Set Custom Field Total Hot Opps (Rollups)](https://support.north52.com/knowledgebase/article/KA-02033-dynamics-crm-365-Training-Video-Legacy-Set-Custom-Field-Total-Hot-Opps-(Rollups)/en-us)
- [#068 - Find Oldest Contact](https://support.north52.com/knowledgebase/article/KA-01072-dynamics-crm-365-xRM-Formula-068-Find-Oldest-Contact/en-us)
- [#136 - Get Associated First Names of an Account](https://support.north52.com/knowledgebase/article/KA-01141-dynamics-crm-365-xRM-Formula-136-Get-Associated-First-Names-of-an-Account/en-us)

### SharePoint Integration
- [#098 - Automatically attach SharePoint documents to an email](https://support.north52.com/knowledgebase/article/KA-01103-dynamics-crm-365-xRM-Formula-098-Automatically-attach-SharePoint-documents-to-an-email/en-us)
- [#111 - Setting SharePoint Document Locations - Classic Formula](https://support.north52.com/knowledgebase/article/KA-01116-dynamics-crm-365-xRM-Formula-111-Setting-SharePoint-Document-Locations-Classic-Formula/en-us)
- [#114 - Transfer Note attachments to SharePoint with Quick Button](https://support.north52.com/knowledgebase/article/KA-01119-dynamics-crm-365-xRM-Formula-114-Transfer-Note-attachments-to-a-SharePoint-folder-with-Quick-Button/en-us)
- [#145 - Move Note Attachments to Sharepoint](https://support.north52.com/knowledgebase/article/KA-01152-dynamics-crm-365-xRM-Formula-145-Move-Note-Attachments-to-Sharepoint/en-us)

### Validation & Data Quality
- [#017 - Validate data entry of US States](https://support.north52.com/knowledgebase/article/KA-01021-dynamics-crm-365-xRM-Formula-017-Validate-data-entry-of-US-States/en-us)
- [#026 - Real Time Data Validation](https://support.north52.com/knowledgebase/article/KA-01030-dynamics-crm-365-xRM-Formula-026-Real-Time-Data-Validation/en-us)
- [#057 - Validate SSN](https://support.north52.com/knowledgebase/article/KA-01061-dynamics-crm-365-xRM-Formula-057-Validate-SSN/en-us)
- [#064 - Validate last 4 digits of Credit Card](https://support.north52.com/knowledgebase/article/KA-01068-dynamics-crm-365-xRM-Formula-064-Validate-last-4-digits-of-Credit-Card/en-us)

### AI & Modern Features
- [#298 - Automatically process Email using Dataverse AI Functions](https://support.north52.com/knowledgebase/article/KA-10607-dynamics-crm-365-xRM-Formula-298-Automatically-process-Email-using-Dataverse-AI-Functions/en-us)
- [#297 - Display Custom Dismissible Alerts in Dataverse Side Pane](https://support.north52.com/knowledgebase/article/KA-10606-dynamics-crm-365-xRM-Formula-297-Display-Custom-Dismissible-Alerts-in-Dataverse-Side-Pane/en-us)

### Industry-Specific Examples
- [#155 - Idaho State Food Assistance](https://support.north52.com/knowledgebase/article/KA-01919-dynamics-crm-365-xRM-Formula-155-Idaho-State-Food-Assistance/en-us)
- [#156 - Idaho State Medicaid or CHIP Assistance](https://support.north52.com/knowledgebase/article/KA-01920-dynamics-crm-365-xRM-Formula-156-Idaho-State-Medicaid-or-CHIP-Assistance/en-us)
- [#277 - Insurance Claims Adjudication - Automated Processing](https://support.north52.com/knowledgebase/article/KA-10458-dynamics-crm-365-xRM-Formula-277-Insurance-Claims-Adjudication-Automated-Processing/en-us)
- [#278 - Complex Pricing for Shipping Agents (CPQ example)](https://support.north52.com/knowledgebase/article/KA-10470-dynamics-crm-365-xRM-Formula-278-Complex-Pricing-for-Shipping-Agents-(CPQ-example)/en-us)
- [#285 - Identifying Risks in the Pension Transfer Process](https://support.north52.com/knowledgebase/article/KA-10521-dynamics-crm-365-xRM-Formula-285-Identifying-Risks-in-the-Pension-Transfer-Process/en-us)
- [#299 - Shopify Fraud Detection and Order Management](https://support.north52.com/knowledgebase/article/KA-10608-dynamics-crm-365-xRM-Formula-299-Shopify-Fraud-Detection-and-Order-Management/en-us)
- [#300 - Managing and Validating Doctor Certifications](https://support.north52.com/knowledgebase/article/KA-10612-dynamics-crm-365-xRM-Formula-300-Managing-and-Validating-Doctor-Certifications/en-us)

---

## Additional Resources

- **North52 Support Portal**: https://support.north52.com/
- **Main BPA Page**: https://support.north52.com/knowledgebase/business-process-activities/
- **Knowledge Base**: https://support.north52.com/knowledgebase/
- **Help Desk**: https://support.north52.com/support/

---

## Usage Notes

1. **Article Categories**: Articles are organized by module, functionality, and complexity level.

2. **Skill Levels**: Most articles indicate the skill level required (Beginner, Intermediate, Advanced).

3. **Reading Time**: Many articles include estimated reading/implementation time.

4. **xRM Formula Samples**: The 300+ formula samples cover real-world business scenarios and can be used as templates for your own implementations.

5. **Video Training**: Legacy training videos provide visual walkthroughs for common scenarios.

6. **Case Studies**: Several case studies demonstrate North52's application in real organizations (Metro Bank, Tribridge).

7. **Version-Specific**: Some articles may be version-specific. Always check the official documentation for the most current information.

---

**Note**: This reference was generated by scraping the North52 Business Process Activities index page. For the most up-to-date information, detailed walkthroughs, and code examples, always refer to the official North52 documentation at the provided links.
