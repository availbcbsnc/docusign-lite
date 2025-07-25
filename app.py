from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
import io
import os
import base64
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
SIGNED_FOLDER = 'signed'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SIGNED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['pdf']
    signature_data = request.form['signature']

    if file and file.filename.endswith('.pdf') and signature_data:
        # Save uploaded PDF
        pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(pdf_path)

        # Convert base64 PNG signature to PIL Image
        header, encoded = signature_data.split(',', 1)
        signature_bytes = base64.b64decode(encoded)
        signature_img = Image.open(io.BytesIO(signature_bytes)).convert("RGBA")

        # Overlay signature and save new PDF
        signed_pdf = overlay_signature(pdf_path, signature_img)
        return send_file(signed_pdf, as_attachment=True, download_name='signed_' + file.filename)

    return 'Invalid request'

def overlay_signature(pdf_path, signature_img):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    # Create signature overlay PDF
    sig_overlay = io.BytesIO()
    c = canvas.Canvas(sig_overlay, pagesize=letter)
    sig_img_io = io.BytesIO()
    signature_img.save(sig_img_io, format='PNG')
    sig_img_io.seek(0)

    # Position signature at bottom-right corner
    c.drawImage(ImageReader(sig_img_io), x=400, y=50, width=150, height=50, mask='auto')
    c.save()
    sig_overlay.seek(0)

    # Merge signature overlay onto first page
    sig_page = PdfReader(sig_overlay).pages[0]
    first_page = reader.pages[0]
    first_page.merge_page(sig_page)

    writer.add_page(first_page)
    for page in reader.pages[1:]:
        writer.add_page(page)

    signed_path = os.path.join(SIGNED_FOLDER, 'signed_output.pdf')
    with open(signed_path, 'wb') as f:
        writer.write(f)

    return signed_path

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
