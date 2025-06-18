"""Module 1 – Data Profile / Quality (Pandera + Evidently)"""
import streamlit as st
import pandas as pd
import pandera as pa
from pandera import infer_schema
from evidently.report import Report
from evidently.metric_preset import DataQualityPreset, DataDriftPreset

def _load_csv(label: str):
    uf = st.file_uploader(label, type=["csv"], key=label)
    if uf:
        return pd.read_csv(uf)
    return None

def render():
    st.header("📊 Data Profile / Quality")

    ref_df = _load_csv("Upload reference dataset (baseline)")
    cur_df = _load_csv("Upload current dataset (to test)")

    if ref_df is None or cur_df is None:
        st.info("Please upload both reference and current CSV files to proceed.")
        return

    # Pandera schema inference & validation
    schema = infer_schema(ref_df)
    with st.expander("🔍  Inferred Schema (Pandera)"):
        st.code(schema.to_script(), language="python")

    validation_errors = None
    try:
        schema.validate(cur_df, lazy=True)
        st.success("Schema validation passed ✅")
    except pa.errors.SchemaErrors as err:
        validation_errors = err.failure_cases
        st.error("Schema validation FAILED ❌")
        st.write(validation_errors)

    # Evidently reports
    dq_report = Report(DataQualityPreset())
    dq_report.run(ref_df, cur_df)

    dd_report = Report(DataDriftPreset())
    dd_report.run(ref_df, cur_df)

    st.subheader("Data Quality Report")
    st.components.v1.html(dq_report.show(mode="inline"), height=600, scrolling=True)

    st.subheader("Data Drift Report")
    st.components.v1.html(dd_report.show(mode="inline"), height=600, scrolling=True)