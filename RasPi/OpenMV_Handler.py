import Queue
import threading
import time

class Handler:
	
	def __init__(self):
		self.data = Queue.queue(300)

		self.orange_ball_key = "BALL"
		self.orange_ball = OrangeBall_Handler(100)

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

class OrangeBall_Handler:
	
	def __init__(self, queue_size):
		self.ball_queue = queue.Queue(queue_size) #using a que to allow for collection of data to collect deltas

	def put(self, message):
		if message.len() != 0: #if there is a message
			self.ball_queue.put(message)

	def get(self):
		return self.ball_queue.get()

