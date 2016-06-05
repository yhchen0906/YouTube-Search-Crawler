#! /usr/bin/env python
# -*- coding: utf-8 -*-
# file: youtube.py
import urllib
import argparse
import requests
from bs4 import BeautifulSoup
parser = argparse.ArgumentParser(description = 'YouTube search crawler')
parser.add_argument('keyword', nargs = '+')
parser.add_argument('-n', type = int, default = 5, help = 'number of search result. default is 5', metavar = 'number')
parser.add_argument('-p', type = int, default = 1, help = 'the page to be parse', metavar = 'page')
args = parser.parse_args()
requests.packages.urllib3.disable_warnings()
keyword, page = '+'.join(urllib.quote_plus(str) for str in args.keyword), args.p
search_url = 'https://www.youtube.com/results?sp=EgIQAQ%253D%253D&search_query={}&page={}'
search_soup = BeautifulSoup(requests.get(search_url.format(keyword, page), verify = False).text, 'html.parser')
search_results = search_soup.find_all('div', {'class' : 'yt-lockup-content'})
for search_result in search_results[:args.n]:
    video_url = 'https://www.youtube.com' + search_result.h3.a['href']
    api_url = 'https://developer.url.fit/api/shorten?long_url='
    shorten_url = 'https://url.fit/' + requests.get(api_url + urllib.quote_plus(video_url), verify = False).json()['url']
    video_soup = BeautifulSoup(requests.get(video_url, verify = False).text, 'html.parser')
    description = search_result.find('div', {'class' : 'yt-lockup-description'})
    like = video_soup.find('button', {'class' : 'like-button-renderer-like-button'}).span
    dislike = video_soup.find('button', {'class' : 'like-button-renderer-dislike-button'}).span
    print search_result.h3.a.text, '(' + shorten_url + ')'
    print description.text if description else '[no description]'
    if like and dislike:
        print 'Like:', like.text + ',', 'Dislike:', dislike.text + '\n'
    else: print '[rating disabled]\n'
