import sys
import os
import time
from dask import delayed
from distributed import Scheduler
from tornado.ioloop import IOLoop
from threading import Thread
from distributed import Client
from dask.multiprocessing import get
from dask.dot import dot_graph

def sleep(time):
	time.sleep(time)


dsk = {
'level0': (sleep, 100),
'level0': (sleep, 100),
'level0': (sleep, 100),
'level0': (sleep, 100),
'level0': (sleep, 100),
'level0': (sleep, 100),
'level0': (sleep, 100),
'level0': (sleep, 100),
'level0': (sleep, 100),
'level0': (sleep, 100),
'level0': (sleep, 100),
'level0': (sleep, 100),
'level0': (sleep, 100),
'level0': (sleep, 100),
'level0': (sleep, 100),
'level0': (sleep, 100),
'level1': (sleep, 100),
'level1': (sleep, 100),
'level1': (sleep, 100),
'level1': (sleep, 100),
'level1': (sleep, 100),
'level1': (sleep, 100),
'level1': (sleep, 100),
'level1': (sleep, 100),
}

d = dsk.dask
dot_graph(d)


