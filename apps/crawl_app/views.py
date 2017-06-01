# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from bs4 import BeautifulSoup, SoupStrainer
from urllib import urlopen
import unicodedata

# Create your views here.
def index(request):
    return render(request, 'crawl_app/index.html')

def orca(request):
    url = 'https://en.wikipedia.org/wiki/Killer_whale'
    html = urlopen(url)
    headline = SoupStrainer('span', {'class' : 'mw-headline'})
    soup = BeautifulSoup(html, 'html.parser')
    headline_soup = soup.find_all(headline)
    #print headline_soup

    def makeHeadlineList(headline_soup):
        headlineArr = []
        for i in range(len(headline_soup)):
            headlineArr.append(headline_soup[i].getText())
        return headlineArr
    
    headlinelist = makeHeadlineList(headline_soup)

    context = {
        'headlines' : makeHeadlineList(headline_soup)
    }
    for item in context['headlines']:
        print item
    return render(request, 'crawl_app/orca.html', context)

def nytimes(request):
    url = 'https://www.nytimes.com/'
    html = urlopen(url)
    headline = SoupStrainer('h2', {'class': 'story-heading'})
    soup = BeautifulSoup(html, 'html.parser')
    headline_soup = soup.find_all(headline)

    #print headline_soup
    #print headline_soup

    url = 'https://www.nytimes.com/'
    html = urlopen(url)
    links = SoupStrainer('a')
    soup = BeautifulSoup(html, 'html.parser')
    link_soup = soup.find_all(links) 

    def makeHeadlineList(headline_soup):
        headlineArr = []
        for i in range(len(headline_soup)):
            headlineArr.append(headline_soup[i].getText())
        return headlineArr

    def cleanArray(arr):
        newarr = []
        for item in arr:
            stringitem = unicodedata.normalize('NFKD', item).encode('ascii', 'ignore')
            itemarr = stringitem.split()
            itemstr = ' '.join(itemarr)
            newarr.append(itemstr)
        return newarr

    def getLinkArray(link_soup):
        urlArr = []
        for i in range(len(link_soup)):
            urlArr.append([link_soup[i]['href'], link_soup[i].getText()])
        return urlArr       

    def cleanLinkArray(arr):
        newarr = []
        for item in arr:
            stringitem0 = unicodedata.normalize('NFKD', item[0]).encode('ascii', 'ignore')
            itemarr0 = stringitem0.split()
            itemstr0 = ' '.join(itemarr0)

            stringitem1 = unicodedata.normalize('NFKD', item[1]).encode('ascii', 'ignore')
            itemarr1 = stringitem1.split()
            itemstr1 = ' '.join(itemarr1)

            newarr.append([itemstr0, itemstr1])
        return newarr

    def findMatch(headlineArr, linkArr):
        matchArray = []
        for item in linkArr:
            if item[1] in headlineArr:
                matchArray.append(item)
        return matchArray

    headlineArr = makeHeadlineList(headline_soup)
    clean_headline_arr = cleanArray(headlineArr)

    linkarray = getLinkArray(link_soup)
    clean_link_array = cleanLinkArray(linkarray)
    matchedArray = findMatch(clean_headline_arr, clean_link_array)

    # for item in matchedArray:
    #     print item
    #     print ""

    # print len(matchedArray)
    # print len(clean_link_array)

    context = {
        'headlines' : matchedArray
    }


    return render(request, 'crawl_app/nytimes.html', context)