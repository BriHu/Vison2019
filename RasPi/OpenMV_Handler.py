import Queue
import threading
import time
import Handlers.OrangeBallHandler

class Handler:
	
	def __init__(self):
		self.data = Queue.queue(300)

		self.orange_ball_key = "BALL"
		self.orange_ball = OrangeBallHandler.OrangeBall_Handler(100)

		self.init_threads()

	def loop(self):
		while True:
			d = self.data.get()
			if d.len() != 0: #if the message exists
				if any(self.orange_ball_key in s for s in d):
					self.orange_ball.put(d)
			time.sleep(1)

	def put_data(self, d):
		self.data.put(d)

	def get_ball_info(self):
		return self.orange_ball.get()

	def init_threads(self):
		#define all threads
		orange_ball_thread = threading.Thread( target = orange_ball.loop )

		#the threads MUST close on progam close
		orange_ball_thread.daemon = True 

		orange_ball_thread.start()