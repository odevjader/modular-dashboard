# IA Coder Workflow (Experimental)

This document outlines the detailed workflow for the **Agente IA Coder (Tipo 1 - Integrado/RooCode)** operating within the experimental autonomous coder flow for the **Modular Dashboard** project.

**Role:** Principal technical implementer, responsible for detailing and executing solutions based on high-level guidance.

**Workflow Steps:**

1.  **Receive and Analyze Task:** Receive the high-level objective, context, and suggested approach from the Dev. Analyze inputs to understand the core requirement and proposed direction.
2.  **Information Gathering:** Gather necessary information using available tools (`environment_details`, `list_files`, `read_file`, `search_files`, `list_code_definition_names`) to deepen understanding and refine the approach.
3.  **Formulate Detailed Technical Plan:** Create a step-by-step technical plan including:
    *   Files to be created, modified, or deleted.
    *   Key code logic, functions, classes, or configurations.
    *   Necessary terminal commands (including `pwd` check before destructive commands).
    *   Identification of significant/risky actions requiring Dev confirmation.
    *   (Optional) Mermaid diagrams for visualization.
4.  **Present Plan for Approval:** Present the detailed technical plan to the Dev for review and approval.
5.  **Save Plan (Optional):** If requested by the Dev, save the approved plan to a markdown file (`write_to_file`).
6.  **Request Mode Switch:** Request to switch to the appropriate mode for implementation (likely "Code" mode) using the `switch_mode` tool.
7.  **Execute Plan:** In the new mode, execute the plan step-by-step using available tools (`read_file`, `apply_diff`, `write_to_file`, `insert_content`, `search_and_replace`, `execute_command`, etc.), waiting for Dev confirmation after each tool use.
8.  **Address Issues:** Analyze and correct any issues arising during implementation (e.g., linter errors, command failures).
9.  **Generate Final Summary:** Compile the "Sumário Final para Orquestrador" upon successful completion.
10. **Signal Completion:** Use the `attempt_completion` tool to signal task completion and provide the final summary.

**Workflow Diagram:**

```mermaid
graph TD
    A[Receive Task (Objective, Approach)] --> B{Analyze & Gather Info<br/>(read_file, search_files, list_code_definition_names)};
    B --> C[Formulate Detailed Technical Plan<br/>(Identify files, logic, commands, risks)];
    C --> D{Present Plan for Dev Approval};
    D -- Approved --> E[Ask to Save Plan to Markdown<br/>(write_to_file - Optional)];
    E --> F[Request Mode Switch<br/>(switch_mode)];
    F --> G[Execute Plan Step-by-Step<br/>(read_file, apply_diff, etc.)];
    G --> H{Tool Use Successful?};
    H -- Yes --> G;
    H -- No --> I[Address Issues/Errors];
    I --> G;
    G --> J[Generate Final Summary];
    J --> K[Signal Completion<br/>(attempt_completion)];
    D -- Not Approved --> C;