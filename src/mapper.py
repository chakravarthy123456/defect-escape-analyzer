"""
Defect-to-requirement mapping utilities.

This module maps escaped defects to their associated requirements
using the Requirement ID shared between the datasets.
"""

import pandas as pd


def map_defects_to_requirements(
    requirements: pd.DataFrame,
    escaped_defects: pd.DataFrame,
) -> pd.DataFrame:
    """
    Map each escaped defect to its associated requirement.

    Args:
        requirements: Requirements dataset.
        escaped_defects: Escaped defects dataset.

    Returns:
        DataFrame containing defect information together with the
        corresponding requirement description.

    Raises:
        ValueError: If a defect references a requirement that does
        not exist.
    """

    requirement_ids = set(
        requirements["requirement_id"]
        .astype(str)
        .str.strip()
    )

    defect_requirement_ids = set(
        escaped_defects["requirement_id"]
        .astype(str)
        .str.strip()
    )

    unknown_ids = sorted(
        defect_requirement_ids - requirement_ids
    )

    if unknown_ids:
        raise ValueError(
            f"Unknown requirement IDs found: {unknown_ids}"
        )

    mapped_data = escaped_defects.merge(
        requirements[
            ["requirement_id", "description"]
        ],
        on="requirement_id",
        how="left",
        suffixes=("_defect", "_requirement"),
    )

    mapped_data = mapped_data.rename(
        columns={
            "description_defect": "defect_description",
            "description_requirement": "requirement_description",
        }
    )

    return mapped_data[
        [
            "defect_id",
            "requirement_id",
            "defect_description",
            "requirement_description",
            "severity",
            "escape_phase",
        ]
    ]