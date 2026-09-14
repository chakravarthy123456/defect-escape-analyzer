"""
Tests for the end-to-end defect escape analysis pipeline.
"""

from unittest.mock import patch

import pandas as pd

from src.analyzer import analyze_defect_escapes
from src.ai_recommender import Recommendation


def load_test_data():
    """Load the project's sample datasets."""

    requirements = pd.read_csv("data/requirements.csv")
    test_cases = pd.read_csv("data/test_cases.csv")
    escaped_defects = pd.read_csv("data/escaped_defects.csv")

    return requirements, test_cases, escaped_defects


def fake_ai_recommendation(self, recommendation_input):
    """
    Return a deterministic AI response for automated testing.

    This prevents the test suite from making live Groq API calls.
    """

    return Recommendation(
        explanation="Test explanation based on the supplied evidence.",
        missing_test_area="Test missing scenario.",
    )


@patch(
    "src.analyzer.GroqRecommendationProvider.generate_recommendation",
    new=fake_ai_recommendation,
)
def test_analyze_defect_escapes_returns_all_defects():
    """Verify that all escaped defects are analyzed."""

    requirements, test_cases, escaped_defects = load_test_data()

    results = analyze_defect_escapes(
        requirements,
        test_cases,
        escaped_defects,
    )

    assert len(results) == 7
    assert set(results["defect_id"]) == {
        "D001",
        "D002",
        "D003",
        "D004",
        "D005",
        "D006",
        "D007",
    }


@patch(
    "src.analyzer.GroqRecommendationProvider.generate_recommendation",
    new=fake_ai_recommendation,
)
def test_analyze_defect_escapes_preserves_deterministic_results():
    """Verify coverage and prevention-gap classifications."""

    requirements, test_cases, escaped_defects = load_test_data()

    results = analyze_defect_escapes(
        requirements,
        test_cases,
        escaped_defects,
    )

    expected_results = {
        "D001": ("Partially Covered", "Negative Testing Gap"),
        "D002": ("Partially Covered", "Boundary Testing Gap"),
        "D003": ("Partially Covered", "Data Validation Gap"),
        "D004": ("Partially Covered", "Negative Testing Gap"),
        "D005": ("Covered", "Process Gap"),
        "D006": ("Partially Covered", "Integration Gap"),
        "D007": ("Partially Covered", "Integration Gap"),
    }

    for defect_id, (coverage, gap) in expected_results.items():
        result = results[
            results["defect_id"] == defect_id
        ].iloc[0]

        assert result["coverage_status"] == coverage
        assert result["prevention_gap"] == gap


@patch(
    "src.analyzer.GroqRecommendationProvider.generate_recommendation",
    new=fake_ai_recommendation,
)
def test_analyze_defect_escapes_includes_ai_results():
    """Verify that AI recommendation fields are included."""

    requirements, test_cases, escaped_defects = load_test_data()

    results = analyze_defect_escapes(
        requirements,
        test_cases,
        escaped_defects,
    )

    assert "ai_explanation" in results.columns
    assert "missing_test_area" in results.columns

    assert results["ai_explanation"].notna().all()
    assert results["missing_test_area"].notna().all()