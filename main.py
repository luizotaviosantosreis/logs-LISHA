import psutil, time
from datetime import datetime
import os

# returns process that most consume memory
'''def get_processes():

    # ps.process_iter() returns all process running with all their details
    # here we take the name and memory usage of the top 5 processes that most consume memory
    processes = [(proc.info['name'], proc.info['memory_percent']) for proc in sorted(ps.process_iter(['name', 'memory_percent']), key=lambda proc:proc.info['memory_percent'])][-5:]
    return processes

for process in get_processes():
    print(process)
'''
for p in ps.process_iter():
    print(ps.disk_usage('/'))
    break


class CustomProcess(psutil.Process):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def try_create_time(self, *args, **kwargs):
        try:
            create_time = datetime.fromtimestamp(super().create_time(*args, **kwargs))
        except OSError:
            create_time = datetime.fromtimestamp(psutil.boot_time())
        return create_time

    def try_CPU_cores(self, *args, **kwargs):
        try:
            cores = len(super().cpu_affinity(*args, **kwargs))
        except psutil.AccessDenied:
            cores = 0
        return cores

    def try_nice(self, *args, **kwargs):
        try:
            nice = int(super().nice(*args, **kwargs))
        except psutil.AccessDenied:
            nice = 0
        return nice

    def try_memory_usage(self, *args, **kwargs):
        try:
            # get the memory usage in bytes
            memory_usage = super().memory_full_info().uss
        except psutil.AccessDenied:
            memory_usage = 0
        return memory_usage

    def try_iocounters(self, *args, **kwargs):
        try:
            io_counters = process.io_counters()
            read_bytes = io_counters.read_bytes
            write_bytes = io_counters.write_bytes
        except psutil.AccessDenied:
            io_counters = 0
            read_bytes = 0
            write_bytes = 0
