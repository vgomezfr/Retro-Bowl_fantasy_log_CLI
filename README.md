This repository contains three files:
1. main.py: Contains code for saving and loading data to and from a JSON file. The user needs to run this file to open the terminal.
2. rb_terminal.py: Contains code for the interactive terminal. All methods for interacting with the stored data are in this file.
3. rb_data_storage.py: This file contains class definitions and the essential data structures which the terminal uses.

Use tips:
  1. Make sure to have all files in the same folder/directory: main.py depends on the rb_terminal.py, which itself relies on all the structures in the rb_data_storage.
  2. Always exit the terminal properly from either the main menu or player hub.
  3. If the terminal is not exited properly, ALL UNSAVED DATA WILL BE LOST. Saving occurs only after a successful terminal close.
  4. The terminal is broadly tolerant of invalid inputs, and will re-prompt if invalid input is received.

Package dependencies:
matplotlib

Enjoy chronicling and remembering your favorite players!
