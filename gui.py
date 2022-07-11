# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 13:53:00 2022

@author: books
"""

from tkinter import *
from tkinter import ttk

root=Tk()

main_frame=ttk.Frame(root, width='800', height='600')
main_frame.grid(sticky='nsew')
main_frame.grid_propagate(0)


navigation_frame=ttk.Frame(main_frame)
navigation_frame.grid(row=1, sticky='nsew')


my_books_button=ttk.Button(navigation_frame, text="My Books")
my_books_button.grid(row=1,column=2)

google_search_button=ttk.Button(navigation_frame, text="Google Books")
google_search_button.grid(row=1, column=3)




my_books_frame=ttk.Frame(main_frame)
my_books_frame.grid(row=2)

title_search_label=ttk.Label(my_books_frame, text="Title: ")
author_search_label=ttk.Label(my_books_frame, text="Author: ")
date_search_label=ttk.Label(my_books_frame, text="Date: ")
isbn_search_label=ttk.Label(my_books_frame, text="ISBN: ")
tags_search_label=ttk.Label(my_books_frame, text="Tags: ")

title_search_field=ttk.Entry(my_books_frame)
author_search_field=ttk.Entry(my_books_frame)
date_search_field=ttk.Entry(my_books_frame)
isbn_search_field=ttk.Entry(my_books_frame)
tags_search_field=ttk.Entry(my_books_frame)


for index, label in enumerate([title_search_label, author_search_label, date_search_label, isbn_search_label, tags_search_label]):
    label.grid(row=index+1, column=1)
    
for index, field in enumerate([title_search_field, author_search_field, date_search_field, isbn_search_field, tags_search_field]):
    field.grid(row=index+1, column=2, sticky='w')
    
    
def create_book_frame(book_dict,parent):
    book_frame=ttk.Frame(parent)
    for index, tup in enumerate(book_dict.items()):
        key=tup[0]
        value=tup[1]
        attribute_string=str(key)+" :"
        attribute_label=ttk.Label(book_frame,text=attribute_string)
        value_label=ttk.Label(book_frame, text=str(value), wraplength=100)
        attribute_label.grid(row=index+1, column=1)
        value_label.grid(row=index+1, column=2)
    return book_frame

from db_tools import *

search_results=search_books(title='Great')
book_tuple=search_results[0]
book_dict=as_dict(book_tuple)

result_frame=create_book_frame(book_dict, my_books_frame)
result_frame.grid(row=6, column=1)


root.mainloop()