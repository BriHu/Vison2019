import threading
import getopt
import time
import struct
import sys
import OpenMV_IN
import OpenMV_Handler

if __name__ == '__main__':
	#opts, args = getopt.getopt(sys.argv[1:], 'l:r:m:', ['left=', 'right=', 'mouse='])

	camera = OpenMV_IN.Reciever()
	handler = OpenMV_Handler.Handler()

	camera_thread = threading.Thread(target = camera.in_loop)
	handler_thread = threading.Thread(target = handler.loop)

	camera_thread.daemon = True #ensure the threads close when oo.py is stopped
	handler_thread.daemon = True

	camera_thread.start()
	handler_thread.start()
	time.sleep(0.2) #wait for the thread to completely start up

	while True:
		handler.put(camera.get_message())
		print("Camera: {5}".format(handler.get_ball_info())
		time.sleep(1)
