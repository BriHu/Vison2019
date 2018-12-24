import queue
import threading
import time
from Handlers import OrangeBallHandler

class Handler:
	
	def __init__(self):
		self.data = queue.Queue(100)
		self.orange_ball_key = "BALL"
		self.orange_ball = OrangeBallHandler.OrangeBall_Handler(100)
		self.init_threads()

	def loop(self):
		while True:
			if(not self.data.empty()):
				d = self.data.get(2)
				if any(self.orange_ball_key in s for s in d):
					self.orange_ball.put(d, 2)
				time.sleep(1)
			else:
				pass
				time.sleep(5)

	def put_data(self, d):
		if(self.data.full()):
			self.data.get(2)
			self.data.put(d, 2)
		else:
			self.data.put(d, 2)

	def get_ball_info(self):
		return self.orange_ball.get(2)

	def init_threads(self):
		#define all threads
		orange_ball_thread = threading.Thread( target = self.orange_ball.loop )

		#the threads MUST close on progam close
		orange_ball_thread.daemon = True 

		orange_ball_thread.start()
