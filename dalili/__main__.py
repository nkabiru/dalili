import argparse
import os
import re

import requests
from bs4 import BeautifulSoup, SoupStrainer

# Globals
verbose = False
timeout = 3


def scrape_link_from_webpage(url) -> str | None:
    """
    Get the <a> tag with a href attribute url that points to the latest interruptions PDF file.
    """
    # Timeout after 5s
    response = requests.get(url, timeout=timeout)

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
        if verbose:
            print("Folder created")
    else:
        if verbose:
            print("Folder 'pdfs' already exists")


def download_pdf(url) -> str | None:
    """
    Downloads the pdf into the pdfs folder.
    """
    filename = url.split("/")[-1]
    filepath = os.path.join("pdfs", filename)

    # Check if file already exists
    if os.path.exists(filepath):
        if verbose:
            print("File already exists")
        return filepath

    # TODO: Check if existing file is complete.

    response = requests.get(url, timeout=timeout)

    if response.status_code == requests.codes.ok:
        with open(filepath, mode="wb") as file:
            file.write(response.content)
        if verbose:
            print("File downloaded")
        return filepath

    else:
        if verbose:
            print("File not downloaded")
        return None


def read_pdf(pdf) -> str:
    from pypdf import PdfReader

    reader = PdfReader(pdf)
    text = ""
    for page in reader.pages:
        text = text + page.extract_text()

    return text


def parse_text(text) -> list:
    interruptions = []

    matches = re.findall(
        r"AREA:\s.*?\nDATE: *\w+ (\d{2}.\d{2}.\d{4})\s+?TIME: (\d{1,2}\.\d{2}) *A\.M\. *(?:–|-) *(\d{1,2}\.\d{2}) *P\.M\.\s*\n([\s\S]*?)(?=\s*&\s*adjacent\s*[cC]ustomers)",
        text,
    )

    for match in matches:
        date, start_time, end_time, locations = match
        interruptions.append(
            {
                "date": date.strip(),
                "start_time": start_time.strip(),
                "end_time": end_time.strip(),
                "locations": locations.strip().replace("\n", ""),
            }
        )

    return interruptions


def filter_by_location(interruptions, location) -> dict | None:
    for i in interruptions:
        if location in i["locations"]:
            return i
    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="dalili",
        description="Setup a Gmail calendar event if your location is scheduled for a power interruption.",
    )
    parser.add_argument("location", help="Location to search for")
    parser.add_argument(
        "-t", "--timeout", help="Request timeout duration. Default is 3s", type=int
    )
    parser.add_argument("--debug", help="Print out debugging info", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    # Change value of verbose & timeout globally
    global verbose, timeout
    verbose = args.verbose
    timeout = args.timeout

    url = scrape_link_from_webpage("https://kplc.co.ke/customer-support#powerschedule")
    if verbose:
        print(f"Link obtained: {url}")

    create_pdf_dir()
    pdf = download_pdf(url)

    if verbose:
        print(f"PDF path: {pdf}")

    if pdf:
        text = read_pdf(pdf)
        interruptions = parse_text(text)
        if args.debug:
            for i in interruptions:
                print(i, end="\n\n")
        interruption = filter_by_location(interruptions, args.location)
        if verbose:
            print(args.location, interruption)


if __name__ == "__main__":
    main()
