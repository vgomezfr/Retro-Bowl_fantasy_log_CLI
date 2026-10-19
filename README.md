This repository contains three files:
1. main.py: Contains code for saving and loading data to and from a JSON file. The user needs to run this file to open the terminal.
2. rb_io_handling.py: Contains code for the interactive terminal. All methods for interacting with the stored data are in this file.
3. retro_bowl_fantasy_stats.py: This file contains class definitions and the essential data structures which the terminal uses.

Use tips:
  1. Make sure to have all files in the same folder/directory: main.py depends on the terminal/IO handling file, which itself relies on all the structures in the data classes file.
  2. Always exit the terminal properly by entering "E". This may require you to navigate to a menu where "E" is a valid input.
  3. If the terminal is not exited properly, ALL UNSAVED DATA WILL BE LOST. Saving occurs only after a successful terminal close.
  4. The terminal is broadly tolerant of invalid inputs, and will re-prompt if invalid input is received.

Enjoy chronicling and remembering your favorite players!
