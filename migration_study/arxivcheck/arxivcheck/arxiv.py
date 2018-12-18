from __future__ import unicode_literals, print_function, absolute_import
from builtins import input
import feedparser
from doi2bib.crossref import get_bib_from_doi
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote
import re
from unidecode import unidecode

import requests
from arxivcheck.wrapper_graphQL import *

months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct',
'nov', 'dec']


def ask_which_is(title, items):
    found = False
    result = {}
    question = "\n\tArxiv:{} \n\tIt is \n\t{}\n\t Correct?y(yes)|n(no)|q(quit)"
    for item in items:
        w = input(question.format(
            unidecode(item["title"]), unidecode(title)))
        if w == "y":
            found = True
            result = item
            break
        if w == "q":
            break
    return found, result


def get_arxiv_info(value, field="id"):
   
    result = arxiv_info(value, field)

    found = False
    items = []

    if field == "id" and result["data"]["entry"] != None:
        items = result["data"]["entry"]
        found = True
    elif field == "ti" and result["data"]["entries"]:
        items = result["data"]["entries"]
        found = True
    else:
        items = []  


    return found, items


def generate_bib_from_arxiv(arxiv_item, value, field="id"):
    # arxiv_cat = arxiv_item.arxiv_primary_category["term"]
    if field == "ti":
        journal = "arxiv:"+arxiv_item["id"].split("http://arxiv.org/abs/")[1]
    else:
        journal = "arxiv:"+value

    url = arxiv_item["pdfUrl"]
    title = arxiv_item["title"]
    authors = arxiv_item["authors"]
    if len(authors) > 0:
        first_author = authors[0].split(" ")
        authors = " and ".join([author for author in authors])
    else:
        first_author = authors
        authors = authors

    published = arxiv_item["published"].split("-")
    year = ''
    if len(published) > 1:
        year = published[0]
    bib = BibDatabase()
    bib.entries = [
        {
            "journal": journal,
            "url": url,
            "ID": year+first_author[0]+journal,
            "title": title,
            "year": year,
            "author": authors,
            "ENTRYTYPE": "article"
        }
    ]
    bib = BibTexWriter().write(bib)
    return bib


def get_arxiv_pdf_link(value, field="id"):
    found, items = get_arxiv_info(value, field)
    if found:
        link = items[0]["pdfUrl"]

    return found, link


def check_arxiv_published(value, field="id", get_first=True):
    found = False
    published = False
    bib = ""
    value = re.sub("arxiv\:", "", value, flags=re.I)
    found, items = get_arxiv_info(value, field)
    if found:
        if get_first is False and field == "ti" and len(items) > 1:
            found, item = ask_which_is(value, items)
        else:
            item = items[0]
    if found:
        if item["doi"] != None:
            doi = item["doi"]
            published, bib = get_bib_from_doi(doi)
        else:
            bib = generate_bib_from_arxiv(item, value, field)
    else:
        print("\t\nArxiv not found.")
    return found, published, bib
