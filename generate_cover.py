import json
import pdfkit
import os
import subprocess

# Define GitHub workspace path (for correct absolute paths)
github_workspace = os.getenv("GITHUB_WORKSPACE", os.getcwd())

# Load magazine data from config.json
config_path = os.path.join(github_workspace, "config.json")
try:
    with open(config_path, "r") as file:
        config = json.load(file)
    print(f"✅ Loaded config.json successfully from {config_path}.")
except Exception as e:
    print(f"❌ Error loading config.json: {e}")
    raise

# Ensure output folder exists
output_dir = os.path.join(github_workspace, "book_to_publish")
try:
    os.makedirs(output_dir, exist_ok=True)
    print(f"✅ Output directory '{output_dir}' created or already exists.")
except Exception as e:
    print(f"❌ Error creating output directory '{output_dir}': {e}")
    raise

# Ensure background image exists
background_path = os.path.join(github_workspace, "book_compilation", "background.jpg")
if not os.path.exists(background_path):
    print(f"❌ Background image not found at {background_path}. Using fallback color.")
else:
    print(f"✅ Background image found at {background_path}.")

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
            background: url("file://{background_path}") no-repeat center center fixed;
            background-size: cover;
            background-color: skyblue; /* Fallback background */
            font-family: Arial, sans-serif;
            color: white;
            text-align: center;
            margin: 0;
            width: 100vw;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .container {{
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }}
        .title {{ font-size: 60px; font-weight: bold; text-transform: uppercase; }}
        .issue {{ font-size: 30px; margin-top: 15px; }}
        .tagline {{ font-size: 25px; font-style: italic; margin-top: 20px; }}
        .subtitle {{ font-size: 22px; margin-top: 15px; }}
        .author {{ font-size: 22px; margin-top: 25px; font-style: italic; }}
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
try:
    with open(html_path, "w") as file:
        file.write(html_content)
    print(f"✅ HTML file saved at {html_path}")
except Exception as e:
    print(f"❌ Error saving HTML file: {e}")
    raise

# Convert HTML to PDF using wkhtmltopdf (forcing full rendering)
pdf_path = os.path.join(output_dir, "magazine_cover.pdf")
try:
    config_pdf = pdfkit.configuration(wkhtmltopdf="/usr/bin/wkhtmltopdf")
    options = {
        "enable-local-file-access": None,
        "javascript-delay": "2000",  # Ensures full rendering before conversion
        "no-stop-slow-scripts": None
    }
    pdfkit.from_file(html_path, pdf_path, options=options, configuration=config_pdf)
    print(f"✅ PDF file generated at {pdf_path}")
except Exception as e:
    print(f"❌ Error generating PDF file: {e}")
    raise

# Convert PDF to JPG using ImageMagick
jpg_path = os.path.join(output_dir, "magazine_cover.jpg")
try:
    subprocess.run(["convert", "-density", "300", pdf_path, "-quality", "90", jpg_path])
    print(f"✅ JPG file generated at {jpg_path}")
except Exception as e:
    print(f"❌ Error generating JPG file: {e}")
    raise

print(f"✅ Magazine cover successfully generated:")
print(f"   - HTML: {html_path}")
print(f"   - PDF: {pdf_path}")
print(f"   - JPG: {jpg_path}")



