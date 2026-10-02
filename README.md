# Defect Escape Analyzer

> Analyze escaped defects. Identify prevention gaps. Improve test coverage.

---

## 1. Project Overview

The **Defect Escape Analyzer** is a lightweight Engineering Quality prototype designed to analyze escaped software defects against requirements and existing test cases.

The tool helps identify:

- Which requirement is associated with an escaped defect
- Whether the escaped scenario was covered by existing test cases
- The likely prevention gap associated with the escaped defect
- A focused AI-generated explanation of the likely gap
- A recommended missing test area
- Related test cases that already exist for the affected requirement

The core analysis is deterministic and rule-based. AI is deliberately limited to explaining the likely prevention gap and suggesting one missing test area.

This separation keeps the primary QA analysis explainable and reproducible while using AI only where contextual reasoning is useful.

---

## 2. Challenge

**IGS Fresher Hackathon – Challenge #14**

### Defect Escape Analyzer

The challenge focuses on comparing escaped defects against requirements and existing test cases to identify what testing may have missed.

The prototype uses static/sample data and does not connect to live production systems or production credentials.

---

## 3. Objective

The objective is to build a practical QA analysis tool that can:

1. Map escaped defects to their associated requirements.
2. Identify related existing test cases.
3. Determine the level of test coverage for the escaped scenario.
4. Classify the likely prevention gap.
5. Use AI to explain the likely escape reason and recommend one missing test area.
6. Present the results in a user-friendly dashboard.
7. Allow the analysis results to be exported as CSV.

---

## 4. Key Features

### Input Validation

The application validates uploaded datasets before analysis.

Validation includes:

- Required column validation
- Duplicate ID detection
- Empty or missing required values
- Cross-reference validation between datasets

Test cases and escaped defects must reference valid requirement IDs.

---

### Defect-to-Requirement Mapping

Each escaped defect is mapped to its associated requirement using the `requirement_id`.

Unknown requirement references are rejected before analysis.

---

### Test Coverage Analysis

The analyzer evaluates existing test cases related to each escaped defect.

Coverage is classified as:

- **Covered** – an existing test directly addresses the escaped scenario.
- **Partially Covered** – related tests exist, but the specific escaped scenario is not directly represented.
- **Not Covered** – no related test exists for the requirement/scenario.

Scenario matching uses reusable whole-word/whole-phrase matching to avoid false matches caused by unrelated substrings.

For example:

```text
limit
```

must not incorrectly match:

```text
unlimited
```

---

### Prevention Gap Classification

Each escaped defect is assigned a likely prevention-gap category based on evidence from the defect, escape phase, related tests, and coverage status.

Current categories:

- **Test Coverage Gap**
- **Negative Testing Gap**
- **Boundary Testing Gap**
- **Data Validation Gap**
- **Integration Gap**
- **Process Gap**

`Process Gap` is used when the available evidence does not indicate a more specific prevention category. It is an inference rather than definitive root-cause proof.

---

### AI-Assisted Recommendation

AI is used for exactly one focused task:

> Explain the likely prevention gap and recommend one specific missing test area.

The AI does **not** determine:

- Defect-to-requirement mapping
- Coverage status
- Prevention-gap classification

These decisions are handled by deterministic application logic.

The AI receives only the relevant analysis evidence and returns two structured outputs:

1. Explanation of the likely escape reason
2. One recommended missing test area

AI recommendations are treated as advisory suggestions. Where the available evidence is insufficient, the AI is instructed to frame the explanation as a hypothesis rather than a confirmed fact.

Missing information is treated as unknown rather than evidence of absence. The AI is specifically instructed not to claim that assertions, test data, execution steps, validation checks, or other testing details were absent unless those details are explicitly provided.

---

### AI Resilience

The application is designed to continue deterministic analysis even when the AI service is unavailable.

Fallback behavior is used when:

- The Groq API key is missing
- The AI provider cannot be initialized
- The AI request fails

The deterministic coverage and prevention-gap results are preserved, while a safe fallback recommendation is generated.

---

### Streamlit Dashboard

The application provides:

