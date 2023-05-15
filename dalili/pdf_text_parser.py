import requests
import re

from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import unquote
from urllib.parse import urlparse


def scrape_link_from_webpage(webpage: str) -> str:
    """Given a webpage, return the first link from that page."""
    link, soup = "", BeautifulSoup(webpage, "html.parser")
    tag = soup.find(
        "a",
        href=re.compile(r"Interruption.*\.pdf")
    )
    if tag:
        link = tag["href"]
    # Some links don't have https:// in the url, so add it
    if link and not link.startswith("https://"):
        link = "https://" + link
    return link


def convert_url_to_filename(url: str) -> str:
    """Given a url, return a properly formatted filename E.g
    interruptions_2023-05-11"""
    filename, url = "", urlparse(url)
    date_match = re.search(
        r'(((0[1-9])|([12][0-9])|(3[01])).((0[1-9])|(1[0-2])).(\d{4}))',
        filename:=unquote(url.path).rpartition("/")[-1]
    )

    if date_match:
        filename = f"interruptions_\
{datetime.strptime(date_match[0], '%d.%m.%Y').strftime('%Y-%m-%d')}"
    return filename
