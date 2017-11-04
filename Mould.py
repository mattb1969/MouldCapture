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

#TODO: After save, clear all the mould settings
#TODO: Show the date on screen
#TODO: Make all the buttons bigger
#TODO: Add descriptions to whatn is held in the text box, e.g. Location: Title: Creator:

from tkinter import *
from tkinter.ttk import *
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

        gbl_log.info("Starting Main Frame")
        # These are the tuples of what is selected in the listbox
        self.current_press = StringVar()
        self.current_shelf = StringVar()
        self.current_position = StringVar()
        self.current_day = StringVar()
        self.current_month = StringVar()
        self.current_year = StringVar()
        self.user = StringVar()

        #These are the check boxes
        self.head_mould = IntVar()
        self.spine_mould = IntVar()
        self.tail_mould = IntVar()
        self.front_board_mould = IntVar()
        self.rear_board_mould = IntVar()
        self.fore_edge_mould = IntVar()
        self.label_text = StringVar()
        self.label_text.set("Enter Book info")

        self.saved = True
        self.found = False
        self.warned = False

        # Build the Selection row
        selection_frame = Frame(self, relief='ridge')
        self.user = Combobox(selection_frame, height=20, textvariable=self.user, width=20,values=SS.USERS)
        self.user.grid(row=1, column=0, padx=50)
        self.press = Combobox(selection_frame, height=20, textvariable=self.current_press, width=10, values=SS.PRESS_LIST)
        self.press.grid(row=1, column=2, padx=10)
        self.shelf = Combobox(selection_frame, height=20, textvariable=self.current_shelf, width=10, values=SS.SHELF_LIST)
        self.shelf.grid(row=1, column=3, padx=10)
        self.position = Combobox(selection_frame, height=20, textvariable=self.current_position, width=10, values=SS.POSITION_LIST)
        self.position.grid(row=1, column=4, padx=10)
        find_selection = Button(selection_frame, text='Find', command=self.find_book).grid(row=1, column=5, padx=20)
        selection_frame.grid(row=0, pady=10, columnspan=2)

        # Date Frame
        date_frame = Frame(self, relief='ridge')
        self.date_info = Label(date_frame, relief='sunken', text="Today's Date")
        self.date_info.grid(row=0, column=0)
        self.day = Combobox(date_frame, textvariable=self.current_day, width=5, values=SS.DAYS)
        self.day.grid(row=1, column=0)
        self.month = Combobox(date_frame, textvariable=self.current_month, width=5, values=SS.MONTHS)
        self.month.grid(row=1, column=1)
        self.year = Combobox(date_frame, textvariable=self.current_year, width=5, values=SS.YEARS)
        self.year.grid(row=1, column=2)
        date_frame.grid(row=1, column=0)
        
        # Build the book display frame and the selection part
        book_frame = Frame(self, relief='ridge')
        self.book_info = Label(book_frame, relief='sunken', text="Enter Book Info", textvariable=self.label_text, width=30, wraplength=200)
        self.book_info.grid(row=0, column=0)
        book_frame.grid(row=2, column=0, pady=10)#, rowspan=4)
        
        # Build the book canvas picture
        mould_frame = Frame(self, relief='ridge')
        mould_book = Canvas(mould_frame, width=450, height=300, background='#ffffff')
        mould_book.create_polygon(140,60,290,75,280,240,130,225, outline="blue", fill="")
        mould_book.create_line(140,60,130,45,120,210,130,225, fill="blue")          # spine line
        mould_book.create_line(128,78,138,93, fill="lightblue")          # across spine line upper
        mould_book.create_line(126,111,136,126, fill="green")          # across spine line upper middle
        mould_book.create_line(124,144,134,159, fill="brown")          # across spine linelower middle
        mould_book.create_line(122,177,132,192, fill="lightgreen")          # across spine line lower
        mould_book.create_line(130,45,280,60,290,75, fill="blue")                   # top line
        mould_book.create_arc(220,185,360,275,outline="red",style="arc")

        head_mould = Checkbutton(mould_book, text="Head", variable=self.head_mould, onvalue=1, offvalue=0)
        spine_mould = Checkbutton(mould_book, text="Spine", variable=self.spine_mould, onvalue=1, offvalue=0)
        tail_mould = Checkbutton(mould_book, text="Tail", variable=self.tail_mould, onvalue=1, offvalue=0)
        front_board_mould = Checkbutton(mould_book, text="Front", variable=self.front_board_mould, onvalue=1, offvalue=0)
        rear_board_mould = Checkbutton(mould_book, text="Rear", variable=self.rear_board_mould, onvalue=1, offvalue=0)
        fore_edge_mould = Checkbutton(mould_book, text="Fore", variable=self.fore_edge_mould, onvalue=1, offvalue=0)
        
        head_mould_window = mould_book.create_window(175, 10, anchor=NW, window=head_mould)
        spine_mould_window = mould_book.create_window(40, 140, anchor=NW, window=spine_mould)
        tail_mould_window = mould_book.create_window(180, 250, anchor=NW, window=tail_mould)
        front_board_mould_window = mould_book.create_window(160, 140, anchor=NW, window=front_board_mould)
        rear_board_mould_window = mould_book.create_window(335, 225, anchor=NW, window=rear_board_mould)
        fore_edge_mould_window = mould_book.create_window(330, 120, anchor=NW, window=fore_edge_mould)
        mould_book.pack()

        mould_frame.grid(row=1, column=1, rowspan=2)

        # identify when the listbox changes using the bind to <ListboxSelect> virtual event

        #TODO: Put exit and save in the mould_frame, but not on the canvas
        close_frame = Frame(self,relief='ridge')
        save_data = Button(close_frame, text="Save", command=self.save_data).grid(row=0, column=1, padx=40)
        exit_program = Button(close_frame, text="Exit", command=self.exit_program).grid(row=0, column=2, padx=40)
        close_frame.grid(row=3, column=1)

        # Put it all together on the screen
        self.pack(fill=BOTH, expand=NO)
                    
        self.UpdateBookText("Please Select a User and a Date")

    def clear_checkboxes(self):
        """
        Reset all the checkboxes to un-checked.
        """
        self.head_mould.set(0)
        self.spine_mould.set(0)
        self.tail_mould.set(0)
        self.front_board_mould.set(0)
        self.rear_board_mould.set(0)
        self.fore_edge_mould.set(0)
        return

    def check_data_entered(self):
        """
        Check the necessary fields have been entered
        """
        if len(self.user.get()) < 1:
            self.UpdateBookText("Please Select a User")
            return False
            
        if len(self.day.get()) < 1 or len(self.month.get()) < 1 or len(self.year.get()) < 1:
            self.UpdateBookText("Please Select a Date")
            return False
            
        if len(self.press.get()) < 1 or len(self.shelf.get()) < 1 or len(self.position.get()) < 1:
            self.UpdateBookText("Please select a press, shelf and row first")
            return False

        return True


    def find_book(self):
        """
        Using the data given, find the book in the list and populate the book info box
        """
        gbl_log.info("Finding a book")
        gbl_log.debug("Current User:%s" % self.user.get())
        gbl_log.debug("Current Date:%s/%s/%s" % (self.day.get(),self.month.get(), self.year.get()))

        if self.check_data_entered() == False:
            return
            
        if self.saved == False and self.warned == False:
            self.UpdateBookText("Data not saved, press button again to continue.   Or press Save")
            self.warned = True
            return

        logging.info("Finding the Book reference:%s" % (self.press.get()))
        book_ref = self.press.get() + '.' + self.shelf.get() + '.' + self.position.get()
     
        self.UpdateBookText("Finding Book:%s" % book_ref)

        if book_ref in self.booklist:
            gbl_log.info(self.booklist[book_ref])
            self.found = True
            book_info = self.booklist[book_ref]['Primary other number'] +"\n" + self.booklist[book_ref]['Title'] + "\n" + self.booklist[book_ref]['Creator']        #if self.booklist[book_ref]
        else:
            book_info = "Reference not found, please record details and continue"
            self.found = False

        self.warned = False     # reset it back for the next time
        self.saved= False

        self.clear_checkboxes()
        
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
       
        logging.info("Text to be added into the Book Text Box:%s" % information)
        self.label_text.set(information)
        return     

    def save_data(self):
        # called on click on save
        # needs to capture the values annd save them to the csv file.

        if self.check_data_entered() == False:
            return
            
        if len(self.user.get()) < 1:
            self.UpdateBookText("Please Select a User")

        if len(self.day.get()) < 1 or len(self.month.get()) < 1 or len(self.year.get()) < 1:
            self.UpdateBookText("Please Select a Date")
        
        data_to_save = []
        book_ref = self.press.get() + '.' + self.shelf.get() + '.' + self.position.get()
        data_to_save.append(book_ref)
        data_to_save.append(self.head_mould.get())
        data_to_save.append(self.spine_mould.get())
        data_to_save.append(self.tail_mould.get())
        data_to_save.append(self.front_board_mould.get())
        data_to_save.append(self.rear_board_mould.get())
        data_to_save.append(self.fore_edge_mould.get())
        data_to_save.append(self.found)
        data_to_save.append(self.user.get())
        data_to_save.append(self.day.get()+"/"+self.month.get()+"/"+self.year.get())

        logging.info("Data to be saved to csv:%s" % data_to_save)

        write_header = False
        header = ["Primary other number", "Head", "Spine", "Tail", "Front", "Rear", "Fore", "Found", "User", "Date"]
        filename = SS.USB_LOCATION + '/' + SS.MOULDDATA_NAME
        if os.path.exists(SS.USB_LOCATION):
            logging.debug("[CTRL] Book File in location:%s" % filename)
            if os.path.isfile(filename) == False:
                # File doesn't exist, create header row
                write_header = True
            with open(filename, mode='a', newline='') as csvfile:
                    record = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                    if write_header == True:
                        record.writerow(header)
                        write_header=False
                    record.writerow(data_to_save)
                
            self.saved = True

        self.clear_checkboxes()
        
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
        with open(filename, 'r', errors='replace') as book:
            #bookdata = csv.DictReader(book)
            for row in csv.DictReader(book):
                # A row of data looks like
                #{'Primary other number': 'L.3.10', 'Creator': 'Charles Dickens (1812-1870).', 'CMS Inventory number': '3045432',
                    #'Title': 'The life and adventures of Martin Chuzzlewit. '}
                bookdata[row['Primary other number']] = row

    else:
        gbl_log.error("[CTRL] Unable to find book data, program aborted")
        sys.exit()
    gbl_log.info("Number of Book Data Records Loaded:%s" % len(bookdata))
    return bookdata
        
def main():

    SetupLogging()

    root = Tk()

    app = MouldCapture(master=root)
    root.geometry("800x410")
    app.master.title("Mould Capturing Tool")
    app.BookData(LoadData())
    # do something here
    app.mainloop()
    return

if __name__ == '__main__':
	main()

