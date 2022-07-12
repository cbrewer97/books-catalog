# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 13:53:00 2022

@author: books
"""

from tkinter import *
from tkinter import ttk

root=Tk()

main_frame=ttk.Frame(root)
main_frame.grid(sticky='nsew')
#main_frame.grid_propagate(0)


navigation_frame=ttk.Frame(main_frame)
navigation_frame.grid(row=1, sticky='nsew')


my_books_button=ttk.Button(navigation_frame, text="My Books")
my_books_button.grid(row=1,column=2)

google_search_button=ttk.Button(navigation_frame, text="Google Books")
google_search_button.grid(row=1, column=3)




# my_books_frame=ttk.Frame(main_frame)
# my_books_frame.grid(row=2)



search_frame=ttk.Frame(main_frame)
search_frame.grid(row=2)

title_search_label=ttk.Label(search_frame, text="Title: ")
author_search_label=ttk.Label(search_frame, text="Author: ")
date_search_label=ttk.Label(search_frame, text="Date: ")
isbn_search_label=ttk.Label(search_frame, text="ISBN: ")
tags_search_label=ttk.Label(search_frame, text="Tags: ")

title_search_field=ttk.Entry(search_frame)
author_search_field=ttk.Entry(search_frame)
date_search_field=ttk.Entry(search_frame)
isbn_search_field=ttk.Entry(search_frame)
tags_search_field=ttk.Entry(search_frame)


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
        value_label=ttk.Label(book_frame, text=str(value), wraplength=200)
        attribute_label.grid(row=index+1, column=1,sticky='')
        value_label.grid(row=index+1, column=2,sticky='w')
    book_frame.grid_columnconfigure(1, weight=1)
    book_frame.grid_columnconfigure(2, weight=2)
    return book_frame

from db_tools import *


from tkscrolledframe import ScrolledFrame

scrolled_frame=ScrolledFrame(main_frame, scrollbars='vertical',use_ttk=True )
scrolled_frame.grid(row=3)
scrolled_frame.bind_arrow_keys(root)
scrolled_frame.bind_scroll_wheel(root)
my_books_frame=scrolled_frame.display_widget(Frame,fit_width=True)
my_books_frame['borderwidth']=5
my_books_frame['relief']='sunken'


search_results=search_books()
# book_tuple=search_results[0]
# book_dict=as_dict(book_tuple)

# result_frame=create_book_frame(book_dict, my_books_frame)
# result_frame.grid(row=6, column=1)

row_number=6
for result in search_results:
    book_dict=as_dict(result)
    result_frame=create_book_frame(book_dict, my_books_frame)
    result_frame['borderwidth']=5
    result_frame['relief']='sunken'
    result_frame.pack(fill='x',expand=True ,side='top')
    # result_frame.grid(row=row_number,column=1,sticky='ew')
    # result_frame.grid_columnconfigure(0, weight=1)
    # result_frame.grid_rowconfigure(0 ,weight=1)
    row_number+=1



root.mainloop()