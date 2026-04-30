# Handwriting OCR Script

This repository contains a Python script that utilizes Microsoft's TrOCR (Transformer-based Optical Character Recognition) to extract cursive handwritten text from images.

## Prerequisites

1.  **Python 3.7+**

## Installation

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Extract Cursive Text from Images (`extract_text.py`)

This script uses the Hugging Face `transformers` library with the `microsoft/trocr-base-handwritten` model to read cursive handwritten text from images and save the outputs as `.txt` files.

**How to run:**
```bash
python extract_text.py
```

You will be prompted to:
1.  Enter the path to a single image file or a folder containing images.
2.  Enter the destination folder where the `.txt` files should be saved.

The script processes common image formats (like `.jpg`, `.jpeg`, `.png`) and creates text files with the same name as the original image (e.g., `image1.jpeg` becomes `image1.txt`). Note that the model is loaded on the first run, which may take a few moments depending on your network connection.
