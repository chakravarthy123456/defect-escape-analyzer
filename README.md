# Defect Escape Analyzer

> Analyze escaped defects. Identify prevention gaps. Improve test coverage.

## 1. Project Overview

The **Defect Escape Analyzer** is a lightweight Engineering Quality prototype designed to analyze escaped software defects against requirements and existing test cases.

The tool helps identify:

- Which requirement is associated with an escaped defect
- Whether the escaped scenario was covered by existing test cases
- The likely prevention gap that allowed the defect to escape
- A focused AI-generated explanation of the likely gap
- A recommended missing test area

The core analysis is deterministic and rule-based. AI is deliberately limited to explaining the likely prevention gap and suggesting one missing test area.

---

## 2. Challenge

**IGS Fresher Hackathon – Challenge #14**

### Defect Escape Analyzer

The challenge focuses on comparing escaped defects against requirements and existing test cases to identify what testing may have missed.

---

## 3. Objective

The objective is to build a practical QA analysis tool that can:

1. Map escaped defects to their associated requirements.
2. Identify related existing test cases.
3. Determine the level of test coverage for the escaped scenario.
4. Classify the likely prevention gap.
5. Use AI to explain the likely escape reason and recommend a missing test area.
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

### Defect-to-Requirement Mapping

Each escaped defect is mapped to its associated requirement using the `requirement_id`.

### Test Coverage Analysis

The analyzer evaluates existing test cases related to each escaped defect.

Coverage is classified as:

- **Covered** – an existing test directly addresses the escaped scenario.
- **Partially Covered** – related tests exist, but the specific escaped scenario is not directly represented.
- **Not Covered** – no meaningful test exists for the requirement or scenario.

### Prevention Gap Classification

Each escaped defect is assigned a likely prevention-gap category based on evidence from the requirement, defect, escape phase, related tests, and coverage status.

Current categories:

- Requirement Gap
- Test Coverage Gap
- Negative Testing Gap
- Boundary Testing Gap
- Data Validation Gap
- Integration Gap
- Process Gap

### AI-Assisted Recommendation

AI is used for exactly one task:

> Explain the likely prevention gap and recommend one specific missing test area.

The AI does **not** determine:

- Defect-to-requirement mapping
- Coverage status
- Prevention-gap classification

These decisions are handled by deterministic application logic.

AI recommendations are treated as evidence-based suggestions. Where the available evidence is insufficient, the AI is instructed to frame the result as a hypothesis rather than a confirmed fact.

### Streamlit Dashboard

The application provides:

- CSV upload interface
- Input validation feedback
- Prevention-gap distribution
- Coverage summary metrics
- Detailed defect analysis
- AI explanation
- Recommended missing test area
- CSV export of analysis results

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
│   ├── project-plan.md
│   └── workflow.md
│
├── src/
│   ├── __init__.py
│   ├── ai_recommender.py
│   ├── analyzer.py
│   ├── coverage.py
│   ├── gap_classifier.py
│   ├── mapper.py
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
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## 8. Input Data

The prototype uses three CSV datasets.

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

### Escaped Defects

Required columns:

```text
defect_id
requirement_id
description
severity
escape_phase
```

Example:

```csv
defect_id,requirement_id,description,severity,escape_phase
D001,R002,System accepts a login attempt when the username format is invalid,High,System Testing
```

---

## 9. Sample Dataset

The included prototype dataset contains:

- 10 requirements
- 15 test cases
- 7 escaped defects

The sample data is synthetic and intended only for demonstration and evaluation.

---

## 10. Prevention Gap Categories

The analyzer currently uses the following categories.

### Requirement Gap

The requirement may be incomplete, ambiguous, or insufficiently defined for the escaped scenario.

### Test Coverage Gap

Related testing exists, but the specific scenario was not adequately represented.

### Negative Testing Gap

The escaped behavior involves an invalid, unauthorized, rejected, or failure-path scenario that was not sufficiently tested.

### Boundary Testing Gap

The defect occurs around a limit, threshold, expiration point, or other boundary condition.