- CSV upload interface
- Input validation feedback
- Coverage summary metrics
- Prevention-gap distribution
- Detailed defect analysis
- Related test cases
- AI explanation
- Recommended missing test area
- CSV export of analysis results

Completed analysis results are stored using Streamlit session state so that normal Streamlit reruns do not unnecessarily discard the generated results.

---

## 5. System Workflow

```text
Requirements CSV
        |
        |
Test Cases CSV -----> Input Validation
        |                    |
        |                    v
Escaped Defects CSV    Cross-Reference Validation
                             |
                             v
                    Defect-Requirement Mapping
                             |
                             v
                     Test Coverage Analysis
                             |
                             v
                  Prevention Gap Classification
                             |
                             v
                    AI Recommendation Layer
                             |
                             v
                    Streamlit Results Dashboard
                             |
                             v
                         CSV Export
```

The deterministic analysis is performed before the AI recommendation step.

---

## 6. Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Core application and analysis logic |
| Pandas | Dataset processing and analysis |
| Streamlit | User interface and dashboard |
| Pytest | Automated testing |
| OpenAI Python SDK | OpenAI-compatible client used for Groq integration |
| Groq API | AI recommendation generation |
| python-dotenv | Secure loading of environment variables |
| Git | Version control |
| GitHub | Source-code repository |
| GitHub Actions | Continuous integration and automated test execution |

---

## 7. Project Structure

```text
Defect-Escape-Analyzer/
│
├── app.py
│
├── data/
│   ├── requirements.csv
│   ├── test_cases.csv
│   └── escaped_defects.csv
│
├── docs/
│   ├── architecture.md
│   ├── data-model.md
│   ├── requirements.md
│   ├── development-plan.md
│   ├── user-stories.md
│   ├── test-checklist.md
│   └── workflow.md
│
├── src/
│   ├── __init__.py
│   ├── ai_recommender.py
│   ├── analyzer.py
│   ├── coverage.py
│   ├── gap_classifier.py
│   ├── mapper.py
│   ├── text_matching.py
│   └── validator.py
│
├── tests/
│   ├── test_ai_recommender.py
│   ├── test_analyzer.py
│   ├── test_coverage.py
│   ├── test_gap_classifier.py
│   ├── test_mapper.py
│   └── test_validator.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## 8. Input Data

The prototype uses three CSV datasets.

The sample datasets are provided for demonstration, but the application can process other datasets as long as they follow the documented schema and reference valid IDs.

### Requirements

Required columns:

```text
requirement_id
description
priority
```

Example:

```csv
requirement_id,description,priority
R001,User should be able to log in with valid credentials,High
```

---

### Test Cases

Required columns:

```text
test_case_id
requirement_id
test_description
test_type
result
```

Example:

```csv
test_case_id,requirement_id,test_description,test_type,result
TC001,R001,Login with valid username and password,Positive,Pass
```

---

### Escaped Defects

Required columns:

```text
id
requirement_id
description
severity
escape_phase
```

Example:

```csv
id,requirement_id,description,severity,escape_phase
D001,R002,System accepts a login attempt when the username format is invalid,High,System Testing
```

---

## 9. Sample Dataset

The included prototype dataset contains:

- 10 requirements
- 15 test cases
- 7 escaped defects

The sample data is synthetic and intended for demonstration and evaluation.

The sample dataset is not hard-coded as the only supported input. Users can upload other datasets that conform to the documented CSV schemas.

---

## 10. Prevention Gap Categories

The analyzer currently uses six categories.

### Test Coverage Gap

Related testing exists, but the specific escaped scenario was not adequately represented.

### Negative Testing Gap

The escaped behavior involves an invalid, unauthorized, rejected, or failure-path scenario that was not sufficiently tested.

### Boundary Testing Gap

The defect occurs around a limit, threshold, expiration point, or other boundary condition.

### Data Validation Gap

The defect involves incorrect acceptance, rejection, or validation of input or data.

### Integration Gap

The defect involves incorrect behavior between connected components, services, systems, or changing data.

### Process Gap

The available evidence does not clearly indicate a more specific prevention gap.

This classification is an inference based on the available evidence and may require additional process evidence for confirmation.

---

## 11. AI Design

AI is intentionally constrained to one task to keep the analysis explainable and reproducible.

### Deterministic Layer

Python logic handles:

```text
Requirement Mapping
        |
        v
