"""A model for a single cylinder engine"""
import time
import sys

from multiprocessing import Lock, Process, Pipe

sys.path.append("C:\\Projects\\engineblock")

from engineblock.components.starter import Starter
from engineblock.components.crankshaft import Crankshaft


if __name__ == '__main__':
    starter_end, crank_end = Pipe()
    timing = Lock()
    e_starter = Starter(starter_end)
    crank = Crankshaft(crank_end, timing)
    crank_process = Process(target=crank.rotate_process, args=(1000,))
    crank_process.start()
    time.sleep(5)
    print("starting")
    e_starter.start()
    time.sleep(10)
    e_starter.stop()
    crank_process.join()
    print("end of run")