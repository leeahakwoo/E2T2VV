"""Module 6 – Explainability (SHAP)"""
import streamlit as st
import shap
import pandas as pd
import pickle

def _upload_model():
    f = st.file_uploader("Upload pickled tree‑based model", type=["pkl", "pickle"], key="shap_model")
    if f:
        return pickle.load(f)
    return None

def _upload_data():
    f = st.file_uploader("Upload background data (CSV)", type="csv", key="shap_data")
    if f:
        return pd.read_csv(f)
    return None

def render():
    st.header("🔎 Explainability")

    model = _upload_model()
    data = _upload_data()
    if model is None or data is None:
        st.info("Upload model and data to generate SHAP values.")
        return

    explainer = shap.Explainer(model, data)
    shap_values = explainer(data)

    st.subheader("Beeswarm Plot")
    st.pyplot(shap.plots.beeswarm(shap_values, show=False))