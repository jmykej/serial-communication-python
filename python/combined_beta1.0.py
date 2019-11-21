
#!/usr/bin/python

'''
Beta 4.0

Want to add for this version:
    
    

Added to this version:



Created on Tue Nov 14 10:00:49 2019

@author: jikaxa
'''
#==========Imports========================#


from tkinter import *
from PIL import Image, ImageTk


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

PROGRAM_NAME = "Maskinen power tester"

#Class for the data logger with the GUI

class DataLogger():
	live_label_running = True
	text_content = []


	def __init__(self, root):

		self.root = root
		self.root.title(PROGRAM_NAME)
		self.init_gui()

##==============FrameWork=======================================###

	def frame_creation(self):

		self.top_frame = Frame(root, bd=2, relief=SUNKEN, bg='burlywood2')
		self.top_frame.pack(side=TOP, expand=False, fill=X)

		self.bottom_frame = Frame(root, bd=2, relief=SUNKEN, bg='wheat1')
		self.bottom_frame.pack(side=BOTTOM, expand=False, fill=X)

		self.left_frame = Frame(root, bd=2, relief=SUNKEN, bg='wheat1')
		self.left_frame.pack(side=LEFT, expand=False, fill='both')

		self.middle_frame = Frame(root, bd=2, relief=SUNKEN, bg='white')
		self.middle_frame.pack(side=LEFT, expand=True, fill='both')

		self.right_frame = Frame(root, bd=2, relief=SUNKEN, bg='wheat1')
		self.right_frame.pack(side=LEFT, expand=False, fill="both")

	def top_picture(self):

		self.photo = PhotoImage('IMG_6518.JPG')

		self.top_label = Label(self.top_frame, text="MASKINEN POWER METER 6000", bg='burlywood2')
		self.top_label.pack()
	#	self.img = root.PhotoImage(Image.open("IMG_6518.JPG"))
	#	self.panel = Label(root, image = img)
	#	self.panel.pack(side = "top", fill = "both", expand = True)

	def bottom_buttons(self):
		self.start_button = Button(self.bottom_frame, text="Start", command=lambda: self.start_data())
		self.start_button.grid(row=0, column=0)

		self.pause_button = Button(self.bottom_frame, text="Pause", command=lambda: self.pause_data())
		self.pause_button.grid(row=0, column=6)

		self.stop_button = Button(self.bottom_frame, text="Stop", command=lambda: self.stop_data())
		self.stop_button.grid(row=0, column=15)	

	def left_widgets(self):

		self.port = serial.tools.list_ports.comports()
		print()

		file_label = Label(self.left_frame, text="File: ", bg='wheat1').grid(row=0, column=0)
		self.file_entry = Entry(self.left_frame)
		self.file_entry.grid(row=1, column=0)

		COM_label = Label(self.left_frame, text='COM Port:', bg='wheat1').grid(row=2, column=0)
		self.com_entry = Entry(self.left_frame)
		self.com_entry.grid(row=3, column=0)
		self.com_entry.insert(0, "COM6")


		Found_COM_ports = Label(self.left_frame, text='Found COM ports', bg='wheat1', font=(None, 10)).grid(row=6, column=0)
		self.Lb1 = Listbox(self.left_frame, bg='cornsilk2', font=('helvetica',10), selectmode="SINGLE", width="35")
		self.Lb1.grid(row=7, column=0)
		self.Lb1.insert(1, self.port[0])
		if len(self.port) == 2:
			self.Lb1.insert(2, self.port[1])
		if len(self.port) == 3:
			self.Lb1.insert(3, self.port[2])
		if len(self.port) == 4:
			self.Lb1.insert(4, self.port[3])

	def right_widgets(self):
		pass
		#file_label1 = Label(self.right_frame, text="File: ", bg='wheat1').grid(row=0, column=0)
		#self.file_entry1 = Entry(self.right_frame)
		#self.file_entry1.grid(row=1, column=0)

##==============Functionality===================================###

	#Thread to get the data in so as no to disturb the main loop
	def get_data_thread(self):
		self.thread2 = threading.Thread(target=self.get_data, name="Getting Data")
		self.thread2.daemon = False
		self.thread2.start()

	#Thread to start the get data thread
	def start_data(self):
		DataLogger.live_label_running = True
		self.get_data_thread()
		self.toggle_start()

	def pause_data(self):
		DataLogger.live_label_running = False
		self.toggle_start()

	#Method to stop the get data thread, will clear window
	def stop_data(self):
		DataLogger.live_label_running = False
		self.live_text.delete(1.0, END)
		self.toggle_start()

	#Method to see if the start button should be disabled or not.
	def toggle_start(self):
		if DataLogger.live_label_running == True:
			self.start_button.configure(state="disabled")
		else:
			self.start_button.configure(state="normal")

	## Create the text widget

	def text_widget(self):

		self.live_text = Text(self.middle_frame, height=15, width=40)
		self.live_text.pack(side=RIGHT, expand=True, fill=X, padx=5)

	def max_text(self):

		self.text_max = Text(self.right_frame, height=2, width=10)
		self.text_max.pack(side=RIGHT, expand=True, fill=X, padx=5)

##==============DataCollecting==================================###

	def get_data(self):
		filename = self.file_entry.get()+".csv"
		data_max = 0.0
		 
		#See if file is not blank
		if filename != ".csv":
			#Try given serial port
			try:
				#declaring the variable method
				ser = serial.Serial(self.com_entry.get(), 115200, timeout=1)
				ser_bytes = ser.readline()
				decoded_bytes = ser_bytes.decode("utf-8")
				data = decoded_bytes
				feilds = []
				i = 0
				headers = ""

				## this is to get the number of variables, so that you can use any number of variables
				for x in data:
					feilds.append("Variable " + str(i))
					i += 1
				## save the header to the csv file. You can change these later in the spreadsheet
				with open(filename, 'w') as csvfile:
					csvwriter = csv.writer(csvfile) #, lineterminator='\n'
					csvwriter.writerow(feilds)

					for pos in feilds:
						headers = headers + str(pos)
				## Loop to get the data and save it to a csv file, the post to the text box.
				while True:
					try:
						ser_bytes = ser.readline()
						decoded_bytes = ser_bytes.decode("utf-8")
						data = decoded_bytes
						data_ut = float(decoded_bytes)


						with open(filename, 'w') as csvfile:
							csvwriter = csv.writer(csvfile, lineterminator="\n")
							csvwriter.writerow([(data)])
							
						if data_max<data_ut:
							data_max=data_ut


						self.live_text.insert(END, str(data) + "\n")
						self.live_text.see("end")

						self.text_max.insert(END, str(data_max) + '\n')
						self.text_max.see("end")

						if DataLogger.live_label_running == False:
							break
					## This is where if anythin went wrong with the data
					except:
						print("Something is wrong")
						break	
					

			## If the serial port did not work it will jump here
			except:
				self.live_text.insert(END, "[ERROR] COM PORT NOT FOUND"+"\n")
				DataLogger.live_label_running = False
				self.toggle_start()

	## This is where the if statement at the top if the method will return to if the filename is empty
		else:
			self.live_text.insert(END, "[ERROR] PLEASE NAME FILE" + "\n")
			DataLogger.live_label_running = False
			self.toggle_start()

##==============InitGUI=========================================###


	def init_gui(self):

		self.frame_creation()
		self.text_widget()
		self.left_widgets()
		self.right_widgets()
		self.bottom_buttons()
		self.top_picture()
		self.max_text()

if __name__=="__main__":
	root = Tk()
	DataLogger(root)
	root.mainloop()
