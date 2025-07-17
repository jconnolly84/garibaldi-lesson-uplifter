
# template_builder.py
from pptx import Presentation
from pptx.util import Inches, Pt
import requests
from io import BytesIO

def insert_images_into_template(uplifted_lesson):
    prs = Presentation()
    for block in uplifted_lesson.split("---"):
        lines = block.strip().split("\n")
        if not lines or len(lines) < 2:
            continue
        slide_title = lines[0].replace("###", "").strip()
        content = "\n".join(lines[1:])

        slide_layout = prs.slide_layouts[1]  # Title and Content layout
        slide = prs.slides.add_slide(slide_layout)
        slide.shapes.title.text = slide_title
        slide.placeholders[1].text = content

    return prs
