"""
Prevention gap classification utilities.

This module assigns a primary prevention-gap category to
escaped defects using deterministic rules.
"""

#import pandas as pd


GAP_CATEGORIES = [
    "Boundary Testing Gap",
    "Integration Gap",
    "Negative Testing Gap",
    "Data Validation Gap",
    "Test Coverage Gap",
    "Requirement Gap",
    "Process Gap",
]


def classify_prevention_gap(
    defect_description: str,
    escape_phase: str,
    coverage_status: str,
) -> str:
    """
    Classify the primary prevention gap for an escaped defect.

    Args:
        defect_description: Description of the escaped defect.
        escape_phase: Testing phase where the defect was discovered.
        coverage_status: Coverage classification for the defect.

    Returns:
        The primary prevention-gap category.
    """

    defect_text = defect_description.lower()
    phase_text = escape_phase.lower()

    boundary_terms = [
        "expiration",
        "limit",
        "threshold",
        "boundary",
    ]

    integration_terms = [
        "inventory",
        "stock changes",
        "after the price is updated",
        "after inventory",
        "integration",
    ]

    negative_terms = [
        "invalid",
        "unauthorized",
        "reject",
        "accepts",
    ]

    data_validation_terms = [
    "domain format",
    "email address",
    "validation",
]

    if (
        "integration" in phase_text
        or any(term in defect_text for term in integration_terms)
    ):
        return "Integration Gap"

    if "zero" in defect_text or any(
        term in defect_text for term in boundary_terms
    ):
        return "Boundary Testing Gap"

    if any(term in defect_text for term in data_validation_terms):
        return "Data Validation Gap"

    if any(term in defect_text for term in negative_terms):
        return "Negative Testing Gap"

    if coverage_status == "Partially Covered":
        return "Test Coverage Gap"

    return "Process Gap"