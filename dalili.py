import json
import os
import re
from datetime import datetime
from urllib.parse import unquote
from urllib.parse import urlparse

import fitz
import requests
from bs4 import BeautifulSoup


def get_pdf() -> str | None:
    res = requests.get('https://kplc.co.ke/category/view/50/planned-power-interruptions')
    soup = BeautifulSoup(res.content, 'html.parser')
    folder = 'interruptions'
    subfolders = ['pdf', 'txt', 'json']

    # Find the latest pdf containing fixtures.
    tag = soup.find('a', href=re.compile(r'Interruption.*\.pdf'))

    # If dirs doesn't exist, create it
    if folder not in os.listdir():
        os.mkdir(folder)

        for subfolder in subfolders:
            os.mkdir(os.path.join(folder, subfolder))

    # Some links don't have https:// in the url, so add it
    link = tag['href']

    if not link.startswith('https://'):
        link = 'https://' + link

    # Filename is the last part of the url path, and is URLencoded
    url = urlparse(link)
    original_filename = unquote(url.path).rpartition('/')[-1]
    filename = original_filename

    # Extract date from the filename and create a more readable filename.
    match = re.search(r'(((0[1-9])|([12][0-9])|(3[01])).((0[1-9])|(1[0-2])).(\d{4}))', original_filename)

    if match:
        date = datetime.strptime(match[0], '%d.%m.%Y').strftime('%Y%m%d');
        filename = 'interruptions_' + date
    # Get the pdf from the link
    r = requests.get(link)
    if r.ok:
        open(folder + '/pdf/' + filename + '.pdf', 'wb').write(r.content)
        print(f"Download '{original_filename}' as '{filename}.pdf' complete")
        return os.path.join(folder, 'pdf', filename + '.pdf')

    print('Failed: ' + r.reason)
    return None


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
        times = re.findall(r"TIME: ?(\d{1,2}.\d{2} A.M.?) ?[-–] ?(\d{1,2}.\d{2} P.M.?)", text)
        locations = re.findall(r"P.M.?\s+([\w\s,&/.'’-]+)&\s*adjacent\s*customers?", text)

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
    pdf = get_pdf()
    if pdf:
        textfile = pdf_to_text(pdf)
        interruptions = parse_text_file(textfile)
        to_json(interruptions)
