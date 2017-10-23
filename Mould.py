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

        # Build the header row
        header_frame = Frame(self, relief='ridge')
        Label(header_frame, text="Mould Capture").grid(row=0, column=0, sticky=W, padx=10)
        Label(header_frame, text="Bostin Technology").grid(row=0, column=4, sticky=E, padx=10)
        header_frame.grid(row=0)

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
        selection_frame.grid(row=1, pady=5)

        # Build the book display frame and the selection part
        book_frame = Frame(self, relief='ridge')
        self.book_info = Text(book_frame, relief='sunken', state=DISABLED, wrap=WORD)
        self.book_info.grid(row=2, column=0)
        book_frame.grid(row=2, column=0, pady=5)

        #Build the Mould capture frame
        mould_frame = Frame(self,relief='ridge')
        head_mould = Checkbutton(mould_frame, text="Head", variable=self.head_mould, onvalue=1, offvalue=0)
        spine_mould = Checkbutton(mould_frame, text="Spine", variable=self.spine_mould, onvalue=1, offvalue=0)
        tail_mould = Checkbutton(mould_frame, text="Tail", variable=self.tail_mould, onvalue=1, offvalue=0)
        front_board_mould = Checkbutton(mould_frame, text="Front Board", variable=self.front_board_mould, onvalue=1, offvalue=0)
        rear_board_mould = Checkbutton(mould_frame, text="Rear Board", variable=self.rear_board_mould, onvalue=1, offvalue=0)
        fore_edge_mould = Checkbutton(mould_frame, text="Fore Edge", variable=self.fore_edge_mould, onvalue=1, offvalue=0)
        head_mould.grid(row=0, column=3)
        spine_mould.grid(row=3, column=0)
        tail_mould.grid(row=5, column=2)
        front_board_mould.grid(row=2, column=3)
        rear_board_mould.grid(row=4, column=5)
        fore_edge_mould.grid(row=3, column=4)
        mould_frame.grid(row=2, column=1)
        exit_program = Button(mould_frame, text="Exit", command=self.exit_program).grid(row=4, column=1, padx=5)

        # Build the book canvas picture
#        book_frame = Frame(self, relief='ridge')
#        book = Canvas(book_frame, width=200, height=300)
#        book.create_rectangle(10, 10, 50, 50, fill="blue")
#        book.pack()
#
#        book_frame.grid(row=2, column=1)

        # identify when the listbox changes using the bind to <ListboxSelect> virtual event

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
        logging.info("Finding the Book reference:%s" % (self.press.get(ACTIVE)))
        book_ref = self.press.get(ACTIVE) + '.' + self.shelf.get(ACTIVE) + '.' + self.position.get(ACTIVE)
     
        self.UpdateBookText("Finding Book:%s" % book_ref)

        
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
        self.book_info.config(state=NORMAL)
        self.book_info.insert(END, information)
        self.book_info.config(state=DISABLED)       

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
            bookdata = csv.DictReader(book)
            #BUG: bookdata is only accessible whilst the file is open and the line below therefore fails
        for row in bookdata:
            print(row['CMS'])
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

