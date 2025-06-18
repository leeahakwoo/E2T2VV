"""Module 5 – Fairness Analysis (Fairlearn)"""
import streamlit as st
import pandas as pd
from fairlearn.metrics import MetricFrame, selection_rate, false_positive_rate, demographic_parity_ratio

def _load_data():
    f = st.file_uploader("Upload scored dataset (CSV)", type="csv", key="fair_data")
    if f:
        return pd.read_csv(f)
    return None

def render():
    st.header("⚖️  Fairness / Bias Analysis")

    df = _load_data()
    if df is None:
        st.info("Upload a scored CSV with y_true, y_pred, and sensitive columns.")
        return

    sensitive = st.selectbox("Sensitive feature column", df.columns)
    y_true_col = st.selectbox("Ground‑truth label column", df.columns, index=0)
    y_pred_col = st.selectbox("Predicted label column", df.columns, index=1)

    mf = MetricFrame(
        metrics={"selection_rate": selection_rate, "false_positive_rate": false_positive_rate},
        y_true=df[y_true_col],
        y_pred=df[y_pred_col],
        sensitive_features=df[sensitive],
    )

    st.subheader("Group Metrics")
    st.dataframe(mf.by_group)

    ratio = demographic_parity_ratio(
        df[y_true_col], df[y_pred_col], sensitive_features=df[sensitive]
    )
    st.write(f"Demographic parity ratio: **{ratio:.3f}**")