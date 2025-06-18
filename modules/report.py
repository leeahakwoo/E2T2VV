"""Module 6 – Model Card HTML download"""
import streamlit as st
from model_card_toolkit import ModelCard, ModelCardToolkit
import tempfile
from pathlib import Path

def render():
    st.header("📄 Export Model Card (HTML)")
    name = st.text_input("Model name", "Demo Model")
    overview = st.text_area("Overview", "This model ...")

    if st.button("Generate & Download HTML"):
        mct = ModelCardToolkit()
        card = ModelCard()
        card.model_details.name = name
        card.model_details.overview = overview
        assets_path = mct.scaffold_assets()
        mct.update_model_card(card)
        html_file = assets_path / "model_card.html"
        st.success("Model card generated!")
        st.download_button("Download HTML", data=open(html_file,"rb"), file_name="model_card.html")