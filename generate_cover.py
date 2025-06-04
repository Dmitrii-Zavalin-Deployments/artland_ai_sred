import json
import pdfkit
import os
from PIL import Image, ImageDraw, ImageFont

# Load magazine data from config.json
with open("config.json", "r") as file:
    config = json.load(file)

# Ensure the output directory exists
output_dir = "book_to_publish"
os.makedirs(output_dir, exist_ok=True)

# Read HTML template
with open("cover_template.html", "r") as file:
    html_template = file.read()

# Replace placeholders with actual content
html_content = html_template.format(
    TITLE=config["title"],
    ISSUE=config["issue"],
    TAGLINE=config["tagline"],
    SUBTITLE=config["subtitle"],
    AUTHOR=config["author"]
)

# Save modified HTML
temp_html_path = os.path.join(output_dir, "temp_cover.html")
with open(temp_html_path, "w") as file:
    file.write(html_content)

# Generate PDF from HTML using wkhtmltopdf (MIT-licensed)
pdf_path = os.path.join(output_dir, "magazine_cover.pdf")
pdfkit.from_file(temp_html_path, pdf_path)

# Generate JPG using Pillow
background = Image.open("book_compilation/background.jpg")
draw = ImageDraw.Draw(background)

# Load fonts (ensure free fonts exist in project)
font_title = ImageFont.truetype("arial.ttf", 60)
font_subtitle = ImageFont.truetype("arial.ttf", 30)

# Draw Text
draw.text((50, 50), config["title"], font=font_title, fill="white")
draw.text((50, 130), config["issue"], font=font_subtitle, fill="white")
draw.text((50, 180), config["tagline"], font=font_subtitle, fill="white")
draw.text((50, 230), config["subtitle"], font=font_subtitle, fill="white")
draw.text((50, 280), config["author"], font=font_subtitle, fill="white")  # Author field

# Save final image in book_to_publish folder
jpg_path = os.path.join(output_dir, "magazine_cover.jpg")
background.save(jpg_path)

print(f"✅ Magazine cover successfully generated in '{output_dir}/':")
print(f"   - PDF: {pdf_path}")
print(f"   - JPG: {jpg_path}")



