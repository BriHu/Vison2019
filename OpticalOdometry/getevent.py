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
		self.dy += dy

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


angle = 0.0
LX = 0.0
LY = 0.0
RX = 0.0
RY = 0.0

def calc_dxdy(acc_LX, acc_LY, acc_RX, acc_RY):
	if(acc_LY == acc_RY):
		return acc_LX, acc_LY, acc_RX, acc_RY, 0
	else:
		fixed_distance = 10.0
		if(acc_RY == 0):
			theta = acc_LY / fixed_distance
			left_y = fixed_distance * math.sin(theta)
			left_angle = ( math.pi / 2 ) - ( math.pi - theta ) / 2
			left_x = left_y / math.tan(left_angle)
			right_y = 0
			right_x = 0
		elif(acc_LY == 0):
			theta = -acc_RY / fixed_distance
			right_y = fixed_distance * math.sin(theta)
			right_angle = ( math.pi / 2 ) - ( math.pi - theta ) / 2
			right_x = right_y / math.tan(right_angle)
			left_y = 0
			left_x = 0
		else:
			#first we figure out the x and y values of the arc (accumulated y)
			#re-arrangment of L/R = (r + D) / r
			radius = (fixed_distance * acc_RY) / (acc_LY - acc_RY)
			#angle measurments done in radians
			theta = acc_LY / (fixed_distance + radius)
			left_inner_angle = (math.pi - theta) / 2
			right_inner_angle = (2 * math.pi - 2 * left_inner_angle) / 2
			left_angle = (math.pi / 2) - left_inner_angle
			right_angle = (math.pi / 2) - right_inner_angle

			left_y = (fixed_distance + radius) * math.sin(theta)
			left_x = left_y / math.tan(left_angle)
			right_y = radius * math.sin(theta)
			right_x = right_y / math.tan(right_angle)
		#now we add the accumulated x under the assumption that the x value was accumulated evenly accross the time of the arc
		half_theta = theta / 2
		#in theory acc_LX should always equal acc_RX or atleast be within 1-2 dots
		if(acc_LX == acc_RX):
			X = acc_LX
		else:
			X = (acc_LX + acc_RX) / 2
		shift_x = X * math.cos(half_theta)
		shift_y = X * math.sin(half_theta)
		left_dx = left_x + shift_x
		left_dy = left_y + shift_y
		right_dx = right_x + shift_x
		right_dy = right_y + shift_y

		return left_dx, left_dy, right_dx, right_dy, theta

def adjust_deltas(left_dx, left_dy, right_dx, right_dy, theta):
	global angle
	global LX
	global LY
	global RX
	global RY
	s = math.sin(angle)
	c = math.cos(angle)
	LX += left_dy * s + left_dx * c
	LY += left_dy * c - left_dx * s
	RX += right_dy * s + right_dx * c
	RY += right_dy * c - right_dx * s
	angle += theta

#
# Use getopt instead so we can do "--left 5 --right 8" or whatever
#
opts, args = getopt.getopt(sys.argv[1:], 'l:r:', ['left=', 'right='])
for opt in opts:
    if opt[0] in ('-l','--left'):
        left_path = "/dev/input/event" + opt[1]
        print("got left")
    if opt[0] in ('-r','--right'):
        right_path = "/dev/input/event" + opt[1]
        print("got right")

left_mouse = Mouse(left_path)
right_mouse = Mouse(right_path)

left_thread = threading.Thread(target = left_mouse.loop)
right_thread = threading.Thread(target = right_mouse.loop)
left_thread.daemon = True
right_thread.daemon = True
left_thread.start()
right_thread.start()
time.sleep(0.2) #wait for the thread to completely start up

while True:
	relative_deltas = calc_dxdy(left_mouse.get_set_dx(0), left_mouse.get_set_dy(0), right_mouse.get_set_dx(0), right_mouse.get_set_dy(0))
	adjust_deltas(relative_deltas[0], relative_deltas[1], relative_deltas[2], relative_deltas[3], relative_deltas[4])
	print("Left [{0},{1}]   Right[{2},{3}]  Angle: {4}".format(LX, LY, RX, RY, angle))
	time.sleep(1)
