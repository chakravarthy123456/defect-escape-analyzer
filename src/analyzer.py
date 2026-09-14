"""
End-to-end defect escape analysis orchestration.

This module coordinates the deterministic analysis modules and
the AI recommendation component.
"""

import pandas as pd

from src.coverage import classify_coverage, find_related_test_cases
from src.gap_classifier import classify_prevention_gap
from src.mapper import map_defects_to_requirements
from src.ai_recommender import (
    GroqRecommendationProvider,
    RecommendationInput,
)


def analyze_defect_escapes(
    requirements: pd.DataFrame,
    test_cases: pd.DataFrame,
    escaped_defects: pd.DataFrame,
):
    """
    Run the complete defect escape analysis workflow.

    The deterministic analysis performs:
    1. Defect-to-requirement mapping.
    2. Related test-case identification.
    3. Coverage classification.
    4. Prevention-gap classification.

    The AI component then:
    5. Explains the likely prevention gap.
    6. Suggests one missing test area.

    Returns:
        DataFrame containing the complete analysis results.
    """

    # Step 1: Map escaped defects to their requirements
    mapped_defects = map_defects_to_requirements(
        requirements,
        escaped_defects,
    )

    # Step 2: Identify test cases related to each defect
    related_tests = find_related_test_cases(
        mapped_defects,
        test_cases,
    )

    analysis_results = []

    # Step 3: Analyze each escaped defect
    for _, defect in mapped_defects.iterrows():

        defect_id = defect["defect_id"]
        requirement_id = defect["requirement_id"]

        # Find test cases associated with this requirement
        matching_tests = test_cases[
            test_cases["requirement_id"] == requirement_id
        ]

        test_descriptions = matching_tests[
            "test_description"
        ].tolist()

        # Step 4: Classify test coverage
        coverage_status = classify_coverage(
            defect["defect_description"],
            test_descriptions,
        )

        # Step 5: Classify the likely prevention gap
        prevention_gap = classify_prevention_gap(
            defect["defect_description"],
            defect["escape_phase"],
            coverage_status,
        )

        # Step 6: Prepare evidence for the AI component
        recommendation_input = RecommendationInput(
            defect_description=defect["defect_description"],
            requirement_description=defect[
                "requirement_description"
            ],
            related_test_cases=test_descriptions,
            coverage_status=coverage_status,
            prevention_gap=prevention_gap,
        )

        # Step 7: Generate AI explanation and recommendation
        provider = GroqRecommendationProvider()

        recommendation = provider.generate_recommendation(
            recommendation_input
        )

        # Step 8: Store the complete analysis result
        analysis_results.append(
            {
                "defect_id": defect_id,
                "requirement_id": requirement_id,
                "defect_description": defect[
                    "defect_description"
                ],
                "requirement_description": defect[
                    "requirement_description"
                ],
                "coverage_status": coverage_status,
                "prevention_gap": prevention_gap,
                "related_test_case_ids": matching_tests[
                    "test_case_id"
                ].tolist(),
                "ai_explanation": recommendation.explanation,
                "missing_test_area": recommendation.missing_test_area,
            }
        )

    return pd.DataFrame(analysis_results)