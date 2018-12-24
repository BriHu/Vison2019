import serial
import json
import time
import queue

class Reciever:

	def __init__(self):
		self.openMVIn = serial.Serial('/dev/ttyUSB0', baudrate = 115200, timeout = 0)
		self.message = ""
		self.messages = queue.Queue(10)

	def in_loop(self):
		while True:
			input = self.openMVIn.read(1)
			if input == b'\n':
				#try:
					#foo = json.loads(self.message)
					#print("{0}".format(foo))
				#except ValueError:
					#pass
				if(self.messages.full()):
					self.messages.get() #waste the least recent data
					self.messages.put(self.message, 2)
				else:
					self.messages.put(self.message, 2)
				self.message = ""
			else:
				self.message += input.decode("utf-8", "ignore")

	def get_message(self):
		if(self.messages.empty()):
			pass
		else:
			return self.messages.get(2)
