import requests
from bs4 import BeautifulSoup
import re

article_props = ['Title','Time','Link']

def scrape_eb(termer):
    eb = requests.get(f"https://ekstrabladet.dk/find/?q={termer}")
    soup = BeautifulSoup(eb.content, 'html.parser')
    articles = soup.find_all("div", class_="flex-item margin-l--b width-1of1")
    return articles

def to_json_eb(article):
    article = str(article.contents.pop(1))
    eb_handling = {
        'Title':r'(?<=<h2 class="card-title">).*(?=<\/h2>)',
        'Time':r'(?<=<\/span> - ).*(?=<\/small><\/div>)',
        'Link':r'(?<=href=").*(?=" style=")'
    }
    to_JSON = dict()
    for prop in article_props:
        extraction = re.findall(eb_handling[prop],article)
        if extraction:
            to_JSON[prop] = extraction[0]
        else:
            to_JSON[prop] = f"NO {prop}"
    return to_JSON

def scrape_TV2(termer):
    TV2 = requests.get(f"https://search.tv2.dk/?query={termer}")
    soup = BeautifulSoup(TV2.content, 'html.parser')
    soup1 = soup.find("ul", class_='tc_grid tc_searchresults__list') 
    articles = soup1.find_all("li")
    return articles

def to_json_TV2(article):
    article = str(article)
    tv2_handling = {
        'Title':r'(?<=tc_heading--weight-400">).*(?=<\/h3>)',
        'Time':r'(?<=item__text">).*\d{4}(?= )',
        'Link':r'(?<=url">).*(?=<\/div><\/div>)'
    }
    to_JSON = dict()
    for prop in article_props:
        extraction = re.findall(tv2_handling[prop],article)
        if extraction:
            to_JSON[prop] = extraction[0]
        else:
            to_JSON[prop] = f"NO {prop}"
    return to_JSON

def scrape_JP(termer):
    JP = requests.get(f"https://jyllands-posten.dk/soeg?term={termer}")
    soup = BeautifulSoup(JP.content, 'html.parser')
    articles = articles = soup.find_all("article") 
    return articles

def to_json_JP(article):
    article = str(article.contents.pop(1))
    jp_handling = {
        'Title':r'(?<=<span>).*(?=<\/span>)',
        'Time':r'(?<=\dZ">).*(?=<\/time>)',
        'Link':r'(?<=href=").*(?=\/">)'
    }
    to_JSON = dict()
    for prop in article_props:
        extraction = re.findall(jp_handling[prop],article)
        if extraction:
            to_JSON[prop] = extraction[0]
        else:
            to_JSON[prop] = f"NO {prop}"
    return to_JSON

def scrape_delegate(bureau,termer):
    scrapers = {
        'Ekstra Bladet': scrape_eb,
        'Jyllands Posten': scrape_JP,
        'TV2': scrape_TV2
    }
    return scrapers[bureau](termer)

def json_delegate(bureau):
    jsons = {
        'Ekstra Bladet': to_json_eb,
        'Jyllands Posten': to_json_JP,
        'TV2': to_json_TV2
    }
    return jsons[bureau]