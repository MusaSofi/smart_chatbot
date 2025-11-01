import xml.etree.ElementTree as ET
import os
import time
import requests

BASE_URL = "https://m2-ufind.univie.ac.at/courses"
STAFF_PATH = "./staff"
SEMESTER = "2025S"
COURSES_PATH = f"./courses_{SEMESTER}"
COURSE_IDS = set()

def extract_course_ids_from_staff(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    for elem in root.iter('photo'):
        elem.clear()

    # Extract the data
    courses = root.findall(f"teaching//term[@id='{SEMESTER}']//course")

    for course in courses:
        id = course.attrib['id']
        COURSE_IDS.add(id)

def list_xml_files_in_directory(directory_path: str) -> list[str]:
    xmls: list[str] = []

    for name in os.listdir(STAFF_PATH):
        if name.endswith(".xml"):
            xmls.append(name)
    return xmls

def write_course_ids_to_file():
    with open('courseid.txt', 'w', encoding='utf-8') as f:
        for course_id in COURSE_IDS:
            f.write(course_id + "\n")

def write_courses_xmls_to_directory():
    for course_id in COURSE_IDS:
        if os.path.exists(f'{COURSES_PATH}/{course_id}.xml'):
            continue
        xmldata = requests.get(f'{BASE_URL}/{course_id}/{SEMESTER}').text.encode('ISO-8859-1').decode('UTF-8')

        with open(f'{COURSES_PATH}/{course_id}.xml', 'w', encoding='utf-8') as f:
            f.write(xmldata)
            print(f'{COURSES_PATH}/{course_id}.xml written')
        #wait 5 seconds
        time.sleep(10)

if __name__ == "__main__":
    xmls = list_xml_files_in_directory(STAFF_PATH)

    for xml in xmls:
        extract_course_ids_from_staff(f"{STAFF_PATH}/{xml}")

    write_course_ids_to_file() # Optional. Good to compare number of files and number of ids

    if not os.path.exists(COURSES_PATH):
        os.makedirs(COURSES_PATH)

    write_courses_xmls_to_directory()
