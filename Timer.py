from time import time
class Timer(object):
    """ Instances variables :
    elapsed - the total time elapsed
    time_start - the time of the last tic"""
    
    def __init__(self):
        self.elapsed = 0
        self.time_start = 0
        
    def tic(self):
        self.time_start = time()
    def add(self):
        self.elapsed += time()-self.time_start
    def toc(self):
        self.elapsed = time()-self.time_start