# North52 Functions Complete Reference

> **📚 About this reference**: This document provides a complete list of all 539 North52 functions with links to official documentation.  
> **📖 For practical examples and usage tips**, see [north52-functions.md](north52-functions.md).  
> **🔧 For business process activities**, see [north52-business-process-activities.md](north52-business-process-activities.md).

This document provides a comprehensive list of all 539 North52 Decision Suite functions with direct links to their official documentation.

**Last Updated**: February 17, 2026  
**Source**: https://support.north52.com/knowledgebase/functions/

---

## Table of Contents

- [North52 Functions Complete Reference](#north52-functions-complete-reference)
  - [Table of Contents](#table-of-contents)
  - [Client Side](#client-side)
  - [Conversions](#conversions)
  - [Date](#date)
  - [Find (Single Values)](#find-single-values)
  - [Find (EntityCollections)](#find-entitycollections)
  - [HTML](#html)
  - [Industry](#industry)
  - [JSON](#json)
  - [Localization](#localization)
  - [Logical](#logical)
  - [Loop](#loop)
  - [Math](#math)
  - [Platform Operations](#platform-operations)
  - [Record Control](#record-control)
  - [Regular Expressions](#regular-expressions)
  - [Rest Services](#rest-services)
  - [Set Native Fields](#set-native-fields)
  - [SharePoint Services](#sharepoint-services)
  - [String](#string)
  - [System](#system)
  - [Web Services](#web-services)
  - [XML](#xml)
  - [xCache](#xcache)
  - [Additional Resources](#additional-resources)
  - [Usage Notes](#usage-notes)

---

## Client Side

Functions that execute in the browser and interact with the Dynamics 365 form interface.

| Function | Description | Link |
|----------|-------------|------|
| AddCustomView | Provides the ability to add a custom view to a lookup control | [Docs](https://support.north52.com/knowledgebase/article/KA-01519-dynamics-crm-365-AddCustomView/en-us) |
| AddPreFilterLookup | Adds a pre filter lookup to the controlid | [Docs](https://support.north52.com/knowledgebase/article/KA-01521-dynamics-crm-365-AddPreFilterLookup/en-us) |
| Alert | Presents a pop-up alert to the user | [Docs](https://support.north52.com/knowledgebase/article/KA-01520-dynamics-crm-365-Alert/en-us) |
| AlertClear | Presents a pop-up alert to the user and clears the listed fields | [Docs](https://support.north52.com/knowledgebase/article/KA-01528-dynamics-crm-365-AlertClear/en-us) |
| BPMoveNextStage | Moves the business process to the next stage | [Docs](https://support.north52.com/knowledgebase/article/KA-01524-dynamics-crm-365-BPMoveNextStage/en-us) |
| BPMovePreviousStage | Moves the business process to the previous stage | [Docs](https://support.north52.com/knowledgebase/article/KA-01525-dynamics-crm-365-BPMovePreviousStage/en-us) |
| BPSetActiveProcess | Sets the active business process for the current record | [Docs](https://support.north52.com/knowledgebase/article/KA-01522-dynamics-crm-365-BPSetActiveProcess/en-us) |
| BrowserReload | Reloads the browser webpage | [Docs](https://support.north52.com/knowledgebase/article/KA-01526-dynamics-crm-365-BrowserReload/en-us) |
| ClearControlNotification | Clears the control notification | [Docs](https://support.north52.com/knowledgebase/article/KA-01531-dynamics-crm-365-ClearControlNotification/en-us) |
| ClearFields | Clears the contents of any fields | [Docs](https://support.north52.com/knowledgebase/article/KA-01529-dynamics-crm-365-ClearFields/en-us) |
| ClearFormNotification | Clears the form notification | [Docs](https://support.north52.com/knowledgebase/article/KA-01530-dynamics-crm-365-ClearFormNotification/en-us) |
| CollapseTabs | Collapses a tab | [Docs](https://support.north52.com/knowledgebase/article/KA-01532-dynamics-crm-365-CollapseTabs/en-us) |
| DisableFields | Disables one or more fields on a form | [Docs](https://support.north52.com/knowledgebase/article/KA-01533-dynamics-crm-365-DisableFields/en-us) |
| EnableFields | Enables one or more fields on a form | [Docs](https://support.north52.com/knowledgebase/article/KA-01534-dynamics-crm-365-EnableFields/en-us) |
| ExecuteDialog | Executes a dialog | [Docs](https://support.north52.com/knowledgebase/article/KA-01536-dynamics-crm-365-ExecuteDialog/en-us) |
| ExecuteWorkflow | Executes a workflow | [Docs](https://support.north52.com/knowledgebase/article/KA-01537-dynamics-crm-365-ExecuteWorkflow/en-us) |
| ExpandTabs | Expands a tab | [Docs](https://support.north52.com/knowledgebase/article/KA-01535-dynamics-crm-365-ExpandTabs/en-us) |
| FormSave | Saves a form | [Docs](https://support.north52.com/knowledgebase/article/KA-01538-dynamics-crm-365-FormSave/en-us) |
| GetAppName | Get the app name | [Docs](https://support.north52.com/knowledgebase/article/KA-10200-dynamics-crm-365-getappname/en-us) |
| HeaderFooterSectionHideAll | Turns on the visibility of the Header Body, Command Bar and Tab Navigator | [Docs](https://support.north52.com/knowledgebase/article/KA-10353-dynamics-crm-365-HeaderFooterSectionHideAll/en-us) |
| HeaderFooterSectionShowAll | Turns off the visibility of the Header Body, Command Bar and Tab Navigator | [Docs](https://support.north52.com/knowledgebase/article/KA-10354-dynamics-crm-365-HeaderFooterSectionShowAll/en-us) |
| HeaderSectionSetBodyVisible | Sets the visibility of the Header Body | [Docs](https://support.north52.com/knowledgebase/article/KA-10357-dynamics-crm-365-Sets-the-visibility-of-the-Header-Body/en-us) |
| HideFields | Hides one or more fields on a form | [Docs](https://support.north52.com/knowledgebase/article/KA-01539-dynamics-crm-365-HideFields/en-us) |
| HideLeftHandNavItems | Hides one or more left hand navigation items | [Docs](https://support.north52.com/knowledgebase/article/KA-01540-dynamics-crm-365-HideLeftHandNavItems/en-us) |
| HideProcess | Hides the BPF control Process | [Docs](https://support.north52.com/knowledgebase/article/KA-10486-dynamics-crm-365-HideProcess/en-us) |
| HideSections | Hides one or more sections on a form | [Docs](https://support.north52.com/knowledgebase/article/KA-01541-dynamics-crm-365-HideSections/en-us) |
| HideTabs | Hides one or more tabs on a form | [Docs](https://support.north52.com/knowledgebase/article/KA-01542-dynamics-crm-365-HideTabs/en-us) |
| MultipleClientSide | Executes multiple client side actions | [Docs](https://support.north52.com/knowledgebase/article/KA-01543-dynamics-crm-365-MultipleClientSide/en-us) |
| NavigateToEntityList | Navigate to the default main view of an Entity List | [Docs](https://support.north52.com/knowledgebase/article/KA-10176-dynamics-crm-365-NavigateToEntityList/en-us) |
| NavigateToEntityRecord | Navigate to a an Entity Record, opening either inline or a dialog | [Docs](https://support.north52.com/knowledgebase/article/KA-10271-dynamics-crm-365-NavigateToEntityRecord/en-us) |
| NavigateToWebresource | Navigate to a Web Resource, opening either inline or a dialog | [Docs](https://support.north52.com/knowledgebase/article/KA-10177-dynamics-crm-365-NavigateToWebresource/en-us) |
| OpenEntityForm | Opens an entity form for either an existing record or to create a new record | [Docs](https://support.north52.com/knowledgebase/article/KA-01545-dynamics-crm-365-OpenEntityForm/en-us) |
| OpenQuickCreate | Opens a new quick create form and optionally set field values | [Docs](https://support.north52.com/knowledgebase/article/KA-01546-dynamics-crm-365-OpenQuickCreate/en-us) |
| OpenURL | Opens the specified URL | [Docs](https://support.north52.com/knowledgebase/article/KA-10154-dynamics-crm-365-OpenURL/en-us) |
| OpenWindow | Opens a new window with the provided URL | [Docs](https://support.north52.com/knowledgebase/article/KA-01544-dynamics-crm-365-OpenWindow/en-us) |
| QuickButtonDisable | Disables a Quick Button | [Docs](https://support.north52.com/knowledgebase/article/KA-01548-dynamics-crm-365-QuickButtonDisable/en-us) |
| QuickButtonEnable | Enables a Quick Button | [Docs](https://support.north52.com/knowledgebase/article/KA-01547-dynamics-crm-365-QuickButtonEnable/en-us) |
| ReflowProcess | Reflows a Process | [Docs](https://support.north52.com/knowledgebase/article/KA-10488-dynamics-crm-365-ReflowProcess/en-us) |
| RefreshForm | Refresh the form | [Docs](https://support.north52.com/knowledgebase/article/KA-01549-dynamics-crm-365-RefreshForm/en-us) |
| RefreshRibbon | Refresh the ribbon | [Docs](https://support.north52.com/knowledgebase/article/KA-10111-dynamics-crm-365-RefreshRibbon/en-us) |
| RefreshSubGrid | Refresh a subgrid | [Docs](https://support.north52.com/knowledgebase/article/KA-01550-dynamics-crm-365-RefreshSubGrid/en-us) |
| RefreshWebResource | Refresh a web-resource | [Docs](https://support.north52.com/knowledgebase/article/KA-01551-dynamics-crm-365-RefreshWebResource/en-us) |
| SelectForm | Selects a given form by index | [Docs](https://support.north52.com/knowledgebase/article/KA-01554-dynamics-crm-365-SelectForm/en-us) |
| SelectFormByName | Selects a given form by name | [Docs](https://support.north52.com/knowledgebase/article/KA-01555-dynamics-crm-365-SelectFormByName/en-us) |
| SetClientSideField | Set a field on the client side | [Docs](https://support.north52.com/knowledgebase/article/KA-01556-dynamics-crm-365-SetClientSideField/en-us) |
| SetDefaultView | Set a default view | [Docs](https://support.north52.com/knowledgebase/article/KA-01559-dynamics-crm-365-SetDefaultView/en-us) |
| SetFocus | Set the focus on a field | [Docs](https://support.north52.com/knowledgebase/article/KA-01561-dynamics-crm-365-SetFocus/en-us) |
| SetFormNotification | Sets the form notification | [Docs](https://support.north52.com/knowledgebase/article/KA-01560-dynamics-crm-365-SetFormNotification/en-us) |
| SetIFrame | Set an iframe | [Docs](https://support.north52.com/knowledgebase/article/KA-01562-dynamics-crm-365-SetIFrame/en-us) |
| SetLabelControl | Set a Controls label property | [Docs](https://support.north52.com/knowledgebase/article/KA-10018-dynamics-crm-365-SetLabelControl/en-us) |
| SetLabelSection | Set a Sections label property | [Docs](https://support.north52.com/knowledgebase/article/KA-01553-dynamics-crm-365-SetLabelSection/en-us) |
| SetLabelTab | Set a Tabs label property | [Docs](https://support.north52.com/knowledgebase/article/KA-01552-dynamics-crm-365-SetLabelTab/en-us) |
| SetPicklistValues | Sets the available picklist values | [Docs](https://support.north52.com/knowledgebase/article/KA-01565-dynamics-crm-365-SetPicklistValues/en-us) |
| SetRequiredFields | Sets one or more fields to be required | [Docs](https://support.north52.com/knowledgebase/article/KA-01563-dynamics-crm-365-SetRequiredFields/en-us) |
| SetVarMultipleClientSide | SetVarMultipleClientSide allows you to set a variable based on MultipleClientSide | [Docs](https://support.north52.com/knowledgebase/article/KA-02135-dynamics-crm-365-SetVarMultipleClientSide/en-us) |
| ShowLeftHandNavItems | Shows one or more left hand navigation items | [Docs](https://support.north52.com/knowledgebase/article/KA-01567-dynamics-crm-365-ShowLeftHandNavItems/en-us) |
| ShowProcess | Shows a BPF control Process | [Docs](https://support.north52.com/knowledgebase/article/KA-10487-dynamics-crm-365-ShowProcess/en-us) |
| ShowSections | Shows one or more sections on a form | [Docs](https://support.north52.com/knowledgebase/article/KA-01568-dynamics-crm-365-ShowSections/en-us) |
| ShowTabs | Shows one or more tabs on a form | [Docs](https://support.north52.com/knowledgebase/article/KA-01569-dynamics-crm-365-ShowTabs/en-us) |
| ToClientSide | Convert to client side | [Docs](https://support.north52.com/knowledgebase/article/KA-02190-dynamics-crm-365-ToClientSide/en-us) |

---

## Conversions

Functions for converting between data types.

| Function | Description | Link |
|----------|-------------|------|
| CDate | Converts a string to a date | [Docs](https://support.north52.com/knowledgebase/article/KA-10476-dynamics-crm-365-CDate/en-us) |
| CDateExact | Converts a string to a date with exact format | [Docs](https://support.north52.com/knowledgebase/article/KA-10477-dynamics-crm-365-CDateExact/en-us) |
| CDecimal | Converts a string to a decimal | [Docs](https://support.north52.com/knowledgebase/article/KA-01570-dynamics-crm-365-CDecimal/en-us) |
| CDecimalToInt32 | Converts a decimal to an int32 | [Docs](https://support.north52.com/knowledgebase/article/KA-01571-dynamics-crm-365-CDecimalToInt32/en-us) |
| CDouble | Converts a string to a double | [Docs](https://support.north52.com/knowledgebase/article/KA-01572-dynamics-crm-365-CDouble/en-us) |
| CFloatToInt32 | Converts a float to an int32 | [Docs](https://support.north52.com/knowledgebase/article/KA-01573-dynamics-crm-365-CFloatToInt32/en-us) |
| CInt32 | Converts a string to an int32 | [Docs](https://support.north52.com/knowledgebase/article/KA-01574-dynamics-crm-365-CInt32/en-us) |
| CInt64 | Converts a string to an int64 | [Docs](https://support.north52.com/knowledgebase/article/KA-01575-dynamics-crm-365-CInt64/en-us) |
| CNodeToXml | Converts a node to XML string | [Docs](https://support.north52.com/knowledgebase/article/KA-01578-dynamics-crm-365-CNodeToXml/en-us) |
| ConvertCollectionToJson | Converts an EntityCollection or xCache collection to a JSON document | [Docs](https://support.north52.com/knowledgebase/article/KA-10150-dynamics-crm-365-ConvertCollectionToJson/en-us) |
| ConvertListToEntityCollection | Returns an Entity Collection from a list of values | [Docs](https://support.north52.com/knowledgebase/article/KA-10034-dynamics-crm-365-ConvertListToEntityCollection/en-us) |
| ConvertxCacheLocalToEntityCollection | Returns an EntityCollection from an Local (in-memory) xCache table | [Docs](https://support.north52.com/knowledgebase/article/KA-10116-dynamics-crm-365-ConvertxCacheLocalToEntityCollection/en-us) |
| COptionSetValue | Returns an OptionSetValue | [Docs](https://support.north52.com/knowledgebase/article/KA-01576-dynamics-crm-365-COptionSetValue/en-us) |
| SpecifyKindUTC | Returns a datetime field that has its Kind property set to UTC | [Docs](https://support.north52.com/knowledgebase/article/KA-10035-dynamics-crm-365-SpecifyKindUTC/en-us) |

---

## Date

Functions for working with dates and times.

| Function | Description | Link |
|----------|-------------|------|
| AddDays | Adds days to a date | [Docs](https://support.north52.com/knowledgebase/article/KA-01579-dynamics-crm-365-AddDays/en-us) |
| AddHours | Adds hours to a date | [Docs](https://support.north52.com/knowledgebase/article/KA-01580-dynamics-crm-365-AddHours/en-us) |
| AddMinutes | Adds minutes to a date | [Docs](https://support.north52.com/knowledgebase/article/KA-01582-dynamics-crm-365-AddMinutes/en-us) |
| AddMonths | Adds months to a date | [Docs](https://support.north52.com/knowledgebase/article/KA-01581-dynamics-crm-365-AddMonths/en-us) |
| AddSeconds | Adds seconds to a date | [Docs](https://support.north52.com/knowledgebase/article/KA-01583-dynamics-crm-365-AddSeconds/en-us) |
| AddYears | Adds years to a date | [Docs](https://support.north52.com/knowledgebase/article/KA-01584-dynamics-crm-365-AddYears/en-us) |
| CreateDate | Returns a date given a set of inputs | [Docs](https://support.north52.com/knowledgebase/article/KA-01605-dynamics-crm-365-CreateDate/en-us) |
| DateDiff | Calculate the difference in time between 2 dates for a specified interval | [Docs](https://support.north52.com/knowledgebase/article/KA-01606-dynamics-crm-365-DateDiff/en-us) |
| DateDiffDescription | Calculate the elapsed description difference in time between 2 dates | [Docs](https://support.north52.com/knowledgebase/article/KA-01608-dynamics-crm-365-DateDiffDescription/en-us) |
| DateDiffElapsed | Calculate the elapsed difference in time between 2 dates for a specified interval | [Docs](https://support.north52.com/knowledgebase/article/KA-01607-dynamics-crm-365-DateDiffElapsed/en-us) |
| DiffWorkingDays | Returns the number of working days between two dates | [Docs](https://support.north52.com/knowledgebase/article/KA-01601-dynamics-crm-365-DiffWorkingDays/en-us) |
| GetDateOnly | Returns the date only part of a datetime | [Docs](https://support.north52.com/knowledgebase/article/KA-01589-dynamics-crm-365-GetDateOnly/en-us) |
| GetDay | Returns the day part of a datetime | [Docs](https://support.north52.com/knowledgebase/article/KA-01590-dynamics-crm-365-GetDay/en-us) |
| GetDayOfWeekName | Returns the day name for the given datetime | [Docs](https://support.north52.com/knowledgebase/article/KA-01591-dynamics-crm-365-GetDayOfWeekName/en-us) |
| GetDayOfWeekNumber | Returns the day number for the given datetime | [Docs](https://support.north52.com/knowledgebase/article/KA-01592-dynamics-crm-365-GetDayOfWeekNumber/en-us) |
| GetDaysInMonth | Returns the number of days in the given month | [Docs](https://support.north52.com/knowledgebase/article/KA-01593-dynamics-crm-365-GetDaysInMonth/en-us) |
| GetDifferenceWorkingTime | Returns the working time between two dates | [Docs](https://support.north52.com/knowledgebase/article/KA-02142-dynamics-crm-365-GetDifferenceWorkingTime/en-us) |
| GetFirstDayOfMonth | Returns the first day of the month given a date | [Docs](https://support.north52.com/knowledgebase/article/KA-01594-dynamics-crm-365-GetFirstDayOfMonth/en-us) |
| GetFirstDayOfWeek | Returns the first day of the week given a date | [Docs](https://support.north52.com/knowledgebase/article/KA-01596-dynamics-crm-365-GetFirstDayOfWeek/en-us) |
| GetHour | Returns the hour part of a datetime | [Docs](https://support.north52.com/knowledgebase/article/KA-10119-dynamics-crm-365-GetHour/en-us) |
| GetLastDayOfMonth | Returns the last day of the month given a date | [Docs](https://support.north52.com/knowledgebase/article/KA-01595-dynamics-crm-365-GetLastDayOfMonth/en-us) |
| GetMinute | Returns the minute part of a datetime value | [Docs](https://support.north52.com/knowledgebase/article/KA-10120-dynamics-crm-365-GetMinute/en-us) |
| GetMonth | Returns the month part of a datetime | [Docs](https://support.north52.com/knowledgebase/article/KA-01597-dynamics-crm-365-GetMonth/en-us) |
| GetNextWorkingDay | Returns the next working day given a date to start from | [Docs](https://support.north52.com/knowledgebase/article/KA-01603-dynamics-crm-365-GetNextWorkingDay/en-us) |
| GetNextWorkingTime | Returns the next working time given a date to start from | [Docs](https://support.north52.com/knowledgebase/article/KA-01604-dynamics-crm-365-GetNextWorkingTime/en-us) |
| GetWeek | Returns the week number for the specified date | [Docs](https://support.north52.com/knowledgebase/article/KA-01599-dynamics-crm-365-GetWeek/en-us) |
| GetWeekElapsed | Returns the elapsed week number for the specified date | [Docs](https://support.north52.com/knowledgebase/article/KA-01600-dynamics-crm-365-GetWeekElapsed/en-us) |
| GetYear | Returns the year part of a datetime | [Docs](https://support.north52.com/knowledgebase/article/KA-01598-dynamics-crm-365-GetYear/en-us) |
| IsLeapYear | Returns true or false if the given date is a leap year | [Docs](https://support.north52.com/knowledgebase/article/KA-01609-dynamics-crm-365-IsLeapYear/en-us) |
| IsWorkingDay | Returns true if the passed date is a working day | [Docs](https://support.north52.com/knowledgebase/article/KA-01602-dynamics-crm-365-IsWorkingDay/en-us) |
| LocalDate | Returns the current date for the timezone that is set for the requesting user | [Docs](https://support.north52.com/knowledgebase/article/KA-01610-dynamics-crm-365-LocalDate/en-us) |
| LocalDateTime | Returns the current date and time for the timezone that is set for the requesting user | [Docs](https://support.north52.com/knowledgebase/article/KA-01611-dynamics-crm-365-LocalDateTime/en-us) |
| LocalTimeFromUtcTime | Returns the date and time given a UTC datetime for the timezone | [Docs](https://support.north52.com/knowledgebase/article/KA-01612-dynamics-crm-365-LocalTimeFromUtcTime/en-us) |
| MaxOfDates | Returns the maximum date from a set of dates | [Docs](https://support.north52.com/knowledgebase/article/KA-01585-dynamics-crm-365-MaxOfDates/en-us) |
| MaxOfDatesWithAnchor | Returns the maximum date given an anchor and operator | [Docs](https://support.north52.com/knowledgebase/article/KA-01587-dynamics-crm-365-MaxOfDatesWithAnchor/en-us) |
| MinOfDates | Returns the minimum date from a set of dates | [Docs](https://support.north52.com/knowledgebase/article/KA-01586-dynamics-crm-365-MinOfDates/en-us) |
| MinOfDatesWithAnchor | Returns the minimum date given an anchor and operator | [Docs](https://support.north52.com/knowledgebase/article/KA-01588-dynamics-crm-365-MinOfDatesWithAnchor/en-us) |
| TimeRangeGetIntersection | Returns the Intersection between two time ranges | [Docs](https://support.north52.com/knowledgebase/article/KA-01614-dynamics-crm-365-TimeRangeGetIntersection/en-us) |
| TimeRangeGetRelation | Returns the relationship between two time ranges | [Docs](https://support.north52.com/knowledgebase/article/KA-01613-dynamics-crm-365-TimeRangeGetRelation/en-us) |
| TimeRangeHasInsideCheck | Returns the HasInside between two time ranges | [Docs](https://support.north52.com/knowledgebase/article/KA-02148-dynamics-crm-365-TimeRangeHasInsideCheck/en-us) |
| TimeRangeOverlapsWithCheck | Returns the OverlapsWith between two time ranges | [Docs](https://support.north52.com/knowledgebase/article/KA-02149-dynamics-crm-365-TimeRangeOverlapsWithCheck/en-us) |
| UnixTimeStamp | Returns a UNIX timestamp at time of execution | [Docs](https://support.north52.com/knowledgebase/article/KA-10098-dynamics-crm-365-UnixTimeStamp/en-us) |
| UtcDate | Returns the current UTC date | [Docs](https://support.north52.com/knowledgebase/article/KA-01639-dynamics-crm-365-UtcDate/en-us) |
| UtcDateTime | Returns the current UTC date and time | [Docs](https://support.north52.com/knowledgebase/article/KA-01640-dynamics-crm-365-UtcDateTime/en-us) |
| UtcTimeFromLocalTime | Returns the current UTC time given a date and time that is local to a specified user | [Docs](https://support.north52.com/knowledgebase/article/KA-01641-dynamics-crm-365-UtcTimeFromLocalTime/en-us) |

---

## Find (Single Values)

Functions for retrieving single values from Dataverse.

| Function | Description | Link |
|----------|-------------|------|
| FindAvg | Returns the average value for the records specified | [Docs](https://support.north52.com/knowledgebase/article/KA-01642-dynamics-crm-365-FindAvg/en-us) |
| FindAvgFD | Returns the average value for the records specified by FetchXML | [Docs](https://support.north52.com/knowledgebase/article/KA-01652-dynamics-crm-365-FindAvgFD/en-us) |
| FindCount | Returns the number of records specified by the input parameters | [Docs](https://support.north52.com/knowledgebase/article/KA-01643-dynamics-crm-365-FindCount/en-us) |
| FindCountFD | Returns the number of records as specified by the FetchXML | [Docs](https://support.north52.com/knowledgebase/article/KA-01653-dynamics-crm-365-FindCountFD/en-us) |
| FindListValues | Finds a comma separated list of values on an entity | [Docs](https://support.north52.com/knowledgebase/article/KA-01644-dynamics-crm-365-FindListValues/en-us) |
| FindMax | Returns the maximum value for the records specified | [Docs](https://support.north52.com/knowledgebase/article/KA-01645-dynamics-crm-365-FindMax/en-us) |
| FindMaxFD | Returns the maximum value for the records specified by FetchXML | [Docs](https://support.north52.com/knowledgebase/article/KA-01654-dynamics-crm-365-FindMaxFD/en-us) |
| FindMin | Returns the minimum value for the records specified | [Docs](https://support.north52.com/knowledgebase/article/KA-01646-dynamics-crm-365-FindMin/en-us) |
| FindMinFD | Returns the minimum value for the records specified by FetchXML | [Docs](https://support.north52.com/knowledgebase/article/KA-01655-dynamics-crm-365-FindMinFD/en-us) |
| FindProductPropertiesByRegardingIDAndPropertyName | Returns a Product Property given a regardingobjectid and property name | [Docs](https://support.north52.com/knowledgebase/article/KA-01660-dynamics-crm-365-FindProductPropertiesByRegardingIDAndPropertyName/en-us) |
| FindRecordValue | Finds a specific field value in an entity | [Docs](https://support.north52.com/knowledgebase/article/KA-02133-dynamics-crm-365-FindRecordValue/en-us) |
| FindRecordValueNative | Finds a specific field value (native datatype) in an entity | [Docs](https://support.north52.com/knowledgebase/article/KA-02134-dynamics-crm-365-FindRecordValueNative/en-us) |
| FindSum | Returns the Sum for the records specified | [Docs](https://support.north52.com/knowledgebase/article/KA-01647-dynamics-crm-365-FindSum/en-us) |
| FindSumFD | Returns the Sum for the records specified by FetchXML | [Docs](https://support.north52.com/knowledgebase/article/KA-01656-dynamics-crm-365-FindSumFD/en-us) |
| FindTemplateId | Find a Template ID based on Name and Language Code | [Docs](https://support.north52.com/knowledgebase/article/KA-10388-dynamics-crm-365-FindTemplateId/en-us) |
| FindValue | Finds a value in any field on any entity based on search criteria | [Docs](https://support.north52.com/knowledgebase/article/KA-01648-dynamics-crm-365-FindValue/en-us) |
| FindValueFD | Finds a value via FetchXML | [Docs](https://support.north52.com/knowledgebase/article/KA-01657-dynamics-crm-365-FindValueFD/en-us) |
| SetFindAnd | Builds multiple 'And' conditions for a FetchXML filter | [Docs](https://support.north52.com/knowledgebase/article/KA-10397-dynamics-crm-365-SetFindAnd/en-us) |
| SetFindSelect | Build the list of attributes to retrieve on a Find function | [Docs](https://support.north52.com/knowledgebase/article/KA-01662-dynamics-crm-365-SetFindSelect/en-us) |

---

## Find (EntityCollections)

Functions for retrieving multiple records from Dataverse.

| Function | Description | Link |
|----------|-------------|------|
| FindRecords | Finds a collection of records | [Docs](https://support.north52.com/knowledgebase/article/KA-01663-dynamics-crm-365-FindRecords/en-us) |
| FindRecordsAudit | Generate an EntityCollection of the Audit Trail for a particular record | [Docs](https://support.north52.com/knowledgebase/article/KA-01664-dynamics-crm-365-FindRecordsAudit/en-us) |
| FindRecordsAuditHtml | Generate a HTML table of the Audit Trail for a particular record | [Docs](https://support.north52.com/knowledgebase/article/KA-01674-dynamics-crm-365-FindRecordsAuditHtml/en-us) |
| FindRecordsFD | Finds a collection of records as defined by FetchXML | [Docs](https://support.north52.com/knowledgebase/article/KA-01665-dynamics-crm-365-FindRecordsFD/en-us) |
| FindRecordsFetchXml | Finds a collection of records as defined by raw FetchXML | [Docs](https://support.north52.com/knowledgebase/article/KA-01666-dynamics-crm-365-FindRecordsFetchXml/en-us) |
| FindJArrayItem | Used with CreateJArrayChildren() function to build data | [Docs](https://support.north52.com/knowledgebase/article/KA-01869-dynamics-crm-365-FindJArrayItem/en-us) |
| FindXmlItem | Used with CreateXmlChildren() function to lookup values | [Docs](https://support.north52.com/knowledgebase/article/KA-01878-dynamics-crm-365-FindXmlItem/en-us) |

---

## HTML

Functions for working with HTML content.

| Function | Description | Link |
|----------|-------------|------|
| HtmlDecode | Returns decoded HTML from encoded HTML | [Docs](https://support.north52.com/knowledgebase/article/KA-01676-dynamics-crm-365-HtmlDecode/en-us) |
| HtmlEncode | Returns encoded HTML from plain HTML | [Docs](https://support.north52.com/knowledgebase/article/KA-01675-dynamics-crm-365-HtmlEncode/en-us) |
| LinkDialogUrl | Generates a hyper link to be used in a Dialog Process | [Docs](https://support.north52.com/knowledgebase/article/KA-01679-dynamics-crm-365-LinkDialogUrl/en-us) |
| LinkHyperLinkUrl | Generates a hyper link url | [Docs](https://support.north52.com/knowledgebase/article/KA-01680-dynamics-crm-365-LinkHyperLinkUrl/en-us) |
| LinkPlainHyperLink | Generates a plain hyper link url | [Docs](https://support.north52.com/knowledgebase/article/KA-01678-dynamics-crm-365-LinkPlainHyperLink/en-us) |
| LinkRawUrl | Generates a raw hyper link url as a string | [Docs](https://support.north52.com/knowledgebase/article/KA-01677-dynamics-crm-365-LinkRawUrl/en-us) |
| SetQueryString | Returns a valid query string | [Docs](https://support.north52.com/knowledgebase/article/KA-01681-dynamics-crm-365-SetQueryString/en-us) |
| StripHtml | Removes all HTML from a field | [Docs](https://support.north52.com/knowledgebase/article/KA-01682-dynamics-crm-365-StripHtml/en-us) |

---

## Industry

Industry-specific or specialized calculation functions.

| Function | Description | Link |
|----------|-------------|------|
| Annuity_NPER | Calculate the number of periods for an annuity | [Docs](https://support.north52.com/knowledgebase/article/KA-10500-dynamics-crm-365-Annuity_NPER/en-us) |
| Annuity_PMT | Calculate the periodic payment for an annuity | [Docs](https://support.north52.com/knowledgebase/article/KA-10494-dynamics-crm-365-Annuity_PMT/en-us) |
| Annuity_PPMT | Calculate principal payments for an annuity | [Docs](https://support.north52.com/knowledgebase/article/KA-10496-dynamics-crm-365-Annuity_PPMT/en-us) |
| Annuity_PV | Calculate the present value of an annuity | [Docs](https://support.north52.com/knowledgebase/article/KA-10497-dynamics-crm-365-Annuity_PV/en-us) |
| Annuity_Rate | Calculate the interest rate per period of an annuity | [Docs](https://support.north52.com/knowledgebase/article/KA-10495-dynamics-crm-365-Annuity_Rate/en-us) |
| DamerauLevenshteinDistance | Computes the Damerau Levenshtein Distance between 2 strings | [Docs](https://support.north52.com/knowledgebase/article/KA-01669-dynamics-crm-365-DamerauLevenshteinDistance/en-us) |
| Depreciation_DDB | Calculate depreciation using double-declining balance method | [Docs](https://support.north52.com/knowledgebase/article/KA-10504-dynamics-crm-365-Depreciation_DDB/en-us) |
| Depreciation_SLN | Calculate straight-line depreciation | [Docs](https://support.north52.com/knowledgebase/article/KA-10505-dynamics-crm-365-Depreciation_SLN/en-us) |
| Depreciation_SYD | Calculate sum-of-years' digits depreciation | [Docs](https://support.north52.com/knowledgebase/article/KA-10506-dynamics-crm-365-Depreciation_SYD/en-us) |
| LevenshteinDistance | Computes the Levenshtein Distance between 2 strings | [Docs](https://support.north52.com/knowledgebase/article/KA-01670-dynamics-crm-365-LevenshteinDistance/en-us) |
| Metaphone3 | Returns a phonetic 'sounds like' encoding of a string | [Docs](https://support.north52.com/knowledgebase/article/KA-01671-dynamics-crm-365-Metaphone3/en-us) |
| PresentValue_NPV | Calculate net present value | [Docs](https://support.north52.com/knowledgebase/article/KA-10501-dynamics-crm-365-PresentValue_NPV/en-us) |
| RatesReturn_IRR | Calculate internal rate of return | [Docs](https://support.north52.com/knowledgebase/article/KA-10503-dynamics-crm-365-RatesReturn_IRR/en-us) |
| RatesReturn_MIRR | Calculate modified internal rate of return | [Docs](https://support.north52.com/knowledgebase/article/KA-10502-dynamics-crm-365-RatesReturn_MIRR/en-us) |
| Similarity | Returns a percentage of how alike 2 strings are | [Docs](https://support.north52.com/knowledgebase/article/KA-01672-dynamics-crm-365-Similarity/en-us) |

---

## JSON

Functions for working with JSON data.

| Function | Description | Link |
|----------|-------------|------|
| CreateJArray | Creates a JSON Array | [Docs](https://support.north52.com/knowledgebase/article/KA-01865-dynamics-crm-365-CreateJArray/en-us) |
| CreateJArrayChildren | Creates a JSON Array populated with JObjects from FindRecords() | [Docs](https://support.north52.com/knowledgebase/article/KA-01866-dynamics-crm-365-CreateJArrayChildren/en-us) |
| CreateJObject | Creates a JSON Object | [Docs](https://support.north52.com/knowledgebase/article/KA-01867-dynamics-crm-365-CreateJObject/en-us) |
| CreateJProperty | Creates a JSON Property | [Docs](https://support.north52.com/knowledgebase/article/KA-01868-dynamics-crm-365-CreateJProperty/en-us) |
| ExecuteCustomJSFunction | Execute a custom JS function | [Docs](https://support.north52.com/knowledgebase/article/KA-01827-dynamics-crm-365-ExecuteCustomJSFunction/en-us) |
| GetVarJsonEC | Get an EntityCollection from a JSON document | [Docs](https://support.north52.com/knowledgebase/article/KA-01871-dynamics-crm-365-GetVarJsonEC/en-us) |
| GetVarJsonValue | Gets a value from a JSON document | [Docs](https://support.north52.com/knowledgebase/article/KA-01870-dynamics-crm-365-GetVarJsonValue/en-us) |
| GetVarXPathEC | Get an EntityCollection from a XML document | [Docs](https://support.north52.com/knowledgebase/article/KA-01880-dynamics-crm-365-GetVarXPathEC/en-us) |
| JObjectParse | Creates a JSON Object from a string of JSON | [Docs](https://support.north52.com/knowledgebase/article/KA-02164-dynamics-crm-365-JObjectParse/en-us) |
| SetVarAppendJArray | Appends an item to a JSON Array variable | [Docs](https://support.north52.com/knowledgebase/article/KA-10398-dynamics-crm-365-SetVarAppendJArray/en-us) |
| SetVarAppendJObject | Appends an item to a JSON Object variable | [Docs](https://support.north52.com/knowledgebase/article/KA-10399-dynamics-crm-365-SetVarAppendJObject/en-us) |

---

## Localization

Functions for working with multiple languages and cultures.

| Function | Description | Link |
|----------|-------------|------|
| GetAttributeDisplayName | Returns the localized string name for an attribute | [Docs](https://support.north52.com/knowledgebase/article/KA-01683-dynamics-crm-365-GetAttributeDisplayName/en-us) |
| GetOptionSetName | Returns the localized string name for an optionset value | [Docs](https://support.north52.com/knowledgebase/article/KA-01684-dynamics-crm-365-GetOptionSetName/en-us) |

---

## Logical

Functions for conditional logic and mathematical operations.

| Function | Description | Link |
|----------|-------------|------|
| and | Returns TRUE if all values are true | [Docs](https://support.north52.com/knowledgebase/article/KA-01692-dynamics-crm-365-and/en-us) |
| Case | Builds a CASE statement | [Docs](https://support.north52.com/knowledgebase/article/KA-01686-dynamics-crm-365-Case/en-us) |
| Divide | Divides two values | [Docs](https://support.north52.com/knowledgebase/article/KA-01695-dynamics-crm-365-Divide/en-us) |
| Equals to ( = ) | Evaluates if two values are equivalent | [Docs](https://support.north52.com/knowledgebase/article/KA-01699-dynamics-crm-365-Equals-to-(-%3d-)-/en-us) |
| ForEachRecord | Iterates over a set of records and performs an action | [Docs](https://support.north52.com/knowledgebase/article/KA-01706-dynamics-crm-365-ForEachRecord/en-us) |
| Greater than | Evaluates if a value is greater than another value | [Docs](https://support.north52.com/knowledgebase/article/KA-01702-dynamics-crm-365-Greater-than/en-us) |
| if | Build an if statement | [Docs](https://support.north52.com/knowledgebase/article/KA-01687-dynamics-crm-365-if/en-us) |
| If Not Equal to ( != ) | Evaluates if two values are not equivalent | [Docs](https://support.north52.com/knowledgebase/article/KA-01700-dynamics-crm-365-If-Not-Equal-to-(-!%3d-)-/en-us) |
| iftrue | Build an iftrue statement | [Docs](https://support.north52.com/knowledgebase/article/KA-01688-dynamics-crm-365-iftrue/en-us) |
| In | Returns true if a value is found within the set of values | [Docs](https://support.north52.com/knowledgebase/article/KA-01690-dynamics-crm-365-In/en-us) |
| Less than | Evaluates if a value is less than another value | [Docs](https://support.north52.com/knowledgebase/article/KA-01701-dynamics-crm-365-Less-than/en-us) |
| Minus (-) | Calculates the difference of two values | [Docs](https://support.north52.com/knowledgebase/article/KA-01694-dynamics-crm-365-Minus-(-)/en-us) |
| Mod | Returns a remainder after division | [Docs](https://support.north52.com/knowledgebase/article/KA-01697-dynamics-crm-365-Mod/en-us) |
| Multiply | Multiplies two values | [Docs](https://support.north52.com/knowledgebase/article/KA-01696-dynamics-crm-365-Multiply/en-us) |
| NoOp | No Operation - do nothing | [Docs](https://support.north52.com/knowledgebase/article/KA-01689-dynamics-crm-365-NoOp/en-us) |
| Not Operator ( ! ) | Negates what it is applied to | [Docs](https://support.north52.com/knowledgebase/article/KA-01698-dynamics-crm-365-Not-Operator-(-!-)-/en-us) |
| or | Returns TRUE if any expression is true | [Docs](https://support.north52.com/knowledgebase/article/KA-01691-dynamics-crm-365-or/en-us) |
| Plus | Calculates the sum of two values | [Docs](https://support.north52.com/knowledgebase/article/KA-01693-dynamics-crm-365-Plus/en-us) |

---

## Loop

Functions for iterating and looping operations.

| Function | Description | Link |
|----------|-------------|------|
| CurrentRecord | Access a field within the current record loop | [Docs](https://support.north52.com/knowledgebase/article/KA-01707-dynamics-crm-365-CurrentRecord/en-us) |
| CurrentRecordNested | Access a field within nested loops | [Docs](https://support.north52.com/knowledgebase/article/KA-10133-dynamics-crm-365-CurrentRecordNested/en-us) |
| DoLoop | Builds a DoLoop statement that executes actions | [Docs](https://support.north52.com/knowledgebase/article/KA-01703-dynamics-crm-365-DoLoop/en-us) |
| DoLoopIndex | Access the current index number of the loop | [Docs](https://support.north52.com/knowledgebase/article/KA-01704-dynamics-crm-365-DoLoopIndex/en-us) |
| DoLoopTotal | Access the total number of loops | [Docs](https://support.north52.com/knowledgebase/article/KA-01705-dynamics-crm-365-DoLoopTotal/en-us) |
| ForEachRecordNested | Loop inside another loop | [Docs](https://support.north52.com/knowledgebase/article/KA-10132-dynamics-crm-365-ForEachRecordNested/en-us) |
| LoopUntilTrue | Performs a loop until condition evaluates to true | [Docs](https://support.north52.com/knowledgebase/article/KA-01711-dynamics-crm-365-LoopUntilTrue/en-us) |
| RecordEntityName | Returns the entity logical name for the current record in loop | [Docs](https://support.north52.com/knowledgebase/article/KA-01708-dynamics-crm-365-RecordEntityName/en-us) |
| RecordEntityNameNested | Returns the entity logical name for nested loop | [Docs](https://support.north52.com/knowledgebase/article/KA-10134-dynamics-crm-365-RecordEntityNameNested/en-us) |
| RecordIndex | Access the current index number of the loop | [Docs](https://support.north52.com/knowledgebase/article/KA-01709-dynamics-crm-365-RecordIndex/en-us) |
| RecordIndexNested | Access the current index number of nested loop | [Docs](https://support.north52.com/knowledgebase/article/KA-10223-dynamics-crm-365-RecordIndexNested/en-us) |
| RecordTotal | Access the total number of loops | [Docs](https://support.north52.com/knowledgebase/article/KA-01710-dynamics-crm-365-RecordTotal/en-us) |
| RecordTotalNested | Access the total number of loops in nested loop | [Docs](https://support.north52.com/knowledgebase/article/KA-10222-dynamics-crm-365-RecordTotalNested/en-us) |

---

## Math

Mathematical calculation functions.

| Function | Description | Link |
|----------|-------------|------|
| Abs | Returns the absolute value | [Docs](https://support.north52.com/knowledgebase/article/KA-01712-dynamics-crm-365-Abs/en-us) |
| Ceiling | Rounds up to the nearest integer | [Docs](https://support.north52.com/knowledgebase/article/KA-01713-dynamics-crm-365-Ceiling/en-us) |
| Exp | Returns e raised to the power of a number | [Docs](https://support.north52.com/knowledgebase/article/KA-01714-dynamics-crm-365-Exp/en-us) |
| Floor | Rounds down to the nearest integer | [Docs](https://support.north52.com/knowledgebase/article/KA-01715-dynamics-crm-365-Floor/en-us) |
| GCD | Returns the Greatest common divisor | [Docs](https://support.north52.com/knowledgebase/article/KA-01716-dynamics-crm-365-GCD/en-us) |
| LCM | Returns the Lowest common multiplier | [Docs](https://support.north52.com/knowledgebase/article/KA-01717-dynamics-crm-365-LCM/en-us) |
| MaxOf | Returns the maximum of two numbers | [Docs](https://support.north52.com/knowledgebase/article/KA-01718-dynamics-crm-365-MaxOf/en-us) |
| MinOf | Returns the minimum of two numbers | [Docs](https://support.north52.com/knowledgebase/article/KA-01719-dynamics-crm-365-MinOf/en-us) |
| Pow | Returns a specified number raised to the specified power | [Docs](https://support.north52.com/knowledgebase/article/KA-01720-dynamics-crm-365-Pow/en-us) |
| Round | Rounds a value to the nearest number | [Docs](https://support.north52.com/knowledgebase/article/KA-01721-dynamics-crm-365-Round/en-us) |
| RoundEx | Round function with extra debugging information | [Docs](https://support.north52.com/knowledgebase/article/KA-10523-dynamics-crm-365-RoundEx/en-us) |
| Sign | Returns -1, 0 or 1 based on the sign of the number | [Docs](https://support.north52.com/knowledgebase/article/KA-01722-dynamics-crm-365-Sign/en-us) |
| Sqrt | Returns the square root | [Docs](https://support.north52.com/knowledgebase/article/KA-01723-dynamics-crm-365-Sqrt/en-us) |
| Truncate | Returns the integer digits, discarding fractional digits | [Docs](https://support.north52.com/knowledgebase/article/KA-01724-dynamics-crm-365-Truncate/en-us) |

---

## Platform Operations

Functions that interact with Dynamics 365 platform operations.

| Function | Description | Link |
|----------|-------------|------|
| AssociateEntities | Creates an N:N relationship between 2 records | [Docs](https://support.north52.com/knowledgebase/article/KA-01725-dynamics-crm-365-AssociateEntities/en-us) |
| CalculateRollupField | Executes a rollup recalculation request | [Docs](https://support.north52.com/knowledgebase/article/KA-02165-dynamics-crm-365-CalculateRollupField/en-us) |
| ConvertQuotetoSalesorder | Converts a Quote to a Sales Order | [Docs](https://support.north52.com/knowledgebase/article/KA-01727-dynamics-crm-365-ConvertQuotetoSalesorder/en-us) |
| ConvertSalesOrdertoInvoice | Converts a Sales Order to an Invoice | [Docs](https://support.north52.com/knowledgebase/article/KA-01726-dynamics-crm-365-ConvertSalesOrdertoInvoice/en-us) |
| DisAssociateEntities | Removes an N:N relationship between 2 records | [Docs](https://support.north52.com/knowledgebase/article/KA-01728-dynamics-crm-365-DisAssociateEntities/en-us) |
| ExecuteAction | Executes an Action | [Docs](https://support.north52.com/knowledgebase/article/KA-01730-dynamics-crm-365-ExecuteAction/en-us) |
| GenerateInvoiceFromOpportunity | Generate Invoice From Opportunity | [Docs](https://support.north52.com/knowledgebase/article/KA-01731-dynamics-crm-365-GenerateInvoiceFromOpportunity/en-us) |
| GenerateQuoteFromOpportunity | Generate Quote From Opportunity | [Docs](https://support.north52.com/knowledgebase/article/KA-01732-dynamics-crm-365-GenerateQuoteFromOpportunity/en-us) |
| GenerateSalesOrderFromOpportunity | Generate SalesOrder From Opportunity | [Docs](https://support.north52.com/knowledgebase/article/KA-01733-dynamics-crm-365-GenerateSalesOrderFromOpportunity/en-us) |
| GetActionOutputParameter | Get the action output parameter from an executed action | [Docs](https://support.north52.com/knowledgebase/article/KA-01734-dynamics-crm-365-GetActionOutputParameter/en-us) |
| GetAssociationRelatedEntityReferenceId | Returns the guid of the related entity in N:N relationship | [Docs](https://support.north52.com/knowledgebase/article/KA-01735-dynamics-crm-365-GetAssociationRelatedEntityReferenceId/en-us) |
| GetAssociationRelationshipName | Returns the name of the N:N relationship | [Docs](https://support.north52.com/knowledgebase/article/KA-01736-dynamics-crm-365-GetAssociationRelationshipName/en-us) |
| RecordShare | Shares a record with a user | [Docs](https://support.north52.com/knowledgebase/article/KA-01739-dynamics-crm-365-RecordShare/en-us) |
| RecordUnShare | Un-shares a record with a user | [Docs](https://support.north52.com/knowledgebase/article/KA-01740-dynamics-crm-365-RecordUnShare/en-us) |
| RecordUnShareAll | Removes all shares with a record | [Docs](https://support.north52.com/knowledgebase/article/KA-01741-dynamics-crm-365-RecordUnShareAll/en-us) |
| StartSchedule | Starts the schedule for the specified name | [Docs](https://support.north52.com/knowledgebase/article/KA-01737-dynamics-crm-365-StartSchedule/en-us) |
| StopSchedule | Stops the schedule for the specified name | [Docs](https://support.north52.com/knowledgebase/article/KA-01738-dynamics-crm-365-StopSchedule/en-us) |

---

## Record Control

Functions for creating, updating, and deleting records.

| Function | Description | Link |
|----------|-------------|------|
| CreateNote | Creates a note within the system | [Docs](https://support.north52.com/knowledgebase/article/KA-01745-dynamics-crm-365-CreateNote/en-us) |
| CreateNoteIfExists | Creates a note if the supplied record guid exists | [Docs](https://support.north52.com/knowledgebase/article/KA-01746-dynamics-crm-365-CreateNoteIfExists/en-us) |
| CreateNoteTraceLog | Creates a Note and stores the output of the trace log | [Docs](https://support.north52.com/knowledgebase/article/KA-10016-dynamics-crm-365-CreateNoteTraceLog/en-us) |
| CreateRecord | Creates a record within the system | [Docs](https://support.north52.com/knowledgebase/article/KA-01742-dynamics-crm-365-CreateRecord/en-us) |
| CreateRecordFromParent | Creates a record from a related lookup record | [Docs](https://support.north52.com/knowledgebase/article/KA-01743-dynamics-crm-365-CreateRecordFromParent/en-us) |
| DeleteRecord | Deletes a record | [Docs](https://support.north52.com/knowledgebase/article/KA-01747-dynamics-crm-365-DeleteRecord/en-us) |
| SetAttribute | Set field value when using CreateRecord or UpdateRecord | [Docs](https://support.north52.com/knowledgebase/article/KA-01755-dynamics-crm-365-SetAttribute/en-us) |
| SetAttributeCustomer | Set customer field when using CreateRecord or UpdateRecord | [Docs](https://support.north52.com/knowledgebase/article/KA-01758-dynamics-crm-365-SetAttributeCustomer/en-us) |
| SetAttributeLookup | Set lookup field when using CreateRecord or UpdateRecord | [Docs](https://support.north52.com/knowledgebase/article/KA-01756-dynamics-crm-365-SetAttributeLookup/en-us) |
| SetAttributePartyList | Set partylist field when using CreateRecord or UpdateRecord | [Docs](https://support.north52.com/knowledgebase/article/KA-01757-dynamics-crm-365-SetAttributePartyList/en-us) |
| SetAttributeStatus | Set status fields when using CreateRecord or UpdateRecord | [Docs](https://support.north52.com/knowledgebase/article/KA-01754-dynamics-crm-365-SetAttributeStatus/en-us) |
| SetAttributeText | Set text attribute | [Docs](https://support.north52.com/knowledgebase/article/KA-10426-dynamics-crm-365-SetAttributeText/en-us) |
| SetEntityTargetRecord | Sets the entity target property bag in pre-operation stage | [Docs](https://support.north52.com/knowledgebase/article/KA-01752-dynamics-crm-365-SetEntityTargetRecord/en-us) |
| UpdateRecord | Updates a record within the system | [Docs](https://support.north52.com/knowledgebase/article/KA-01748-dynamics-crm-365-UpdateRecord/en-us) |
| UpdateRecordWithXml | Updates a record using XML | [Docs](https://support.north52.com/knowledgebase/article/KA-01749-dynamics-crm-365-UpdateRecordWithXml/en-us) |
| UpdateRecordWithJson | Updates a record using JSON | [Docs](https://support.north52.com/knowledgebase/article/KA-01750-dynamics-crm-365-UpdateRecordWithJson/en-us) |
| UpdateRecordsFromCollection | Updates records from an entity collection | [Docs](https://support.north52.com/knowledgebase/article/KA-01751-dynamics-crm-365-UpdateRecordsFromCollection/en-us) |

---

## Regular Expressions

Functions for pattern matching with regular expressions.

| Function | Description | Link |
|----------|-------------|------|
| RegexIsMatch | Returns true if the regex pattern has a match | [Docs](https://support.north52.com/knowledgebase/article/KA-01760-dynamics-crm-365-RegexIsMatch/en-us) |
| RegexMatch | Searches for the first occurrence of the regular expression | [Docs](https://support.north52.com/knowledgebase/article/KA-01759-dynamics-crm-365-RegexMatch/en-us) |
| RegexReplace | Replaces all regex matches with replacement string | [Docs](https://support.north52.com/knowledgebase/article/KA-01761-dynamics-crm-365-RegexReplace/en-us) |

---

## Rest Services

Functions for calling REST APIs.

| Function | Description | Link |
|----------|-------------|------|
| CallRestAPI | Allows you to call a REST based web service | [Docs](https://support.north52.com/knowledgebase/article/KA-01881-dynamics-crm-365-CallRestAPI/en-us) |
| SetRequestActionFail | Execute actions when expected status code is not found | [Docs](https://support.north52.com/knowledgebase/article/KA-01891-dynamics-crm-365-SetRequestActionFail/en-us) |
| SetRequestActionPass | Execute actions when expected status code is found | [Docs](https://support.north52.com/knowledgebase/article/KA-01890-dynamics-crm-365-SetRequestActionPass/en-us) |
| SetRequestAuthenticationNone | Set the authentication to none | [Docs](https://support.north52.com/knowledgebase/article/KA-01887-dynamics-crm-365-SetRequestAuthenticationNone/en-us) |
| SetRequestBaseURL | Sets the Base URL for an API call | [Docs](https://support.north52.com/knowledgebase/article/KA-01882-dynamics-crm-365-SetRequestBaseURL/en-us) |
| SetRequestDetails | Sets the HTTP method (POST, GET, PUT, PATCH) | [Docs](https://support.north52.com/knowledgebase/article/KA-01884-dynamics-crm-365-SetRequestDetails/en-us) |
| SetRequestExpected | Sets the expected response status code | [Docs](https://support.north52.com/knowledgebase/article/KA-01889-dynamics-crm-365-SetRequestExpected/en-us) |
| SetRequestFiles | Pass files as part of the API call | [Docs](https://support.north52.com/knowledgebase/article/KA-01888-dynamics-crm-365-SetRequestFiles/en-us) |
| SetRequestHeaders | Pass name/value set of headers | [Docs](https://support.north52.com/knowledgebase/article/KA-01885-dynamics-crm-365-SetRequestHeaders/en-us) |
| SetRequestParams | Pass name/value set of params | [Docs](https://support.north52.com/knowledgebase/article/KA-01886-dynamics-crm-365-SetRequestParams/en-us) |
| SetRequestResource | Sets the resource name for an API call | [Docs](https://support.north52.com/knowledgebase/article/KA-01883-dynamics-crm-365-SetRequestResource/en-us) |

---

## Set Native Fields

Functions for setting special field types in Dynamics 365.

| Function | Description | Link |
|----------|-------------|------|
| GetPartyListCount | Gets the count of parties in a party list | [Docs](https://support.north52.com/knowledgebase/article/KA-01765-dynamics-crm-365-GetPartyListCount/en-us) |
| GetPartyListItemId | Gets a party record id from a partylist | [Docs](https://support.north52.com/knowledgebase/article/KA-01762-dynamics-crm-365-GetPartyListItemId/en-us) |
| GetPartyListItemName | Gets a party record name from a partylist | [Docs](https://support.north52.com/knowledgebase/article/KA-01764-dynamics-crm-365-GetPartyListItemName/en-us) |
| GetPartyListItemType | Gets a party record type from a partylist | [Docs](https://support.north52.com/knowledgebase/article/KA-01763-dynamics-crm-365-GetPartyListItemType/en-us) |
| SetLookup | Sets the target property when it is of type lookup | [Docs](https://support.north52.com/knowledgebase/article/KA-01767-dynamics-crm-365-SetLookup/en-us) |
| SetPartyList | Sets values for a field of type Party List | [Docs](https://support.north52.com/knowledgebase/article/KA-01770-dynamics-crm-365-SetPartyList/en-us) |
| SetPartyListCombined | Combines multiple SetPartList to a single combined list | [Docs](https://support.north52.com/knowledgebase/article/KA-01771-dynamics-crm-365-SetPartyListCombined/en-us) |
| SetRegardingLookup | Sets the target property when it is a regarding field | [Docs](https://support.north52.com/knowledgebase/article/KA-01772-dynamics-crm-365-SetRegardingLookup/en-us) |
| SetState | Sets the state and status of a record | [Docs](https://support.north52.com/knowledgebase/article/KA-01773-dynamics-crm-365-SetState/en-us) |

---

## SharePoint Services

Functions for interacting with SharePoint.

| Function | Description | Link |
|----------|-------------|------|
| SharePointCreateDocumentLocation | Create a SharePoint Document Location | [Docs](https://support.north52.com/knowledgebase/article/KA-01895-dynamics-crm-365-SharePointCreateDocumentLocation/en-us) |
| SharePointCreateFile | Create a SharePoint File | [Docs](https://support.north52.com/knowledgebase/article/KA-01896-dynamics-crm-365-SharePointCreateFile/en-us) |
| SharePointCreateFolder | Create a SharePoint Folder | [Docs](https://support.north52.com/knowledgebase/article/KA-01897-dynamics-crm-365-SharePointCreateFolder/en-us) |
| SharePointCreateSite | Create a SharePoint Site | [Docs](https://support.north52.com/knowledgebase/article/KA-01898-dynamics-crm-365-SharePointCreateSite/en-us) |
| SharePointDoesFolderExist | Checks if a SharePoint folder exists | [Docs](https://support.north52.com/knowledgebase/article/KA-01901-dynamics-crm-365-SharePointDoesFolderExist/en-us) |
| SharePointFindDocumentsByFetchXml | Find SharePoint documents via fetchxml | [Docs](https://support.north52.com/knowledgebase/article/KA-01902-dynamics-crm-365-SharePointFindDocumentsByFetchXml/en-us) |

---

## String

Functions for manipulating and working with text strings.

| Function | Description | Link |
|----------|-------------|------|
| AppendFormat | Takes a base string and generates a set of strings | [Docs](https://support.north52.com/knowledgebase/article/KA-01774-dynamics-crm-365-AppendFormat/en-us) |
| Base64Decode | Returns a Base64 decoding of a string | [Docs](https://support.north52.com/knowledgebase/article/KA-01776-dynamics-crm-365-Base64Decode/en-us) |
| Base64Encode | Returns a Base64 encoding of a string | [Docs](https://support.north52.com/knowledgebase/article/KA-01775-dynamics-crm-365-Base64Encode/en-us) |
| Capitalize | Capitalize the first letter in a string | [Docs](https://support.north52.com/knowledgebase/article/KA-01777-dynamics-crm-365-Capitalize/en-us) |
| Compress | Returns a compressed string | [Docs](https://support.north52.com/knowledgebase/article/KA-01779-dynamics-crm-365-Compress/en-us) |
| Contains | Returns true if the substring is found | [Docs](https://support.north52.com/knowledgebase/article/KA-01778-dynamics-crm-365-Contains/en-us) |
| CountCharacters | Returns the number of characters in a string | [Docs](https://support.north52.com/knowledgebase/article/KA-01780-dynamics-crm-365-CountCharacters/en-us) |
| CountOccurrences | Returns the number of occurrences of a string | [Docs](https://support.north52.com/knowledgebase/article/KA-02103-dynamics-crm-365-CountOccurrences/en-us) |
| Decompress | Returns a decompressed string | [Docs](https://support.north52.com/knowledgebase/article/KA-01781-dynamics-crm-365-Decompress/en-us) |
| EndsWith | Returns true if one string ends with another | [Docs](https://support.north52.com/knowledgebase/article/KA-01782-dynamics-crm-365-EndsWith/en-us) |
| EscapeDataString | Converts a string to escaped representation | [Docs](https://support.north52.com/knowledgebase/article/KA-01783-dynamics-crm-365-EscapeDataString/en-us) |
| EscapeUriString | Converts a URI string to escaped representation | [Docs](https://support.north52.com/knowledgebase/article/KA-01784-dynamics-crm-365-EscapeUriString/en-us) |
| ExtractDataBetweenTwoStrings | Extracts data from a string, given start and end strings | [Docs](https://support.north52.com/knowledgebase/article/KA-10524-dynamics-crm-365-ExtractDataBetweenTwoStrings/en-us) |
| GenerateGuid | Returns a Guid | [Docs](https://support.north52.com/knowledgebase/article/KA-01785-dynamics-crm-365-GenerateGuid/en-us) |
| GetParamFromUrl | Returns a parameter from a URL | [Docs](https://support.north52.com/knowledgebase/article/KA-01786-dynamics-crm-365-GetParamFromUrl/en-us) |
| IndexOf | Returns the position where first instance was located | [Docs](https://support.north52.com/knowledgebase/article/KA-01787-dynamics-crm-365-IndexOf/en-us) |
| Insert | Inserts one string into another at a position | [Docs](https://support.north52.com/knowledgebase/article/KA-01788-dynamics-crm-365-Insert/en-us) |
| IsAlpha | Checks if a string only contains letters | [Docs](https://support.north52.com/knowledgebase/article/KA-02104-dynamics-crm-365-IsAlpha/en-us) |
| IsAlphaNumeric | Checks if a string only contains letters or numbers | [Docs](https://support.north52.com/knowledgebase/article/KA-02105-dynamics-crm-365-IsAlphaNumeric/en-us) |
| IsDecimal | Checks if a string is a Decimal | [Docs](https://support.north52.com/knowledgebase/article/KA-02102-dynamics-crm-365-IsDecimal/en-us) |
| IsInteger | Checks if a string is an Integer | [Docs](https://support.north52.com/knowledgebase/article/KA-02101-dynamics-crm-365-IsInteger/en-us) |
| Left | Returns the left number of characters in a string | [Docs](https://support.north52.com/knowledgebase/article/KA-01789-dynamics-crm-365-Left/en-us) |
| Lower | Converts all string elements to lower case | [Docs](https://support.north52.com/knowledgebase/article/KA-01790-dynamics-crm-365-Lower/en-us) |
| MatchAndReplace | Match and replace strings | [Docs](https://support.north52.com/knowledgebase/article/KA-02189-dynamics-crm-365-MatchAndReplace/en-us) |
| MatchListFindIntersect | Compares two strings and returns matching patterns | [Docs](https://support.north52.com/knowledgebase/article/KA-10047-dynamics-crm-365-MatchListFindIntersect/en-us) |
| MatchListFindIntersectExists | Compares two strings and returns TRUE if matching pattern exists | [Docs](https://support.north52.com/knowledgebase/article/KA-10048-dynamics-crm-365-MatchListFindIntersectExists/en-us) |
| MatchListFindMissing | Compares strings and returns missing patterns | [Docs](https://support.north52.com/knowledgebase/article/KA-10049-dynamics-crm-365-MatchListFindMissing/en-us) |
| MD5 | Returns a MD5 hash of a string | [Docs](https://support.north52.com/knowledgebase/article/KA-01791-dynamics-crm-365-MD5/en-us) |
| PadLeft | Puts string characters to the left of an input string | [Docs](https://support.north52.com/knowledgebase/article/KA-01792-dynamics-crm-365-PadLeft/en-us) |
| PadRight | Puts string characters to the right of an input string | [Docs](https://support.north52.com/knowledgebase/article/KA-01793-dynamics-crm-365-PadRight/en-us) |
| Remove | Removes a number of characters from a string | [Docs](https://support.north52.com/knowledgebase/article/KA-01796-dynamics-crm-365-Remove/en-us) |
| Replace | Replaces all occurrences of a specified string | [Docs](https://support.north52.com/knowledgebase/article/KA-01794-dynamics-crm-365-Replace/en-us) |
| ReplaceFirstOccurrence | Replaces the first occurrence of a specified string | [Docs](https://support.north52.com/knowledgebase/article/KA-02099-dynamics-crm-365-ReplaceFirstOccurrence/en-us) |
| ReplaceLastOccurrence | Replaces the last occurrence of a specified string | [Docs](https://support.north52.com/knowledgebase/article/KA-02100-dynamics-crm-365-ReplaceLastOccurrence/en-us) |
| ReplaceMultiple | Replaces multiple strings with another string | [Docs](https://support.north52.com/knowledgebase/article/KA-01795-dynamics-crm-365-ReplaceMultiple/en-us) |
| Reverse | Reverse the contents of a string | [Docs](https://support.north52.com/knowledgebase/article/KA-01798-dynamics-crm-365-Reverse/en-us) |
| Right | Returns the right number of characters in a string | [Docs](https://support.north52.com/knowledgebase/article/KA-01797-dynamics-crm-365-Right/en-us) |
| SHA1 | Returns a SHA1 hash of a string | [Docs](https://support.north52.com/knowledgebase/article/KA-01799-dynamics-crm-365-SHA1/en-us) |
| Slice | Returns a substring between a start and end position | [Docs](https://support.north52.com/knowledgebase/article/KA-01800-dynamics-crm-365-Slice/en-us) |
| Split | Returns a substring based on a split character and index | [Docs](https://support.north52.com/knowledgebase/article/KA-01801-dynamics-crm-365-Split/en-us) |
| StartsWith | Returns true if one string starts with another | [Docs](https://support.north52.com/knowledgebase/article/KA-01802-dynamics-crm-365-StartsWith/en-us) |
| StringConcat | Concatenates many strings together | [Docs](https://support.north52.com/knowledgebase/article/KA-01803-dynamics-crm-365-StringConcat/en-us) |
| StringFormat | Takes a string and inserts the values with params | [Docs](https://support.north52.com/knowledgebase/article/KA-01804-dynamics-crm-365-StringFormat/en-us) |
| StringJoin | Returns a string made up from parameter strings with delimiter | [Docs](https://support.north52.com/knowledgebase/article/KA-01805-dynamics-crm-365-StringJoin/en-us) |
| Substring | Returns part of the input string based on position and length | [Docs](https://support.north52.com/knowledgebase/article/KA-01806-dynamics-crm-365-Substring/en-us) |
| ToString | Returns a string representation of any value | [Docs](https://support.north52.com/knowledgebase/article/KA-01808-dynamics-crm-365-ToString/en-us) |
| ToTitleCase | Converts the first character of a word to uppercase | [Docs](https://support.north52.com/knowledgebase/article/KA-01809-dynamics-crm-365-ToTitleCase/en-us) |
| Trim | Removes specified characters from beginning and end | [Docs](https://support.north52.com/knowledgebase/article/KA-01810-dynamics-crm-365-Trim/en-us) |
| TrimEnd | Removes specified characters from the end | [Docs](https://support.north52.com/knowledgebase/article/KA-02115-dynamics-crm-365-TrimEnd/en-us) |
| TrimStart | Removes specified characters from the beginning | [Docs](https://support.north52.com/knowledgebase/article/KA-02116-dynamics-crm-365-TrimStart/en-us) |
| UnEscapeDataString | Converts a string to unescaped representation | [Docs](https://support.north52.com/knowledgebase/article/KA-10075-dynamics-crm-365-UnEscapeData/en-us) |
| Upper | Converts all string elements to upper case | [Docs](https://support.north52.com/knowledgebase/article/KA-01811-dynamics-crm-365-Upper/en-us) |

---

## System

Core system functions for various operations.

| Function | Description | Link |
|----------|-------------|------|
| AddToQueue | Adds/moves an item to a Queue | [Docs](https://support.north52.com/knowledgebase/article/KA-01817-dynamics-crm-365-AddToQueue/en-us) |
| AddUsersToAccessTeam | Add users to a team and create Access Team if necessary | [Docs](https://support.north52.com/knowledgebase/article/KA-02143-dynamics-crm-365-AddUsersToAccessTeam/en-us) |
| AddUsersToTeam | Add users to a team | [Docs](https://support.north52.com/knowledgebase/article/KA-02145-dynamics-crm-365-AddUsersToTeam/en-us) |
| AutoNumber | Autonumber | [Docs](https://support.north52.com/knowledgebase/article/KA-02161-dynamics-crm-365-AutoNumber/en-us) |
| AzureCognitiveIssueToken | Returns a token for Azure Cognitive | [Docs](https://support.north52.com/knowledgebase/article/KA-01864-dynamics-crm-365-AzureCognitiveIssueToken/en-us) |
| Between | Returns true if a test value lies between 2 other values | [Docs](https://support.north52.com/knowledgebase/article/KA-01814-dynamics-crm-365-Between/en-us) |
| Break | Allows you to exit immediately either a SmartFlow or ForEachRecord | [Docs](https://support.north52.com/knowledgebase/article/KA-01849-dynamics-crm-365-Break/en-us) |
| CalcMaxRecordCount | Returns the maximum record count given page number and batch size | [Docs](https://support.north52.com/knowledgebase/article/KA-02192-dynamics-crm-365-CalcMaxRecordCount/en-us) |
| CalcMinRecordCount | Returns the minimum record count given page number and batch size | [Docs](https://support.north52.com/knowledgebase/article/KA-02191-dynamics-crm-365-CalcMinRecordCount/en-us) |
| CalculateDaylightSavingsDifference | Calculate daylight savings difference | [Docs](https://support.north52.com/knowledgebase/article/KA-10118-dynamics-crm-365-CalculateDaylightSavingsDifference/en-us) |
| CheckAttributeExistsOnEntity | Check if an attribute exists on entity | [Docs](https://support.north52.com/knowledgebase/article/KA-02117-dynamics-crm-365-CheckAttributeExistsOnEntity/en-us) |
| Clear | Sets the target property of a formula to a null value | [Docs](https://support.north52.com/knowledgebase/article/KA-01816-dynamics-crm-365-Clear/en-us) |
| Clone | Clones a record and optionally all 1:N & N:N records | [Docs](https://support.north52.com/knowledgebase/article/KA-01821-dynamics-crm-365-Clone/en-us) |
| CloneInActiveRecords | Used when you do not want to clone in-active records | [Docs](https://support.north52.com/knowledgebase/article/KA-10507-dynamics-crm-365-CloneInActiveRecords/en-us) |
| ColumnSet | ColumnSet | [Docs](https://support.north52.com/knowledgebase/article/KA-10122-dynamics-crm-365-ColumnSet/en-us) |
| ContainsData | Returns true if all fieldtocheck arguments contain data | [Docs](https://support.north52.com/knowledgebase/article/KA-01822-dynamics-crm-365-ContainsData/en-us) |
| ContainsDataAndNotZero | Returns true if all fieldtocheck contain data and are not zero | [Docs](https://support.north52.com/knowledgebase/article/KA-01823-dynamics-crm-365-ContainsDataAndNotZero/en-us) |
| ContainsDataList | Returns the list of fields-to-check which contain data | [Docs](https://support.north52.com/knowledgebase/article/KA-10525-dynamics-crm-365-ContainsDataList/en-us) |
| CreateEC | Creates an entity collection object in memory | [Docs](https://support.north52.com/knowledgebase/article/KA-02108-dynamics-crm-365-CreateEC/en-us) |
| CreateEmailFromTemplate | Create an email from a template | [Docs](https://support.north52.com/knowledgebase/article/KA-01820-dynamics-crm-365-CreateEmailFromTemplate/en-us) |
| CreateEntity | Creates an in-memory entity | [Docs](https://support.north52.com/knowledgebase/article/KA-02111-dynamics-crm-365-CreateEntity/en-us) |
| CreateEntityReference | Create a native EntityReference field | [Docs](https://support.north52.com/knowledgebase/article/KA-02119-dynamics-crm-365-CreateEntityReference/en-us) |
| CreateMoney | Creates a native Money field | [Docs](https://support.north52.com/knowledgebase/article/KA-02118-dynamics-crm-365-CreateMoney/en-us) |
| CreateOptionSetValue | Creates a native OptionSetValue field | [Docs](https://support.north52.com/knowledgebase/article/KA-02120-dynamics-crm-365-CreateOptionSetValue/en-us) |
| CreateQuickTile | Creates a Quick Tile | [Docs](https://support.north52.com/knowledgebase/article/KA-01818-dynamics-crm-365-CreateQuickTile/en-us) |
| CreateQuickTileCollection | Creates a Quick Tile collection | [Docs](https://support.north52.com/knowledgebase/article/KA-01819-dynamics-crm-365-CreateQuickTileCollection/en-us) |
| CreateRecordFromEntity | Creates a record in the database from an in-memory entity | [Docs](https://support.north52.com/knowledgebase/article/KA-02160-dynamics-crm-365-CreateRecordFromEntity/en-us) |
| DecisionTable | A DecisionTable allows you to execute multiple steps | [Docs](https://support.north52.com/knowledgebase/article/KA-01825-dynamics-crm-365-DecisionTable/en-us) |
| DoesNotContainData | Returns true if all fieldtocheck do not contain data | [Docs](https://support.north52.com/knowledgebase/article/KA-01824-dynamics-crm-365-DoesNotContainData/en-us) |
| DoesNotContainDataList | Returns the list of fields-to-check which do not contain data | [Docs](https://support.north52.com/knowledgebase/article/KA-10526-dynamics-crm-365-DoesNotContainDataList/en-us) |
| DoesUserHavePrivilege | Returns true if a user has a certain privilege | [Docs](https://support.north52.com/knowledgebase/article/KA-01829-dynamics-crm-365-DoesUserHavePrivilege/en-us) |
| ExecuteFormula | Execute a North52 formula | [Docs](https://support.north52.com/knowledgebase/article/KA-01826-dynamics-crm-365-ExecuteFormula/en-us) |
| ExitAllDecisionTables | Exits all Decision Tables | [Docs](https://support.north52.com/knowledgebase/article/KA-02163-dynamics-crm-365-ExitAllDecisionTables/en-us) |
| ExpandCalendar | Returns an entitycollection of calendar entries | [Docs](https://support.north52.com/knowledgebase/article/KA-01850-dynamics-crm-365-ExpandCalendar/en-us) |
| GetCalendarRules | Returns an entity collection of calendar rules for a given calendar | [Docs](https://support.north52.com/knowledgebase/article/KA-01855-dynamics-crm-365-GetCalendarRules/en-us) |
| GetCorrelationId | Gets the GUID for the current correlation ID record | [Docs](https://support.north52.com/knowledgebase/article/KA-10385-dynamics-crm-365-GetCorrelationId/en-us) |
| GetCurrentUserAttribute | Retrieve information about current user | [Docs](https://support.north52.com/knowledgebase/article/KA-01838-dynamics-crm-365-GetCurrentUserAttribute/en-us) |
| GetDepth | Gets the current depth of the code that is executing | [Docs](https://support.north52.com/knowledgebase/article/KA-10389-dynamics-crm-365-GetDepth/en-us) |
| GetEntityMetadata | Returns any top level meta data attribute on specified entity | [Docs](https://support.north52.com/knowledgebase/article/KA-10057-dynamics-crm-365-GetEntityMetadata/en-us) |
| GetFetchXml | Gets the associated fetch-xml for the formula detail name | [Docs](https://support.north52.com/knowledgebase/article/KA-01852-dynamics-crm-365-GetFetchXml/en-us) |
| GetMessageName | Gets the current message name for the code that is executing | [Docs](https://support.north52.com/knowledgebase/article/KA-01853-dynamics-crm-365-GetMessageName/en-us) |
| GetOptionSetValueExternal | Returns the optionset external value | [Docs](https://support.north52.com/knowledgebase/article/KA-10508-dynamics-crm-365-GetOptionSetValueExternal/en-us) |
| GetPlatformVersion | Returns the version of the platform | [Docs](https://support.north52.com/knowledgebase/article/KA-10390-dynamics-crm-365-GetPlatformVersion/en-us) |
| GetPrimaryEntityId | Gets the GUID for the record currently executing | [Docs](https://support.north52.com/knowledgebase/article/KA-10381-dynamics-crm-365-GetPrimaryEntityId/en-us) |
| GetSharedVariable | Get shared variable | [Docs](https://support.north52.com/knowledgebase/article/KA-02188-dynamics-crm-365-GetSharedVariable/en-us) |
| GetShortCode | Returns the Short Code of the currently executing Formula | [Docs](https://support.north52.com/knowledgebase/article/KA-10158-dynamics-crm-365-GetShortCode/en-us) |
| GetSolutionVersion | Returns the version of a solution | [Docs](https://support.north52.com/knowledgebase/article/KA-10391-dynamics-crm-365-GetSolutionVersion/en-us) |
| GetSourceChangeList | Returns a CSV list of the fields that have changed | [Docs](https://support.north52.com/knowledgebase/article/KA-02137-dynamics-crm-365-GetSourceChangeList/en-us) |
| GetSourceProperty | Returns the contents of the Source Entity | [Docs](https://support.north52.com/knowledgebase/article/KA-01856-dynamics-crm-365-GetSourceProperty/en-us) |
| GetUserRoles | Returns a comma separated list of a users roles | [Docs](https://support.north52.com/knowledgebase/article/KA-01830-dynamics-crm-365-GetUserRoles/en-us) |
| GetUserTeams | Returns a comma separated list of a users teams | [Docs](https://support.north52.com/knowledgebase/article/KA-01831-dynamics-crm-365-GetUserTeams/en-us) |
| GetVar | GetVar allows you to retrieve a variable | [Docs](https://support.north52.com/knowledgebase/article/KA-01851-dynamics-crm-365-GetVar/en-us) |
| HaveFieldsChanged | Returns True if specified fields have all had changes | [Docs](https://support.north52.com/knowledgebase/article/KA-01834-dynamics-crm-365-HaveFieldsChanged/en-us) |
| HaveFieldsNotChanged | Returns True if specified fields have NOT all had changes | [Docs](https://support.north52.com/knowledgebase/article/KA-01836-dynamics-crm-365-HaveFieldsNotChanged/en-us) |
| HaveFieldsNotTriggered | Returns True if specified fields were NOT in original trigger | [Docs](https://support.north52.com/knowledgebase/article/KA-01835-dynamics-crm-365-HaveFieldsNotTriggered/en-us) |
| HaveFieldsTriggered | Returns True if specified fields were in original trigger | [Docs](https://support.north52.com/knowledgebase/article/KA-01833-dynamics-crm-365-HaveFieldsTriggered/en-us) |
| HaversineDistance | Returns the distance in meters between two geo-locations | [Docs](https://support.north52.com/knowledgebase/article/KA-01832-dynamics-crm-365-HaversineDistance/en-us) |
| Interpolation | Calculates the Interpolation of a set | [Docs](https://support.north52.com/knowledgebase/article/KA-10484-dynamics-crm-365-Interpolation/en-us) |
| IsGuid | Returns true if the passed string is a valid GUID | [Docs](https://support.north52.com/knowledgebase/article/KA-10392-dynamics-crm-365-IsGuid/en-us) |
| IsUserInSecurityRoles | Returns true if the user is in the list of security roles | [Docs](https://support.north52.com/knowledgebase/article/KA-01837-dynamics-crm-365-IsUserInSecurityRoles/en-us) |
| IsValidIBAN | Returns true if the passed string is a valid IBAN | [Docs](https://support.north52.com/knowledgebase/article/KA-02136-dynamics-crm-365-IsValidIBAN/en-us) |
| Merge | Merge two entities together | [Docs](https://support.north52.com/knowledgebase/article/KA-10450-dynamics-crm-365-Merge/en-us) |
| MergeEntityCollections | Merge multiple entity collections into one | [Docs](https://support.north52.com/knowledgebase/article/KA-01857-dynamics-crm-365-MergeEntityCollections/en-us) |
| MultipleDecisionTable | A DecisionTable with multiple sheets | [Docs](https://support.north52.com/knowledgebase/article/KA-01828-dynamics-crm-365-MultipleDecisionTable/en-us) |
| OutputToTrace | Send the passed parameter to the trace log | [Docs](https://support.north52.com/knowledgebase/article/KA-01858-dynamics-crm-365-OutputToTrace/en-us) |
| Random | Returns a random integer between min and max values | [Docs](https://support.north52.com/knowledgebase/article/KA-01840-dynamics-crm-365-Random/en-us) |
| RandomCollectionOfIntegers | Returns a collection of random integers | [Docs](https://support.north52.com/knowledgebase/article/KA-01841-dynamics-crm-365-RandomCollectionOfIntegers/en-us) |
| SendEmail | Send an email | [Docs](https://support.north52.com/knowledgebase/article/KA-01845-dynamics-crm-365-SendEmail/en-us) |
| SetActionOutputParameters | Set an Actions Output Parameters | [Docs](https://support.north52.com/knowledgebase/article/KA-02107-dynamics-crm-365-SetActionOutputParameters/en-us) |
| SetDefaultBusinessCalendar | Sets the default holiday calendar | [Docs](https://support.north52.com/knowledgebase/article/KA-10015-dynamics-crm-365-SetDefaultBusinessCalendar/en-us) |
| SetFormulaParameters | SetFormulaParameters | [Docs](https://support.north52.com/knowledgebase/article/KA-10197-dynamics-crm-365-setformulaparameters/en-us) |
| SetIgnoreFields | Supports the Clone function so you can ignore certain fields | [Docs](https://support.north52.com/knowledgebase/article/KA-01859-dynamics-crm-365-SetIgnoreFields/en-us) |
| SetParams | Supports Find functions with fetch-xml to pass dynamic values | [Docs](https://support.north52.com/knowledgebase/article/KA-01860-dynamics-crm-365-SetParams/en-us) |
| SetParamsNoEncoding | Supports Find functions with FetchXML (no encoding) | [Docs](https://support.north52.com/knowledgebase/article/KA-10121-dynamics-crm-365-SetParamsNoEncoding/en-us) |
| SetSharedVariable | Set shared variable | [Docs](https://support.north52.com/knowledgebase/article/KA-02187-dynamics-crm-365-SetSharedVariable/en-us) |
| SetVar | SetVar allows you to set a variable for later re-use | [Docs](https://support.north52.com/knowledgebase/article/KA-01862-dynamics-crm-365-SetVar/en-us) |
| SetVarConcat | SetVarConcat allows you to set a variable to itself plus another value | [Docs](https://support.north52.com/knowledgebase/article/KA-01863-dynamics-crm-365-SetVarConcat/en-us) |
| Sleep | Sleep | [Docs](https://support.north52.com/knowledgebase/article/KA-02106-dynamics-crm-365-Sleep/en-us) |
| SmartFlow | SmartFlow allows you to execute multiple steps in a formula | [Docs](https://support.north52.com/knowledgebase/article/KA-01861-dynamics-crm-365-SmartFlow/en-us) |
| SmartFlowExceptionGuard | SmartFlowExceptionGuard | [Docs](https://support.north52.com/knowledgebase/article/KA-10124-dynamics-crm-365-SmartFlowExceptionGuard/en-us) |
| ThrowError | Shows the user an error message | [Docs](https://support.north52.com/knowledgebase/article/KA-01847-dynamics-crm-365-ThrowError/en-us) |
| WhoAmI | Returns a GUID representing the current user | [Docs](https://support.north52.com/knowledgebase/article/KA-01848-dynamics-crm-365-WhoAmI/en-us) |

---

## Web Services

Functions for calling external web services and working with Azure.

| Function | Description | Link |
|----------|-------------|------|
| AzureADGetToken | Retrieves an oAuth token from Azure Active Directory | [Docs](https://support.north52.com/knowledgebase/article/KA-10042-dynamics-crm-365-AzureADGetToken/en-us) |
| AzureADGetTokenV2 | Retrieves an oAuth token using Azure AD v2.0 endpoint | [Docs](https://support.north52.com/knowledgebase/article/KA-10043-dynamics-crm-365-AzureADGetTokenV2/en-us) |
| AzureEventGridSendMessage | Sends a message to Azure Event Grid | [Docs](https://support.north52.com/knowledgebase/article/KA-10059-dynamics-crm-365-AzureEventGridSendMessage/en-us) |
| GeoCodeBing | Returns the latitude and longitude of the given address | [Docs](https://support.north52.com/knowledgebase/article/KA-01892-dynamics-crm-365-GeoCodeBing/en-us) |
| GetExchangeRate | Returns the exchange rate between 2 currencies | [Docs](https://support.north52.com/knowledgebase/article/KA-01893-dynamics-crm-365-GetExchangeRate/en-us) |
| GetSystemUrl | Gets the system URL | [Docs](https://support.north52.com/knowledgebase/article/KA-10076-dynamics-crm-365-GetSystemUrl/en-us) |
| GetVarHeaderValue | Returns the https response header from the previous webservice call | [Docs](https://support.north52.com/knowledgebase/article/KA-10206-dynamics-crm-365-getvarheadervalue/en-us) |
| SetBrokeredProperties | Sets the brokered properties for Azure Send Messages | [Docs](https://support.north52.com/knowledgebase/article/KA-10384-dynamics-crm-365-SetBrokeredProperties/en-us) |
| Translate | Returns the translation of the given text | [Docs](https://support.north52.com/knowledgebase/article/KA-01894-dynamics-crm-365-Translate/en-us) |
| UnEscapeUriString | Unconverts a URI string to escaped/encoded representation | [Docs](https://support.north52.com/knowledgebase/article/KA-10201-dynamics-crm-365-unescapeuristring/en-us) |
| UriGetFileName | Returns the file name from a URI | [Docs](https://support.north52.com/knowledgebase/article/KA-10073-dynamics-crm-365-UriGetFileName/en-us) |

---

## XML

Functions for working with XML data.

| Function | Description | Link |
|----------|-------------|------|
| CreateXmlAttribute | Creates an XML Attribute | [Docs](https://support.north52.com/knowledgebase/article/KA-01872-dynamics-crm-365-CreateXmlAttribute/en-us) |
| CreateXmlChildren | Creates a set of child XML Elements | [Docs](https://support.north52.com/knowledgebase/article/KA-01873-dynamics-crm-365-CreateXmlChildren/en-us) |
| CreateXmlDeclaration | Creates an XML Declaration | [Docs](https://support.north52.com/knowledgebase/article/KA-01874-dynamics-crm-365-CreateXmlDeclaration/en-us) |
| CreateXmlElement | Creates an XML Element | [Docs](https://support.north52.com/knowledgebase/article/KA-01875-dynamics-crm-365-CreateXmlElement/en-us) |
| CreateXmlRootAttribute | Creates an XML Root Attribute | [Docs](https://support.north52.com/knowledgebase/article/KA-01876-dynamics-crm-365-CreateXmlRootAttribute/en-us) |
| CreateXmlRootNode | Creates the Xml Root Node for the document | [Docs](https://support.north52.com/knowledgebase/article/KA-01877-dynamics-crm-365-CreateXmlRootNode/en-us) |
| GetVarXPathValue | Gets a value from a XML document | [Docs](https://support.north52.com/knowledgebase/article/KA-01879-dynamics-crm-365-GetVarXPathValue/en-us) |

---

## xCache

Functions for working with North52's xCache caching system.

| Function | Description | Link |
|----------|-------------|------|
| xCacheAddCalculatedFieldLocal | Adds a calculated field to an existing local xCache collection | [Docs](https://support.north52.com/knowledgebase/article/KA-01908-dynamics-crm-365-xCacheAddCalculatedFieldLocal/en-us) |
| xCacheCalculateLocal | Returns a calculated value from the local xCache collection | [Docs](https://support.north52.com/knowledgebase/article/KA-01909-dynamics-crm-365-xCacheCalculateLocal/en-us) |
| xCacheDistinct | xCacheDistinct | [Docs](https://support.north52.com/knowledgebase/article/KA-10198-dynamics-crm-365-xcachedistinct/en-us) |
| xCacheFilterLocal | Loads an xCache collection with a supplied filter | [Docs](https://support.north52.com/knowledgebase/article/KA-01910-dynamics-crm-365-xCacheFilterLocal/en-us) |
| xCacheGetGlobal | Returns the xCache value for the given key for the Global xCache | [Docs](https://support.north52.com/knowledgebase/article/KA-01907-dynamics-crm-365-xCacheGetGlobal/en-us) |
| xCacheLoadLocal | Loads an xCache collection from an EntityCollection | [Docs](https://support.north52.com/knowledgebase/article/KA-01912-dynamics-crm-365-xCacheLoadLocal/en-us) |
| xCacheLoadLocalEx | Same as xCacheLoadLocal but returns the xCache collection | [Docs](https://support.north52.com/knowledgebase/article/KA-10482-dynamics-crm-365-xCacheLoadLocalEx/en-us) |
| xCacheLoadLocalFromJson | Loads an xCache collection from a JSON document | [Docs](https://support.north52.com/knowledgebase/article/KA-10149-dynamics-crm-365-xCacheLoadLocalFromJson/en-us) |
| xCacheRemoveFields | Removes a field from the xCache collection | [Docs](https://support.north52.com/knowledgebase/article/KA-10148-dynamics-crm-365-xCacheRemoveFields/en-us) |

---

## Additional Resources

- **North52 Support Portal**: https://support.north52.com/
- **Main Functions Page**: https://support.north52.com/knowledgebase/functions/
- **Knowledge Base**: https://support.north52.com/knowledgebase/
- **Help Desk**: https://support.north52.com/support/

---

## Usage Notes

1. **Function Categories**: Functions are organized by their primary use case. Some functions may fit into multiple categories.

2. **Documentation Links**: All links point to the official North52 knowledge base. Click any link for detailed documentation including:
   - Syntax and parameters
   - Usage examples
   - Best practices
   - Related functions

3. **Version Compatibility**: Functions availability may vary based on your North52 Decision Suite version. Check the official documentation for version-specific details.

4. **Skill Level**: Most functions are marked as "Beginner" level in the North52 documentation. Some advanced functions may require intermediate or advanced knowledge.

5. **Performance**: Always refer to the original `north52-functions.md` file in this folder for performance considerations and best practices for commonly used functions.

---

**Note**: This reference was generated by scraping the North52 functions index page. For the most up-to-date information and detailed examples, always refer to the official North52 documentation at the provided links.
