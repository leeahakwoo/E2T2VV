"""Module 2 – Expectations (Great Expectations)"""
import streamlit as st
import pandas as pd
import great_expectations as gx
from pathlib import Path

data_root = Path("gx_light_data")
data_root.mkdir(exist_ok=True)

def _load_csv(label):
    file = st.file_uploader(label, type=["csv"], key=label)
    if file:
        return pd.read_csv(file)
    return None

def render():
    st.header("📝 Expectations / Schema Validation")
    df = _load_csv("Upload dataset for validation")
    if df is None:
        st.info("Upload a CSV to create or validate expectations.")
        return

    gx_ctx = gx.get_context(project_root_dir=str(data_root))
    suite_name = st.text_input("Expectation Suite name", "demo_suite")
    suite_path = data_root / "expectations" / f"{suite_name}.json"

    if not suite_path.exists():
        if st.button("Create suite from data"):
            ds = gx.dataset.PandasDataset(df)
            suite = ds.profile(expectation_suite_name=suite_name)
            gx_ctx.save_expectation_suite(suite)
            st.success("Suite created. Re-run to validate.")
            return

    suite = gx_ctx.get_expectation_suite(suite_name)
    res = gx.validate(df, expectation_suite=suite)
    st.write(res.render())