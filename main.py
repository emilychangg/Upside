"""CSC111 Winter Final project: Main module

DESCRIPTION:
===============================

This module contains all the imports necessary to run our file.
You should be able to run this file and access our finished project: the Upside app!

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of instructors and TAs
from CSC111 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) Sophia Abolore, Michelle Chernyi, Emily Chang and Umayrah Chonee.
"""
# import statements
import upside2
import main_display
import tkinter as tk

# load the graph
graph = upside2.load_emotion_graph('data/emotions.csv', 'data/journal_entries.csv')

# initialise the app
app = main_display.UpsideApp(graph, tk.Frame)

# keep running
app.mainloop()
