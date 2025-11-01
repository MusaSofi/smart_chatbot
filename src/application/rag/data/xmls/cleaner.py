import os
import re
import glob

def remove_photo_tags_from_xml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Regex to find and remove <photo>...</photo> including line breaks
    cleaned_content = re.sub(r'<photo>.*?</photo>', '', content, flags=re.DOTALL)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)

def clean_xml_folder(folder_path):
    xml_files = glob.glob(os.path.join(folder_path, '*.xml'))
    for xml_file in xml_files:
        print(f"🧹 Cleaning {xml_file}")
        remove_photo_tags_from_xml(xml_file)
    print("✅ Done!")

if __name__ == "__main__":
    folder = "./staff"
    clean_xml_folder(folder)