import json
import os
import re

from dalili.pdf_text_parser import scrape_link_from_webpage
from dalili.pdf_text_parser import convert_url_to_filename

import fitz
import requests


FOLDER = "interruptions"
SUBFOLDERS = ('pdf', 'txt', 'json')


def pdf_to_text(path):
    infile = fitz.open(path)

    # Get filename, remove .pdf extension, and append .txt extension
    outfile_name = os.path.splitext(os.path.split(path)[-1])[0] + '.txt'
    outfile_path = os.path.join('interruptions/txt', outfile_name)
    outfile = open(outfile_path, 'wb')

    # Just in case the pdf has multiple pages
    for page in infile:
        text = page.get_text().encode('utf8')
        outfile.write(text)
        # Form feed / Page delimiter
        outfile.write(bytes((12,)))

    outfile.close()
    print(f"Write {outfile_name} completed")

    return outfile_path


def parse_text_file(path):
    with open(path, 'r') as file:
        text = file.read()

        areas = re.findall(r"AREA: +(?P<area>.*)", text)
        dates = re.findall(r"DATE: +\w+ (\d{2}.\d{2}. ?\d{4})", text)
        times = re.findall(
            r"TIME: ?(\d{1,2}.\d{2} A.M.?) ?[-–] ?(\d{1,2}.\d{2} P.M.?)", text)
        locations = re.findall(
            r"P.M.?\s+([\w\s,&/.'’-]+)&\s*adjacent\s*customers?", text)

        # If areas list doesn't have the same no. of elements as the date & time, raise an errori
        interruptions = []
        if len(areas) == len(dates) == len(times) == len(locations):
            for i in range(len(areas)):
                interruptions.append({
                    "area": areas[i],
                    "date": dates[i],
                    "time": times[i],
                    "locations": locations[i].replace('\n', '')
                })
        else:
            raise Exception("Regex matches don't match up")

        return interruptions


def to_json(data, filename='data'):
    # Get the filename from the text file
    filename = f'interruptions/json/{filename}.json'

    with open(filename, "w") as f:
        json.dump(data, f)


def to_stdout(data):
    for i in data:
        print(i)


if __name__ == "__main__":
    # Initial Bootstrapping
    if FOLDER not in os.listdir():
        os.mkdir(FOLDER)
        for subfolder in SUBFOLDERS:
            os.mkdir(os.path.join(FOLDER, subfolder))

    link = scrape_link_from_webpage(
        requests.get(
            "https://kplc.co.ke/category/view/50/planned-power-interruptions"
        ).content
    )
    filename = convert_url_to_filename(link)

    # Fetch the PDF file
    r = requests.get(link)
    pdf = os.path.join(FOLDER, "pdf", filename+".pdf")
    if r.ok:
        with open(pdf, "wb") as file_:
            file_.write(r.content)
            print(f"Download: {FOLDER}/pdf/{filename}complete\n")
    else:
        exit("Failed to download PDF file from KPLC")

    if pdf:
        textfile = pdf_to_text(pdf)
        interruptions = parse_text_file(textfile)
        to_json(interruptions)