Test Coverage Analysis
        |
        v
Prevention Gap Classification
```

These results are generated independently of the AI service.

### AI Layer

The AI receives relevant evidence and produces:

```text
1. Explanation of the likely escape reason
2. One recommended missing test area
```

The AI is instructed not to:

- Change the deterministic coverage result
- Change the prevention-gap category
- Invent requirements
- Invent existing test cases
- Claim unsupported system behavior as fact
- Treat missing information as proof that something was absent

This separation keeps the core QA analysis reproducible while using AI only where contextual reasoning is useful.

---

## 12. AI Failure Handling

The application is designed so that AI availability does not determine whether the core defect analysis can be completed.

If the AI provider is unavailable, the application:

1. Continues deterministic analysis.
2. Preserves the coverage result.
3. Preserves the prevention-gap classification.
4. Generates a deterministic fallback recommendation.

This allows the application to remain usable even when an external AI service is temporarily unavailable.

---

## 13. Environment Configuration

The Groq API key is stored locally in a `.env` file.

Create:

```text
.env
```

and add:

```text
GROQ_API_KEY=your_groq_api_key
```

The `.env` file is excluded from Git using `.gitignore`.

**Never commit or share the API key.**

The repository is designed to keep secrets outside source control.

---

## 14. Installation

### 1. Clone the repository

```bash
git clone https://github.com/chakravarthy123456/defect-escape-analyzer.git
cd defect-escape-analyzer
```

### 2. Create a virtual environment

Windows:

```cmd
python -m venv .venv
```

### 3. Activate the virtual environment

Windows CMD:

```cmd
.venv\Scripts\activate
```

### 4. Install dependencies

```cmd
pip install -r requirements.txt
```

### 5. Configure the environment variable

Create the `.env` file described above and add the Groq API key.

---

## 15. Running the Application

Start the Streamlit application:

```cmd
streamlit run app.py
```

The application will open in the browser.

Upload:

1. Requirements CSV
2. Test Cases CSV
3. Escaped Defects CSV

Then select:

```text
Run Analysis
```

The application validates the input data before running the analysis.

---

## 16. Running Tests

The project uses Pytest for automated testing.

Run:

```cmd
pytest
```

Current test result:

```text
33 passed
```

The test suite covers:

- AI recommendation behavior
- AI failure/fallback behavior
- End-to-end analyzer behavior
- Test coverage classification
- Coverage edge cases
- Prevention-gap classification
- Prevention-gap edge cases
- Defect-to-requirement mapping
- Input validation
- Cross-reference validation
- Regression scenarios

The test suite is also executed automatically using GitHub Actions.

---

## 17. Continuous Integration

The project uses GitHub Actions to automatically execute the test suite.

The CI workflow runs on:

- Pushes to `main`
- Pull requests targeting `main`

The workflow:

1. Checks out the repository.
2. Sets up Python 3.11.
3. Installs dependencies from `requirements.txt`.
4. Runs `pytest`.

A pull request is considered ready for merging only after the automated CI check passes.

Current CI validation:

```text
pytest → 33 passed
GitHub Actions → Passed
```

---

## 18. Example Analysis Results

For the included sample dataset, the deterministic analyzer identifies the following prevention gaps:

| Defect | Coverage | Prevention Gap |
|--------|----------|----------------|
| D001 | Partially Covered | Negative Testing Gap |
| D002 | Partially Covered | Boundary Testing Gap |
| D003 | Partially Covered | Data Validation Gap |
| D004 | Partially Covered | Negative Testing Gap |
| D005 | Partially Covered | Test Coverage Gap |
| D006 | Partially Covered | Integration Gap |
| D007 | Partially Covered | Integration Gap |

These results are generated by the deterministic analysis layer.

The AI then provides an explanation and recommended missing test area for each defect.

---

## 19. Testing Strategy

The project uses multiple complementary testing approaches.

### Unit Testing

Individual validation, mapping, coverage, classification, and recommendation components are tested using Pytest.

### Integration / End-to-End Testing

The complete analysis pipeline is tested from uploaded datasets through mapping, coverage analysis, prevention-gap classification, and AI recommendation generation.

### Functional Testing

The Streamlit workflow is manually tested:

```text
Upload CSVs
    ↓
