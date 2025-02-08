import os
import re

import requests
from bs4 import BeautifulSoup, SoupStrainer


def scrape_link_from_webpage(url):
    response = requests.get(url)

    if response.ok:
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


def download_pdf(url) -> bool:
    """
    Downloads the pdf into the pdfs folder.
    """
    filename = url.split("/")[-1]
    filepath = os.path.join("pdfs", filename)

    # Check if file already exists
    if os.path.exists(filepath):
        return True

    # TODO: Check if existing file is complete.

    response = requests.get(url, timeout=5)

    if response.status_code == requests.codes.ok:
        with open(filepath, mode="wb") as file:
            file.write(response.content)
        print("File downloaded")
        return True

    else:
        print("File not downloaded")
        return False


def main() -> None:
    url = scrape_link_from_webpage("https://kplc.co.ke/customer-support#powerschedule")
    print(f"Link obtained: {url}")

    create_pdf_dir()
    download_pdf(url)


if __name__ == "__main__":
    main()
