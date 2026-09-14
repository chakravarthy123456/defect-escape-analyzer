"""
AI recommendation interface.

This module defines the input and output structure for the
AI-assisted recommendation step of the Defect Escape Analyzer.
"""
import json
import os
from dataclasses import dataclass

from openai import OpenAI


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


class GroqRecommendationProvider:
    """Generate QA recommendations using the Groq API."""

    def __init__(
        self,
        model: str = "openai/gpt-oss-20b",
    ):
        self.model = model

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY environment variable is not set."
            )

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
        )

    def generate_recommendation(
        self,
        recommendation_input: RecommendationInput,
    ) -> Recommendation:
        """Generate a structured AI recommendation."""

        prompt = build_recommendation_prompt(
            recommendation_input
        )

        response = self.client.responses.create(
            model=self.model,
            input=prompt,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "qa_recommendation",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "explanation": {
                                "type": "string"
                            },
                            "missing_test_area": {
                                "type": "string"
                            },
                        },
                        "required": [
                            "explanation",
                            "missing_test_area",
                        ],
                        "additionalProperties": False,
                    },
                }
            },
        )

        result = json.loads(response.output_text)

        return Recommendation(
            explanation=result["explanation"],
            missing_test_area=result["missing_test_area"],
        )