// ============================================================
// PluginTest.cs
// FakeXrmEasy 3.x unit test skeleton for MNP plugins
// NuGet: FakeXrmEasy.Core (3.x), FakeXrmEasy.Plugins (3.x),
//        Microsoft.NET.Test.Sdk, xunit, xunit.runner.visualstudio
// Targets .NET Framework 4.6.2 or .NET 6+
// ============================================================
using System;
using System.Collections.Generic;
using FakeXrmEasy.Core;
using FakeXrmEasy.Core.Fakes.Middleware.Crud;
using FakeXrmEasy.Core.Fakes.Middleware.Messages;
using FakeXrmEasy.Plugins.Extensions;
using Microsoft.Xrm.Sdk;
using Xunit;

// Replace MNP.SOLUTION.Plugins with your actual namespace
namespace MNP.SOLUTION.Plugins.Tests
{
    // ============================================================
    // PluginTestContext — shared FakeXrmEasy context setup helper
    // ============================================================
    public static class PluginTestContext
    {
        /// <summary>
        /// Creates a pre-configured XrmFakedContext for unit tests.
        /// Use XrmFakedContext.GetOrganizationService() to get the fake IOrganizationService.
        /// </summary>
        public static XrmFakedContext Create(IEnumerable<Entity> initialData = null)
        {
            // Middleware pipeline: enable basic CRUD + standard messages
            var context = XrmFakedContext.New()
                .WithMiddleware(m => m
                    .AddCrudFakeMessageExecutors()
                    .AddFakeMessageExecutors());

            if (initialData != null)
                context.Initialize(initialData);

            return context;
        }
    }

    // ============================================================
    // Example: Tests for ProcessApplicationEntity plugin
    // ============================================================
    public class ProcessApplicationEntityTests
    {
        // ----------------------------------------------------------
        // Shared test data builders
        // ----------------------------------------------------------
        private static Entity CreateApplicationRecord(
            Guid? id = null,
            string name = "APP-001",
            int? statusCode = null)
        {
            var entity = new Entity("mnp_application")
            {
                Id = id ?? Guid.NewGuid(),
                ["mnp_name"]       = name,
                ["statuscode"]     = statusCode.HasValue
                                        ? new OptionSetValue(statusCode.Value)
                                        : null,
            };
            return entity;
        }

        // ----------------------------------------------------------
        // Test: plugin should throw when required field is missing
        // ----------------------------------------------------------
        [Fact]
        public void Execute_WhenRequiredFieldMissing_ThrowsInvalidPluginExecutionException()
        {
            // Arrange
            var context = PluginTestContext.Create();

            var target = new Entity("mnp_application") { Id = Guid.NewGuid() };
            // Intentionally omit required field

            var pluginContext = context.GetDefaultPluginContext();
            pluginContext.MessageName          = "Create";
            pluginContext.Stage                = 20; // Pre-Operation
            pluginContext.PrimaryEntityName    = "mnp_application";
            pluginContext.InputParameters["Target"] = target;

            // Act & Assert
            Assert.Throws<InvalidPluginExecutionException>(() =>
                context.ExecutePluginWith<ProcessApplicationEntity>(pluginContext));
        }

        // ----------------------------------------------------------
        // Test: plugin should succeed with valid data
        // ----------------------------------------------------------
        [Fact]
        public void Execute_WithValidTarget_CompletesSuccessfully()
        {
            // Arrange
            var context = PluginTestContext.Create();

            var targetId = Guid.NewGuid();
            var target = new Entity("mnp_application")
            {
                Id = targetId,
                ["mnp_name"]              = "APP-001",
                ["mnp_applicantid"]       = new EntityReference("contact", Guid.NewGuid()),
                ["mnp_applicationdate"]   = DateTime.UtcNow,
            };

            var pluginContext = context.GetDefaultPluginContext();
            pluginContext.MessageName          = "Create";
            pluginContext.Stage                = 20; // Pre-Operation
            pluginContext.PrimaryEntityName    = "mnp_application";
            pluginContext.PrimaryEntityId      = targetId;
            pluginContext.InputParameters["Target"] = target;

            // Act — should not throw
            context.ExecutePluginWith<ProcessApplicationEntity>(pluginContext);

            // Assert: verify any post-execution expectations
            // e.g. check that a field was set on Target
            // Assert.Equal(expectedValue, target.GetAttributeValue<string>("mnp_name"));
        }

        // ----------------------------------------------------------
        // Test: plugin reads pre-image correctly (Update step)
        // ----------------------------------------------------------
        [Fact]
        public void Execute_OnUpdate_ReadsPreImageAttributes()
        {
            // Arrange
            var context = PluginTestContext.Create();

            var recordId = Guid.NewGuid();

            var preImage = new Entity("mnp_application", recordId)
            {
                ["mnp_name"]       = "OLD-NAME",
                ["statuscode"]     = new OptionSetValue(1),
            };

            var target = new Entity("mnp_application")
            {
                Id = recordId,
                ["mnp_name"] = "NEW-NAME",
            };

            var pluginContext = context.GetDefaultPluginContext();
            pluginContext.MessageName           = "Update";
            pluginContext.Stage                 = 40; // Post-Operation
            pluginContext.PrimaryEntityName     = "mnp_application";
            pluginContext.PrimaryEntityId       = recordId;
            pluginContext.InputParameters["Target"] = target;
            pluginContext.PreEntityImages["PreImage"] = preImage;

            // Act
            context.ExecutePluginWith<ProcessApplicationEntity>(pluginContext);

            // Assert
            // var updatedRecord = context.GetFakedOrganizationService().Retrieve(
            //     "mnp_application", recordId, new ColumnSet("mnp_name"));
            // Assert.Equal("EXPECTED", updatedRecord["mnp_name"]);
        }
    }

    // ============================================================
    // Example: Tests for a workflow activity
    // ============================================================
    public class CalculateBenefitActivityTests
    {
        [Fact]
        public void Execute_ReturnsExpectedCalculation()
        {
            // Arrange
            var context = PluginTestContext.Create();

            var workflowContext = context.GetDefaultWorkflowContext();
            workflowContext.PrimaryEntityName = "mnp_benefit";
            workflowContext.PrimaryEntityId   = Guid.NewGuid();

            // Act
            // FakeXrmEasy workflow activity execution:
            // context.ExecuteCodeActivity<CalculateBenefitActivity>(workflowContext, inputs, outputs);
            //
            // var inputs = new Dictionary<string, object>
            // {
            //     { "BenefitAmount", new Money(1000m) },
            //     { "Multiplier",    1.5m }
            // };
            // var outputs = context.ExecuteCodeActivity<CalculateBenefitActivity>(inputs);

            // Assert
            // Assert.Equal(new Money(1500m), outputs["CalculatedValue"] as Money);
        }
    }
}
