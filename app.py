# app.py
import streamlit as st
from datetime import datetime
import tempfile
import os
from template_builder import insert_images_into_template, extract_text_from_pptx, build_prompt, call_chatgpt

# --- App Setup ---
st.set_page_config(page_title="Lessonary Uplifter", layout="centered")

st.image("LOGO_Lessonary.png", use_container_width=True)
st.title("📚 Lessonary PowerPoint Uplifter")
st.write("Welcome! Upload a PowerPoint (.pptx) file to automatically restructure and enrich it using your school's T&L model and embedded TLC strategies.")

# --- Dropdown for AI Boost ---
enrichment_level = st.selectbox("Optional AI Boost: Enrichment Level", ["Base", "Enhanced", "Max"], index=0)

# --- Upload UI ---
uploaded_file = st.file_uploader("Upload a .pptx file", type=["pptx"])

# --- Processing Logic ---
if uploaded_file is not None:
    uploaded_filename = uploaded_file.name.replace(".pptx", "")
    upload_date = datetime.now().strftime("%Y%m%d")
    output_filename = f"{uploaded_filename}_uplifted_{upload_date}.pptx"

    with st.spinner("🔍 Analysing your slides and enriching your lesson..."):
        slide_text = extract_text_from_pptx(uploaded_file)
        prompt = build_prompt(slide_text, enrichment_level=enrichment_level)
        uplifted_lesson = call_chatgpt(prompt)

    # Show text preview
    st.success("✅ Lesson uplift complete!")
    st.subheader("📋 Uplifted Lesson Structure")
    st.text_area("Slide-by-slide output:", uplifted_lesson, height=600)

    # Text download button
    st.download_button(
        label="📥 Download as text file",
        data=uplifted_lesson,
        file_name="Lessonary_Uplifted_Lesson.txt",
        mime="text/plain"
    )

    # PPTX download button
    if st.button("📤 Download as PPTX with AI Images & Videos"):
        pptx_output = insert_images_into_template(uplifted_lesson)
        tmp_pptx = tempfile.NamedTemporaryFile(delete=False, suffix=".pptx")
        pptx_output.save(tmp_pptx.name)
        tmp_pptx.close()
        with open(tmp_pptx.name, "rb") as f:
            st.download_button(
                label="📥 Download PowerPoint File",
                data=f,
                file_name=output_filename,
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )
        os.unlink(tmp_pptx.name)
