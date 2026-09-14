from src.gap_classifier import classify_prevention_gap


def test_expiration_issue_is_boundary_testing_gap():
    result = classify_prevention_gap(
        "Password reset link remains usable after the configured expiration period",
        "System Testing",
        "Partially Covered",
    )

    assert result == "Boundary Testing Gap"


def test_inventory_issue_is_integration_gap():
    result = classify_prevention_gap(
        "Unavailable product can be added to the cart after inventory reaches zero",
        "Integration Testing",
        "Partially Covered",
    )

    assert result == "Integration Gap"


def test_invalid_input_is_negative_testing_gap():
    result = classify_prevention_gap(
        "System accepts a login attempt when the username format is invalid",
        "System Testing",
        "Partially Covered",
    )

    assert result == "Negative Testing Gap"


def test_email_domain_issue_is_data_validation_gap():
    result = classify_prevention_gap(
        "System accepts an email address with an invalid domain format",
        "System Testing",
        "Partially Covered",
    )

    assert result == "Data Validation Gap"


def test_partial_coverage_without_specific_category_is_test_coverage_gap():
    result = classify_prevention_gap(
        "System does not handle the expected user scenario",
        "System Testing",
        "Partially Covered",
    )

    assert result == "Test Coverage Gap"


def test_fully_covered_unclassified_issue_is_process_gap():
    result = classify_prevention_gap(
        "System behaves differently under an unexpected condition",
        "System Testing",
        "Covered",
    )

    assert result == "Process Gap"

def test_real_project_defects_have_expected_gap_categories():
    expected_gaps = {
        "D001": "Negative Testing Gap",
        "D002": "Boundary Testing Gap",
        "D003": "Data Validation Gap",
        "D004": "Negative Testing Gap",
        "D005": "Process Gap",
        "D006": "Integration Gap",
        "D007": "Integration Gap",
    }

    actual_gaps = {
        "D001": classify_prevention_gap(
            "System accepts a login attempt when the username format is invalid",
            "System Testing",
            "Partially Covered",
        ),
        "D002": classify_prevention_gap(
            "Password reset link remains usable after the configured expiration period",
            "System Testing",
            "Partially Covered",
        ),
        "D003": classify_prevention_gap(
            "System accepts an email address with an invalid domain format",
            "System Testing",
            "Partially Covered",
        ),
        "D004": classify_prevention_gap(
            "Unauthorized user can modify another users profile information",
            "Security Testing",
            "Partially Covered",
        ),
        "D005": classify_prevention_gap(
            "Search does not return products when only part of the product name is entered",
            "System Testing",
            "Covered",
        ),
        "D006": classify_prevention_gap(
            "Product page displays an outdated product price after the price is updated",
            "Integration Testing",
            "Partially Covered",
        ),
        "D007": classify_prevention_gap(
            "Unavailable product can be added to the cart after inventory reaches zero",
            "Integration Testing",
            "Partially Covered",
        ),
    }

    assert actual_gaps == expected_gaps