import psutil
from datetime import datetime

class CustomProcess():
    def __init__(self, process):
        self.process = process
        self.pid()
        self.name()
        self.create_time()
        self.cpu_usage()
        self.status()
        self.CPU_cores()
        self.nice()
        self.memory_usage()
        self.io_counters()
        self.num_threads()
        self.username()

    def pid(self):
        try:
            self.pid = self.process.pid
        except psutil.AccessDenied:
            self.pid = -1

    def name(self):
        try:
            self.name = self.process.name()
        except psutil.AccessDenied:
            self.name = 'Access Denied'

    def create_time(self):
        try:
            self.create_time = datetime.fromtimestamp(self.process.create_time())
        except OSError:
            self.create_time = datetime.fromtimestamp(psutil.boot_time())

    def cpu_usage(self):
        try:
            self.cpu_usage = self.process.cpu_percent()
        except psutil.AccessDenied:
            self.cpu_usage = -1

    def status(self):
        try:
            self.status = self.process.status()
        except psutil.AccessDenied:
            self.status = 'Access Denied'

    def CPU_cores(self):
        try:
            self.cores = len(self.process.cpu_affinity())
        except psutil.AccessDenied:
            self.cores = -1

    def nice(self):
        try:
            self.nice = int(self.process.nice())
        except psutil.AccessDenied:
            self.nice = 0

    def memory_usage(self):
        try:
            self.memory_usage = self.process.memory_info().rss
        except psutil.AccessDenied:
            self.memory_usage = -1

    def io_counters(self):
        try:
            io_counters = self.process.io_counters()
            self.read_bytes = io_counters.read_bytes
            self.write_bytes = io_counters.write_bytes
        except psutil.AccessDenied:
            self.read_bytes = -1
            self.write_bytes = -1

    def num_threads(self):
        try:
            self.n_threads = self.process.num_threads()
        except psutil.AccessDenied:
            self.n_threads = -1

    def username(self):
        try:
            self.username = self.process.username()
        except psutil.AccessDenied:
            self.username = 'Access Denied'

    def get_data(self, *args):
        data = {'pid' : self.pid,
                'name' : self.name,
                'cpu_usage' : self.cpu_usage,
                'memory_usage' : self.memory_usage,
                'read_bytes' : self.read_bytes,
                'write_bytes' : self.write_bytes,
                'status' : self.status,
                'username' : self.username
                }
        return data
