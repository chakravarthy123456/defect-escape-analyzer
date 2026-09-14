from src.ai_recommender import (
    Recommendation,
    RecommendationInput,
    build_recommendation_prompt,
)

def test_recommendation_input_stores_analysis_evidence():
    evidence = RecommendationInput(
        defect_description="Expired reset link remains usable",
        requirement_description="User can reset a forgotten password",
        related_test_cases=[
            "Reset password using registered email",
        ],
        coverage_status="Partially Covered",
        prevention_gap="Boundary Testing Gap",
    )

    assert evidence.defect_description == (
        "Expired reset link remains usable"
    )
    assert evidence.coverage_status == "Partially Covered"
    assert evidence.prevention_gap == "Boundary Testing Gap"
    assert len(evidence.related_test_cases) == 1


def test_prompt_contains_required_evidence():
    evidence = RecommendationInput(
        defect_description="Expired reset link remains usable",
        requirement_description="User can reset a forgotten password",
        related_test_cases=[
            "Reset password using registered email",
        ],
        coverage_status="Partially Covered",
        prevention_gap="Boundary Testing Gap",
    )

    prompt = build_recommendation_prompt(evidence)

    assert "Expired reset link remains usable" in prompt
    assert "User can reset a forgotten password" in prompt
    assert "Reset password using registered email" in prompt
    assert "Partially Covered" in prompt
    assert "Boundary Testing Gap" in prompt


def test_prompt_restricts_ai_to_recommendation_task():
    evidence = RecommendationInput(
        defect_description="Expired reset link remains usable",
        requirement_description="User can reset a forgotten password",
        related_test_cases=[],
        coverage_status="Not Covered",
        prevention_gap="Boundary Testing Gap",
    )

    prompt = build_recommendation_prompt(evidence)

    assert "Explanation:" in prompt
    assert "Missing Test Area:" in prompt
    assert "Do not change the coverage status." in prompt
    assert "Do not change the prevention-gap category." in prompt

def test_recommendation_has_required_fields():
    recommendation = Recommendation(
        explanation="The defect escaped because the scenario was not sufficiently tested.",
        missing_test_area="Add a dedicated negative test for invalid username formats.",
    )

    assert recommendation.explanation
    assert recommendation.missing_test_area