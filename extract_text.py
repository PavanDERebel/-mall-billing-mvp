import os
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image

def detect_text(image_path, output_dir, processor, model):
    """Detects cursive handwritten text in the file and saves it to a txt file."""
    try:
        # Load image and convert to RGB
        image = Image.open(image_path).convert("RGB")
    except FileNotFoundError:
        print(f"Error: File not found {image_path}")
        return
    except Exception as e:
        print(f"Error reading {image_path}: {e}")
        return

    print(f"Processing: {image_path}")

    # Process image
    try:
        pixel_values = processor(images=image, return_tensors="pt").pixel_values
        generated_ids = model.generate(pixel_values)
        extracted_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    except Exception as e:
        print(f"Error during OCR processing for {image_path}: {e}")
        return

    if extracted_text:
        # Determine output file path
        filename = os.path.basename(image_path)
        name, _ = os.path.splitext(filename)
        output_filename = f"{name}.txt"
        output_path = os.path.join(output_dir, output_filename)

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(extracted_text)

        print(f"Saved text to: {output_path}")
    else:
        print(f"No text found in: {image_path}")

def process_path(input_path, output_dir):
    """Processes a single file or a directory of files."""

    # Initialize the processor and model from Hugging Face
    print("Loading TrOCR model (microsoft/trocr-base-handwritten)... This may take a moment.")
    processor = TrOCRProcessor.from_pretrained('microsoft/trocr-base-handwritten')
    model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-base-handwritten')

    if os.path.isfile(input_path):
        detect_text(input_path, output_dir, processor, model)
    elif os.path.isdir(input_path):
        valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff')
        for root, _, files in os.walk(input_path):
            for file in files:
                if file.lower().endswith(valid_extensions):
                    file_path = os.path.join(root, file)
                    detect_text(file_path, output_dir, processor, model)
    else:
        print(f"Invalid path: {input_path}")

def get_clean_input(prompt):
    user_input = input(prompt).strip()
    return user_input.strip('\'"')

def main():
    input_path = get_clean_input("Enter the path to a picture or a folder containing pictures: ")
    output_path = get_clean_input("Enter the path to save the completed .txt files: ")

    process_path(input_path, output_path)
    print("Extraction complete.")

if __name__ == '__main__':
    main()
