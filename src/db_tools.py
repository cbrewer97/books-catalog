# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 17:59:40 2022

@author: books
"""

from os.path import exists
import google_tools as gt
import sqlite3

if exists('books.db'):
    connection=sqlite3.connect('books.db')
    print('books.db found. Connected to db.')
else:
    connection=sqlite3.connect('books.db')
    print('Created file books.db ')
    
def get_column_names(table_name):
    """
Return a list of column names from given table.

:param table_name: Name of table to access
:type table_name: str
:return: List of column names.
:rtype: list[str]

"""
    global connection
    description_tuple=connection.execute("select * from "+table_name+" ").description
    names=[]
    for item in description_tuple:
        names.append(item[0])
    return names

def get_tables():
    """
    Returns a list of tuples, where each tuple contains \
        the name of one table in the db.    
    """
    global connection
    results=connection.execute("select name from sqlite_master where type='table';")
    tables=results.fetchall()
    return tables

def insert_record(**kwargs):
    """
    Inserts a new record to the books table
    
    :param **kwargs: optional arguments with keyname equal \
        to a column name of the books table. Keynames not \
        supplied will default to value None.
        
    :returns: None
    
    """
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
    #print(query_string)
    connection.execute(query_string)
    connection.commit()
    
def create_books_table():
    """
    Creates table with name "books"
    
    Creates the following columns and types:
        
        id integer primary key, \
            title text, authors text, publisher text, publish_date text, \
            description text, isbn10 integer, isbn13 integer, \
            page_count integer, notes text, tags text, \
            image_path text
            
    :param: None
    :returns: None

    """
    global connection
    connection.execute('create table books(id integer primary key, \
        title text, authors text, publisher text, publish_date text, \
        description text, isbn10 integer, isbn13 integer, \
        page_count integer, notes text, tags text, \
        image_path text )')
    connection.commit()
        
def is_integer(value):
    """
    Convenience function to test if argument is of int type, \
        or if it is a string that can be cast to int.
    
    :param value: 
    :type value: str or int
    :rtype: bool
    """
    flag=False
    if type(value)==type('string'):
        flag=value.isdigit()
    elif type(value)==type(1):
        flag=True
    return flag

def search_books(**kwargs):
    """
    Searches the books table. For each argument supplied, \
        returns the records for which that argument is IN \
        (substring) the row\'s corresponding cell. Returned \
        records must satisfy ALL supplied conditions.
    
    :param **kwargs: Optional arguments with keyname equal \
        to some column name from books table.
    :returns: list of tuples, where each tuple is a row \
        with values in the same order as the columns.
    """
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

def as_dict(result_tuple):
    """
    Converts a result_tuple to a dictionary, where the \
        dictionary keys are the corresponding column \
        names and the values are the entries of the tuple.
        
    :param result_tuple: tuple of values representing a row \
        of the table
    :type result_tuple: tuple
    :returns: dictionary with same values as result_tuple, \
        with keynames given by the corresponding column names.
    :rtype: dict 
    """
    results_dict=dict()
    keys=get_column_names('books')
    for index, result in enumerate(result_tuple):
        key=keys[index]
        results_dict[key]=result
    return results_dict

def clean_description_string(book_dict):
    """
    Removes [backslash \'] and [backslash \"] from the description string of \
        book_dict so that it doesn't cause errors when \
        inserting to the db.
        
    :param book_dict: dictionary representing a row of the \
        books table
    :type book_dict: dict
    :returns: dictionary representing a row of the books \
        which is same as books_dict, except that the \
        description is cleaned
    :rtype: dict
    """
    book_dict['description']=book_dict['description'].replace("\'",'').replace("\"", '')
    return book_dict

            
def batch_import(file_path):
    with open(file_path, 'r') as file:
        line_number=1
        failed_lines=[]
        for line in file:
            try:
                isbn=line.strip()
                result=gt.search_google_books(isbn=isbn)[0]
                result=gt.parse_google_record(result)
                result=clean_description_string(result)
                insert_record(**result)
                print('Inserted record.')
            except Exception:
                print('Failed to import record: '+line.strip()+'. Continuing next line.')
                line_tuple=(line_number, line.strip())
                failed_lines.append(line_tuple)
            line_number+=1
        print('')
        print('Import completed.\n')
        if len(failed_lines)!=0:
            print('Failed to import '+str(len(failed_lines))+' records.')
            print('Failed lines:')
            print(failed_lines)
            
      
