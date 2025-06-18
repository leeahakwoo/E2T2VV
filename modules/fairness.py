"""Module 4 – Fairness Analysis (Fairlearn)"""
import streamlit as st
import pandas as pd
from fairlearn.metrics import MetricFrame, selection_rate, false_positive_rate, demographic_parity_ratio

def _load_data():
    f = st.file_uploader("Upload scored dataset", type="csv")
    if f:
        return pd.read_csv(f)
    return None

def render():
    st.header("⚖️  Fairness / Bias")
    df = _load_data()
    if df is None:
        st.info("Upload scored CSV with y_true, y_pred, sensitive feature.")
        return
    sensitive = st.selectbox("Sensitive feature column", df.columns)
    y_true = st.selectbox("y_true column", df.columns, index=0)
    y_pred = st.selectbox("y_pred column", df.columns, index=1)
    mf = MetricFrame(
        metrics={"selection_rate": selection_rate, "false_positive_rate": false_positive_rate},
        y_true=df[y_true], y_pred=df[y_pred], sensitive_features=df[sensitive],
    )
    st.dataframe(mf.by_group)
    ratio = demographic_parity_ratio(df[y_true], df[y_pred], sensitive_features=df[sensitive])
    st.write(f"Demographic parity ratio: **{ratio:.3f}**")