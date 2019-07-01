#!/usr/bin/python3
import bs4
import requests

import os
import re
import sys

crawl_url = sys.argv[1]
pname = crawl_url.split('/')[-1]

response = requests.get(crawl_url)
html = response.text
soup = bs4.BeautifulSoup(html, "html.parser")

doi_reg = r"\b(10[.][0-9]{4,}(?:[.][0-9]+)*(?:(?![\"&\'<>])\S)+)\b"
doi_url = "http://dx.doi.org/"

try:
	os.remove(f"./{pname+'.bib'}")
except:
	pass
	
references_section = soup.find(['ol'], { "class" : "references"})
references_list = references_section.find_all(['li'])
for ref in references_list:
    dois = re.findall(doi_reg, str(ref))
    for doi in dois:
        os.system(f"doi2bib \"{doi_url + doi}\" >> \"{pname+'.bib'}\"")