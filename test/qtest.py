import queue

test = queue.Queue()

for i in range(5):
	test.put(i)

while not test.empty():
	print(test.get(), end = ' ')
print()
