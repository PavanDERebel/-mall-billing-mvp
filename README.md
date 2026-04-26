# OCR and Spell Checking Scripts

This repository contains two Python scripts to help extract text from images and check for spelling mistakes in the extracted text using AI.

## Prerequisites

1.  **Python 3.7+**
2.  **Google Cloud SDK**: You need to have the Google Cloud SDK installed and authenticated locally. The script `extract_text.py` uses your local default credentials.
    *   To authenticate, run: `gcloud auth application-default login`
    *   Ensure your Google Cloud project has the Cloud Vision API enabled.
3.  **Gemini API Key**: You need an API key for Google Gemini to run `check_spelling.py`.
    *   Set the environment variable `GEMINI_API_KEY` to your API key.
    *   Linux/macOS: `export GEMINI_API_KEY="your_api_key_here"`
    *   Windows: `set GEMINI_API_KEY=your_api_key_here`

## Installation

Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### 1. Extract Text from Images (`extract_text.py`)

This script uses the Google Cloud Vision API to read text from images and save them as `.txt` files.

**How to run:**
```bash
python extract_text.py
```

You will be prompted to:
1.  Enter the path to a single image file or a folder containing images.
2.  Enter the destination folder where the `.txt` files should be saved.

The script processes all common image formats and creates text files with the same name as the original image (e.g., `image1.jpeg` becomes `image1.txt`). It removes extra blank lines from the Google Cloud Vision output.

### 2. Check Spelling (`check_spelling.py`)

This script uses the Gemini API to compare the original image with the extracted text file. It identifies spelling mistakes and generates an Excel report.

### 3. Correct Scrambled Text (`replacer.py`)

This script uses the Gemini 2.5 Pro API to correct scrambled text extracted by Cloud Vision. It compares the original JPEG images with the scrambled text files and generates perfect, line-by-line corrected copies named `*_updated.txt`.

**How to run:**
```bash
python replacer.py
```
*Note: Ensure you are authenticated with Application Default Credentials (ADC) via `gcloud auth application-default login` as it uses the modern `google-genai` SDK.*

The script looks for matching `.jpeg` or `.jpg` files and `.txt` files in the folder specified within the script (look for `# folder path for pictures, text files`). It generates corrected copies like `1301_updated.txt` for an image `1301.jpeg` and its text `1301.txt`.

**How to run:**
```bash
python check_spelling.py
```

You will be prompted to:
1.  Enter the folder containing the original images.
2.  Enter the folder containing the generated `.txt` files.
3.  Enter the output path for the Excel log file (e.g., `spelling_log.xlsx`).

The generated Excel file will contain the following columns:
*   File name
*   Line number
*   Correct word
*   Incorrect word
