import streamlit as st

from modules import (
    data_profile,
    expectations,
    model_eval,
    fairness,
    explainability,
    robustness,
    report,
)

PAGES = {
    "1️⃣  Data Profile": data_profile.render,
    "2️⃣  Expectations": expectations.render,
    "3️⃣  Model Eval": model_eval.render,
    "4️⃣  Fairness": fairness.render,
    "5️⃣  Explainability": explainability.render,
    "6️⃣  Robustness": robustness.render,
    "7️⃣  Export Report": report.render,
}

def main():
    st.set_page_config(page_title="ETVV + TEVV QA Tool", layout="wide")
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Select module", list(PAGES.keys()))
    PAGES[choice]()

if __name__ == "__main__":
    main()