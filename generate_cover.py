import json
import pdfkit
import os
from PIL import Image, ImageDraw, ImageFont

# Load magazine data from config.json
with open("config.json", "r") as file:
    config = json.load(file)

# Ensure output folder exists
output_dir = "book_to_publish"
os.makedirs(output_dir, exist_ok=True)

# Read HTML template
with open("cover_template.html", "r") as file:
    html_template = file.read()

# SAFE placeholder replacement (avoids KeyError)
html_content = html_template.replace("{TITLE}", config.get("title", ""))
html_content = html_content.replace("{ISSUE}", config.get("issue", ""))
html_content = html_content.replace("{TAGLINE}", config.get("tagline", ""))
html_content = html_content.replace("{SUBTITLE}", config.get("subtitle", ""))
html_content = html_content.replace("{AUTHOR}", config.get("author", ""))

# Save modified HTML
temp_html_path = os.path.join(output_dir, "temp_cover.html")
with open(temp_html_path, "w") as file:
    file.write(html_content)

# Configure wkhtmltopdf
config_pdf = pdfkit.configuration(wkhtmltopdf="/usr/bin/wkhtmltopdf")  # Adjust path if needed
options = {
    'enable-local-file-access': None  # Prevent network errors
}

# Generate PDF from HTML using wkhtmltopdf
pdf_path = os.path.join(output_dir, "magazine_cover.pdf")
pdfkit.from_file(os.path.abspath(temp_html_path), os.path.abspath(pdf_path), options=options, configuration=config_pdf)

# Generate JPG using Pillow
background = Image.open("book_compilation/background.jpg")
draw = ImageDraw.Draw(background)

# Load fonts (ensure they exist in the project)
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



