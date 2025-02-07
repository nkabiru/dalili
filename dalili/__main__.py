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


def download_pdf(url):
# TODO: Download the pdf for parsing.


def main():
    latest_link = scrape_link_from_webpage(
        "https://kplc.co.ke/customer-support#powerschedule"
    )



if __name__ == "__main__":
    main()
