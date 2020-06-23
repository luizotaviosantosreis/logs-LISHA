import psutil as ps


# returns process that most consume memory
def get_processes():

    # ps.process_iter() returns all process running with all their details
    # here we take the name and memory usage of the top 5 processes that most consume memory
    processes = [(proc.info['name'], proc.info['memory_percent']) for proc in sorted(ps.process_iter(['name', 'memory_percent']), key=lambda proc:proc.info['memory_percent'])][-5:]
    processes2 = [(proc.info['name'], '%.2f %%'%(proc.info['cpu_percent'])) for proc in sorted(ps.process_iter(['name', 'cpu_percent']), key=lambda proc:proc.info['cpu_percent'])][-5:]
    return processes, processes2

for process in get_processes():
    print(process)
