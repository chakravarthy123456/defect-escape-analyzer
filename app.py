"""
Defect Escape Analyzer - Streamlit Application.

This module provides the user interface for uploading datasets,
validating inputs, running defect escape analysis, and displaying
the resulting QA insights.
"""

import pandas as pd
import streamlit as st

from src.analyzer import analyze_defect_escapes
from src.validator import (
    validate_dataset,
    validate_reference_ids,
)


# -------------------------------------------------------------------
# Page configuration
# -------------------------------------------------------------------

st.set_page_config(
    page_title="Defect Escape Analyzer",
    page_icon="🔍",
    layout="wide",
)


# -------------------------------------------------------------------
# Application title
# -------------------------------------------------------------------

st.title("🔍 Defect Escape Analyzer")

st.markdown(
    """
    **Analyze escaped defects. Identify prevention gaps. Improve test coverage.**
    Upload requirements, test cases, and escaped defects to identify
    testing gaps and prevention opportunities.
    """
)


# -------------------------------------------------------------------
# Input data upload
# -------------------------------------------------------------------

st.header("1. Upload Input Data")

requirements_file = st.file_uploader(
    "Upload Requirements CSV",
    type=["csv"],
    key="requirements",
)

test_cases_file = st.file_uploader(
    "Upload Test Cases CSV",
    type=["csv"],
    key="test_cases",
)

escaped_defects_file = st.file_uploader(
    "Upload Escaped Defects CSV",
    type=["csv"],
    key="escaped_defects",
)


# -------------------------------------------------------------------
# Run analysis
# -------------------------------------------------------------------

