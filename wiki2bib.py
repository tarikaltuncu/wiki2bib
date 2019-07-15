#!/usr/bin/python3
import bs4
import requests

import os
import re

import argparse

parser = argparse.ArgumentParser(description='Short sample app')

parser.add_argument('--doi2bib', '-doi', action="store_true", default=True)
parser.add_argument('--anystyle', '-any', action="store_true", default=False)
parser.add_argument('-url', dest='url_list', nargs='+')
# parser.add_argument('--pname', dest='pname_list', nargs='+')

args = parser.parse_args()
print(args)

prefix = 'https://en.wikipedia.org/wiki/'
references_list = list()
for url in args.url_list:
#     pname = url.split('/')[-1]
    pname = url
    crawl_url = prefix + pname
    response = requests.get(crawl_url)
    html = response.text
    soup = bs4.BeautifulSoup(html, "html.parser")
    
    references_section = soup.find(['ol'], { "class" : "references"})
    references_list.extend(references_section.find_all(['li']))

doi_reg = r"\b(10[.][0-9]{4,}(?:[.][0-9]+)*(?:(?![\"&\'<>])\S)+)\b"
doi_url = "http://dx.doi.org/"

try:
	os.remove(f"./{pname+'.bib'}")
except:
	pass

if args.anystyle:
    f = open(f"./{pname+'.ref'}", 'w+')
	

for ref in references_list:
    
    if args.doi2bib:
        dois = re.findall(doi_reg, str(ref))
        for doi in dois:
            os.system(f"doi2bib \"{doi_url + doi}\" >> \"{pname+'.bib'}\"")
    
    if args.anystyle:
        reference = ref.find_all("span", {'class':'reference-text'})[0].text
        f.write(reference+'\n')
        
if args.anystyle:
    f.close()

    cmd = f"anystyle -f bib parse {pname}.ref >> \"{pname+'.bib'}\""
    proc = os.popen(cmd)
    proc.close()

    try:
        os.remove(f"./{pname+'.ref'}")
    except:
        pass