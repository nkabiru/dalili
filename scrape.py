import os
import re
import requests
from urllib.parse import unquote
from urllib.parse import urlparse
from datetime import datetime
from bs4 import BeautifulSoup

dir = "interruptions"
res = requests.get("https://kplc.co.ke/category/view/50/planned-power-interruptions")
soup = BeautifulSoup(res.content, 'html.parser')

# Find the latest pdf containing interruptions. Should be run EoB Thursday.
tags = soup.find_all('a', href=re.compile('\\.pdf'), limit=10)

# TODO: The interruption PDFs are not in order, an option is grab the list of links
# on the first page and diff it against a list of links that I already have.

# If dir doesn't exist, create it
if dir not in os.listdir():
    os.mkdir(dir)

for tag in tags:
    link = tag['href']
    if not link.startswith('https://'):
        link = "https://" +  link

    # Filename is the last part of the url path, and is URLencoded 
    url = urlparse(link)
    original_filename = unquote(url.path).rpartition('/')[-1]
    filename = original_filename
    
    # Extract date from the filename and create an easier filename.
    match = re.search(r'(((0[1-9])|([12][0-9])|(3[01])).((0[1-9])|(1[0-2])).(\d{4}))', original_filename)

    if match:
        date = datetime.strptime(match[0], '%d.%m.%Y').strftime('%Y%m%d')
        filename = 'interruptions_' + date

    r = requests.get(link)

    if r.ok:
        open(dir + '/' + filename + '.pdf', 'wb').write(r.content)
        print(f'Download {original_filename} as {filename} complete')
    else:
        print('Failed: ' + r.reason)
