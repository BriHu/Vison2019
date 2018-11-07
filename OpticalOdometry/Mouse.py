import threading
import getopt
import time
import struct
import sys
import math

#long int, long int, unsigned short, unsigned short, unsigned int
FORMAT = 'llhhI'
EVENT_SIZE = struct.calcsize(FORMAT)
# From https://elixir.bootlin.com/linux/v4.9.20/source/include/uapi/linux/input-event-codes.h
REL_X = 0
REL_Y = 1
TYPE_TOUCHPAD = 3
TYPE_MOUSE = 2

class Mouse:
	def __init__(self, path):
		self.ev = open(path, "rb")
		self.dx = 0
		self.dy = 0

	def get_event(self):
		return self.ev.read(EVENT_SIZE)

	def get_dx(self):
		return self.dx

	def get_dy(self):
		return self.dy

	def set_dx(self, dx):
		self.dx += dx

	def set_dy(self, dy):
		self.dy -= dy #y-values are reversed

	def get_set_dx(self, dx):
		a = self.dx
		self.dx = dx
		return a

	def get_set_dy(self, dy):
		a = self.dy
		self.dy = dy
		return a

	def loop(self):
		print("loop start")
		while True:
			event = self.get_event()
			(tv_sec, tv_usec, type, code, value) = struct.unpack(FORMAT, event)
			if code <= REL_Y and value != 0:
				#print("----> Event type %u, code %d, value %u at %d.%d" % (type, code, value, tv_sec, tv_usec))
				if value > 1000:
					value = -0x100000000 + value
					code_str = hex(code)
				if code == REL_X:
					self.set_dx( value )
					code_str = "X"
					#print("code %s, value %u at %d.%d" % (code_str, self.get_dx(), tv_sec, tv_usec))
				if code == REL_Y:
					self.set_dy( value )
					code_str = "Y"
					#print("code %s, value %u at %d.%d" % (code_str, self.get_dy(), tv_sec, tv_usec))


