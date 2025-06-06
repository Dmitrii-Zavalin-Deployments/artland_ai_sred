import os
from PIL import Image
from PyPDF2 import PdfMerger

# Define GitHub workspace path (for correct absolute paths)
github_workspace = os.getenv("GITHUB_WORKSPACE", os.getcwd())

# Directories
input_dir = os.path.join(github_workspace, "book_compilation")
output_dir = os.path.join(github_workspace, "book_to_publish")
background_image = os.path.join(input_dir, "background.jpg")
pdf_path = os.path.join(output_dir, "photo_collection.pdf")

# **Fix: Set Introduction.pdf path to the root of the repository**
intro_pdf = os.path.join(github_workspace, "Introduction.pdf")  

# Ensure output folder exists
try:
    os.makedirs(output_dir, exist_ok=True)
    print(f"✅ Output directory '{output_dir}' created or already exists.")
except Exception as e:
    print(f"❌ Error creating output directory '{output_dir}': {e}")
    raise

# Collect all images (excluding background.jpg)
image_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith((".jpg", ".png")) and f != "background.jpg"]

if not image_files:
    print("❌ No images found in 'book_compilation/' (excluding background.jpg). Exiting.")
    exit(1)

print(f"✅ Found {len(image_files)} images to add to PDF.")

# Convert images to a temporary PDF
temp_pdf_path = os.path.join(output_dir, "temp_photo_collection.pdf")
try:
    image_list = [Image.open(img).convert("RGB") for img in image_files]
    image_list[0].save(temp_pdf_path, save_all=True, append_images=image_list[1:])
    print(f"✅ Temporary image-based PDF created: {temp_pdf_path}")
except Exception as e:
    print(f"❌ Error generating temporary PDF file: {e}")
    raise

# Merge Introduction.pdf with the generated image-based PDF
try:
    merger = PdfMerger()
    
    if os.path.exists(intro_pdf):
        merger.append(intro_pdf)
        print(f"✅ Introduction PDF '{intro_pdf}' added as first page.")
    else:
        print(f"❌ Introduction PDF '{intro_pdf}' not found! Make sure it's in the repository root.")

    merger.append(temp_pdf_path)
    merger.write(pdf_path)
    merger.close()
    
    print(f"✅ Final merged PDF created: {pdf_path}")
except Exception as e:
    print(f"❌ Error merging PDFs: {e}")
    raise

# Copy background.jpg to book_to_publish
if os.path.exists(background_image):
    background_dest = os.path.join(output_dir, "background.jpg")
    try:
        Image.open(background_image).save(background_dest)
        print(f"✅ Background image copied to '{background_dest}'")
    except Exception as e:
        print(f"❌ Error copying background.jpg: {e}")
else:
    print(f"❌ Background image '{background_image}' not found!")

print("✅ Photo collection PDF with Introduction.pdf successfully saved in 'book_to_publish/'")



