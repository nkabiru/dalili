import re
import io
import pdftotext
import requests

from dalili.pdf_text_parser import scrape_link_from_webpage


def fetch_interruptions(binary):
    text = "\n".join(
        pdftotext.PDF(io.BytesIO(binary), raw=True)
    )
    # TODO: Re-work regex
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


if __name__ == "__main__":
    response = requests.get(
        scrape_link_from_webpage(
            requests.get(
                "https://kplc.co.ke/category/view/50/planned-power-interruptions"
            ).content
        )
    )
    if response.ok:
        interruptions = fetch_interruptions(
            response.content
        )
        print(interruptions)
    else:
        exit("Failed to download PDF file from KPLC")
