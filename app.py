
import streamlit as st
from pptx import Presentation
import openai
from PIL import Image
import io

# Set OpenAI API key from secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- Extract slide text ---
def extract_text_from_pptx(file):
    prs = Presentation(file)
    content = []
    for i, slide in enumerate(prs.slides):
        slide_text = f"Slide {i+1}:\n"
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                slide_text += shape.text + "\n"
        content.append(slide_text.strip())
    return "\n\n".join(content)

# --- Build prompt ---
def build_prompt(slide_text):
    prompt = f"""
You are an expert teacher and lesson designer. A teacher has uploaded a PowerPoint lesson.

Please analyse and rebuild the lesson using the following structure:
1. Ready to Learn / Entry
2. Connect & Recall
3. Explore / Impart Knowledge
4. Collaborate / Facilitate
5. Independent Practice (FIT)
6. Review & Improve
7. Exit & ILT

Your task:
- Reorder content into that structure
- Suggest new slides where needed (title + content)
- Improve clarity, challenge, and engagement
- Recommend relevant images or diagrams for each slide
- Embed TLC strategies: retrieval practice, desirable difficulty, cold calling, red pen reflection, the Learning Pit, etc.

Here is the raw content:

{slide_text}

Return the uplifted slide-by-slide version, labelled with headers like:
--- Slide 1: Ready to Learn ---
[Slide title, content, image suggestion, strategy used]
"""
    return prompt

# --- Call GPT ---
def call_chatgpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    return response['choices'][0]['message']['content']

# --- Streamlit UI ---
st.set_page_config(page_title="Lessonary Uplifter", layout="centered")

col1, col2 = st.columns([1, 4])
with col1:
    st.image("LOGO_Lessonary.png", width=100)
with col2:
    st.title("Lessonary Uplifter")
    st.write("📚 Upload a PowerPoint and get it automatically restructured using our T&L model.")

uploaded_file = st.file_uploader("Upload a .pptx file", type="pptx")

if uploaded_file is not None:
    with st.spinner("Extracting slide text and analysing..."):
        slide_text = extract_text_from_pptx(uploaded_file)
        prompt = build_prompt(slide_text)
        uplifted_lesson = call_chatgpt(prompt)

    st.success("✅ Lesson uplift complete!")
    st.subheader("🔍 Uplifted Lesson Structure")
    st.text_area("Slide-by-slide output:", uplifted_lesson, height=600)

    st.download_button(
        label="📥 Download as text file",
        data=uplifted_lesson,
        file_name="Lessonary_Uplifted_Lesson.txt",
        mime="text/plain"
    )
