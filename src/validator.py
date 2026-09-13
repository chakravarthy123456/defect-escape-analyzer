"""
Input validation utilities for the Defect Escape Analyzer.

This module validates the structure and basic integrity of the
requirements, test cases, and escaped defects datasets.
"""

import pandas as pd


def validate_required_columns(
    dataframe: pd.DataFrame,
    required_columns: list[str]
) -> list[str]:
    """
    Check whether all required columns are present.

    Returns:
        A list containing the names of missing columns.
    """

    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    return missing_columns


def validate_unique_ids(
    dataframe: pd.DataFrame,
    id_column: str
) -> list[str]:
    """
    Check whether values in the specified ID column are unique.

    Returns:
        A list of duplicate IDs.
    """

    duplicate_ids = (
        dataframe.loc[
            dataframe[id_column].duplicated(keep=False),
            id_column
        ]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    return duplicate_ids


def validate_required_values(
    dataframe: pd.DataFrame,
    required_columns: list[str]
) -> list[str]:
    """
    Check whether required fields contain missing or empty values.

    Returns:
        A list of column names containing invalid values.
    """

    invalid_columns = []

    for column in required_columns:
        if dataframe[column].isna().any():
            invalid_columns.append(column)
            continue

        if dataframe[column].astype(str).str.strip().eq("").any():
            invalid_columns.append(column)

    return invalid_columns


def validate_reference_ids(
    dataframe: pd.DataFrame,
    reference_column: str,
    valid_ids: set[str]
) -> list[str]:
    """
    Check whether referenced IDs exist in the valid ID set.

    Returns:
        A list of unknown referenced IDs.
    """

    referenced_ids = set(
        dataframe[reference_column]
        .dropna()
        .astype(str)
        .str.strip()
    )

    return sorted(referenced_ids - valid_ids)


def validate_dataset(
    dataframe: pd.DataFrame,
    required_columns: list[str],
    id_column: str
) -> dict:
    """
    Perform structural validation on a dataset.

    Returns:
        A dictionary containing validation results.
    """

    missing_columns = validate_required_columns(
        dataframe,
        required_columns
    )

    if missing_columns:
        return {
            "valid": False,
            "missing_columns": missing_columns,
            "duplicate_ids": [],
            "invalid_values": []
        }

    duplicate_ids = validate_unique_ids(
        dataframe,
        id_column
    )

    invalid_values = validate_required_values(
        dataframe,
        required_columns
    )

    is_valid = not duplicate_ids and not invalid_values

    return {
        "valid": is_valid,
        "missing_columns": [],
        "duplicate_ids": duplicate_ids,
        "invalid_values": invalid_values
    }