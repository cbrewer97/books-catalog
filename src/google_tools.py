# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 09:32:31 2022

@author: books
"""

import requests
import json

def search_google_books(author=None, isbn=None, title=None, num_results=1, language="en", verbose=False):
    """
    Searches for book information from the Google Books API. \
        Information is first retreived in JSON format, and \
        then parsed to a list of dictionaries.
    
    :param author: Part of author name (first and/or last)
    :type author: str
    :param isbn: ISBN10 or ISBN13
    :type isbn: str or int
    :param title: Part of the book title
    :type title: str
    :param num_results: Number of results to be returned
    :type num_results: int
    :param language: String of the 2-character laguage code\
        for the desired language
    :type language: str
    
    """
    query_url="https://www.googleapis.com/books/v1/volumes?q="
    if author!=None and author!='':
        query_url=query_url+"inauthor:"+author+"+"
    if isbn!=None and isbn!='':
       query_url=query_url+"isbn:"+isbn +"+"
    if title!=None and title!='':
        query_url=query_url+"intitle:"+title
    query_url=query_url.strip("+")
    query_url=query_url+"&langRestrict="+language
        
    #query_url=query_url.strip("&")
        
    if verbose==True:
        print(query_url)
    r=requests.get(query_url)
    return json.loads(r.text)['items'][0:num_results]

def parse_google_record(record):
    """
    Removes unnecessary key/values from record and returns a \
        dictionary with only necessary key/values.
        
    :param record: dictionary representing a book
    :type record: dict
    :returns: dictionary with only necessary key/values
    :rtype: dict
    """
    try:
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
    except:
        print('Error occured.')