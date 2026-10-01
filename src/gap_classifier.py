"""
Prevention gap classification utilities.

This module assigns a primary prevention-gap category to
escaped defects using deterministic rules.
"""

#import pandas as pd
from src.text_matching import contains_term

GAP_CATEGORIES = [
    "Boundary Testing Gap",
    "Integration Gap",
    "Negative Testing Gap",
    "Data Validation Gap",
    "Test Coverage Gap",
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
        contains_term(phase_text, "integration")
        or any(contains_term(defect_text, term) for term in integration_terms)
    ):
        return "Integration Gap"

    if contains_term(defect_text, "zero") or any(
        contains_term(defect_text, term)
        for term in boundary_terms
    ):
        return "Boundary Testing Gap"

    if any(
        contains_term(defect_text, term)
        for term in data_validation_terms
    ):
        return "Data Validation Gap"

    if any(
        contains_term(defect_text, term)
        for term in negative_terms
    ):
        return "Negative Testing Gap"

    if coverage_status == "Partially Covered":
        return "Test Coverage Gap"

    return "Process Gap"
