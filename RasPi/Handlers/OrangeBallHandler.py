import Queue
import threading
import time

class OrangeBall_Handler:
	
	def __init__(self, queue_size):
        #using a queue to store unfiltered data
		self.ball_queue = queue.Queue(queue_size)
        self.ball_data =  queue.Queue(queue_size)

	def put(self, message):
		if message.len() != 0: #if there is a message
			self.ball_queue.put(message)

	def get(self):
		return self.ball_queue.get()

    def loop(self):
        while True:
			try:
				d = self.ball_queue.get()
			except:
				time.sleep(10)
			else:
				#filter info
            