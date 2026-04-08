# Pattern: Reference Tables

## WHY?

Use Reference Tables (instead of Global Option Sets) when:
- Security is needed at the user/team/BU level
- Choices must be deactivatable for archival/historical purposes
- Additional metadata is needed per choice (e.g. a Country needs Name, 3-char code, 2-char code, ISO Number, map data)
- The portal needs to display English and French content

## Table Design

- Leverage **User & Team record ownership** to allow security and BU segmentation
- **Attributes to include:**
  - A **Code** field for unique identification
  - For portal usage: **Portal Name** and **Portal Name (FR)** to distinguish records for external users

## Form Design

- Follow [Form Standards](../../mda-standards/form-standards.md)
- Use a simple layout -- reference tables typically only need a single-column form
