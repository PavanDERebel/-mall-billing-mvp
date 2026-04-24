import os
import json
import pandas as pd
import google.generativeai as genai
from PIL import Image

def configure_gemini():
    """Configures the Gemini API using the environment variable."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        print("Please set it using: export GEMINI_API_KEY='your_api_key'")
        return False
    genai.configure(api_key=api_key)
    return True

def analyze_with_gemini(image_path, text_content):
    """Uses Gemini to compare the image and text, finding spelling mistakes."""
    try:
        # Load the image
        img = Image.open(image_path)
    except Exception as e:
        print(f"Error loading image {image_path}: {e}")
        return []

    # Choose a multimodal model
    model = genai.GenerativeModel('gemini-1.5-flash')

    prompt = f"""
    You are an expert OCR proofreader. I am providing you with an image of text, and the corresponding text that was extracted from it via OCR.

    Your task is to compare the extracted text against the original image and identify ONLY spelling mistakes or OCR reading errors.

    Here is the extracted text:
    ---
    {text_content}
    ---

    Please return the result as a JSON array of objects. Each object must have the following keys:
    "line": the approximate line number in the extracted text where the mistake occurred (integer).
    "correct_word": the word as it actually appears in the image.
    "incorrect_word": the word as it incorrectly appears in the extracted text.

    If there are no mistakes, return an empty JSON array: []

    IMPORTANT: Respond ONLY with the raw JSON array. Do not include markdown formatting like ```json or ```.
    """

    try:
        response = model.generate_content([prompt, img])
        response_text = response.text.strip()

        # Clean up the response in case the model includes markdown formatting
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]

        response_text = response_text.strip()

        try:
            mistakes = json.loads(response_text)
            return mistakes
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from Gemini response: {e}")
            print(f"Raw response: {response_text}")
            return []

    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return []

def process_folders(images_dir, texts_dir, output_excel_path):
    """Matches images and texts, processes them, and saves to Excel."""
    if not os.path.isdir(images_dir):
        print(f"Error: Images directory not found: {images_dir}")
        return
    if not os.path.isdir(texts_dir):
        print(f"Error: Texts directory not found: {texts_dir}")
        return

    all_logs = []
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff')

    for image_filename in os.listdir(images_dir):
        if image_filename.lower().endswith(valid_extensions):
            name, _ = os.path.splitext(image_filename)
            text_filename = f"{name}.txt"

            image_path = os.path.join(images_dir, image_filename)
            text_path = os.path.join(texts_dir, text_filename)

            if os.path.exists(text_path):
                print(f"Analyzing pair: {image_filename} & {text_filename}")

                try:
                    with open(text_path, 'r', encoding='utf-8') as f:
                        text_content = f.read()
                except Exception as e:
                    print(f"Error reading {text_path}: {e}")
                    continue

                mistakes = analyze_with_gemini(image_path, text_content)

                if mistakes:
                    for mistake in mistakes:
                        all_logs.append({
                            "File name": image_filename,
                            "Line number": mistake.get("line", "N/A"),
                            "Correct word": mistake.get("correct_word", ""),
                            "Incorrect word": mistake.get("incorrect_word", "")
                        })
                    print(f"  Found {len(mistakes)} mistake(s).")
                else:
                    print("  No mistakes found.")
            else:
                print(f"Warning: No corresponding text file found for {image_filename}")

    if all_logs:
        df = pd.DataFrame(all_logs)
        try:
            df.to_excel(output_excel_path, index=False)
            print(f"\nSuccessfully saved spelling mistake logs to: {output_excel_path}")
        except Exception as e:
            print(f"Error saving to Excel: {e}")
    else:
        print("\nNo spelling mistakes were found in any of the processed files.")
        # Create an empty excel file with headers anyway
        df = pd.DataFrame(columns=["File name", "Line number", "Correct word", "Incorrect word"])
        try:
            df.to_excel(output_excel_path, index=False)
            print(f"Created empty log file at: {output_excel_path}")
        except Exception as e:
             pass

def main():
    if not configure_gemini():
        return

    images_dir = input("Enter the path to the folder containing the original pictures: ").strip()
    images_dir = images_dir.strip('\'"')

    texts_dir = input("Enter the path to the folder containing the extracted .txt files: ").strip()
    texts_dir = texts_dir.strip('\'"')

    output_excel = input("Enter the path and filename to save the log file (e.g., C:/logs/spelling_mistakes.xlsx): ").strip()
    output_excel = output_excel.strip('\'"')

    if not output_excel.endswith('.xlsx'):
        output_excel += '.xlsx'

    # Ensure output directory exists if a path is provided
    output_dir = os.path.dirname(output_excel)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    process_folders(images_dir, texts_dir, output_excel)

if __name__ == '__main__':
    main()
