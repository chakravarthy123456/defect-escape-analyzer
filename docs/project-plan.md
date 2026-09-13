# Project Development Plan

## 1. Project Overview

### Project Name

Defect Escape Analyzer

### Challenge

IGS Fresher Hackathon - Challenge #14

### Purpose

The project will be developed as a lightweight prototype for analyzing
escaped software defects against requirements and existing test cases.

The goal is to identify potential testing/prevention gaps and provide
actionable recommendations for improving test coverage or testing
processes.

---

## 2. Development Approach

The project will follow a structured Software Development Life Cycle
(SDLC) approach.

The major stages are:

1. Requirement Analysis
2. Planning
3. System Design
4. Incremental Development
5. Testing
6. Integration and Refinement
7. Documentation
8. Final Delivery and Presentation

Each stage will produce identifiable project artifacts.

Development will be incremental rather than implementing the entire
application at once.

---

## 3. Development Principles

The following principles will be followed throughout the project:

### 3.1 Incremental Development

The application will be developed in small functional increments.

Each increment will be implemented, reviewed, and verified before moving
to the next increment.

### 3.2 Modular Design

The application logic will be separated into independent modules based
on responsibility.

This will improve maintainability, readability, and testability.

### 3.3 Documentation Throughout Development

Documentation will be maintained throughout the SDLC rather than being
created only at the end.

The README and supporting documentation will be updated as the project
progresses.

### 3.4 Git-Based Development

Git will be used to maintain the development history.

Changes will be committed early and frequently using meaningful commit
messages.

Each meaningful increment will represent a logical step in the project
history.

### 3.5 Explainable Changes

Commit messages and documentation will describe what was changed and,
where appropriate, why the change was made.

The Git history will provide a chronological view of the development
process.

---

## 4. Technology Selection

### 4.1 Python

Python will be used as the primary programming language because it
provides a simple development environment and has suitable libraries
for data processing and application development.

### 4.2 Streamlit

Streamlit will be used to create the lightweight web-based user
interface for the prototype.

It allows the analysis workflow to be demonstrated through an
interactive interface without requiring a complex frontend framework.

### 4.3 Pandas

Pandas will be used for loading, validating, transforming, and analyzing
the tabular requirements, test-case, and defect data.

### 4.4 AI Component

AI will be used for one specific task:

- Explaining the likely prevention gap.
- Suggesting a missing test area.

The core evidence-based analysis will remain separate from the AI
component so that the application's primary analysis can remain
understandable and testable.

---

## 5. Development Milestones

### Milestone 1 — Requirement Analysis

Activities:

- Define problem statement.
- Define objective.
- Define functional requirements.
- Define non-functional requirements.
- Define scope and constraints.
- Define assumptions.
- Define success criteria.

Status: Completed

Artifact:

- `docs/requirements.md`

---

### Milestone 2 — Project Planning

Activities:

- Define development approach.
- Select technology stack.
- Define development milestones.
- Identify risks.
- Define Git strategy.
- Define testing approach.

Status: In Progress

Artifact:

- `docs/project-plan.md`

---

### Milestone 3 — System Design

Activities:

- Define high-level architecture.
- Define data flow.
- Define input data model.
- Define analysis workflow.
- Define prevention-gap categories.
- Define AI integration boundary.
- Define UI structure.

Expected artifacts:

- Architecture documentation
- Data model documentation
- Workflow documentation

---

### Milestone 4 — Incremental Development

Development will be performed as separate functional increments.

Planned increments:

1. Project/data structure
2. Sample data handling
3. Input validation
4. Requirement-defect mapping
5. Test coverage analysis
6. Prevention-gap classification
7. Recommendation generation
8. AI-assisted explanation
9. Streamlit interface
10. Error handling and refinement

Each completed increment will be reviewed and committed separately.

---

### Milestone 5 — Testing

Testing activities will include:

- Unit testing
- Functional testing
- Integration testing
- Input validation testing
- Edge-case testing
- End-to-end workflow testing

Testing evidence will be documented.

---

### Milestone 6 — Integration and Refinement

After the core components are implemented:

- Integrate the analysis modules.
- Integrate the user interface.
- Verify the end-to-end workflow.
- Fix identified defects.
- Improve error handling.
- Refactor code where necessary.
- Improve usability.

---

### Milestone 7 — Documentation

The following documentation will be maintained:

- README
- Requirements
- Project plan
- System architecture
- Data model
- Testing strategy
- Test evidence
- Assumptions
- Limitations
- Future enhancements

---

### Milestone 8 — Final Delivery

Final activities:

- Verify complete functionality.
- Run the final test suite.
- Review Git history.
- Update README.
- Document limitations.
- Prepare demonstration.
- Prepare presentation.
- Prepare for technical discussion.

---

## 6. Risk Management

| Risk | Impact | Mitigation |
|---|---|---|
| Scope expansion | High | Keep the implementation within the challenge scope |
| Incorrect input data | Medium | Implement input validation |
| Incorrect defect mapping | High | Provide traceable mapping evidence |
| AI-generated inaccurate recommendations | High | Keep AI output advisory and grounded in analyzed evidence |
| Integration issues | Medium | Integrate components incrementally |
| Insufficient testing | High | Maintain automated and functional test coverage |
| Poor documentation | Medium | Update documentation throughout development |
| Time constraints | High | Prioritize core functionality before enhancements |

---

## 7. Git Strategy

Git will be used throughout the project lifecycle.

### Commit Principles

- Commit early.
- Commit often.
- Keep commits focused on a logical change.
- Use meaningful commit messages.
- Avoid combining unrelated changes into one commit.
- Push completed increments to the remote repository.

### Commit Message Convention

The project will use descriptive prefixes such as:

- `docs:` for documentation changes
- `feat:` for new functionality
- `test:` for tests
- `fix:` for defect fixes
- `refactor:` for code restructuring
- `chore:` for project maintenance

### Example

```text
docs: add system architecture
feat: implement input validation
feat: implement defect requirement mapping
test: add coverage analysis tests
fix: handle unmapped requirement IDs