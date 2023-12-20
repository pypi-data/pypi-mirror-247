import psutil
import time
from multiprocessing import Process, Queue, Event

class Profiler(Process):
    def __init__(self):
        super(Profiler, self).__init__()
        self.result_queue = Queue()
        self.stop_event = Event()
        self.cpu_data = []
        self.memory_data = []

    def run(self):
        while not self.stop_event.is_set():
            cpu_percent = psutil.cpu_percent()
            memory_percent = psutil.virtual_memory().percent
            print('cpu_percent', cpu_percent, 'memory_percent', memory_percent)
            self.cpu_data.append(cpu_percent)
            self.memory_data.append(memory_percent)
            time.sleep(1)

        self.result_queue.put({'cpu_data': self.cpu_data, 'memory_data': self.memory_data})


    def stop(self):
        self.stop_event.set()
        self.join()

    def get_result(self):
        return self.result_queue.get()
