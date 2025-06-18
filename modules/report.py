"""Module 4 – Generate Model Card PDF"""
import streamlit as st
from model_card_toolkit import ModelCard, ModelCardToolkit
import tempfile
from pathlib import Path
import subprocess

def render():
    st.header("📄 Export Model Card")

    name = st.text_input("Model name", "Demo Model")
    overview = st.text_area("Overview", "This model ...")

    if st.button("Generate & Download PDF"):
        mct = ModelCardToolkit()
        mc = ModelCard()
        mc.model_details.name = name
        mc.model_details.overview = overview

        tmp = Path(tempfile.mkdtemp())
        mct.update_model_card(mc)
        html_path = mct.scaffold_assets() / "model_card.html"
        pdf_path = tmp / "model_card.pdf"
        subprocess.run(["weasyprint", str(html_path), str(pdf_path)], check=False)

        st.success("Model card generated!")
        st.download_button(
            label="Download PDF", data=open(pdf_path, "rb"), file_name="model_card.pdf"
        )