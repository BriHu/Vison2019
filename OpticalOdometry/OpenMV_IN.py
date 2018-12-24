import serial
import json
import time
import Queue

class Reciever:

	def __init__(self):
		self.openMVIn = serial.Serial('/dev/ttyUSB0', baudrate =  115200, timeout = 0)
		self.message = ""
		self.messages = queue.Queue(50)

	def in_loop(self):
		while True:
			input = self.openMVIn.read(1)
			if input == b'\n':
				try:
					foo = json.loads(self.message)
					#print("{0} {1}".format(foo, foo["seq"]-50))
				except ValueError:
					pass
				self.messages.put(self.message)
				self.message = ""
			else:
				self.message += input.decode("utf-8", "ignore")

	def get_message(self):
		return self.messages.get()
