#!/usr/local/bin/python3
import threading
import getopt
import time
import struct
import sys
import Mouse
import MouseNav
import OpenMV_IN

if __name__ == '__main__':
	opts, args = getopt.getopt(sys.argv[1:], 'l:r:m:', ['left=', 'right=', 'mouse='])
	is_single = False
	for opt in opts:
		if opt[0] in ('-l','--left'):
			left_path = "/dev/input/event" + opt[1]
			print("got left")
		if opt[0] in ('-r','--right'):
			right_path = "/dev/input/event" + opt[1]
			print("got right")
		if opt[0] in ('-m','--mouse'):
			mouse_path = "/dev/input/event" + opt[1]
			is_single = True
			print("got mouse")

	if is_single:
		mouse = Mouse.Mouse(mouse_path)
		mouse_thread = threading.Thread(target = mouse.loop)
		mouse_thread.daemon = True
		mouse_thread.start()
		while True:
			print("X: {0}, Y: {1}".format(mouse.get_dx(), mouse.get_dy()))
			time.sleep(1)

	left_mouse = Mouse.Mouse(left_path)
	right_mouse = Mouse.Mouse(right_path)
	camera = OpenMV_IN.Reciever()

	left_thread = threading.Thread(target = left_mouse.loop)
	right_thread = threading.Thread(target = right_mouse.loop)
	camera_thread = threading.Thread(target = camera.in_loop)
	left_thread.daemon = True
	right_thread.daemon = True
	camera_thread.daemon = True #ensure the threads close when oo.py is stopped
	left_thread.start()
	right_thread.start()
	camera_thread.start()
	time.sleep(0.2) #wait for the thread to completely start up

	MN = MouseNav.MouseNav()

	while True:
		relative_deltas = MN.calc_dxdy(left_mouse.get_set_dx(0), left_mouse.get_set_dy(0), right_mouse.get_set_dx(0), right_mouse.get_set_dy(0))
		MN.adjust_deltas(relative_deltas[0], relative_deltas[1], relative_deltas[2], relative_deltas[3], relative_deltas[4])
		Nav_data = MN.get_all()
		print("Left [{0},{1}]   Right[{2},{3}]  Angle: {4}  Camera: {5}".format(Nav_data[0], Nav_data[1], Nav_data[2], Nav_data[3], Nav_data[4], camera.get_message()))
		time.sleep(1)
