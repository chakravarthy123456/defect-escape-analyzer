"""
Test coverage analysis utilities.

This module identifies existing test cases associated with the
requirements linked to escaped defects.
"""

import pandas as pd


def find_related_test_cases(
    mapped_defects: pd.DataFrame,
    test_cases: pd.DataFrame,
) -> pd.DataFrame:
    """
    Find test cases related to each escaped defect.

    Test cases are related to a defect when they reference the
    same requirement ID.

    Args:
        mapped_defects: Defects already mapped to requirements.
        test_cases: Test case dataset.

    Returns:
        DataFrame containing each defect and its related test cases.
    """

    related_data = []

    for _, defect in mapped_defects.iterrows():
        requirement_id = defect["requirement_id"]

        matching_tests = test_cases[
            test_cases["requirement_id"] == requirement_id
        ]

        test_case_ids = matching_tests["test_case_id"].tolist()

        related_data.append(
            {
                "defect_id": defect["defect_id"],
                "requirement_id": requirement_id,
                "related_test_case_ids": test_case_ids,
                "related_test_case_count": len(test_case_ids),
            }
        )

    return pd.DataFrame(related_data)

def classify_coverage(
    defect_description: str,
    related_test_descriptions: list[str],
) -> str:
    """
    Classify the coverage of an escaped defect.

    Returns:
        Covered, Partially Covered, or Not Covered.
    """

    if not related_test_descriptions:
        return "Not Covered"

    defect_text = defect_description.lower()
    test_text = " ".join(related_test_descriptions).lower()

    scenario_indicators = {
        "format",
        "expiration",
        "domain",
        "unauthorized",
        "partial",
        "outdated",
        "zero",
        "stock",
    }

    defect_scenarios = {
        word
        for word in scenario_indicators
        if word in defect_text
    }

    uncovered_scenarios = {
        word
        for word in defect_scenarios
        if word not in test_text
    }

    if uncovered_scenarios:
        return "Partially Covered"

    return "Covered"