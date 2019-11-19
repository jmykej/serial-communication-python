
#!/usr/bin/python

'''
Beta 2.1

Want to add for this version:
    
    Fix problem with program crash when data stream is sending wrong data.

Added to this version:

    Seems fixed
    Also fixed with the wrong amount of datapoints

Created on Tue Nov 14 10:00:49 2019

@author: jikaxa
'''
#==========Imports========================#

from tkinter import *
import serial                   #Module to read serial port
import time                     #Module for the timing
import serial.tools.list_ports  #Module to check for ports
import os                       #Module to clear screen in terminal
import threading				#Module for threading
import csv						#Module for csv documents
from openpyxl import Workbook   #Modules for the Excel-files
from openpyxl.chart import (
    LineChart,
    Reference,
)

#=========================================#

