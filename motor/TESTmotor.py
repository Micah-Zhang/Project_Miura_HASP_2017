import queue
q = queue.Queue()

def main():
	print("motor thread verified")
	q.put("motor queued")
