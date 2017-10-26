#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Mould.py
#  
#  Copyright 2017 Matthew Bennett <Bostin Technology>
#  
"""
    This program preovides a user interface that allows the mould data regarding
    the book to be captured and stored

    Requres the data in a specific format adn to be imported into the application

"""
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
from tkinter import *
import logging
import logging.config
import dict_Logging

import os
import sys
import os.path
import csv

import SystemSettings as SS

class MouldCapture(Frame):
    def __init__(self, master=None):
        Frame.__init__(self,master)

        # These are the tuples of what is selected in the listbox
        self.current_press = []
        self.current_shelf = []
        self.current_position = []

        #These are the check boxes
        self.head_mould = IntVar()
        self.spine_mould = IntVar()
        self.tail_mould = IntVar()
        self.front_board_mould = IntVar()
        self.rear_board_mould = IntVar()
        self.fore_edge_mould = IntVar()
        self.label_text = StringVar()
        self.label_text.set("Enter Book info")

        self.saved = False
        self.found = False
        
        # Build the header row
        header_frame = Frame(self, relief='ridge')
        Label(header_frame, text="Mould Capture").grid(row=0, column=0, sticky=W, padx=10)
        Label(header_frame, text="Bostin Technology").grid(row=0, column=4, sticky=E, padx=10)
        header_frame.grid(row=0, columnspan=2)

        # Build the Selection row
        selection_frame = Frame(self, relief='ridge')
        user = Button(selection_frame, text="User", command=self.user).grid(row=1, column=0, padx=5)
        self.press = Listbox(selection_frame, height=1, listvariable=self.current_press, selectmode=SINGLE )
        self.press.grid(row=1, column=1, padx=5)
        self.shelf = Listbox(selection_frame, height=1, listvariable=self.current_shelf, selectmode=BROWSE)
        self.shelf.grid(row=1, column=2, padx=5)
        self.position = Listbox(selection_frame, height=1, listvariable=self.current_position, selectmode=BROWSE)
        self.position.grid(row=1, column=3, padx=5)
        find_selection = Button(selection_frame, text='Find', command=self.find_book).grid(row=1, column=4, padx=5)
        selection_frame.grid(row=1, pady=5, columnspan=2)

        # Build the book display frame and the selection part
        book_frame = Frame(self, relief='ridge')
        self.book_info = Label(book_frame, relief='sunken', text="Enter Book Info", textvariable=self.label_text, width=30, height=20, wraplength=200)
        self.book_info.grid(row=0, column=0)
        book_frame.grid(row=2, column=0, pady=5, rowspan=2)

        #Build the Mould capture frame
        #mould_frame = Frame(self,relief='ridge')
        #head_mould = Checkbutton(mould_frame, text="Head", variable=self.head_mould, onvalue=1, offvalue=0)
        #spine_mould = Checkbutton(mould_frame, text="Spine", variable=self.spine_mould, onvalue=1, offvalue=0)
        #tail_mould = Checkbutton(mould_frame, text="Tail", variable=self.tail_mould, onvalue=1, offvalue=0)
        #front_board_mould = Checkbutton(mould_frame, text="Front Board", variable=self.front_board_mould, onvalue=1, offvalue=0)
        #rear_board_mould = Checkbutton(mould_frame, text="Rear Board", variable=self.rear_board_mould, onvalue=1, offvalue=0)
        #fore_edge_mould = Checkbutton(mould_frame, text="Fore Edge", variable=self.fore_edge_mould, onvalue=1, offvalue=0)
        #head_mould.grid(row=0, column=12, pady=10, padx=3)
        #spine_mould.grid(row=2, column=6, pady=10, padx=3)
        #tail_mould.grid(row=5, column=8, pady=10, padx=3)
        #front_board_mould.grid(row=2, column=12, pady=10, padx=3)
        #rear_board_mould.grid(row=4, column=16, pady=10, padx=3)
        #fore_edge_mould.grid(row=3, column=17, pady=10, padx=3)
        #exit_program = Button(mould_frame, text="Exit", command=self.exit_program).grid(row=6, column=20, padx=3)
        #save_data = Button(mould_frame, text="Save", command=self.save_data).grid(row=6, column=0, padx=3)
        #mould_frame.grid(row=2, column=1)
        
        # Build the book canvas picture
        mould_frame = Frame(self, relief='ridge')
        mould_book = Canvas(mould_frame, width=350, height=200, background='#ffffff')
        mould_book.create_polygon(130,40,230,50,220,170,120,160, outline="blue", fill="")
        mould_book.create_line(130,40,120,35,110,155,120,160, fill="blue")
        mould_book.create_line(120,35,220,45,230,50, fill="blue")
        mould_book.create_arc(190,125,290,190,outline="red",style="arc")
        #mould_book.create_rectangle(100, 50, 250, 175, fill="blue")

        head_mould = Checkbutton(mould_book, text="Head", variable=self.head_mould, onvalue=1, offvalue=0)
        spine_mould = Checkbutton(mould_book, text="Spine", variable=self.spine_mould, onvalue=1, offvalue=0)
        tail_mould = Checkbutton(mould_book, text="Tail", variable=self.tail_mould, onvalue=1, offvalue=0)
        front_board_mould = Checkbutton(mould_book, text="Front", variable=self.front_board_mould, onvalue=1, offvalue=0)
        rear_board_mould = Checkbutton(mould_book, text="Rear", variable=self.rear_board_mould, onvalue=1, offvalue=0)
        fore_edge_mould = Checkbutton(mould_book, text="Fore", variable=self.fore_edge_mould, onvalue=1, offvalue=0)
        
        head_mould_window = mould_book.create_window(150, 10, anchor=NW, window=head_mould)
        spine_mould_window = mould_book.create_window(20, 70, anchor=NW, window=spine_mould)
        tail_mould_window = mould_book.create_window(150, 180, anchor=NW, window=tail_mould)
        front_board_mould_window = mould_book.create_window(150, 90, anchor=NW, window=front_board_mould)
        rear_board_mould_window = mould_book.create_window(275, 170, anchor=NW, window=rear_board_mould)
        fore_edge_mould_window = mould_book.create_window(270, 100, anchor=NW, window=fore_edge_mould)
        mould_book.pack()

        mould_frame.grid(row=2, column=1)

        # identify when the listbox changes using the bind to <ListboxSelect> virtual event

        #TODO: Put exit and save in the mould_frame, but not on the canvas
        close_frame = Frame(self,relief='ridge')
        save_data = Button(close_frame, text="Save", command=self.save_data).grid(row=0, column=1, padx=40)
        exit_program = Button(close_frame, text="Exit", command=self.exit_program).grid(row=0, column=2, padx=40)
        close_frame.grid(row=3, column=1)

        # Put it all together on the screen
        self.pack(fill=BOTH, expand=NO)

        # Populate the drop downs
        for f in SS.PRESS_LIST:
            self.press.insert(END, f)

        for f in SS.SHELF_LIST:
            self.shelf.insert(END, f)
        
        for f in SS.POSITION_LIST:
            self.position.insert(END, f)

        # Set initial selection
        self.position.select_set(0)
        self.shelf.select_set(0)
        self.press.select_set(0)
                    
        self.UpdateBookText("Please Select a Press, Row and shelf then click on Find")


    def user(self):
        # called form the capture button
        logging.debug("Selecting User")
        return

    def find_book(self):
        """
        Using the data given, find the book in the list and populate the book info box
        """

        if self.saved == False:
            print("Data not saved, do you want to continue?")
        
        logging.info("Finding the Book reference:%s" % (self.press.get(ACTIVE)))
        book_ref = self.press.get(ACTIVE) + '.' + self.shelf.get(ACTIVE) + '.' + self.position.get(ACTIVE)
     
        self.UpdateBookText("Finding Book:%s" % book_ref)

        if book_ref in self.booklist:
            print(self.booklist[book_ref])
            self.found = True
            book_info = self.booklist[book_ref]['Location'] +"\n" + self.booklist[book_ref]['Title'] + "\n" + self.booklist[book_ref]['Creator']        #if self.booklist[book_ref]
        else:
            book_info = "Reference not found, please continue"
            self.found = False

        self.UpdateBookText(book_info)
        return

    def BookData(self, booklist):
        """
        Get given a dictionary containing all the books in the library
        """
        self.booklist = booklist
        
        return

    def UpdateBookText(self, information):
        """
        Repalce the existing text in the book text box and reaplce it with information
        """

        #TODO: This currently adds the text to the existing text, not replace it
        
        logging.info("Text to be added into the Book Text Box:%s" % information)
        self.label_text.set(information)
        return     

    def save_data(self):
        # called on click on save
        # needs to capture the values annd save them to the csv file.

        data_to_save = []
        book_ref = self.press.get(ACTIVE) + '.' + self.shelf.get(ACTIVE) + '.' + self.position.get(ACTIVE)
        data_to_save.append(book_ref)
        data_to_save.append(self.head_mould.get())
        data_to_save.append(self.spine_mould.get())
        data_to_save.append(self.tail_mould.get())
        data_to_save.append(self.front_board_mould.get())
        data_to_save.append(self.rear_board_mould.get())
        data_to_save.append(self.fore_edge_mould.get())
        data_to_save.append(self.found)

        logging.info("data to be saved to csv:%s" % data_to_save)

        filename = SS.USB_LOCATION + '/' + SS.MOULDDATA_NAME
        if os.path.exists(SS.USB_LOCATION):
            logging.debug("[CTRL] Book File in location:%s" % filename)
            with open(filename, mode='a', newline='') as csvfile:
                    record = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    record.writerow(data_to_save)
                
            self.saved = True
        return
        
    def exit_program(self):
        # called form the capture button
        logging.debug("Exiting Program")
        exit()
        return
        
