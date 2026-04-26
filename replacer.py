import os
from google import genai
from PIL import Image

def process_files():
    # folder path for pictures, text files
    folder_path = "./target_folder"

    client = genai.Client() # Requires GEMINI_API_KEY environment variable or Vertex AI setup

    # Check if folder exists
    if not os.path.isdir(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    # Find all jpegs and txts
    jpeg_files = set()
    txt_files = set()

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.jpeg', '.jpg')):
                jpeg_files.add(os.path.join(root, file))
            elif file.lower().endswith('.txt') and not file.lower().endswith('_updated.txt'):
                txt_files.add(os.path.join(root, file))

    # Match files
    all_bases = set()

    # Store the actual paths
    jpeg_map = {}
    txt_map = {}

    for jpeg_path in jpeg_files:
        base_name = os.path.splitext(os.path.basename(jpeg_path))[0]
        # Using relative path to the base folder for mapping
        rel_dir = os.path.relpath(os.path.dirname(jpeg_path), folder_path)
        key = os.path.join(rel_dir, base_name) if rel_dir != '.' else base_name

        all_bases.add(key)
        jpeg_map[key] = jpeg_path

    for txt_path in txt_files:
        base_name = os.path.splitext(os.path.basename(txt_path))[0]
        rel_dir = os.path.relpath(os.path.dirname(txt_path), folder_path)
        key = os.path.join(rel_dir, base_name) if rel_dir != '.' else base_name

        all_bases.add(key)
        txt_map[key] = txt_path

    for base_key in all_bases:
        if base_key not in jpeg_map:
            print(f"Warning: Missing image file for '{txt_map[base_key]}'")
            continue
        if base_key not in txt_map:
            print(f"Warning: Missing text file for '{jpeg_map[base_key]}'")
            continue

        # Both exist
        jpeg_path = jpeg_map[base_key]
        txt_path = txt_map[base_key]

        updated_txt_path = os.path.join(os.path.dirname(txt_path), f"{os.path.basename(base_key)}_updated.txt")

        print(f"Processing '{jpeg_path}' and '{txt_path}'...")

        try:
            with open(txt_path, 'r', encoding='utf-8') as f:
                scrambled_text = f.read()

            image = Image.open(jpeg_path)

            prompt = (
                "You are an expert OCR and text correction assistant.\n"
                "I am providing you with an image containing text, and a scrambled, imperfect text extraction from that image.\n"
                "Your task is to produce a perfect, line-by-line copy of the text as it appears in the image. "
                "Use the provided scrambled text as a reference to help you identify characters, but correct all mistakes, "
                "ensure perfect spelling, and match the line breaks exactly as they appear in the image.\n"
                "Output ONLY the corrected text, with no introductory or concluding remarks.\n\n"
                "--- Scrambled Text Reference ---\n"
                f"{scrambled_text}\n"
                "--------------------------------"
            )

            response = client.models.generate_content(
                model='gemini-2.5-pro',
                contents=[image, prompt]
            )

            with open(updated_txt_path, 'w', encoding='utf-8') as f:
                f.write(response.text)

            print(f"Successfully created '{updated_txt_path}'")

        except Exception as e:
            print(f"Error processing {base_key}: {e}")

if __name__ == "__main__":
    process_files()