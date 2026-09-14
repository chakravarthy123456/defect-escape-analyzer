"""
Defect Escape Analyzer - Streamlit Application.

This is the user interface layer for the defect escape
analysis prototype.
"""

import streamlit as st
import pandas as pd

from src.analyzer import analyze_defect_escapes

# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Defect Escape Analyzer",
    page_icon="🔍",
    layout="wide",
)


# ---------------------------------------------------------
# Application header
# ---------------------------------------------------------

st.title("🔍 Defect Escape Analyzer")

st.write(
    "Analyze escaped defects, identify prevention gaps, "
    "and improve test coverage."
)


# ---------------------------------------------------------
# Input section
# ---------------------------------------------------------

st.header("Input Data")

st.write(
    "Upload the three CSV files required for the analysis."
)

requirements_file = st.file_uploader(
    "Upload Requirements CSV",
    type=["csv"],
)

test_cases_file = st.file_uploader(
    "Upload Test Cases CSV",
    type=["csv"],
)

escaped_defects_file = st.file_uploader(
    "Upload Escaped Defects CSV",
    type=["csv"],
)


# ---------------------------------------------------------
# Analysis control
# ---------------------------------------------------------

if st.button("Analyze Defects", type="primary"):

    if not all(
        [
            requirements_file,
            test_cases_file,
            escaped_defects_file,
        ]
    ):
        st.error(
            "Please upload all three CSV files before "
            "starting the analysis."
        )

    else:
     st.success(
        "All required input files have been uploaded."
    )

    # Load uploaded CSV files
    requirements = pd.read_csv(requirements_file)
    test_cases = pd.read_csv(test_cases_file)
    escaped_defects = pd.read_csv(escaped_defects_file)

    st.success("Input files loaded successfully.")

    # Run the complete defect escape analysis
    with st.spinner("Analyzing escaped defects..."):
        results = analyze_defect_escapes(
            requirements,
            test_cases,
            escaped_defects,
        )

    st.success("Analysis completed successfully.")

    # Display analysis results
    st.header("Analysis Results")

# ---------------------------------------------------------
# Analysis Summary
# ---------------------------------------------------------

total_defects = len(results)

partially_covered = (
    results["coverage_status"] == "Partially Covered"
).sum()

fully_covered = (
    results["coverage_status"] == "Covered"
).sum()

gap_types = results["prevention_gap"].nunique()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Escaped Defects",
        total_defects,
    )

with col2:
    st.metric(
        "Partially Covered",
        partially_covered,
    )

with col3:
    st.metric(
        "Fully Covered",
        fully_covered,
    )

with col4:
    st.metric(
        "Prevention Gap Types",
        gap_types,
    )


# ---------------------------------------------------------
# Detailed Results
# ---------------------------------------------------------

st.subheader("Detailed Defect Analysis")

st.dataframe(
    results,
    use_container_width=True,
)
    