### Data Validation Gap

The defect involves incorrect acceptance, rejection, or validation of input or data.

### Integration Gap

The defect involves incorrect behavior between connected components, services, systems, or changing data.

### Process Gap

The available evidence does not clearly indicate a more specific prevention gap. This classification is an inference and may require additional process evidence for confirmation.

---

## 11. AI Design

AI is intentionally constrained to one task to keep the analysis explainable and reproducible.

### Deterministic Layer

Python logic handles:

```text
Requirement Mapping
        ↓
Test Coverage Analysis
        ↓
Prevention Gap Classification
```

### AI Layer

The AI receives the relevant analysis evidence and produces:

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

This separation keeps the core QA analysis reproducible while using AI only where contextual reasoning is useful.

---

## 12. Environment Configuration

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

---

## 13. Installation

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

## 14. Running the Application

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

## 15. Running Tests

The project uses Pytest for automated testing.

Run:

```cmd
pytest
```

Current test result:

```text
30 passed
```

The test suite covers:

- AI recommendation behavior
- End-to-end analyzer behavior
- Test coverage classification
- Prevention-gap classification
- Defect-to-requirement mapping
- Input validation
- Cross-reference validation

---

## 16. Example Analysis Results

For the included sample dataset, the analyzer identifies the following prevention gaps:

| Defect | Prevention Gap |
|--------|----------------|
| D001 | Negative Testing Gap |
| D002 | Boundary Testing Gap |
| D003 | Data Validation Gap |
| D004 | Negative Testing Gap |
| D005 | Process Gap |
| D006 | Integration Gap |
| D007 | Integration Gap |

These results are generated by the deterministic analysis layer.

The AI then provides an explanation and recommended missing test area for each defect.

---

## 17. Quality and Engineering Practices

The project follows a lightweight SDLC-oriented development approach.

Key practices include:

- Modular source code
- Separation of deterministic analysis and AI functionality
- Input validation before processing
- Automated unit and integration-level tests
- Synthetic demonstration data
- Environment-based secret management
- Meaningful Git commits
- Incremental development
- Documentation maintained alongside development
- Explicit assumptions and limitations

---

## 18. Assumptions

- Input datasets follow the documented CSV structures.
- Requirement IDs are the primary traceability mechanism between requirements, test cases, and escaped defects.
- Test coverage is determined using the implemented deterministic scenario-matching logic.
- Prevention-gap classification represents the most likely category based on the available evidence.
- AI recommendations are advisory and should be reviewed by a QA engineer.
- The prototype uses synthetic/static data.

---

## 19. Limitations

- The prototype does not connect to live production systems.
- The quality of coverage analysis depends on the structure and wording of the supplied test cases and defect descriptions.
- Keyword/scenario-based matching may not capture every semantic relationship between a defect and a test case.
- Prevention-gap classifications are based on available evidence and should not be treated as definitive root-cause analysis.
- AI-generated explanations are recommendations and require human review.
- The prototype is intended as a focused proof of concept rather than a complete enterprise defect-management platform.

---

## 20. Development Status

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
- [x] Prevention-gap classification
- [x] AI recommendation interface
- [x] Groq AI integration
- [x] End-to-end analyzer
- [x] Streamlit dashboard
- [x] CSV result export
- [x] Automated testing
- [x] Environment-based API key configuration
- [x] Git/GitHub version control

---

## 21. Git Development Approach

Development was performed incrementally using Git.

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

This provides a traceable development history rather than treating the prototype as a single code drop.

---

## 22. Conclusion

The Defect Escape Analyzer provides a focused approach to analyzing escaped software defects using requirements, existing test cases, deterministic QA logic, and a constrained AI recommendation layer.

The prototype demonstrates how AI can support Engineering Quality analysis without replacing deterministic validation and traceability.

The resulting workflow helps QA engineers move from:

```text
Escaped Defect
      ↓
What was missed?
      ↓
Why might it have escaped?
      ↓
What test area should be added?
```

while keeping the core analysis explainable and reproducible.
