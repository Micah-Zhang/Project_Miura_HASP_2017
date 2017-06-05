import queue
q = queue.Queue()

def main():
	print("camera thread verified")
	q.put("camera queued")
