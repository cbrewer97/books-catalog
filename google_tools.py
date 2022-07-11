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