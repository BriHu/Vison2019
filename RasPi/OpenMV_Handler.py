import Queue
import threading
import time

class Handler:
	
	def __init__(self):
		self.data = Queue.queue(50)

		self.yellow_box_key = "BOX"
		self.yellow_box = YellowBoxHandler(10)

	def loop(self):
		while True:
			d = self.data.get()
			if d.len() != 0: #if the message exists
				if any(self.yellow_box_key in s for s in d):
					self.yellow_box.put(d)
			time.sleep(1)

	def put_data(self, d):
		self.data.put(d)

	def get_box_info(self):
		return self.yellow_box.get()

class YellowBoxHandler:
	
	def __init__(self, queue_size):
		self.box_queue = queue.Queue(queue_size) #using a que to allow for collection of data to collect deltas

	def put(self, message):
		if message.len() != 0: #if there is a message
			self.box_queue.put(message)

	def get(self):
		return self.box_queue.get()

