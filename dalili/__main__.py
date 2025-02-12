import os
import re

import requests
from bs4 import BeautifulSoup, SoupStrainer


def scrape_link_from_webpage(url):
    """
    Get the <a> tag with a href attribute url that points to the latest interruptions PDF file.
    """
    # Timeout after 5s
    response = requests.get(url, timeout=5)

    if response.status_code == requests.codes.ok:
        power_schedule_div = SoupStrainer(id="powerschedule")
        soup = BeautifulSoup(
            response.text, "html.parser", parse_only=power_schedule_div
        )
        return soup.find_all(
            href=re.compile(r"https://kplc.co.ke/storage/[^\s]+\.pdf\b")
        )[0]["href"]
    else:
        return None


def create_pdf_dir() -> None:
    """
    Create the dir for holding the files
    """
    if not os.path.exists("pdfs"):
        os.mkdir("pdfs")
        print("Folder created")


def download_pdf(url) -> str | None:
    """
    Downloads the pdf into the pdfs folder.
    """
    filename = url.split("/")[-1]
    filepath = os.path.join("pdfs", filename)

    # Check if file already exists
    if os.path.exists(filepath):
        print("File already exists")
        return filepath

    # TODO: Check if existing file is complete.

    response = requests.get(url, timeout=5)

    if response.status_code == requests.codes.ok:
        with open(filepath, mode="wb") as file:
            file.write(response.content)
        print("File downloaded")
        return filepath

    else:
        print("File not downloaded")
        return None


def read_pdf(pdf) -> str:
    from pypdf import PdfReader

    reader = PdfReader(pdf)
    text = ""
    for page in reader.pages:
        text = text + page.extract_text()

    return text


def main() -> None:
    url = scrape_link_from_webpage("https://kplc.co.ke/customer-support#powerschedule")
    print(f"Link obtained: {url}")

    create_pdf_dir()
    pdf = download_pdf(url)

    # Read the pdf file.
    if pdf:
        text = read_pdf(pdf)
        print(text)


if __name__ == "__main__":
    main()