Validate inputs
    ↓
Run analysis
    ↓
View results
    ↓
Review recommendations
    ↓
Download CSV
```

### Regression Testing

The existing automated suite is rerun after changes to ensure previously working functionality remains intact.

### Negative Testing

Failure and invalid-input scenarios are tested, including:

- Invalid requirement references
- Missing or invalid input values
- AI provider failure
- Unsupported matching scenarios

### Edge-Case Testing

Text matching is tested against substring false positives such as:

```text
limit
unlimited
```

The matching logic uses whole-word/whole-phrase matching to reduce false positives.

### AI Resilience Testing

The application is tested to verify that deterministic analysis continues when the AI service fails.

### CI Testing

GitHub Actions automatically executes the automated test suite on pull requests and pushes to `main`.

---

## 20. Quality and Engineering Practices

The project follows a lightweight SDLC-oriented development approach.

Key practices include:

- Modular source code
- Separation of deterministic analysis and AI functionality
- Input validation before processing
- Automated unit and integration-level tests
- Negative and edge-case testing
- Synthetic demonstration data
- Environment-based secret management
- Meaningful Git commits
- Incremental development
- GitHub Issues for task tracking
- Feature/fix branches for individual tasks
- Pull Requests for changes
- Automated GitHub Actions checks
- Documentation maintained alongside development
- Explicit assumptions and limitations

---

## 21. Git Development Workflow

Development was performed incrementally using Git and GitHub.

The workflow used for hardening tasks is:

```text
GitHub Issue
      |
      v
Create task branch
      |
      v
Implement change
      |
      v
Run automated tests
      |
      v
Manual validation when required
      |
      v
Push branch
      |
      v
Create Pull Request
      |
      v
GitHub Actions CI
      |
      v
Self-review
      |
      v
Merge
      |
      v
Delete local/remote branch
      |
      v
