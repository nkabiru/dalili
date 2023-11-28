import re

from bs4 import BeautifulSoup


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
