import psutil
from datetime import datetime

class CustomProcess():
    def __init__(self, process):
        self.process = process
        self.io_counters()

    # get process pid
    def pid(self):
        try:
            pid = self.process.pid
        except psutil.AccessDenied:
            pid = -1
        return pid

    # get process name
    def name(self):
        try:
            name = self.process.name()
        except psutil.AccessDenied:
            name = 'Access Denied'
        return name

    # get process creation time
    def create_time(self):
        try:
            create_time = datetime.fromtimestamp(self.process.create_time())
        except OSError:
            create_time = datetime.fromtimestamp(psutil.boot_time())
        return create_time

    # get process cpu usage (percent)
    def cpu_usage(self):
        try:
            cpu_usage = self.process.cpu_percent()/psutil.cpu_count()
        except psutil.AccessDenied:
            cpu_usage = -1
        return cpu_usage

    # get process status
    def status(self):
        try:
            status = self.process.status()
        except psutil.AccessDenied:
            status = 'Access Denied'
        return status

    # get process niceness (priority from -20 to 19, where -20 is the highest, 19 the lowest and 0 the default)
    def nice(self):
        try:
            nice = int(self.process.nice())
        except psutil.AccessDenied:
            nice = 0
        return nice

    # get process memory usage (rss)
    def memory_usage(self):
        try:
            memory_usage = self.process.memory_full_info().uss
        except psutil.AccessDenied:
            memory_usage = -1
        return memory_usage

    # get process i/o statistics
    def io_counters(self):
        try:
            self.io_counters = self.process.io_counters()
        except psutil.AccessDenied:
            self.io_counters = False

    # get process read bytes
    def read_bytes(self):
        if self.io_counters:
            try:
                read_bytes = self.io_counters.read_bytes
            except psutil.AccessDenied:
                read_bytes = -1
            return read_bytes
        return -1

    # get process write bytes
    def write_bytes(self):
        if self.io_counters:
            try:
                write_bytes = self.io_counters.write_bytes
            except psutil.AccessDenied:
                write_bytes = -1
            return write_bytes
        return -1

    # get name of the user that owns the process
    def username(self):
        try:
            username = self.process.username()
        except psutil.AccessDenied:
            username = 'Access Denied'
        return username

    # get the process data specified in args
    def get_data(self, *args):
        s_to_f = {'pid' : self.pid,
                  'name' : self.name,
                  'cpu_usage' : self.cpu_usage,
                  'memory_usage' : self.memory_usage,
                  'read_bytes' : self.read_bytes,
                  'write_bytes' : self.write_bytes,
                  'status' : self.status,
                  'username' : self.username,
                  'nice' : self.nice,
                  'create_time' : self.create_time
                  }
        data = {}
        data['pid'] = s_to_f['pid']()
        for arg in args:
            try:
                data[arg] = s_to_f[arg]()
            except KeyError:
                raise KeyError(f'invalid column specified: \'{arg}\'') from None
        return data
