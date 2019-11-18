from tkinter import *

import serial
import threading
import time
import csv
import serial                   #Module to read serial port
import time                     #Module for the timing
import serial.tools.list_ports  #Module to check for ports
import os

PROGRAM_NAME = "Serial Data Logger"


class DataLogger():
	live_label_running = True
	text_content = []

	def __init__(self, root):

		self.root = root
		self.root.title(PROGRAM_NAME)
		self.init_gui()

## Create a frame

	def frame_creation(self):
		self.left_frame = Frame(root, bd=2, relief=SUNKEN)
		self.left_frame.pack(side=LEFT, expand=False, fill=Y)
		self.bottom_frame = Frame(root, bd=2, relief=SUNKEN)
		self.bottom_frame.pack(side=BOTTOM, expand=False, fill=X)
		self.right_frame = Frame(root, bd=2, relief=SUNKEN)
		self.right_frame.pack(side=RIGHT, expand=True, fill="both")

## Create the text widget

	def text_widget(self):

		self.live_text = Text(self.right_frame, height=15, width=40)
		self.live_text.pack(side=LEFT, expand=True, fill="both", padx=5)

## Main method for streaming and saving data

	def get_data(self):
		filename = self.file_entry.get()+".csv"
		#See if file is not blank
		if filename != ".csv":
			#Try given serial port
			try:
				#declaring the variable method
				ser = serial.Serial(self.com_entry.get(), 115200, timeout=1)
				ser_bytes = ser.readline()
				decoded_bytes = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
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
					csvwriter = csv.writer(csvfile, lineterminator='\n')
					csvwriter.writerow(feilds)
					for pos in feilds:
						headers = headers + str(pos)
				## Loop to get the data and save it to a csv file, the post to the text box.
				while True:
					try:
						ser_bytes = ser.readline()
						decoded_bytes = str(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
						data = decoded_bytes
						with open(filename, 'a') as csvfile:
							csvwriter = csv.writer(csvfile, lineterminator="\n")
							csvwriter.writerow([data])
							print("Data has been logged")

						self.live_text.insert(END, str(data) + "\n")
						self.live_text.see("end")

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
	#Method to pause the get data thread, will clear output window
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
	#Method starts widget on the left side, in the left frame.
	def left_widgets(self):
		file_label = Label(self.left_frame, text="File: ").grid(row=0, column=0)
		self.file_entry = Entry(self.left_frame)
		self.file_entry.grid(row=1, column=0)

		COM_label = Label(self.left_frame, text='COM Port:').grid(row=2, column=0)
		self.com_entry = Entry(self.left_frame)
		self.com_entry.grid(row=3, column=0)
		self.com_entry.insert(0, "COM3")

		Split_label = Label(self.left_frame, text='Split at: ').grid(row=4, column=0) 
		self.split_entry = Entry(self.left_frame)
		self.split_entry.grid(row=5, column=0)
		self.split_entry.insert(0, " ")
	#Method works the buttons in the bottom.
	def bottom_buttons(self):
		self.start_button = Button(self.bottom_frame, text="Start", command=lambda: self.start_data())
		self.start_button.grid(row=3, column=0)

		self.pause_button = Button(self.bottom_frame, text="Pause", command=lambda: self.pause_data())
		self.pause_button.grid(row=3, column=1)

		self.stop_button = Button(self.bottom_frame, text="Stop", command=lambda: self.stop_data())
		self.stop_button.grid(row=3, column=2)

	## ********************* GUI initialization method **********************************###
	 
	def init_gui(self):
		self.frame_creation()
		self.text_widget()
		self.left_widgets()
		self.bottom_buttons()

if __name__=="__main__":
	root = Tk()
	DataLogger(root)
	root.mainloop()

