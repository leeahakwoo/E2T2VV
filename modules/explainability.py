"""Module 5 – Explainability (SHAP)"""
import streamlit as st
import shap
import pandas as pd
import pickle

def _upload_model():
    f = st.file_uploader("Upload pickled tree model", type=["pkl","pickle"])
    if f:
        return pickle.load(f)
    return None

def _upload_data():
    f = st.file_uploader("Upload background data (CSV)", type="csv")
    if f:
        return pd.read_csv(f)
    return None

def render():
    st.header("🔎 Explainability (SHAP)")
    model = _upload_model()
    data = _upload_data()
    if model is None or data is None:
        st.info("Upload model and data.")
        return
    explainer = shap.Explainer(model, data)
    values = explainer(data)
    st.pyplot(shap.plots.beeswarm(values, show=False))