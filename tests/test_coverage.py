import pandas as pd

from src.coverage import (
    classify_coverage,
    find_related_test_cases,
)
from src.mapper import map_defects_to_requirements


def test_related_test_cases_are_identified():
    mapped_defects = pd.DataFrame(
        {
            "defect_id": ["D001", "D002"],
            "requirement_id": ["R002", "R003"],
        }
    )

    test_cases = pd.DataFrame(
        {
            "test_case_id": ["TC001", "TC002", "TC003"],
            "requirement_id": ["R002", "R002", "R003"],
        }
    )

    result = find_related_test_cases(
        mapped_defects,
        test_cases,
    )

    assert len(result) == 2

    assert result.loc[0, "defect_id"] == "D001"
    assert result.loc[0, "related_test_case_ids"] == [
        "TC001",
        "TC002",
    ]
    assert result.loc[0, "related_test_case_count"] == 2

    assert result.loc[1, "defect_id"] == "D002"
    assert result.loc[1, "related_test_case_ids"] == ["TC003"]
    assert result.loc[1, "related_test_case_count"] == 1


def test_defect_with_no_related_test_cases_returns_empty_list():
    mapped_defects = pd.DataFrame(
        {
            "defect_id": ["D001"],
            "requirement_id": ["R999"],
        }
    )

    test_cases = pd.DataFrame(
        {
            "test_case_id": ["TC001"],
            "requirement_id": ["R002"],
        }
    )

    result = find_related_test_cases(
        mapped_defects,
        test_cases,
    )

    assert result.loc[0, "related_test_case_ids"] == []
    assert result.loc[0, "related_test_case_count"] == 0

def test_coverage_is_classified_as_covered():
    defect_description = (
        "Search does not return products when only part "
        "of the product name is entered"
    )

    related_test_descriptions = [
        "Search using an exact product name",
        "Search using a partial product name",
    ]

    result = classify_coverage(
        defect_description,
        related_test_descriptions,
    )

    assert result == "Covered"


def test_coverage_is_classified_as_partially_covered():
    defect_description = (
        "System accepts a login attempt when the "
        "username format is invalid"
    )

    related_test_descriptions = [
        "Login with invalid password",
        "Login with invalid username",
    ]

    result = classify_coverage(
        defect_description,
        related_test_descriptions,
    )

    assert result == "Partially Covered"


def test_coverage_is_classified_as_not_covered():
    defect_description = (
        "Password reset link remains usable after "
        "the configured expiration period"
    )

    related_test_descriptions = []

    result = classify_coverage(
        defect_description,
        related_test_descriptions,
    )

    assert result == "Not Covered"

def test_real_project_data_coverage_analysis():
    requirements = pd.read_csv("data/requirements.csv")
    test_cases = pd.read_csv("data/test_cases.csv")
    escaped_defects = pd.read_csv("data/escaped_defects.csv")

    mapped_defects = map_defects_to_requirements(
        requirements,
        escaped_defects,
    )

    related_tests = find_related_test_cases(
        mapped_defects,
        test_cases,
    )

    coverage_results = []

    for _, defect in mapped_defects.iterrows():
        matching_tests = test_cases[
            test_cases["requirement_id"]
            == defect["requirement_id"]
        ]

        test_descriptions = matching_tests[
            "test_description"
        ].tolist()

        coverage = classify_coverage(
            defect["defect_description"],
            test_descriptions,
        )

        coverage_results.append(coverage)

    assert len(coverage_results) == 7
    assert coverage_results.count("Covered") == 1
    assert coverage_results.count("Partially Covered") == 6