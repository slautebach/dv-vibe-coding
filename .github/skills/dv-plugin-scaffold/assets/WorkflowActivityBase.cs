// ============================================================
// WorkflowActivityBase.cs
// MNP base workflow activity pattern — copy to MNP.{Solution}.Plugins
// Targets .NET Framework 4.6.2
// NuGet: Microsoft.CrmSdk.Workflow
// ============================================================
using System;
using System.Activities;
using Microsoft.Xrm.Sdk;
using Microsoft.Xrm.Sdk.Workflow;

namespace MNP.SOLUTION.Plugins
{
    /// <summary>
    /// Abstract base class for all MNP custom workflow activities.
    /// Extends CodeActivity and resolves IWorkflowContext, IOrganizationService,
    /// and ITracingService before delegating to ExecuteCrmWorkFlowActivity.
    /// </summary>
    public abstract class WorkflowActivityBase : CodeActivity
    {
        // -------------------------------------------------------
        // CodeActivity.Execute — entry point called by Dataverse
        // -------------------------------------------------------
        protected override void Execute(CodeActivityContext context)
        {
            if (context == null) throw new ArgumentNullException(nameof(context));

            var localContext = new LocalWorkflowContext(context);
            localContext.Trace($"Entered {GetType().Name}.Execute()");

            try
            {
                ExecuteCrmWorkFlowActivity(context, localContext);
                localContext.Trace($"Exiting {GetType().Name}.Execute()");
            }
            catch (InvalidPluginExecutionException)
            {
                throw;
            }
            catch (Exception ex)
            {
                localContext.Trace($"Exception in {GetType().Name}: {ex}");
                throw new InvalidPluginExecutionException(
                    $"An unexpected error occurred in {GetType().Name}. " +
                    $"Please contact your system administrator. Detail: {ex.Message}", ex);
            }
        }

        /// <summary>Override this method to implement workflow activity logic.</summary>
        protected abstract void ExecuteCrmWorkFlowActivity(
            CodeActivityContext context,
            ILocalWorkflowContext localContext);

        // -------------------------------------------------------
        // ILocalWorkflowContext — public surface for derived classes
        // -------------------------------------------------------
        public interface ILocalWorkflowContext
        {
            IWorkflowContext     WorkflowContext       { get; }
            IOrganizationService OrganizationService  { get; }
            ITracingService      TracingService        { get; }
            void Trace(string message);
        }

        // -------------------------------------------------------
        // LocalWorkflowContext — concrete implementation
        // -------------------------------------------------------
        protected class LocalWorkflowContext : ILocalWorkflowContext
        {
            public IWorkflowContext     WorkflowContext       { get; }
            public IOrganizationService OrganizationService  { get; }
            public ITracingService      TracingService        { get; }

            public LocalWorkflowContext(CodeActivityContext context)
            {
                if (context == null) throw new ArgumentNullException(nameof(context));

                WorkflowContext = context.GetExtension<IWorkflowContext>();

                TracingService = context.GetExtension<ITracingService>();

                var serviceFactory = context.GetExtension<IOrganizationServiceFactory>();

                // Service acting as the user who triggered the workflow
                OrganizationService =
                    serviceFactory.CreateOrganizationService(WorkflowContext.InitiatingUserId);
            }

            public void Trace(string message)
            {
                if (string.IsNullOrWhiteSpace(message) || TracingService == null) return;
                TracingService.Trace(message);
            }
        }
    }
}

// ============================================================
// EXAMPLE: Derived workflow activity
// ============================================================
// namespace MNP.SOLUTION.Plugins
// {
//     public class CalculateBenefitActivity : WorkflowActivityBase
//     {
//         [RequiredArgument]
//         [Input("Benefit Amount")]
//         [AttributeTarget("mnp_benefit", "mnp_amount")]
//         public InArgument<Money> BenefitAmount { get; set; }
//
//         [Input("Multiplier")]
//         [Default("1.0")]
//         public InArgument<decimal> Multiplier { get; set; }
//
//         [Output("Calculated Value")]
//         public OutArgument<Money> CalculatedValue { get; set; }
//
//         protected override void ExecuteCrmWorkFlowActivity(
//             CodeActivityContext context,
//             ILocalWorkflowContext localContext)
//         {
//             var amount     = BenefitAmount.Get(context)?.Value ?? 0m;
//             var multiplier = Multiplier.Get(context);
//
//             var result = amount * multiplier;
//             localContext.Trace($"Calculated: {amount} x {multiplier} = {result}");
//
//             CalculatedValue.Set(context, new Money(result));
//         }
//     }
// }
