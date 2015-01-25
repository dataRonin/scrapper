#!/usr/bin/python
# -*- coding: utf-8 -*-


import csv
import datetime
from bs4 import BeautifulSoup
import requests
from threading import Timer
import itertools
import pdfkit
import datetime
import itertools

def get_title(soup):
    titleTag = soup.find("title")
    return titleTag.string

def get_inner_links(soup):
    inner_links = []

    for link in soup.find_all("a"):

        if "Introduction" in str(link.string):
            b = link.get("href")
            inner_links.append(b)
        elif "Sensor" in str(link.string):
            b = link.get("href")
            inner_links.append(b)
        else:
            pass
    return inner_links

def get_new_urls(inner_links):
    prefix = "http://wiki.esipfed.org"
    newpages = []
    for link in inner_links:
        newpage = prefix + link
        newpages.append(newpage)

    return newpages

def get_flatviews(inner_links):
    prefix = "http://wiki.esipfed.org"
    newpages = []
    # example:  
    # http://wiki.esipfed.org/index.php?title=Introduction&action=render
    for each_link in inner_links:
        valid_text=each_link.split('/index.php/')[1]
        flatpage = prefix + '/index.php?title='+valid_text+'&action=render'
        newpages.append(flatpage)

    return newpages
        
def to_pdf(il, newpages):
    now = datetime.datetime.now()
    now = now.isoformat()

    for (link, page_render) in itertools.izip(il, newpages):
        pdf_name = link.split('/index.php/')[1]
        pdf_save_name = pdf_name + now + '.pdf'

        pdfkit.from_url(page_render, pdf_save_name)
        print ("created pdf for %s") %(pdf_save_name)



if __name__ == "__main__":

    mainpage = "http://wiki.esipfed.org/index.php/EnviroSensing_Cluster"

    r = requests.get(mainpage)
    data = r.text 
    soup = BeautifulSoup(data)

    #gt = get_title(soup)
    #soupy_title = str(gt)
    il = get_inner_links(soup)
    # newu = get_new_urls(il)
    flatpg = get_flatviews(il)
    to_pdf(il, flatpg)

    
