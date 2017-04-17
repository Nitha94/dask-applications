import sys
import os
import random
import pprint
from dask import delayed
from distributed import Scheduler
from tornado.ioloop import IOLoop
from threading import Thread
from distributed import Client



loop = IOLoop.current()
t = Thread(target=loop.start, daemon=True)
t.start()

# Set up scheduler
s = Scheduler(loop=loop)
s.start()

#Set up Workers
w = Worker('comet-14-02.sdsc.edu', loop=loop)
w.start(0) 

# Set up client 
client = Client('comet-14-02.sdsc.edu:8786')

def chunks(l,n):
	for i in range(0,len(l),n):
		yield l[i:i+n]

#pprint.pprint(list(chunks(range(0, 255), 64)))
output = []
y = list(chunks(range(0, 255), 64))
#print y[0]

for ix in y:
	a = client.map(sum, ix)
	output.append(a)

total = client.submit(sum, output)
total.visualize()
print total.compute()
client.gather(total)