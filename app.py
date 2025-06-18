import streamlit as st

from modules import (
    data_profile,
    expectations,
    model_eval,
    fairness,
    explainability,
    report,
)

PAGES = {
    "1️⃣  Data Profile": data_profile.render,
    "2️⃣  Model Eval": model_eval.render,
    "3️⃣  Fairness": fairness.render,
    "4️⃣  Explainability": explainability.render,
}

def main():
    st.set_page_config(page_title="ETVV + TEVV QA Tool (Light)", layout="wide")
    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Select module", list(PAGES.keys()))
    PAGES[choice]()

if __name__ == "__main__":
    main()
