# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from bs4 import BeautifulSoup, SoupStrainer
from urllib import urlopen
import unicodedata
from random import randint
from .models import Video

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

#get parentheses

def youtube(request):
    # url = 'https://en.wikipedia.org/wiki/List_of_most_viewed_YouTube_videos'
    # html = urlopen(url)
    # td = SoupStrainer('td')
    # soup = BeautifulSoup(html, 'html.parser')
    # td_soup = soup.find_all(td)

    # def makeRowList(td_soup):
    #     tdArr = []
    #     for i in range(81*6-6):
    #         tdArr.append(td_soup[i].getText())
    #     return tdArr
    
    # rowlist = makeRowList(td_soup)
    # # for item in rowlist:
    # #     print item

    # def filterRowList(arr):
    #     filteredArr = []
    #     count = 1
    #     while count < len(arr):
    #         name = ''
    #         for i in range(len(arr[count])):
    #             stringword = unicodedata.normalize('NFKD', arr[count]).encode('ascii', 'ignore')
    #             if stringword[i] == " " or stringword[i].isalpha():
    #                 name += arr[count][i]
    #         author = arr[count+1]
    #         views = float(arr[count+2])
    #         date = arr[count+3]

    #         filteredArr.append([name, author, views, date])
    #         count += 6
    #     return filteredArr
    # filteredlist = filterRowList(rowlist)

    index1 = randint(1, 80)
    index2 = randint(1, 80)
    while index1 == index2:
        index2 = randint(1, 80)

    # print index1, index2
    # print filteredlist[index1], filteredlist[index2]

    videos = Video.objects.all()
    #print videos
    context = {
        #'list' : videos,
        'song1' : Video.objects.get(pk=index1),
        'song2' : Video.objects.get(pk=index2)
    }
    return render(request, 'crawl_app/youtube.html', context)