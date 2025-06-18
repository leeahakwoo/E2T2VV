"""Module 1 – Data Profile / Quality"""
import streamlit as st
import pandas as pd
import pandera as pa
from pandera import infer_schema
from evidently.report import Report
from evidently.metric_preset import DataQualityPreset, DataDriftPreset

def _load_csv(label):
    file = st.file_uploader(label, type=["csv"], key=label)
    if file:
        return pd.read_csv(file)
    return None

def render():
    st.header("📊 Data Profile / Quality")
    ref_df = _load_csv("Upload reference dataset (baseline)")
    cur_df = _load_csv("Upload current dataset (to test)")

    if ref_df is None or cur_df is None:
        st.info("Please upload both reference and current CSV files.")
        return

    # Pandera validation
    schema = infer_schema(ref_df)
    with st.expander("Inferred schema (Pandera)"):
        st.code(schema.to_script(), language="python")

    try:
        schema.validate(cur_df, lazy=True)
        st.success("Schema validation passed ✅")
    except pa.errors.SchemaErrors as err:
        st.error("Schema validation failed ❌")
        st.write(err.failure_cases)

    # Evidently
    dq = Report(DataQualityPreset())
    dq.run(ref_df, cur_df)
    dd = Report(DataDriftPreset())
    dd.run(ref_df, cur_df)

    st.subheader("Data Quality Report")
    st.components.v1.html(dq.show(mode="inline"), height=600, scrolling=True)
    st.subheader("Data Drift Report")
    st.components.v1.html(dd.show(mode="inline"), height=600, scrolling=True)