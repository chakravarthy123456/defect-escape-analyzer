# User Stories and Acceptance Criteria

## 1. Upload Analysis Data

### User Story
As a QA engineer, I want to upload requirements, test cases, and escaped defects so that I can analyze escaped defects against existing quality artifacts.

### Acceptance Criteria
- The user can upload the requirements CSV.
- The user can upload the test cases CSV.
- The user can upload the escaped defects CSV.
- The application prompts the user when any required file is missing.
- The application accepts the files only when their required structure is valid.

### Priority
High

---

## 2. Validate Input Data

### User Story
As a QA engineer, I want the uploaded datasets to be validated before analysis so that invalid input does not produce misleading results.

### Acceptance Criteria
- Required columns are checked.
- Duplicate IDs are detected.
- Missing or empty required values are detected.
- Invalid requirement references are detected.
- Analysis is stopped when validation fails.
- Validation errors are clearly presented to the user.

### Priority
High

---

## 3. Map Escaped Defects to Requirements

### User Story
As a QA engineer, I want escaped defects to be mapped to their associated requirements so that each defect can be traced back to the expected system behavior.

### Acceptance Criteria
- Each valid defect is mapped using `requirement_id`.
- The associated requirement description is available for analysis.
- Invalid requirement references are rejected during validation.
- The mapping remains traceable in the analysis results.

### Priority
High

---

## 4. Analyze Test Coverage

### User Story
As a QA engineer, I want escaped defect scenarios to be compared with existing test cases so that I can identify whether the escaped scenario was adequately tested.

### Acceptance Criteria
- Related test cases are identified using the requirement relationship.
- Each escaped defect receives a coverage status.
- Coverage is classified as `Covered`, `Partially Covered`, or `Not Covered`.
- Related test case IDs are shown in the results.
- Coverage classification is performed by deterministic application logic.

### Priority
High

---

## 5. Classify Prevention Gaps

### User Story
As a QA engineer, I want each escaped defect to be assigned a likely prevention-gap category so that I can identify areas where testing or prevention could be improved.

### Acceptance Criteria
- Each analyzed defect receives one prevention-gap category.
- Categories are selected from the defined classification set.
- Classification is based on available requirement, defect, test, and coverage evidence.
- The classification is performed independently of the AI recommendation.
- Where evidence is insufficient for a specific category, `Process Gap` may be used as an inference.

### Priority
High

---

## 6. Generate AI Recommendations

### User Story
As a QA engineer, I want an AI-generated explanation of the likely escape reason and a recommended missing test area so that I can identify actionable testing improvements.

### Acceptance Criteria
- The AI receives the relevant analysis evidence.
- The AI explains the likely reason for the defect escape.
- The AI recommends one specific missing test area.
- The AI does not change the deterministic coverage result.
- The AI does not change the deterministic prevention-gap classification.
- The AI does not invent requirements or existing test cases.
- AI output follows the expected structured format.

### Priority
High

---

## 7. View Analysis Results

### User Story
As a QA engineer, I want to view defect-level analysis results in a dashboard so that I can understand the overall quality gaps and investigate individual defects.

### Acceptance Criteria
- Total escaped defects are displayed.
- Coverage metrics are displayed.
- Prevention-gap distribution is displayed.
- Individual defect details can be reviewed.
- Related requirements and test cases are shown.
- AI explanation and recommended test area are shown where available.

### Priority
Medium

---

## 8. Export Analysis Results

### User Story
As a QA engineer, I want to download the analysis results so that I can review or share the findings outside the application.

### Acceptance Criteria
- Analysis results can be downloaded as a CSV file.
- The exported results contain the defect analysis information.
- The export is available after a successful analysis.

### Priority
Medium

---

# Prioritization Approach

Due to the limited prototype development time, requirements were prioritized around the minimum end-to-end business value.

The implementation priority was:

1. Input validation
2. Defect-to-requirement mapping
3. Test coverage analysis
4. Prevention-gap classification
5. AI recommendation
6. Results presentation
7. Results export

The core analysis path was implemented before secondary usability features.

The following were intentionally kept outside the prototype scope:

- Production database integration
- Live defect-management system integration
- Authentication and authorization
- REST API layer
- Enterprise-scale infrastructure
- CI/CD infrastructure
- Production monitoring
- Kubernetes or microservice architecture

These can be considered in a future production-oriented iteration.