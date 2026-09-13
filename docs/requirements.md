# Software Requirements Specification

## 1. Introduction

### 1.1 Project Name

Defect Escape Analyzer

### 1.2 Challenge

IGS Fresher Hackathon - Challenge #14

### 1.3 Problem Statement

Software defects may escape the testing process and be discovered at a
later stage. Such escaped defects can indicate gaps in requirements
coverage, test coverage, test design, or the testing process.

The Defect Escape Analyzer will analyze escaped defects against available
requirements and existing test cases to identify what testing may have
missed.

### 1.4 Objective

The objective of the system is to:

- Map escaped defects to relevant requirements or weak test coverage.
- Identify a prevention-gap category for each defect.
- Recommend additional tests or process improvements.

---

## 2. Input Requirements

The prototype will use static or synthetic input data.

### 2.1 Requirements

Requirements will represent the expected behaviour of the system.

Proposed fields:

| Field | Description |
|---|---|
| Requirement ID | Unique identifier |
| Requirement Description | Description of the requirement |
| Priority | Importance of the requirement |

### 2.2 Test Cases

Test cases will represent the existing testing coverage.

Proposed fields:

| Field | Description |
|---|---|
| Test Case ID | Unique test identifier |
| Requirement ID | Requirement covered by the test |
| Test Description | Description of the test |
| Test Type | Type of testing performed |
| Result | Test execution result |

### 2.3 Escaped Defects

Escaped defects represent defects that were not detected during the
existing testing process.

Proposed fields:

| Field | Description |
|---|---|
| Defect ID | Unique defect identifier |
| Requirement ID | Related requirement |
| Defect Description | Description of the escaped defect |
| Severity | Impact/severity of the defect |
| Escape Phase | Stage where the defect was discovered |

> Note: The exact fields above are proposed data-model decisions for the
> prototype and are subject to refinement during the design phase.

---

## 3. Functional Requirements

### FR-01: Input Loading

The system shall accept requirements, test cases, and escaped defect data.

### FR-02: Input Validation

The system shall validate the input data and identify invalid or
incomplete records.

### FR-03: Defect Mapping

The system shall associate escaped defects with relevant requirements.

### FR-04: Test Coverage Analysis

The system shall identify the existing test cases associated with the
relevant requirement and analyze their coverage.

### FR-05: Gap Identification

The system shall identify missing or weak testing coverage associated with
an escaped defect.

### FR-06: Prevention Gap Classification

The system shall assign a prevention-gap category to each analyzed defect.

### FR-07: Recommendation

The system shall recommend additional tests or process improvements based
on the identified gap.

### FR-08: AI-Assisted Analysis

The system shall use AI to explain the likely prevention gap and suggest a
missing test area.

AI usage will be intentionally limited to this task.

### FR-09: Results Presentation

The system shall present the analysis results in a clear and
understandable format.

---

## 4. Non-Functional Requirements

### NFR-01: Usability

The interface should be simple and understandable for users involved in
testing and delivery activities.

### NFR-02: Explainability

The system should provide evidence supporting the identified testing gap
rather than presenting only a final classification.

### NFR-03: Maintainability

The implementation should use modular components so that individual
functional areas can be maintained independently.

### NFR-04: Testability

The core analysis logic should be independently testable.

### NFR-05: Reliability

Invalid input should be handled gracefully with meaningful validation
messages.

### NFR-06: Performance

The prototype should efficiently process the synthetic dataset provided
for the challenge.

### NFR-07: Documentation

The project shall maintain documentation covering requirements,
architecture, implementation, testing, assumptions, limitations, and
future enhancements as the project progresses.

---

## 5. Scope

### 5.1 In Scope

- Static/synthetic requirements data
- Static/synthetic test-case data
- Static/synthetic escaped-defect data
- Input validation
- Requirement and defect mapping
- Test coverage analysis
- Prevention-gap identification
- Test/process recommendations
- AI-assisted explanation of the likely prevention gap
- Lightweight result presentation

### 5.2 Out of Scope

- Live production systems
- Real production credentials
- Live defect tracking systems
- Execution of actual application test cases
- Real-time production monitoring
- Enterprise-scale test management integration
- Training a custom machine-learning model

---

## 6. Constraints

- The prototype must be developed within the challenge time constraints.
- The solution should remain within the defined challenge scope.
- Input data will be static or synthetic.
- AI usage will be limited to the specified AI-assisted task.
- The implementation should prioritize clarity, modularity, and
  demonstrability.

---

## 7. Initial Assumptions

1. Requirements have unique identifiers.
2. Test cases can be associated with requirements.
3. Escaped defects can be associated with relevant requirements.
4. The provided data contains sufficient information for basic coverage
   analysis.
5. AI-generated recommendations are advisory and should be reviewed by a
   human.
6. The prototype is intended to demonstrate the concept rather than replace
   a complete enterprise test-management platform.

---

## 8. Expected Outputs

For each escaped defect, the system should provide:

1. Requirement/test coverage mapping.
2. Prevention-gap category.
3. Recommended tests or process improvements.

---

## 9. Success Criteria

The prototype will be considered successful when it can:

- Accept the required input data.
- Validate the input.
- Analyze escaped defects.
- Identify associated requirements and test coverage.
- Identify potential prevention gaps.
- Provide actionable recommendations.
- Provide the specified AI-assisted explanation.
- Present the results clearly.
- Demonstrate the analysis through a working prototype.

---

## 10. Requirement Traceability

Requirement traceability between requirements, test cases, and escaped
defects will be designed and refined during the system-design stage.

---

## 11. Requirement Review Status

**Status:** Initial Draft

**SDLC Stage:** Requirement Analysis

**Next Stage:** Planning