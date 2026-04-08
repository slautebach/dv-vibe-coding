# MDA Standards: Canvas Dialogs in Model-Driven Apps

## Overview

A Canvas page can be used as a dialog within a Model-Driven App. This allows for rich, custom UI experiences embedded directly in the MDA without navigating away from the record.

## Canvas Page Setup

Create a Canvas page within your solution.

In the **App.OnStart** event, capture the record GUID from the launch parameters:

```powerfx
// Set the record Guid from the parameters
Set(recordGUID, GUID(
    Substitute(
        Substitute(Param("recordId"), "{", ""),
        "}", "")
    )
);

// Retrieve the selected record
Set(record,
    LookUp('<Table Set Name>', '<ID ColumnName>' = recordGUID)
);
```

## Command Button

Add a Command Button to the MDA form or view ribbon to launch the Canvas dialog.

- Configure the button's action to open the Canvas page
- Pass the current record ID as the `recordId` parameter

## Adding the Canvas Page to the App

1. Open the MDA in the App Designer
2. Add the Canvas page as a component
3. Configure the page launch from the command button

## When to Use

- When the native Dynamics 365 dialog experience is insufficient
- For multi-step input flows that require conditional visibility or complex calculations
- As a replacement for legacy HTML web resource dialogs
- When Power FX expressions are needed for form logic
