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

def insert_record(**kwargs):
    global connection
    values_dict={}
    for key,value in kwargs.items():
        if key not in get_column_names('books'):
            print('Invalid key: '+key)
            print('Please use a valid key from the following list: ' +str(get_column_names('books')) )
            raise Exception('Invalid key. Please use keys from the following list :'+ str(get_column_names('books')) )
        else:
            values_dict[key]=value
    keys_tuple=tuple(values_dict.keys())
    values_tuple=tuple(values_dict.values())
    if len(keys_tuple)==1:
        keys_string=str(keys_tuple).replace(',','')
        values_string=str(values_tuple).replace(',','')
    else:
        keys_string=str(keys_tuple)
        values_string=str(values_tuple)
    query_string="insert into books"+keys_string+" values"+values_string
    print(query_string)
    connection.execute(query_string)
    
