import os
from google.cloud import vision
import io

def clean_text(text):
    """Removes extra blank lines and trailing spaces."""
    lines = text.split('\n')
    cleaned_lines = [line.strip() for line in lines if line.strip()]
    return '\n'.join(cleaned_lines)

def detect_text(image_path, output_dir):
    """Detects text in the file and saves it to a txt file."""
    client = vision.ImageAnnotatorClient()

    try:
        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()
    except FileNotFoundError:
        print(f"Error: File not found {image_path}")
        return
    except Exception as e:
        print(f"Error reading {image_path}: {e}")
        return

    image = vision.Image(content=content)

    print(f"Processing: {image_path}")
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if response.error.message:
        print(f"Error from Vision API: {response.error.message}")
        return

    if texts:
        # The first element contains the entire text block
        extracted_text = texts[0].description
        cleaned_text = clean_text(extracted_text)

        # Determine output file path
        filename = os.path.basename(image_path)
        name, _ = os.path.splitext(filename)
        output_filename = f"{name}.txt"
        output_path = os.path.join(output_dir, output_filename)

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_text)

        print(f"Saved text to: {output_path}")
    else:
        print(f"No text found in: {image_path}")

def process_path(input_path, output_dir):
    """Processes a single file or a directory of files."""
    if os.path.isfile(input_path):
        detect_text(input_path, output_dir)
    elif os.path.isdir(input_path):
        valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff')
        for root, _, files in os.walk(input_path):
            for file in files:
                if file.lower().endswith(valid_extensions):
                    file_path = os.path.join(root, file)
                    detect_text(file_path, output_dir)
    else:
        print(f"Invalid path: {input_path}")

def main():
    input_path = input("Enter the path to a picture or a folder containing pictures: ").strip()
    # Strip quotes if the user drag-and-dropped the folder/file
    input_path = input_path.strip('\'"')

    output_path = input("Enter the path to save the completed .txt files: ").strip()
    output_path = output_path.strip('\'"')

    process_path(input_path, output_path)
    print("Extraction complete.")

if __name__ == '__main__':
    main()
