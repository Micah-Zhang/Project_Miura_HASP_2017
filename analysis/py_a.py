import re

with open('data1.raw') as file:
	data = file.read()
print(re.escape(data))


#print(re.search(data,'BU'))
