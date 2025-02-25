from flask import Flask, request, send_file, render_template_string, url_for
from PIL import Image
import numpy as np
import os

app = Flask(__name__)

# Ensure a static folder exists for serving images
STATIC_FOLDER = 'static'
if not os.path.exists(STATIC_FOLDER):
    os.makedirs(STATIC_FOLDER)
app.config['STATIC_FOLDER'] = STATIC_FOLDER

# Embed undetectable watermark in LSB
def embed_watermark(image_path, watermark_text, output_path):
    img = Image.open(image_path).convert('RGBA')
    img_array = np.array(img)

    watermark_bits = ''.join(format(ord(char), '08b') for char in watermark_text)
    watermark_length = len(watermark_bits)
    max_capacity = img_array.size // 4  # One bit per RGBA channel

    if watermark_length > max_capacity:
        raise ValueError("Watermark too large for this image.")

    flat_array = img_array.flatten()
    bit_index = 0

    for i in range(len(flat_array)):
        if bit_index >= watermark_length:
            break
        flat_array[i] = (flat_array[i] & 0xFE) | int(watermark_bits[bit_index])
        bit_index += 1

    watermarked_array = flat_array.reshape(img_array.shape)
    watermarked_img = Image.fromarray(watermarked_array.astype(np.uint8))
    watermarked_img.save(output_path, 'PNG')
    return watermark_length  # For extraction

# Extract watermark to prove it’s there
def extract_watermark(image_path, watermark_length):
    img = Image.open(image_path).convert('RGBA')
    img_array = np.array(img).flatten()

    extracted_bits = ''
    for i in range(watermark_length):
        extracted_bits += str(img_array[i] & 1)

    watermark_text = ''
    for i in range(0, len(extracted_bits), 8):
        byte = extracted_bits[i:i+8]
        watermark_text += chr(int(byte, 2))
    
    return watermark_text

# HTML template with preview and proof
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Watermarker</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
        .container { max-width: 800px; margin: auto; }
        input[type="file"], input[type="text"], button { margin: 10px; padding: 8px; }
        button { background-color: #4CAF50; color: white; border: none; cursor: pointer; }
        button:hover { background-color: #45a049; }
        img { max-width: 100%; height: auto; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Image Watermarker</h1>
        <form method="POST" enctype="multipart/form-data" action="/">
            <input type="file" name="image" accept="image/*" required><br>
            <input type="text" name="watermark" placeholder="Enter watermark text" required><br>
            <button type="submit">Add Watermark</button>
        </form>
        {% if preview_url %}
            <h3>Watermark Added!</h3>
            <p>Embedded Watermark: "{{ watermark_text }}"</p>
            <p>Extracted Watermark: "{{ extracted_text }}"</p>
            <p>(The watermark is hidden in the image’s pixel data and not visible)</p>
            <img src="{{ preview_url }}" alt="Watermarked Image">
            <br>
            <a href="{{ download_link }}" download="watermarked_image.png">
                <button>Download Image</button>
            </a>
        {% endif %}
        {% if error %}
            <p style="color: red;">{{ error }}</p>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            if 'image' not in request.files:
                return render_template_string(HTML_TEMPLATE, error="No image uploaded.")
            image = request.files['image']
            if image.filename == '':
                return render_template_string(HTML_TEMPLATE, error="No image selected.")

            watermark_text = request.form.get('watermark')
            if not watermark_text:
                return render_template_string(HTML_TEMPLATE, error="Watermark text is required.")

            upload_path = os.path.join(app.config['STATIC_FOLDER'], 'uploaded_image.jpg')
            image.save(upload_path)

            output_path = os.path.join(app.config['STATIC_FOLDER'], 'watermarked_image.png')
            watermark_length = embed_watermark(upload_path, watermark_text, output_path)

            # Extract to prove it’s there
            extracted_text = extract_watermark(output_path, watermark_length)

            os.remove(upload_path)

            preview_url = url_for('static', filename='watermarked_image.png')
            download_link = url_for('download_file', filename='watermarked_image.png')

            return render_template_string(HTML_TEMPLATE, 
                                        preview_url=preview_url,
                                        download_link=download_link,
                                        watermark_text=watermark_text,
                                        extracted_text=extracted_text)
        except Exception as e:
            return render_template_string(HTML_TEMPLATE, error=str(e))

    return render_template_string(HTML_TEMPLATE)

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['STATIC_FOLDER'], filename), 
                    as_attachment=True, 
                    download_name='watermarked_image.png')

if __name__ == '__main__':
    app.run(debug=True)