Update main
```

Major development areas were committed separately, including:

- Project requirements and scope
- System design
- Project planning
- Python environment setup
- Synthetic datasets
- Input validation
- Defect mapping
- Coverage analysis
- Prevention-gap classification
- AI recommendation interface
- AI integration
- End-to-end analysis
- Streamlit dashboard
- Result presentation
- Validation and environment configuration
- Coverage classification hardening
- Prevention-gap hardening
- AI resilience
- Streamlit session-state persistence
- GitHub Actions CI
- AI evidence grounding

This provides a traceable development history rather than treating the prototype as a single code drop.

---

## 22. Assumptions

- Input datasets follow the documented CSV structures.
- Requirement IDs are the primary traceability mechanism between requirements, test cases, and escaped defects.
- Test coverage is determined using the implemented deterministic scenario-matching logic.
- Prevention-gap classification represents the most likely category based on the available evidence.
- AI recommendations are advisory and should be reviewed by a QA engineer.
- Missing information is not treated as proof that a testing activity was absent.
- The prototype uses synthetic/static data.
- The application is intended for focused Engineering Quality analysis rather than complete enterprise defect management.

---

## 23. Limitations

- The prototype does not connect to live production systems.
- The quality of coverage analysis depends on the structure and wording of supplied test cases and defect descriptions.
- Keyword/scenario-based matching may not capture every semantic relationship between a defect and a test case.
- Prevention-gap classifications are based on available evidence and should not be treated as definitive root-cause analysis.
- AI-generated explanations are recommendations and require human review.
- The current test-case schema contains test descriptions but does not represent detailed assertions, test data, execution steps, or complete execution evidence.
- The prototype does not perform formal load, stress, or performance testing.
- The prototype does not implement a complete enterprise authentication and authorization model.
- The prototype is intended as a focused proof of concept rather than a complete enterprise defect-management platform.

---

## 24. Development Status

### Current Status: Working Prototype

Implemented:

- [x] Requirement analysis
- [x] Project planning
- [x] System architecture
- [x] Data model
- [x] Input validation
- [x] Cross-reference validation
- [x] Defect-to-requirement mapping
- [x] Test coverage analysis
- [x] Whole-word scenario matching
- [x] Prevention-gap classification
- [x] AI recommendation interface
- [x] Groq AI integration
- [x] AI fallback handling
- [x] AI evidence grounding
- [x] End-to-end analyzer
- [x] Streamlit dashboard
- [x] Streamlit session-state persistence
- [x] CSV result export
- [x] Automated testing
- [x] 33 passing automated tests
- [x] GitHub Actions CI
- [x] Environment-based API key configuration
- [x] Git/GitHub version control
- [x] Issue/branch/PR-based development workflow

---

## 25. Demo Screenshots

The final project documentation includes screenshots demonstrating the working prototype.

### 25.1 Application Landing Page

Shows the main Streamlit interface and the three required CSV inputs.

**Screenshot:**

```text
docs/screenshots/01-landing-page.png
```

---

### 25.2 Input Validation

Shows successful validation of:

- Requirements
- Test Cases
- Escaped Defects

**Screenshot:**

```text
docs/screenshots/02-input-validation.png
```

---

### 25.3 Analysis Dashboard

Shows the completed defect escape analysis and summary metrics.

**Screenshot:**

```text
docs/screenshots/03-analysis-dashboard.png
```

---

### 25.4 Prevention Gap Distribution

Shows the distribution of identified prevention gaps.

**Screenshot:**

```text
docs/screenshots/04-prevention-gap-distribution.png
```

---

### 25.5 Detailed Defect Analysis

Shows:

- Defect
- Requirement
- Coverage status
- Prevention gap
- Related test cases
- AI explanation
- Recommended missing test area

**Screenshot:**

```text
docs/screenshots/05-detailed-analysis.png
```

---

### 25.6 CSV Export

Shows the ability to download the completed analysis results.

**Screenshot:**

```text
docs/screenshots/06-export-results.png
```

---

### 25.7 GitHub Actions CI

Shows the automated test workflow passing successfully.

**Screenshot:**

```text
docs/screenshots/07-github-actions-ci.png
```

> Screenshot files should be added to the repository before using these paths as embedded images in the final documentation.

---

## 26. Future Enhancements

The following improvements are outside the current prototype scope but could be considered for a future version.

### Data and Traceability

- Support larger datasets
- Database-backed input and storage
- Improved semantic requirement-to-test traceability
- Richer test-case evidence such as assertions, test data, and execution steps
- Historical defect and coverage trend analysis

### Enterprise Integration

- Jira or other defect-management integration
- ALM/test-management system integration
- REST API support
- Authentication and role-based access control

### AI Enhancements

- More advanced evidence-grounded QA recommendations
- Historical defect pattern analysis
- Test-prioritization recommendations
- Improved semantic analysis while keeping deterministic QA rules as the core decision layer

### Deployment

- Cloud deployment
- Containerization using Docker
- Production-grade configuration and monitoring
- Database integration

### Quality Engineering

- Performance testing
- Load and stress testing
- Larger-scale regression datasets
- Additional security testing
- Automated test-data generation

### Reporting

- Interactive trend dashboards
- PDF/Excel reporting
- Requirement-to-test traceability visualization
- Historical prevention-gap reports

---

## 27. Conclusion

The **Defect Escape Analyzer** provides a focused approach to analyzing escaped software defects using requirements, existing test cases, deterministic QA logic, and a constrained AI recommendation layer.

The prototype demonstrates how AI can support Engineering Quality analysis without replacing deterministic validation and traceability.

The resulting workflow helps QA engineers move from:

```text
Escaped Defect
      |
      v
What was missed?
      |
      v
How was it covered?
      |
      v
What prevention gap is indicated?
      |
      v
What test area should be added?
```

The project combines:

```text
Deterministic QA Analysis
          +
Evidence-Grounded AI Assistance
          +
Automated Testing
          +
Git/GitHub Workflow
          +
Continuous Integration
          +
Streamlit Dashboard
```

while keeping the core analysis explainable, reproducible, testable, and suitable for a focused Engineering Quality prototype.
