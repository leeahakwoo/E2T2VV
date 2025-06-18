"""Module 3 – Model Evaluation via Giskard"""
import streamlit as st
import pandas as pd
import pickle
import giskard

def _upload_model():
    f = st.file_uploader("Upload pickled sklearn model", type=["pkl", "pickle"], key="giskard_model")
    if f:
        return pickle.load(f)
    return None

def _upload_dataset(label):
    f = st.file_uploader(label, type=["csv"], key=label)
    if f:
        return pd.read_csv(f)
    return None

def render():
    st.header("🧪 Model Evaluation / Giskard Scan")

    model = _upload_model()
    test_df = _upload_dataset("Upload test dataset (CSV)")
    target = st.text_input("Target column", "target")

    if model is None or test_df is None:
        st.info("Upload model and test data to run the scan.")
        return

    dataset = giskard.Dataset(df=test_df, target=target)
    scan = giskard.scan(model, dataset)

    st.subheader("Scan Results")
    st.dataframe(scan.to_dataframe())