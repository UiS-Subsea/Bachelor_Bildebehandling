import multiprocessing
from multiprocessing import Queue

q = multiprocessing.Queue()
q.put("hello")
print(q[0])