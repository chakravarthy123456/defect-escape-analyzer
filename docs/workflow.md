# Analysis Workflow

## 1. Purpose

The analysis workflow defines how requirements, test cases, and escaped
defects move through the Defect Escape Analyzer.

The workflow is designed to provide traceable evidence for each analysis
result.

---

## 2. End-to-End Workflow

The system will follow these major steps:

1. Load input data.
2. Validate input data.
3. Map escaped defects to requirements.
4. Identify related test cases.
5. Analyze available test coverage.
6. Identify potential prevention gaps.
7. Generate AI-assisted explanation and recommendation.
8. Present structured results.

---

## 3. Step 1 — Load Input Data

The application will load the three datasets:

- Requirements
- Test Cases
- Escaped Defects

The prototype will use static/pre-provided sample data.

---

## 4. Step 2 — Validate Input Data

Before analysis begins, the system will validate the input.

Validation includes:

- Required columns exist.
- Required values are present.
- IDs are unique where required.
- Referenced Requirement IDs exist.
- Data follows the expected structure.

If validation fails, the analysis should not continue until the input
problem is addressed.

---

## 5. Step 3 — Map Escaped Defects to Requirements

Each escaped defect will be associated with a Requirement ID.

The system will retrieve the corresponding requirement information.

Example:

Defect D001
    |
    | Requirement ID = R002
    v
Requirement R002

The mapping provides the basis for subsequent test coverage analysis.

---

## 6. Step 4 — Identify Related Test Cases

For each escaped defect, the system will identify test cases associated
with its requirement.

Example:

Requirement R002
    |
    +---- TC003
    +---- TC004
    +---- TC005

The analyzer will retain the identified test cases as evidence.

---

## 7. Step 5 — Analyze Test Coverage

The system will examine the available test cases for the affected
requirement.

The analysis will consider evidence such as:

- Whether test cases exist.
- Number of related test cases.
- Test types represented.
- Whether negative or boundary scenarios are represented where
  applicable.
- Test execution results.

The purpose is to identify whether existing testing appears to have
covered the escaped behavior adequately.

---

## 8. Step 6 — Identify Prevention Gap

Based on the available evidence, the system will classify the escaped
defect into a prevention-gap category.

The classification will be based on deterministic analysis rules.

The initial prevention-gap categories will include:

### Requirement Gap

The requirement does not provide sufficient information to derive an
appropriate test.

### Test Coverage Gap

The requirement exists, but relevant test coverage is missing or
insufficient.

### Negative Testing Gap

Positive scenarios are covered, but negative/error scenarios are not
adequately tested.

### Boundary Testing Gap

Boundary conditions or limit values are not adequately represented in
the test cases.

### Data Validation Gap

Testing does not adequately cover invalid, unexpected, or incorrect
input data.

### Integration Gap

The escaped behavior involves interaction between components or
systems that was not adequately tested.

### Process Gap

The available evidence suggests that the issue may be related to a
testing or review process weakness rather than a single missing test.

These categories are project design decisions and may be refined during
implementation and testing.

---

## 9. Step 7 — AI-Assisted Explanation

After deterministic analysis identifies the likely prevention gap,
the AI component will receive the relevant analysis evidence.

The AI component will perform only the following tasks:

1. Explain why the identified prevention gap is likely.
2. Suggest a missing test area.

The AI will not independently determine the primary defect mapping or
coverage calculation.

AI output will be advisory and should remain grounded in the provided
evidence.

---

## 10. Step 8 — Results Presentation

The application will present the results for each escaped defect.

The structured result will contain:

1. Defect-to-requirement mapping and coverage evidence.
2. Prevention-gap category.
3. Recommended new tests or process improvements.

Additional supporting information may be displayed to make the result
traceable and understandable.

---

## 11. Example Analysis

Example input:

Requirement:

R002 — System should reject invalid credentials.

Existing tests:

TC003 — Valid credentials
TC004 — Invalid password

Escaped defect:

D001 — Invalid username format accepted.

The analyzer may determine:

- Requirement: R002
- Related tests: TC003, TC004
- Existing coverage: Negative password scenario exists
- Potential gap: Input validation / negative scenario coverage
- AI explanation: Explain why the existing tests did not adequately
  cover the escaped behavior.
- Recommendation: Add tests for invalid username formats and malformed
  credential inputs.

The exact classification will depend on the implemented deterministic
rules and available evidence.

---

## 12. Traceability

Each analysis result should be traceable through the following chain:

Escaped Defect
      |
      v
Requirement
      |
      v
Related Test Cases
      |
      v
Coverage Evidence
      |
      v
Prevention Gap
      |
      v
AI Explanation / Recommendation

This traceability will make the analysis easier to verify and explain
during testing and technical discussion.

---

## 13. Error Handling

The workflow should handle situations such as:

- Missing input data.
- Invalid file structure.
- Missing required columns.
- Unknown Requirement IDs.
- Duplicate IDs.
- Empty datasets.
- No test cases associated with a requirement.
- AI service failure.

Core deterministic analysis should remain usable even if the AI
component is unavailable.

---

## 14. Workflow Design Principles

### Evidence First

Analysis decisions should be based on available input evidence.

### Deterministic Core

Core mapping and coverage analysis should be deterministic.

### Controlled AI

AI should only perform the explicitly defined explanation and
recommendation task.

### Traceability

Results should be traceable back to the source requirement, defect,
and test cases.

### Graceful Failure

Invalid input or AI failure should result in understandable feedback
rather than application failure.

---

## 15. Design Status

Analysis workflow design is in progress.

## Coverage Analysis Rules

The coverage analysis determines whether an existing test case should have detected an escaped defect.

The analysis uses the relationship between the escaped defect, its requirement, and the test cases linked to that requirement.

### Coverage Status

Each escaped defect is assigned one of the following coverage statuses:

- **Covered** — An existing test case directly addresses the scenario described by the escaped defect.
- **Partially Covered** — Existing test cases cover the related requirement or a similar scenario, but do not directly address the escaped defect scenario.
- **Not Covered** — No existing test case meaningfully addresses the requirement or scenario associated with the escaped defect.

### Analysis Approach

The initial implementation uses deterministic rule-based analysis:

1. Identify the requirement associated with the escaped defect.
2. Find all test cases linked to that requirement.
3. Compare the escaped defect description with the available test case descriptions.
4. Determine whether the specific defect scenario appears to be tested.
5. Assign the appropriate coverage status.
6. Preserve the related test case IDs as evidence for the analysis.

The coverage decision is produced by the application logic and does not depend on AI.

AI is reserved for the later prevention-gap explanation and missing-test recommendation, as defined in the system architecture.

### Coverage Classification Logic

The analyzer uses the related test cases as evidence when classifying coverage.

- **Covered** — The test case description directly represents the scenario described by the escaped defect.
- **Partially Covered** — Test cases exist for the requirement, but the specific escaped scenario is not directly represented.
- **Not Covered** — No test cases exist for the requirement associated with the escaped defect.

The classification is deterministic and based on the available requirement and test-case evidence.

The initial implementation uses keyword and scenario matching rather than an AI-generated decision. This keeps the core coverage result reproducible and explainable.