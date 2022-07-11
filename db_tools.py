# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 17:59:40 2022

@author: books
"""

from os.path import exists

import sqlite3

if exists('books.db'):
    connection=sqlite3.connect('books.db')
    print('books.db found. Connected to db.')
else:
    connection=sqlite3.connect('books.db')
    
def get_column_names(table_name):
    global connection
    description_tuple=connection.execute("select * from "+table_name+" ").description
    names=[]
    for item in description_tuple:
        names.append(item[0])
    return names

def get_tables():
    results=connection.execute("select name from sqlite_master where type='table';")
    tables=results.fetchall()
    return tables

    