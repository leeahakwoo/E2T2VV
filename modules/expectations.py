"""Module 2 – Expectations with Great Expectations"""
import streamlit as st
import pandas as pd
import great_expectations as gx
from pathlib import Path

data_root = Path("gx_data")
data_root.mkdir(exist_ok=True)

def _load_csv(label: str):
    uf = st.file_uploader(label, type=["csv"], key=label)
    if uf:
        return pd.read_csv(uf)
    return None

def render():
    st.header("📝 Expectations / Schema Validation")

    df = _load_csv("Upload dataset for validation")
    if df is None:
        st.info("Upload a CSV to create or validate Expectations.")
        return

    gx_context = gx.get_context(project_root_dir=str(data_root))
    suite_name = st.text_input("Expectation Suite name", "demo_suite")
    expectation_path = data_root / "expectations" / f"{suite_name}.json"

    if not expectation_path.exists():
        if st.button("Create Expectation Suite from current data"):
            ds = gx.dataset.PandasDataset(df)
            suite = ds.profile(expectation_suite_name=suite_name)
            gx_context.save_expectation_suite(suite)
            st.success("Suite created. Re‑run to validate 🚀")
            return

    suite = gx_context.get_expectation_suite(suite_name)
    result = gx.validate(df, expectation_suite=suite)
    st.subheader("Validation Results")
    st.write(result.render())