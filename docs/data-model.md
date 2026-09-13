# Data Model

## 1. Purpose

The Defect Escape Analyzer will work with three primary datasets:

1. Requirements
2. Test Cases
3. Escaped Defects

These datasets will provide the evidence required to analyze escaped
defects and identify potential testing or prevention gaps.

The prototype will use synthetic/static sample data.

---

## 2. Requirements Data

The Requirements dataset represents the expected system behavior.

### Fields

| Field | Description |
|---|---|
| Requirement ID | Unique identifier for the requirement |
| Description | Description of the expected behavior |
| Priority | Importance of the requirement |

### Example

| Requirement ID | Description | Priority |
|---|---|---|
| R001 | User should be able to log in with valid credentials | High |
| R002 | System should reject invalid credentials | High |

---

## 3. Test Case Data

The Test Cases dataset represents the tests created to verify
requirements.

### Fields

| Field | Description |
|---|---|
| Test Case ID | Unique identifier for the test case |
| Requirement ID | Requirement covered by the test |
| Test Description | Description of the test scenario |
| Test Type | Type of testing performed |
| Result | Test execution result |

### Example

| Test Case ID | Requirement ID | Test Description | Test Type | Result |
|---|---|---|---|---|
| TC001 | R001 | Login with valid credentials | Positive | Pass |
| TC002 | R002 | Login with invalid password | Negative | Pass |

---

## 4. Escaped Defect Data

The Escaped Defects dataset represents defects that were discovered
after the relevant testing stage.

### Fields

| Field | Description |
|---|---|
| Defect ID | Unique identifier for the defect |
| Requirement ID | Requirement associated with the defect |
| Description | Description of the escaped defect |
| Severity | Impact/severity of the defect |
| Escape Phase | Stage at which the defect was discovered |

### Example

| Defect ID | Requirement ID | Description | Severity | Escape Phase |
|---|---|---|---|---|
| D001 | R002 | Invalid password accepted | High | System Testing |

---

## 5. Relationships

The datasets are related through identifiers.

### Primary relationships

Requirements
    |
    | Requirement ID
    v
Test Cases

Requirements
    |
    | Requirement ID
    v
Escaped Defects

A requirement may have:

- Multiple test cases.
- Multiple escaped defects.

A test case belongs to a specific requirement.

An escaped defect is associated with a requirement.

---

## 6. Analysis Evidence

The analysis engine will use the relationships between the datasets
to determine:

- Whether the escaped defect is associated with a known requirement.
- Whether test cases exist for the associated requirement.
- What type of tests were available.
- Whether the available tests provide evidence of a potential
  coverage gap.

The analysis should retain enough evidence to explain how a conclusion
was reached.

---

## 7. Validation Rules

The following validation rules will be considered during implementation:

### Requirement Validation

- Requirement IDs should be unique.
- Required fields should not be missing.
- Requirement descriptions should not be empty.

### Test Case Validation

- Test Case IDs should be unique.
- Referenced Requirement IDs should exist.
- Required fields should not be missing.

### Defect Validation

- Defect IDs should be unique.
- Referenced Requirement IDs should exist.
- Required fields should not be missing.

Invalid records should be identified before analysis.

---

## 8. Design Considerations

The data model is intentionally simple because the challenge requires
a lightweight prototype using static/pre-provided data.

The model can be extended later if additional fields are required
during implementation or testing.

The exact sample values may change during implementation, but the
relationships between requirements, test cases, and escaped defects
should remain clear and traceable.

---

## 9. Design Status

Data model design is in progress.