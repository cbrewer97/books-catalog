# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 09:32:31 2022

@author: books
"""

import requests
import json

def search_google_books(author=None, isbn=None, title=None, num_results=1, language="en", verbose=False):
    query_url="https://www.googleapis.com/books/v1/volumes?q="
    if author!=None:
        query_url=query_url+"inauthor:"+author+"+"
    if isbn!=None:
       query_url=query_url+"isbn:"+isbn +"+"
    if title!=None:
        query_url=query_url+"intitle:"+title
    query_url=query_url.strip("+")
    query_url=query_url+"&langRestrict="+language
        
    #query_url=query_url.strip("&")
        
    if verbose==True:
        print(query_url)
    r=requests.get(query_url)
    return json.loads(r.text)['items'][0:num_results]

def parse_google_record(record):
    volume_info=record['volumeInfo']
    title=volume_info['title']
    authors=volume_info['authors'][0]
    publisher=volume_info['publisher']
    publish_date=volume_info['publishedDate']
    description=volume_info['description']
    identifiers=volume_info['industryIdentifiers']
    isbn10=None
    isbn13=None
    for item_dict in identifiers:
        if len(item_dict['identifier'])==10:
            isbn10=item_dict['identifier']
        elif len(item_dict['identifier'])==13:
            isbn13=item_dict['identifier']
    page_count=volume_info['pageCount']
    parsed_dict={'title':title, 'authors':authors,\
        'publisher':publisher, 'publish_date':publish_date,\
        'description':description, 'isbn10':isbn10,\
        'isbn13':isbn13, 'page_count':page_count}
    return parsed_dict
    