def SetupLogging():
    """
    Setup the logging defaults
    Using the logger function to span multiple files.
    """
    global gbl_log
    # Create a logger with the name of the function
    logging.config.dictConfig(dict_Logging.log_cfg)
    gbl_log = logging.getLogger()

    gbl_log.info("\n\n")
    gbl_log.info("[CTRL] Logging Started, current level is %s" % gbl_log.getEffectiveLevel())

    return

def LoadData():
    """
    Load the data from the USB stick
    """
    bookdata = {}
    print("Loading Book Data")
    gbl_log.info("[CTRL] Reading the book data")
    filename = SS.USB_LOCATION + '/' + SS.BOOKFILE_NAME
    if os.path.isfile(filename):
        gbl_log.debug("[CTRL] Book File in location:%s" % filename)
        with open(filename, 'r') as book:
            #bookdata = csv.DictReader(book)
            for row in csv.DictReader(book):
                # A row of data looks like
                #{'Location': 'L.3.10', 'Creator': 'Charles Dickens (1812-1870).', 'CMS': '3045432',
                    #'Title': 'The life and adventures of Martin Chuzzlewit. '}
                bookdata[row['Location']] = row

    else:
        gbl_log.error("[CTRL] Unable to find book data, program aborted")
        sys.exit()
    gbl_log.info("Book Data Loaded:%s" % bookdata)
    return bookdata
        
def main():

    SetupLogging()

    root = Tk()
    app = MouldCapture(master=root)
    app.master.title("Mould Capturing Tool")
    app.BookData(LoadData())
    # do something here
    app.mainloop()
    return

if __name__ == '__main__':
	main()

