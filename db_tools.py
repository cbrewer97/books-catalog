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
    print('Created file books.db ')
    
def get_column_names(table_name):
    global connection
    description_tuple=connection.execute("select * from "+table_name+" ").description
    names=[]
    for item in description_tuple:
        names.append(item[0])
    return names

def get_tables():
    global connection
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
            raise Exception('Invalid key. Please use keys from the following list: '+ str(get_column_names('books')) )
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
    connection.commit()
    
def create_books_table():
    global connection
    connection.execute('create table books(id integer primary key, \
        title text, authors text, publisher text, publish_date text, \
        description text, isbn10 integer, isbn13 integer, \
        page_count integer, image_path text )')
    connection.commit()
        
def is_integer(value):
    flag=False
    if type(value)==type('string'):
        flag=value.isdigit()
    elif type(value)==type(1):
        flag=True
    return flag

def search_books(**kwargs):
    query_string="select * from books"
    if len(kwargs)>0:
        query_string=query_string+" where "
    for key, value in kwargs.items():
        if key not in get_column_names('books'):
            raise Exception('Invalid key. Please use keys from the following list: '+ str(get_column_names('books')) )
        elif is_integer(value):
            query_string=query_string+key+"="+str(value)+" and "
        elif type(value)==type('string'):
            query_string=query_string+key+" like '%"+value+"%' and "
    query_string=query_string.strip("and ")
    return connection.execute(query_string).fetchall()
            
            
