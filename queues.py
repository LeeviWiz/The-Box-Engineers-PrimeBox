

"""
You can use this class as a mold to create new queues
that only let the newest data through it when you
put things in the queue. 
"""


# ============================================================
# 0. Library imports, constants, and global variables
# ============================================================

import queue


# ============================================================
# 1. Data queues for inputting and outputting data between layers
# ============================================================

class FreshestDataQueue:
    def __init__(self, maxsize=1):
        self.queue = queue.Queue(maxsize=maxsize)
    
    def put(self, item):
        try:
            self.queue.put_nowait(item)
        except queue.Full:
            try:
                self.queue.get_nowait()
                self.queue.put_nowait(item)
            except queue.Empty:
                pass
            
    def get(self, timeout=None):
        try:
            return self.queue.get(timeout=timeout)
        except queue.Empty:
            return None  # Return None if queue is empty or timeout occurs

    