import pytest
from dalili.pdf_text_parser import scrape_link_from_webpage
from dalili.pdf_text_parser import convert_url_to_filename


@pytest.mark.parametrize("response, expected", [
    ("""
<!doctype html>
<html lang="en">
    <head>
        <meta charset="UTF-8"/>
        <title>Document</title>
    </head>
    <body>
	<a href="https://kplc.co.ke/img/full/Interruption%20-%2011.05.2023.pdf">
	    Interruption - 11.05.2023.pdf
	</a>
	<a href="https://kplc.co.ke/img/full/Interruption%20-%2004.05.2023.pdf">
	    Interruption - 04.05.2023
	</a>

    </body>
</html>
    """,
     "https://kplc.co.ke/img/full/Interruption%20-%2011.05.2023.pdf"),
    ("", "")
])
def test_scrape_link_from_webpage(response, expected):
    assert scrape_link_from_webpage(response) == expected


@pytest.mark.parametrize("url, filename", [
    (
        "https://kplc.co.ke/img/full/Interruption%20-%2011.05.2023.pdf",
        "interruptions_2023-05-11"
    )
])
def test_convert_url_to_filename(url, filename):
    assert convert_url_to_filename(url) == filename
