"""
Beta 2.1

Want to add for this version:
    Adding different sheets for one file.

Added to this version:

    Added more sheets to same xl-file
    Also fixed bug with float-conversion in read_serial

Created on Mon Oct 14 10:00:49 2019

@author: jikaxa
"""
#==========Imports========================#

#!/usr/bin/python
import serial                   #Module to read serial port
from serial import Serial
import time                     #Module for the timing
import serial.tools.list_ports  #Module to check for ports
import os                       #Module to clear screen in terminal
from openpyxl import Workbook   #Modules for the Excel-files
from openpyxl.chart import (
    LineChart,
    Reference,
)

#===============Settings==================#

portname = 'COM3'   # Name of the serial port.
baudrate = 9600     # The baudrate. 
timeout = 2         # Waiting time for opening the serial. (Seconds)
wb = Workbook()     # Create xl-file
ws = wb.active      # Grab the active worksheet

#===============Initialize================#

keep_measuring = True # Bool to keep program run for more measurements

#===============Functions================#

def measure(answer):
    #A function to set the variable keep_measuring to true or false after every measurement

    meas_ans = ''
    
    while meas_ans != 'y' or meas_ans != 'n':
         
        meas_ans = input('\n\n\tDo you wanna go again? y/n: ')
    
        if meas_ans == 'y':
            answer = True
            break
        elif meas_ans == 'n':     
            answer = False
            break
        else:
            print('\tYou have to choose y or n..')
            
    return answer

def creat_xl_graph(filename, excercise_ws, datapoint_amount):

    #Creates a sheet in the Excel-file for every measurement.
    #Takes in "filename" for the name of the Excel-file choosen by the user
    #Takes in "excercise_ws" to create a new sheet for every new measurement
    #Takes in "datapoints_ amount" to know how many datapoints were collected. Used when making the graph 
        
    excercise_ws['A1'] = 'Weight(KG)'               #Names first column
    excercise_ws['B1'] = 'Time(Seconds)'            #Names second column
    excercise_ws.column_dimensions['A'].width = 15  #Sets the width of first column
    excercise_ws.column_dimensions['B'].width = 15  #Sets the width of second column
    
    c1 = LineChart()                                #Creates a line chart
    c1.title = "Mätmaskinen"                        
    c1.style = 13
    c1.y_axis.title = 'Weight(kg)'
    c1.x_axis.title = 'Time(s)'
    c1.y_axis.scaling.min = 0                       #Sets minimum scale
    c1.y_axis.scaling.max = 5                       #Sets maximum scale
    c1.height = 20                                  #Sets height of graph
    c1.width = 40                                   #Sets width of graph
    data = Reference(excercise_ws, min_col=1, min_row=2, max_col=1, max_row=len(datapoint_amount))      #Decides from which column to collect data for y-axis in graph
    c1.add_data(data, titles_from_data=True)                                                            #Adds above data
    times = Reference(excercise_ws, min_col=2, min_row=2, max_col=2, max_row=len(datapoint_amount))     #Decides from which column to collect data for x-axis in graph
    c1.set_categories(times)                                                                            #Adds above data
    excercise_ws.add_chart(c1, "F10")                                                                   #Adds chart to sheet at position "F10".
    wb.save(filename + ".xlsx")                                                                         #Saves the sheet in choosen file.

def create_serial(portname, baudrate, timet):

    #Creates a connection to a COM-port. 
    #Lists all the connected units and looks for one named Arduino
    #Returns an COM-port object.
    
    port = serial.tools.list_ports.comports()       #Lists all connected ports
    print('\n\t\t Ports found: \n')
    print('\t\t #####################\n')
    
    for i in port:                                  #Looks for a unit named Arduino that it can connect to.
        print('\t\t ' + str(i))
        a = str(i)
        if 'Arduino' in a:
            port2 = str(a[0:4])
    print('\n\t\t #####################')       
    print('\n\t\t Connected to: ' + (port2))
    print('\n\t\t #####################\n') 
          
    return serial.Serial(port2, baudrate, timeout=timet)
  
def read_serial_data(serial, datatime, excercise):

    #Function to read the serial data and decode it for the Excel-file
    
    data_holder = []                    #List to put data through one iteration
    datapoint_amount = []               #List thats used to see how many datapoints is saved. Used when creating the graphs later. (Change to use an int in the future)
    serial.flushInput()                 #Cleans the serial input.
    millis2 = 0                 
    millis = time.time()                #Start timer for timestamps
    
    while millis2 < datatime:                                                 #Runs measurement loop for the amount of time choosen by the user.
        ser_bytes = ser.readline()                                            #Reads one line on the serial bus
        millis2 = float(round((time.time() - millis), 3))                     #Calculate the time when the measurement is made.
        decoded_bytes = ser_bytes[0:len(ser_bytes)-2].decode("utf-8")         #Decodes the serial data to a string
        if '.' not in decoded_bytes:                                          #An if-statement to avoid reading faulty data and then interupting the program. (Can be improved maybe.)
            continue
        else:
            data_holder.append(float(decoded_bytes))                          #Add the decoded data to a list
            data_holder.append(millis2)                                       #Add the timestamp from the measurement to the same list as above.
            datapoint_amount.append(millis2)                                  #Add timestamp to this list just to know how many datapoints is saved.
            excercise.append(data_holder)                                     #Add the datapoint and timestamp from the dataholder to the Excel sheet.
            del data_holder[:]                                                #Empty the data holder. This is done because the excel module saved the data in rows and not columns otherwise
            print('\t\t' + decoded_bytes + ',' + str(millis2))
        
    return datapoint_amount
    

#==========Main=========================#


while True:
        
    clear = lambda: os.system('cls') #Clears the screen. At least on windows computer
    clear()
    
    ##Welcome text. Tells you a little bit about the program.

    print('\n\n\t########### Welcome to Maskinmätaren ###########')
    print('\n\t\tYou will choose a name for your excel-file.')
    print('\t\tAnd the you will choose for how long your\n\t\tmeasurement is gonna be.')
    print('\t\tYou can press Ctrl-c if you wanna exit the program.')

    ##Opens the serial port

    ser = create_serial(portname, baudrate, timeout)
    print('\n\t\t Starting to read serial data... ')

    ##Takes some input. Names the excel-file and the first sheet aka excercise.

    filename = input('\t\t Choose name for your excel-file:')
    excercise_name = input('\t\t Name your excercise: ')
    ws.title = excercise_name

    ##Takes the input for how long the first measurement will be.

    data_time = float(input('\t\t How long measurement do you wanna do? (seconds): '))
    
    datapoint_amount = read_serial_data(ser, data_time, ws)
        
    creat_xl_graph(filename, ws, datapoint_amount)
    print('\n\t\t Your data was saved in:  ' + filename)
    keep_measuring = measure(keep_measuring)
    
    #Runs the program for as many times you want it. And save each measurement in a new sheet of the Excel-file.

    while keep_measuring:
        excercise_name = input('\t Name your excercise: ')
        excercise = wb.create_sheet(excercise_name)
        data_time = float(input('\t\t How long measurement do you wanna do? (seconds): '))
        datapoint_amount = read_serial_data(ser, data_time, excercise)
        creat_xl_graph(filename, excercise, datapoint_amount)
        print('\n\t\t Your data was saved in:  ' + filename)
        keep_measuring = measure(keep_measuring)
       
    #Closes the COM-port and exits the program when you are done.   

    if keep_measuring == False:
        ser.close()
        exit()
