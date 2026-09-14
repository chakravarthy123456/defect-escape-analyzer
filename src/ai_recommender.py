"""
AI recommendation interface.

This module defines the input and output structure for the
AI-assisted recommendation step of the Defect Escape Analyzer.
"""

from dataclasses import dataclass


@dataclass
class RecommendationInput:
    """Evidence provided to the AI recommendation component."""

    defect_description: str
    requirement_description: str
    related_test_cases: list[str]
    coverage_status: str
    prevention_gap: str


@dataclass
class Recommendation:
    """Structured recommendation returned by the AI component."""

    explanation: str
    missing_test_area: str


def build_recommendation_prompt(
    recommendation_input: RecommendationInput,
) -> str:
    """
    Build a focused prompt for the AI recommendation task.

    The prompt restricts the AI to explaining the likely
    prevention gap and suggesting a missing test area.
    """

    related_tests = "\n".join(
        f"- {test}"
        for test in recommendation_input.related_test_cases
    )

    return f"""
You are assisting a QA engineer with an escaped-defect analysis.

Use only the evidence provided below.

Defect:
{recommendation_input.defect_description}

Requirement:
{recommendation_input.requirement_description}

Related Test Cases:
{related_tests}

Coverage Status:
{recommendation_input.coverage_status}

Prevention Gap:
{recommendation_input.prevention_gap}

Provide exactly two outputs:

1. Explanation:
Explain the likely reason this defect escaped based on
the available testing evidence.

2. Missing Test Area:
Suggest one specific test area that should be added
to help prevent a similar defect in the future.

Do not change the coverage status.
Do not change the prevention-gap category.
Do not invent requirements or test results.
""".strip()