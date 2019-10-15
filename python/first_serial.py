# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 10:00:49 2019

@author: jikaxa
"""
#!/usr/bin/python
import serial
import time
import csv
import os


#===============Settings==================#

portname = 'COM3'   # Name of the serial port
baudrate = 9600     # The baudrate. Use same as sent from Arduino
timeout = 1         # Waiting time for opening the serial. (seconds)

#If you wanna use datapoints instead of time. Dont forget
#to change loop in read_serial_data()
datapoints = [100,800,1600,2400]
#Amount of data points
# [0] = 100  -Default, mostly for testing
# [1] = 800  -Around 10s of data
# [2] = 1600 -Around 20s of data
# [3] = 2400 -Around 30s of data
# [4] = 80*s -Choose approximated time of measurement

data_points = datapoints[1]



#===============Initialize================#

meas = True

#===============Functions================#

def measure(answer):
    measure = ''
    
    while measure != 'y' or measure != 'n':
         
        measure = input('\n\n\tDo you wanna go again? y/n: ');
    
        if measure == 'y':
            answer = True
            break
        elif measure == 'n':     
            answer = False
            break
        else:
            print('\tYou have to choose y or n..')
            
    return answer

def create_serial(port,baudrate,timet):
    
    return serial.Serial(port,baudrate,timeout = timet)
  
def read_serial_data(serial,datatime):
    
    serial.flushInput()
    millis2 = 0
    millis = time.time() # Start timer for timestamps
    #for i in range(0,datapoints): 
    while float(millis2) < datatime:
        ser_bytes = ser.readline()
        decoded_bytes = ser_bytes[0:len(ser_bytes)-2].decode("utf-8")
        millis2 = str(round((time.time() - millis),2))
        print('\t\t' + decoded_bytes + ',' + millis2)
            
def save_to_csv():
    None

#==========Main=========================#


while True:
    
    while meas:
        
        clear = lambda: os.system('cls') #Clears the screen
        clear()
        
        print('\n\n\t### Welcome to Maskinmätaren ###')
        print('\n\n\t Connecting to COM-port... ')
        ser = create_serial(portname,baudrate,timeout)
        print('\t COM port found:  ' + portname)
        print('\n\t Starting to read serial data... ')
        filename = input('\t Choose name for your csv-file:')
        data_time = float(input('\t How long measurement do you wanna do? (seconds): '))
        read_serial_data(ser,data_time)
        ser.close()
        print('\n\t Your data was saved in:  ' + filename + '.csv ')
        meas = measure(meas)
        
        if meas == False:
            exit()

#ser_bytes = ser.readline()



#while True:
#    
#    try:
#        
#            ser_bytes = ser.readline()
#            decoded_bytes = ser_bytes[0:len(ser_bytes)-2].decode("utf-8")
#            millis2 = float((int(round(time.time()*1000)) - millis)/1000)
#            print(decoded_bytes)
#            with open(file_name + ".csv","a+",newline='') as f:
#                writer = csv.writer(f,delimiter=',',quotechar='|')
#                writer.writerow([millis2,decoded_bytes])
#
#    except:
#        ser.close()
#        print("Keyboard Interrupt")
#        break 
            
            
