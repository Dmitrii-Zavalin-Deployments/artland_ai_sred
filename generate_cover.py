import json
import pdfkit
import os
from selenium import webdriver
from PIL import Image

# Load magazine data from config.json
with open("config.json", "r") as file:
    config = json.load(file)

# Ensure output folder exists
output_dir = "book_to_publish"
os.makedirs(output_dir, exist_ok=True)

# Generate HTML content dynamically
html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Magazine Cover</title>
    <style>
        body {{
            background: url("book_compilation/background.jpg") no-repeat center center fixed;
            background-size: cover;
            font-family: Arial, sans-serif;
            color: white;
            text-align: center;
            padding: 50px;
        }}
        .container {{
            width: 100%;
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}
        .title {{ font-size: 50px; font-weight: bold; text-transform: uppercase; }}
        .issue {{ font-size: 25px; margin-top: 10px; }}
        .tagline {{ font-size: 20px; font-style: italic; margin-top: 15px; }}
        .subtitle {{ font-size: 18px; margin-top: 10px; opacity: 0.8; }}
        .author {{ font-size: 18px; margin-top: 20px; opacity: 0.7; font-style: italic; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="title">{config["title"]}</div>
        <div class="issue">{config["issue"]}</div>
        <div class="tagline">{config["tagline"]}</div>
        <div class="subtitle">{config["subtitle"]}</div>
        <div class="author">{config["author"]}</div>
    </div>
</body>
</html>
"""

# Save the HTML file
html_path = os.path.join(output_dir, "magazine_cover.html")
with open(html_path, "w") as file:
    file.write(html_content)

# Convert HTML to PDF using wkhtmltopdf
pdf_path = os.path.join(output_dir, "magazine_cover.pdf")
config_pdf = pdfkit.configuration(wkhtmltopdf="/usr/bin/wkhtmltopdf")
options = {"enable-local-file-access": None}
pdfkit.from_file(html_path, pdf_path, options=options, configuration=config_pdf)

# Convert HTML to JPG using Selenium (Headless Browser)
jpg_path = os.path.join(output_dir, "magazine_cover.jpg")

options = webdriver.FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.get(f"file://{html_path}")
driver.save_screenshot(jpg_path)
driver.quit()

print(f"✅ Magazine cover successfully generated:")
print(f"   - HTML: {html_path}")
print(f"   - PDF: {pdf_path}")
print(f"   - JPG: {jpg_path}")



