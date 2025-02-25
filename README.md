

# Image Watermarking Tool

A Flask-based web application to embed and extract invisible watermarks in images using the Least Significant Bit (LSB) technique.

**Repository Link**: [https://github.com/MuhammadWaseem29/Image-Watermarking-Tool](https://github.com/MuhammadWaseem29/Image-Watermarking-Tool)

## Overview

This project allows users to upload an image and embed a text-based watermark into the image's pixel data. The watermark is invisible to the naked eye but can be extracted programmatically to prove its existence. The tool is built using Python, Flask, and the Pillow library for image processing.

## Features

- **Embed Watermark**: Hide a text watermark in the LSB of an image's pixel data.
- **Extract Watermark**: Extract the hidden watermark from the image to verify its presence.
- **User-Friendly Interface**: A simple web interface for uploading images, adding watermarks, and downloading the watermarked image.
- **Dynamic Preview**: Preview the watermarked image and verify the extracted watermark.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/MuhammadWaseem29/Image-Watermarking-Tool.git
   cd Image-Watermarking-Tool
   ```

2. **Set Up a Virtual Environment** (Optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   python app.py
   ```

5. **Access the Application**:
   Open your browser and go to `http://127.0.0.1:5000/`.

## Usage

1. **Upload an Image**: Use the file upload button to select an image from your device.
2. **Enter Watermark Text**: Type the text you want to embed as a watermark.
3. **Add Watermark**: Click the "Add Watermark" button to process the image.
4. **Preview and Download**: The watermarked image will be displayed along with the extracted watermark for verification. You can download the watermarked image using the "Download Image" button.

## Project Structure

```
Image-Watermarking-Tool/
├── static/                  # Folder for storing uploaded and watermarked images
├── app.py                   # Main Flask application
├── README.md                # Project documentation
├── requirements.txt         # List of dependencies
├── .gitignore               # Files to ignore in Git
```

## Dependencies

- Flask
- Pillow (PIL)
- NumPy

Install all dependencies using:
```bash
pip install -r requirements.txt
```

## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