if st.button("Run Analysis", type="primary"):

    # ---------------------------------------------------------------
    # Check whether all required files were uploaded
    # ---------------------------------------------------------------

    if not all(
        [
            requirements_file,
            test_cases_file,
            escaped_defects_file,
        ]
    ):
        st.error(
            "Please upload all three required CSV files "
            "before running the analysis."
        )
        st.stop()

    # ---------------------------------------------------------------
    # Load CSV files
    # ---------------------------------------------------------------

    try:
        requirements = pd.read_csv(requirements_file)
        test_cases = pd.read_csv(test_cases_file)
        escaped_defects = pd.read_csv(escaped_defects_file)

    except Exception as error:
        st.error(
            f"Unable to read the uploaded CSV files: {error}"
        )
        st.stop()

    # ---------------------------------------------------------------
    # Define required columns
    # ---------------------------------------------------------------

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

    # ---------------------------------------------------------------
    # Validate individual datasets
    # ---------------------------------------------------------------

    requirements_validation = validate_dataset(
        requirements,
        requirement_columns,
        "requirement_id",
    )

    test_cases_validation = validate_dataset(
        test_cases,
        test_case_columns,
        "test_case_id",
    )

    escaped_defects_validation = validate_dataset(
        escaped_defects,
        defect_columns,
        "defect_id",
    )

    # ---------------------------------------------------------------
    # Validate cross-dataset requirement references
    #
    # Test cases and escaped defects must reference requirements
    # that actually exist in the requirements dataset.
    # ---------------------------------------------------------------

    unknown_test_case_requirements = []
    unknown_defect_requirements = []

    if "requirement_id" in requirements.columns:

        requirement_ids = set(
            requirements["requirement_id"]
            .dropna()
            .astype(str)
            .str.strip()
        )

        if "requirement_id" in test_cases.columns:
            unknown_test_case_requirements = (
                validate_reference_ids(
                    test_cases,
                    "requirement_id",
                    requirement_ids,
                )
            )

        if "requirement_id" in escaped_defects.columns:
            unknown_defect_requirements = (
                validate_reference_ids(
                    escaped_defects,
                    "requirement_id",
                    requirement_ids,
                )
            )

    # ---------------------------------------------------------------
    # Display validation results
    # ---------------------------------------------------------------

    st.header("2. Input Validation")

    validation_failed = False

    # Cross-reference validation
    if unknown_test_case_requirements:
        st.error(
            "Test Cases: Unknown requirement IDs: "
            f"{unknown_test_case_requirements}"
        )
        validation_failed = True

    if unknown_defect_requirements:
        st.error(
            "Escaped Defects: Unknown requirement IDs: "
            f"{unknown_defect_requirements}"
        )
        validation_failed = True

    # Individual dataset validation
    validation_results = [
        (
            "Requirements",
            requirements_validation,
        ),
        (
            "Test Cases",
            test_cases_validation,
        ),
        (
            "Escaped Defects",
            escaped_defects_validation,
        ),
    ]

    for dataset_name, validation in validation_results:

        if validation["valid"]:
            st.success(
                f"{dataset_name}: Validation passed."
            )
            continue

        validation_failed = True

        if validation["missing_columns"]:
            st.error(
                f"{dataset_name}: Missing required columns: "
                f"{validation['missing_columns']}"
            )

        if validation["duplicate_ids"]:
            st.error(
                f"{dataset_name}: Duplicate IDs found: "
                f"{validation['duplicate_ids']}"
            )

        if validation["invalid_values"]:
            st.error(
                f"{dataset_name}: Missing or empty values in: "
                f"{validation['invalid_values']}"
            )

    # ---------------------------------------------------------------
    # Stop analysis if validation fails
    # ---------------------------------------------------------------

    if validation_failed:
        st.error(
            "Input validation failed. "
            "Please correct the uploaded datasets and try again."
        )
        st.stop()

    st.success(
        "All input datasets passed validation."
    )

    # ---------------------------------------------------------------
    # Run defect escape analysis
    # ---------------------------------------------------------------

    st.header("3. Defect Escape Analysis")

    try:
        analysis_results = analyze_defect_escapes(
            requirements,
            test_cases,
            escaped_defects,
        )

    except Exception as error:
        st.error(
            f"Analysis failed: {error}"
        )
        st.stop()

    # ---------------------------------------------------------------
    # Prevention gap distribution
    # ---------------------------------------------------------------

    st.subheader("Prevention Gap Distribution")

    gap_distribution = (
        analysis_results["prevention_gap"]
        .value_counts()
    )

    st.bar_chart(gap_distribution)

    # ---------------------------------------------------------------
    # Summary metrics
    # ---------------------------------------------------------------

    st.subheader("Analysis Summary")

    total_defects = len(analysis_results)

    covered_count = (
        analysis_results["coverage_status"]
        == "Covered"
    ).sum()

    partially_covered_count = (
        analysis_results["coverage_status"]
        == "Partially Covered"
    ).sum()

    not_covered_count = (
        analysis_results["coverage_status"]
        == "Not Covered"
    ).sum()

    metric_1, metric_2, metric_3, metric_4 = st.columns(4)

    metric_1.metric(
        "Escaped Defects",
        total_defects,
    )

    metric_2.metric(
        "Covered",
        covered_count,
    )

    metric_3.metric(
        "Partially Covered",
        partially_covered_count,
    )

    metric_4.metric(
        "Not Covered",
        not_covered_count,
    )

    # ---------------------------------------------------------------
    # Detailed defect results
    # ---------------------------------------------------------------

    st.subheader("Detailed Defect Analysis")

    for _, row in analysis_results.iterrows():

        with st.expander(
            f"{row['defect_id']} — {row['prevention_gap']}"
        ):

            st.markdown(
                f"**Requirement:** "
                f"{row['requirement_id']}"
            )

            st.markdown(
                f"**Defect:** "
                f"{row['defect_description']}"
            )

            st.markdown(
                f"**Requirement Description:** "
                f"{row['requirement_description']}"
            )

            st.markdown(
                f"**Coverage Status:** "
                f"{row['coverage_status']}"
            )

            st.markdown(
                f"**Prevention Gap:** "
                f"{row['prevention_gap']}"
            )

            st.markdown(
                f"**Related Test Cases:** "
                f"{row['related_test_case_ids']}"
            )

            st.markdown("---")

            st.markdown("**AI Explanation**")

            st.write(
                row["ai_explanation"]
            )

            st.markdown("**Recommended Missing Test Area**")

            st.write(
                row["missing_test_area"]
            )

    # ---------------------------------------------------------------
    # Download analysis results
    # ---------------------------------------------------------------

    st.header("4. Export Results")

    csv_data = analysis_results.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Analysis Results",
        data=csv_data,
        file_name="defect_escape_analysis.csv",
        mime="text/csv",
    )