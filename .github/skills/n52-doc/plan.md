# Overview

This document is to allow me to brain dump some feature plans that the AI agent and I will work on to build out additional features

# Ideas

- **Canonical output location (required):**
  - AI documentation files (`README.md`, `CodeReview.md`, `diagram.puml`, `diagram.png`, `dt_*.md`) must be written to:
    - `Documentation/North52/<entity>/<shortcode>/`
  - Do **not** write or copy these AI docs into:
    - `D365Solution/IncomeAssistanceNorth52/WebResources/north52_/formula/...`
  - If docs are found in the wrong location, move/remove them and keep the canonical `Documentation/North52/<entity>/<shortcode>/` copy only.

- Review and update the Prompt for the Description
- Review and update the prompt for the Code Review
- Rename Description to README.md so it is rendered in git by default on the folder.
- Add a link N52 formula in the Dev environment in the README.md file.
- Update to to clarify Decision tables
  - Any comments can only be embedded in the tables
  - Analyze the json comment table, so it can be more clearly documented and deliver a clearer picture of the decision table.
- Add a new prompt to create a plantuml diagram of the flow of the formula
