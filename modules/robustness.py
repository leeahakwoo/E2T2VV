"""Module 7 – Robustness Testing (ART)"""
import streamlit as st
import pandas as pd
import pickle
from art.estimators.classification import SklearnClassifier
from art.attacks.evasion import FastGradientMethod
from sklearn.metrics import accuracy_score

def render():
    st.header("🛡️  Robustness / Adversarial FGSM Attack")

    model_file = st.file_uploader("Upload pickled sklearn model", type=["pkl", "pickle"], key="art_model")
    data_file = st.file_uploader("Upload test data (CSV)", type="csv", key="art_data")
    target_col = st.text_input("Target column", "target")

    if model_file is None or data_file is None:
        st.info("Upload model and data.")
        return

    model = pickle.load(model_file)
    df = pd.read_csv(data_file)
    X = df.drop(columns=[target_col]).values
    y = df[target_col].values

    classifier = SklearnClassifier(model=model)
    preds_clean = model.predict(X)
    acc_clean = accuracy_score(y, preds_clean)

    attack = FastGradientMethod(estimator=classifier, eps=0.2)
    X_adv = attack.generate(X)
    preds_adv = model.predict(X_adv)
    acc_adv = accuracy_score(y, preds_adv)

    st.write(f"Accuracy on clean data: **{acc_clean:.3f}**")
    st.write(f"Accuracy on adversarial data: **{acc_adv:.3f}**")