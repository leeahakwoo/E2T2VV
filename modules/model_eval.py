"""Module 3 – Model Evaluation (Giskard)"""
import streamlit as st
import pandas as pd
import pickle
import giskard

def _upload_model():
    f = st.file_uploader("Upload pickled sklearn model", type=["pkl","pickle"])
    if f:
        return pickle.load(f)
    return None

def _upload_csv(label):
    f = st.file_uploader(label, type=["csv"], key=label)
    if f:
        return pd.read_csv(f)
    return None

def render():
    st.header("🧪 Model Evaluation / Giskard")
    model = _upload_model()
    test_df = _upload_csv("Upload test dataset (CSV)")
    target = st.text_input("Target column", "target")
    if model is None or test_df is None:
        st.info("Upload model and dataset.")
        return
    dataset = giskard.Dataset(df=test_df, target=target)
    scan = giskard.scan(model, dataset)
    st.dataframe(scan.to_dataframe())