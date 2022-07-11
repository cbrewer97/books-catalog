# -*- coding: utf-8 -*-
"""
Created on Sun Jul 10 13:14:41 2022

@author: books
"""

#Need to set up the database
#Here is a list of fields I can access from Google Books that would be useful
#  title, authors, publisher, publish date, description, isbn10, isbn13, page count, image link, text snippet
#I should probably add a field that tracks the path to the image file

#To get a URL
#  r=requests.get('URL string')
#The raw text (html or json text) is
#  text=r.text
#In the case of json output (like from Google Books API) we can convert to dict by
#  my_dict=json.loads(text)
#Then all the attributes can be accessed like normal using the keys
#
#
#


from tkinter import *
from tkinter import ttk



root=Tk()
#frame1=ttk.Frame(root, width=800, height=600,borderwidth=5,relief='sunken').grid()

counter=0
def toggle():
    global counter
    if counter==0:
        counter=1
        frame2.lift()
    else:
        counter=0
        frame3.lift()
    print(counter)


frame2=ttk.Frame(root,height=200, width=200,borderwidth=5,relief='sunken') 
frame2.grid(column=1,row=2)
label2=ttk.Label(frame2,text='label for frame2')
label2.grid(column=1,row=2)

frame3=ttk.Frame(root,height=200, width=200,borderwidth=5,relief='sunken')
frame3.grid(column=1,row=2)
label3=ttk.Label(frame3,text='label for frame3')
label3.grid(column=1,row=2)

ttk.Button(root, text='frame2', command=lambda: toggle).grid(column=1,row=1)
ttk.Button(root, text='frame3', command=toggle).grid(column=2,row=1)



#frame1.tkraise()

#frame1=ttk.Frame(root).grid(column=1, row=1,sticky='E')


root.mainloop()