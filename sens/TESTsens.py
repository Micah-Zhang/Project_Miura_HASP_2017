import queue
q = queue.Queue()

def main():
	print("sensor thread verified")
	q.put("sensor queued")
