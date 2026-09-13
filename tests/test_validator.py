import pandas as pd

from src.validator import (
    validate_dataset,
    validate_reference_ids,
)


def test_valid_requirements_dataset():
    dataframe = pd.DataFrame(
        {
            "requirement_id": ["R001", "R002"],
            "description": ["Login", "Logout"],
            "priority": ["High", "Medium"],
        }
    )

    result = validate_dataset(
        dataframe,
        ["requirement_id", "description", "priority"],
        "requirement_id",
    )

    assert result["valid"] is True
    assert result["missing_columns"] == []
    assert result["duplicate_ids"] == []
    assert result["invalid_values"] == []


def test_missing_required_column():
    dataframe = pd.DataFrame(
        {
            "requirement_id": ["R001"],
            "priority": ["High"],
        }
    )

    result = validate_dataset(
        dataframe,
        ["requirement_id", "description", "priority"],
        "requirement_id",
    )

    assert result["valid"] is False
    assert "description" in result["missing_columns"]


def test_duplicate_ids():
    dataframe = pd.DataFrame(
        {
            "requirement_id": ["R001", "R001"],
            "description": ["Login", "Logout"],
            "priority": ["High", "Medium"],
        }
    )

    result = validate_dataset(
        dataframe,
        ["requirement_id", "description", "priority"],
        "requirement_id",
    )

    assert result["valid"] is False
    assert "R001" in result["duplicate_ids"]


def test_empty_required_value():
    dataframe = pd.DataFrame(
        {
            "requirement_id": ["R001"],
            "description": [""],
            "priority": ["High"],
        }
    )

    result = validate_dataset(
        dataframe,
        ["requirement_id", "description", "priority"],
        "requirement_id",
    )

    assert result["valid"] is False
    assert "description" in result["invalid_values"]


def test_unknown_reference_ids():
    dataframe = pd.DataFrame(
        {
            "requirement_id": ["R001", "R999"],
        }
    )

    valid_ids = {"R001", "R002"}

    unknown_ids = validate_reference_ids(
        dataframe,
        "requirement_id",
        valid_ids,
    )

    assert unknown_ids == ["R999"]

def test_project_sample_data():
    requirements = pd.read_csv("data/requirements.csv")
    test_cases = pd.read_csv("data/test_cases.csv")
    escaped_defects = pd.read_csv("data/escaped_defects.csv")

    requirement_columns = [
        "requirement_id",
        "description",
        "priority",
    ]

    test_case_columns = [
        "test_case_id",
        "requirement_id",
        "test_description",
        "test_type",
        "result",
    ]

    defect_columns = [
        "defect_id",
        "requirement_id",
        "description",
        "severity",
        "escape_phase",
    ]

    requirements_result = validate_dataset(
        requirements,
        requirement_columns,
        "requirement_id",
    )

    test_cases_result = validate_dataset(
        test_cases,
        test_case_columns,
        "test_case_id",
    )

    escaped_defects_result = validate_dataset(
        escaped_defects,
        defect_columns,
        "defect_id",
    )

    valid_requirement_ids = set(
        requirements["requirement_id"]
        .astype(str)
        .str.strip()
    )

    unknown_test_requirements = validate_reference_ids(
        test_cases,
        "requirement_id",
        valid_requirement_ids,
    )

    unknown_defect_requirements = validate_reference_ids(
        escaped_defects,
        "requirement_id",
        valid_requirement_ids,
    )

    assert requirements_result["valid"] is True
    assert test_cases_result["valid"] is True
    assert escaped_defects_result["valid"] is True

    assert unknown_test_requirements == []
    assert unknown_defect_requirements == []