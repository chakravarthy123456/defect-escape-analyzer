# System Architecture

## 1. Purpose

The Defect Escape Analyzer will use a lightweight modular architecture
to analyze escaped defects against software requirements and existing
test cases.

The architecture is designed to keep the core analysis explainable,
testable, and independent from the AI-assisted component.

---

## 2. Architecture Overview

The system will consist of the following major components:

1. User Interface
2. Input Data Layer
3. Input Validation Module
4. Defect Analysis Engine
5. Prevention Gap Classification Module
6. AI Recommendation Component
7. Results and Reporting Layer

High-level flow:

User Interface
      |
      v
Input Data
      |
      v
Input Validation
      |
      v
Defect Analysis Engine
      |
      +----> Requirement Mapping
      |
      +----> Test Coverage Analysis
      |
      v
Prevention Gap Classification
      |
      v
AI Recommendation Component
      |
      v
Results and Reporting


---

## 3. Component Responsibilities

### 3.1 User Interface

The user interface will provide a simple web-based interface for:

- Loading the provided sample data.
- Starting the analysis.
- Displaying analysis results.
- Displaying prevention-gap information.
- Displaying AI-generated explanations and recommendations.

Streamlit will be used for the prototype interface.

---

### 3.2 Input Data Layer

The input data layer will handle the three primary datasets:

- Requirements
- Test Cases
- Escaped Defects

The prototype will use static or pre-provided sample data as specified
by the challenge scope.

---

### 3.3 Input Validation Module

The validation module will verify that:

- Required input fields are available.
- Requirement IDs referenced by defects exist.
- Requirement IDs referenced by test cases exist.
- Required values are not missing.
- Input data follows the expected structure.

Invalid input should produce a clear and understandable error message.

---

### 3.4 Defect Analysis Engine

The analysis engine will perform the core evidence-based analysis.

Responsibilities include:

- Mapping escaped defects to requirements.
- Identifying relevant test cases.
- Evaluating available test coverage.
- Identifying evidence of testing gaps.

The analysis engine will not depend on AI for its primary results.

---

### 3.5 Prevention Gap Classification Module

This module will classify each escaped defect into an appropriate
prevention-gap category based on the available evidence.

The initial categories will be defined during the system design stage.

The categories are a project design decision and may be refined during
implementation and testing.

---

### 3.6 AI Recommendation Component

The AI component will have a deliberately limited responsibility.

It will:

- Explain the likely prevention gap.
- Suggest a missing test area.

The AI component will not be responsible for:

- Performing the primary defect-to-requirement mapping.
- Calculating test coverage.
- Replacing deterministic validation logic.
- Making unsupported claims about the input data.

AI output will be treated as advisory.

---

### 3.7 Results and Reporting Layer

The results layer will present the structured analysis for each escaped
defect.

The output will include:

1. Mapping of escaped defects to missed requirements or weak test
   coverage.
2. Prevention-gap category.
3. Recommended new tests or process improvements.

---

## 4. Architecture Principles

The following principles will guide implementation:

### Separation of Responsibilities

Each component will have a clearly defined responsibility.

### Explainability

Core analysis results should be traceable to the provided input data.

### Modularity

Analysis components should be independently testable.

### Controlled AI Usage

AI will be restricted to the specified recommendation and explanation
task.

### Incremental Development

Components will be implemented and integrated incrementally rather than
building the complete application in one step.

---

## 5. Technology Mapping

| Component | Technology |
|---|---|
| User Interface | Streamlit |
| Data Processing | Python / Pandas |
| Validation | Python |
| Analysis Engine | Python / Pandas |
| Gap Classification | Python |
| AI Component | AI service/model |
| Results Display | Streamlit |

---

## 6. Architecture Scope

The prototype will remain intentionally lightweight.

The following are outside the initial implementation scope:

- Live production-system integration
- Jira or other external defect-management integration
- Enterprise authentication
- Microservices architecture
- Distributed infrastructure
- Continuous production monitoring

These may be considered as future enhancements if required.

---

## 7. Design Status

System architecture design is in progress.