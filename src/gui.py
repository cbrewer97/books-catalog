# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 13:53:00 2022

@author: books
"""

import tkinter as tk
from tkinter import ttk
import db_tools as dbt
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






# my_books_frame=ttk.Frame(main_frame)
# my_books_frame.grid(row=2)

class SearchFrame:
    def __init__(self, main_frame):
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
                    command=lambda:populate_result_frames(\
                                title=self.text_vars['title'].get(), \
                                author=self.text_vars['author'].get()))
        self.search_button.grid(row=self.frame.grid_size()[1], column=1, sticky='e')

        self.clear_button=ttk.Button(self.frame, text='Clear', command=clear_books_results)
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


class MyBooksFrame():
    def __init__(self, main_frame):
        scrolled_frame=ScrolledFrame(main_frame, scrollbars='vertical',use_ttk=True )
        scrolled_frame.grid(row=2, sticky='ns')
        scrolled_frame.bind_arrow_keys(root)
        scrolled_frame.bind_scroll_wheel(root)
        widget_class=ttk.Frame
        books_frame=scrolled_frame.display_widget(widget_class,fit_width=True)
        self.frame=books_frame
        self.frame['borderwidth']=5
        self.frame['relief']='sunken'
        
def populate_result_frames(title, author):
    #title=title_text_variable.get()
    search_results=dbt.search_books(title=title, authors=author)
    
    for result in search_results:
        book_dict=dbt.as_dict(result)
        result_frame=BookFrame(book_dict, my_books_frame.frame).frame
        result_frame['borderwidth']=5
        result_frame['relief']='sunken'
        grid_size=my_books_frame.frame.grid_size()
        print(grid_size)
        result_frame.grid(row=grid_size[1]+1, column=0, sticky='w')
        #result_frame.pack(fill='x',expand=True ,side='top')
        # result_frame.grid(row=row_number,column=1,sticky='ew')
        # result_frame.grid_columnconfigure(0, weight=1)
        # result_frame.grid_rowconfigure(0 ,weight=1)
        #row_number+=1
        
def clear_books_results():
    children=my_books_frame.frame.winfo_children()
    for child in children:
        child.destroy()
    my_books_frame.frame.grid_forget()


#search_results=search_books()
# book_tuple=search_results[0]
# book_dict=as_dict(book_tuple)

# result_frame=create_book_frame(book_dict, my_books_frame)
# result_frame.grid(row=6, column=1)




        


# for result in search_results:
#     book_dict=as_dict(result)
#     result_frame=create_book_frame(book_dict, my_books_frame)
#     result_frame['borderwidth']=5
#     result_frame['relief']='sunken'
#     grid_size=my_books_frame.grid_size()
#     result_frame.grid(row=grid_size[0], column=0, sticky='w')
#     #result_frame.pack(fill='x',expand=True ,side='top')
#     # result_frame.grid(row=row_number,column=1,sticky='ew')
#     # result_frame.grid_columnconfigure(0, weight=1)
#     # result_frame.grid_rowconfigure(0 ,weight=1)
#     row_number+=1

root=tk.Tk()

main_frame=ttk.Frame(root)
main_frame.pack(fill='both', expand=True)
#main_frame.grid(sticky='nsew')
#main_frame.grid_propagate(0)


navigation_frame=ttk.Frame(main_frame)
navigation_frame.grid(row=0, sticky='nsew')


my_books_button=ttk.Button(navigation_frame, text="My Books")
my_books_button.grid(row=1,column=2)

google_search_button=ttk.Button(navigation_frame, text="Google Books")
google_search_button.grid(row=1, column=3)

search_frame=SearchFrame(main_frame)
print(search_frame.frame.grid_size())

my_books_frame=MyBooksFrame(main_frame)

main_frame.grid_rowconfigure((0,1), weight=0)
main_frame.grid_rowconfigure(2, weight=1)
main_frame.columnconfigure(0, weight=1)
root.mainloop()

def main():
    pass

