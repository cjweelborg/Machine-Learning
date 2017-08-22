# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 23:03:51 2017

@author: Christian
"""

import tkinter as tk
from tkinter import ttk

# Define Constants
LARGE_FONT = ("Verdana", 12)

class IPS_Man(tk.Tk):
    
    # Initialization of everything needed to start the application
    def __init__(self, *args, **kwargs):
        
        # Run the tkinter init function
        tk.Tk.__init__(self, *args, **kwargs)
        
        # Create a container to contain everything 
        container = tk.Frame(self)
        
        # fill="both" will fill in the space allotted for the pack, expand = True will allow for expanding beyond the limits set
        container.pack(side="top", fill="both", expand = True)
        
        # Configure the rows and columns
        # 0 = minimum size, weight = 1 (priority)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        # Set self.frames = empty dictionary
        # Will hold the frames for the GUI
        self.frames = {}
        
        # Add all the pages to the dictionary self.frames
        for F in (StartPage, PageOne, PageTwo):
        
            # Create the StartPage frame which is the initial page
            frame = F(container, self)
            
            # Put the StartPage into the frames dictionary
            self.frames[F] = frame
            
            # Set a grid at row 0 and column 0 and stretch/alignment north,south,east,west (entire window)
            frame.grid(row=0, column = 0, sticky="nsew")
        
        # Show the StartPage frame
        self.show_frame(StartPage)
        
    # show_frame function which shows whatever frame that is passed in as controller
    # Input: self, cont    :   cont = controller
    def show_frame(self, cont):
        
        # Set frame = the controller or frame to show
        frame = self.frames[cont]
        
        # Bring the frame to the front
        frame.tkraise()
        
# StartPage Class, inherits from tk.Frame        
class StartPage(tk.Frame):
    
    # Initialization for the StartPage
    def __init__(self, parent, controller):
        
        # Initialize tk.Frame
        tk.Frame.__init__(self, parent)
        
        # Create label object from the tk.Label class
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        
        # Put the label(text) onto the StartPage frame with padding
        label.pack(pady=10,padx=10)
        
        # Create a button object from tk.Button class
        # button1 = ttk.Button(self, text="Visit Page 1", command=functionhere)
        # button1 = ttk.Button(self, text="Visit Page 1", command=lambda: functionhere("works with params"))
        button1 = ttk.Button(self, text="Visit Page 1", command=lambda: controller.show_frame(PageOne))
        
        # Put the button onto the StartPage frame
        button1.pack()
        
        # Create a button object from tk.Button class
        button2 = ttk.Button(self, text="Page Two", command=lambda: controller.show_frame(PageTwo))
        
        # Put the button onto the frame
        button2.pack()
        
# PageOne Class, inherits from tk.Frame
class PageOne(tk.Frame):
    
    # Initialization for the Page
    def __init__(self, parent, controller):
        
        # Initialize tk.Frame
        tk.Frame.__init__(self, parent)
        
        # Create label object from the tk.Label class
        label = tk.Label(self, text="Page One", font=LARGE_FONT)
        
        # Put the label(text) onto the frame with padding
        label.pack(pady=10,padx=10)
        
        # Create a button object from tk.Button class
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        
        # Put the button onto the frame
        button1.pack()
        
        # Create a button object from tk.Button class
        button2 = ttk.Button(self, text="Page Two", command=lambda: controller.show_frame(PageTwo))
        
        # Put the button onto the frame
        button2.pack()

# PageOne Class, inherits from tk.Frame
class PageTwo(tk.Frame):
    
    # Initialization for the Page
    def __init__(self, parent, controller):
        
        # Initialize tk.Frame
        tk.Frame.__init__(self, parent)
        
        # Create label object from the tk.Label class
        label = tk.Label(self, text="Page Two", font=LARGE_FONT)
        
        # Put the label(text) onto the frame with padding
        label.pack(pady=10,padx=10)
        
        # Create a button object from tk.Button class
        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        
        # Put the button onto the frame
        button1.pack()
        
        # Create a button object from tk.Button class
        button2 = ttk.Button(self, text="Page One", command=lambda: controller.show_frame(PageOne))
        
        # Put the button onto the frame
        button2.pack()
        
app = IPS_Man()
app.mainloop()