# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 13:53:00 2022

@author: books
"""

import tkinter as tk
from idlelib.tooltip import Hovertip
from tkinter import ttk
import db_tools as dbt
import google_tools as gt
from tkscrolledframe import ScrolledFrame




# Here is a rough outline of the widget hierarchy
#
# root
# -main_frame
#   -navigation frame
#     -My books button
#     -Google books button
#   -search frame
#     -attribute labels
#     -search fields
#   -my books frame
#     -result frames
#       -attribute labels
#       -value labels
#
#
#
#


class MyBooksSearchFrame:
    def __init__(self, main_frame,my_books_frame):
        self.frame=ttk.Frame(main_frame)
        self.frame.grid(row=1)
        print(self.frame.grid_size())
        
        title_search_label=ttk.Label(self.frame, text="Title: ")
        author_search_label=ttk.Label(self.frame, text="Author: ")
        date_search_label=ttk.Label(self.frame, text="Date: ")
        isbn_search_label=ttk.Label(self.frame, text="ISBN: ")
        tags_search_label=ttk.Label(self.frame, text="Tags: ")
        self.search_labels={'title': title_search_label,\
                            'author':author_search_label,\
                            'date':date_search_label,\
                            'isbn':isbn_search_label,\
                            'tags':tags_search_label}
        
        title_text_variable=tk.StringVar()
        author_text_variable=tk.StringVar()
        date_text_variable=tk.StringVar()
        isbn_text_variable=tk.StringVar()
        tags_text_variable=tk.StringVar()
        self.text_vars={'title': title_text_variable,\
                        'author': author_text_variable,\
                        'date': date_text_variable,\
                        'isbn': isbn_text_variable,\
                        'tags': tags_text_variable}
        
        title_search_field=ttk.Entry(self.frame, textvariable=title_text_variable)
        author_search_field=ttk.Entry(self.frame, textvariable=author_text_variable)
        date_search_field=ttk.Entry(self.frame, textvariable=date_text_variable)
        isbn_search_field=ttk.Entry(self.frame, textvariable=isbn_text_variable)
        tags_search_field=ttk.Entry(self.frame, textvariable=tags_text_variable)
        self.search_fields={'title': title_search_field,\
                            'author': author_search_field,\
                            'date': date_search_field,\
                            'isbn': isbn_search_field,\
                            'tags': tags_search_field}
            
        for index, label in enumerate([title_search_label, author_search_label, date_search_label, isbn_search_label, tags_search_label]):
            label.grid(row=index, column=0)
            
        for index, field in enumerate([title_search_field, author_search_field, date_search_field, isbn_search_field, tags_search_field]):
            field.grid(row=index, column=1, sticky='w')
            
        self.search_button=ttk.Button(self.frame, text="Search", \
                    command=lambda:my_books_frame.populate_result_frames(\
                                title=self.text_vars['title'].get(), \
                                author=self.text_vars['author'].get()))
        self.search_button.grid(row=self.frame.grid_size()[1], column=1, sticky='e')

        self.clear_button=ttk.Button(self.frame, text='Clear', command=lambda: my_books_frame.clear_books_results())
        self.clear_button.grid(row=self.frame.grid_size()[1]-1, column=0)
        

    

class BookFrame():
    def __init__(self, book_dict, parent):
        self.frame=ttk.Frame(parent)
        for index, tup in enumerate(book_dict.items()):
            key=tup[0]
            value=tup[1]
            attribute_string=str(key)+" :"
            attribute_label=ttk.Label(self.frame,text=attribute_string)
            value_label=ttk.Label(self.frame, text=str(value), wraplength=200)
            attribute_label.grid(row=index+1, column=1,sticky='')
            value_label.grid(row=index+1, column=2,sticky='w')
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=2)
        
class GoogleBooksBookFrame():
    def __init__(self, book_dict, parent):
        self.frame=ttk.Frame(parent)
        for index, tup in enumerate(book_dict.items()):
            key=tup[0]
            value=tup[1]
            attribute_string=str(key)+" :"
            attribute_label=ttk.Label(self.frame,text=attribute_string)
            value_label=ttk.Label(self.frame, text=str(value), wraplength=200)
            attribute_label.grid(row=index+1, column=1,sticky='')
            value_label.grid(row=index+1, column=2,sticky='w')
        import_button=ttk.Button(self.frame, text='Import', command=lambda: [dbt.insert_record(**book_dict), print('World')])
        import_button.grid(row=len(book_dict.items())+1, column=2, sticky='e')
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=2)

class MyBooksFrame():
    def __init__(self, main_frame):
        self.container_frame=ttk.Frame(main_frame)
        self.container_frame.grid(row=1, sticky='ns' )
        
        search_frame=MyBooksSearchFrame(self.container_frame,self)
        
        scrolled_frame=ScrolledFrame(self.container_frame, scrollbars='vertical',use_ttk=True )
        scrolled_frame.grid(row=2, sticky='ns')
        scrolled_frame.bind_arrow_keys(root)
        scrolled_frame.bind_scroll_wheel(root)
        widget_class=ttk.Frame
        books_frame=scrolled_frame.display_widget(widget_class,fit_width=True)
        self.results_frame=books_frame
        self.results_frame['borderwidth']=5
        self.results_frame['relief']='sunken'
        
    
    def populate_result_frames(self, title, author):
        #title=title_text_variable.get()
        search_results=dbt.search_books(title=title, authors=author)
        
        for result in search_results:
            book_dict=dbt.as_dict(result)
            result_frame=BookFrame(book_dict, self.results_frame).frame
            result_frame['borderwidth']=5
            result_frame['relief']='sunken'
            grid_size=self.results_frame.grid_size()
            print(grid_size)
            result_frame.grid(row=grid_size[1]+1, column=0, sticky='w')

            
    def clear_books_results(self):
        children=self.results_frame.winfo_children()
        for child in children:
            child.destroy()
        self.results_frame.grid_forget()
        
class GoogleBooksSearchFrame:   
    def __init__(self, parent, google_books_frame):
        self.frame=ttk.Frame(parent)
        self.frame.grid(row=1, sticky='ns')
        
        title_search_label=ttk.Label(self.frame, text='Title: ')
        author_search_label=ttk.Label(self.frame, text='Author: ')
        isbn_search_label=ttk.Label(self.frame, text="ISBN: ")
        
        self.title_text_variable=tk.StringVar()
        self.author_text_variable=tk.StringVar()
        self.isbn_text_variable=tk.StringVar()
        
        title_search_field=ttk.Entry(self.frame, textvariable=self.title_text_variable)
        author_search_field=ttk.Entry(self.frame,textvariable=self.author_text_variable)
        isbn_search_field=ttk.Entry(self.frame, textvariable=self.isbn_text_variable)
        
        title_search_label.grid(row=1, column=1)
        title_search_field.grid(row=1, column=2)
        author_search_label.grid(row=2, column=1)
        author_search_field.grid(row=2, column=2)
        isbn_search_label.grid(row=3, column=1)
        isbn_search_field.grid(row=3, column=2, sticky='w')
        
        search_button=ttk.Button(self.frame, text='Search', command=lambda: google_books_frame.populate_result_frames(title=self.title_text_variable.get(), author=self.author_text_variable.get(),isbn=self.isbn_text_variable.get()))
        clear_button=ttk.Button(self.frame, text='Clear', command=lambda: google_books_frame.clear_books_results())
        search_button.grid(row=4, column=2, sticky='e')
        clear_button.grid(row=4, column=1)
        
        hovertip=Hovertip(search_button, 'Ollo World\nUh sir, it\'s pronounced \"Hello\"')
        
        
class GoogleBooksFrame():
    def __init__(self, main_frame):
        self.container_frame=ttk.Frame(main_frame)
        self.container_frame.grid(row=1, sticky='ns')
        google_search_frame=GoogleBooksSearchFrame(self.container_frame, self)
        scrolled_frame=ScrolledFrame(self.container_frame, scrollbars='vertical',use_ttk=True , )
        scrolled_frame.grid(row=2, sticky='ns')
        scrolled_frame.bind_arrow_keys(root)
        scrolled_frame.bind_scroll_wheel(root)
        widget_class=ttk.Frame
        books_frame=scrolled_frame.display_widget(widget_class,fit_width=True)
        self.results_frame=books_frame
        self.results_frame['borderwidth']=5
        self.results_frame['relief']='sunken'
        
    def populate_result_frames(self, title=None, author=None, isbn=None):
        
        
        search_results=gt.search_google_books(title=title, author=author, isbn=isbn, num_results=4, verbose=True)
        
        parsed_search_results=[]
        for item in search_results:
            parsed_search_results.append(gt.parse_google_record(item))
        
        for result in parsed_search_results:
            result_frame=GoogleBooksBookFrame(result, self.results_frame).frame
            result_frame['borderwidth']=5
            result_frame['relief']='sunken'
            grid_size=self.results_frame.grid_size()
            print(grid_size)
            result_frame.grid(row=grid_size[1]+1, column=0, sticky='w')
            
    def clear_books_results(self):
        children=self.results_frame.winfo_children()
        for child in children:
            child.destroy()
        self.results_frame.grid_forget()

class NavigationFrame():
    def __init__(self, parent, my_books_frame, google_books_frame):
        self.frame=ttk.Frame(parent)
        self.frame.grid(row=0, sticky='nsew')
        my_books_button=ttk.Button(self.frame, text="My Books", command=lambda: my_books_frame.container_frame.lift())
        my_books_button.grid(row=1,column=2)

        google_search_button=ttk.Button(self.frame, text="Google Books", command=lambda: google_books_frame.container_frame.lift())
        google_search_button.grid(row=1, column=3)

root=tk.Tk()




def main():
    main_frame=ttk.Frame(root)
    main_frame.pack(fill='both', expand=True)


    #navigation_frame=NavigationFrame(main_frame)


    my_books_frame=MyBooksFrame(main_frame)
    my_books_frame.container_frame.grid(row=1, sticky='nsew')
    
    google_books_frame=GoogleBooksFrame(main_frame)
    
    navigation_frame=NavigationFrame(main_frame, my_books_frame, google_books_frame)
    
    
    

    main_frame.grid_rowconfigure((0,1), weight=0)
    main_frame.grid_rowconfigure(2, weight=1)
    main_frame.columnconfigure(0, weight=1)
    root.mainloop()
    
main()

