import bs4, requests, re, os
from normalComma import normal_comma as kuwa
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def searchAlledrogo(search):
    searchURL = search.replace(" ", "%20")
    searchSave = search.replace(" ", "_")
    chwilioAm = "http://allegro.pl/listing?string={}".format(searchURL)
    res = requests.get(chwilioAm)
    res.raise_for_status()
   # print(res.text)
    requestResult = str(res.text)
    sponsoredFinder = re.compile(r'<a href="(https?://allegro.pl/events/clicks[^"]*)" [^>]*>')
    productFinder = re.compile(r'<a href="(https?://allegro.pl/oferta/[^"]*)" [^>]*>')
    sponsoredItemsUnclean = sponsoredFinder.findall(requestResult)
    itemsUnclean = productFinder.findall(requestResult)
    items = []
    for link in sponsoredItemsUnclean:
        if link not in items:
            items.append(link)
    for link in itemsUnclean:
        if link not in items:
            items.append(link)
    for item in items:
        print(item)
    print(len(items))

    zapiszWyniki = open(r"C:\Users\kamil\Desktop\Alledrogo\Obserwowane\XD{}.txt".format(searchSave), "w")
    for item in items:
        zapiszWyniki.write(item + "\n")
    zapiszWyniki.close()

    return r"XD{}".format(searchSave)


def checkNumberOfPages(search):
    searchURL = search.replace(" ", "%20")
    chwilioAm = "http://allegro.pl/listing?string={}".format(searchURL)
    #webbrowser.open(chwilioAm)
    res = requests.get(chwilioAm)
    res.raise_for_status()

    soup = str(bs4.BeautifulSoup(res.text, "html.parser"))

    # TODO

#print(searchAlledrogo("długopis żelowy niebieski"))
#print(os.getcwd())