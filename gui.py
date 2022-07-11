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


for label in [title_search_label, author_search_label, date_search_label, isbn_search_label, tags_search_label]:
    label.pack()


root.mainloop()