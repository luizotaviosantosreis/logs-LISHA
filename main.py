from customprocess import CustomProcess
import psutil, time, os, argparse, json, logging
import pandas as pd

# get configuration from config.json
def config():
    global verbose_config
    global report_config
    # open config.json
    file = open("config.json", "r")
    # load the file as json
    config = json.load(file)
    # get update and report configuration
    verbose_config = config['verbose_config']
    report_config = config['report_config']
    file.close()

# cofigure report system
def log():
    global logger
    LOG_FORMAT = '%(asctime)s - %(message)s'
    logging.basicConfig(filename='report.log',
                        level = logging.DEBUG,
                        format = LOG_FORMAT,
                        filemode = 'w')
    logger = logging.getLogger()

# return all the processes and the detail specified
def get_processes(*args):
    # contain all processes dictionaries
    processes = []
    for process in psutil.process_iter():
        # get process info in oneshot
        with process.oneshot():
            cp = CustomProcess(process)
            # get the process detail
            cp_data = cp.get_data(*args)
            processes.append(cp_data)
    return processes

# construct the processes data frame
def construct_table(processes, sort_by, ascending):
    # create the dataframe
    table = pd.DataFrame(processes)
    # sort processes
    if sort_by in table.columns:
        table.sort_values(sort_by, inplace=True, ascending=ascending)
    # apply a nice view to the bytes amount
    if 'memory_usage' in table.columns:
        table['memory_usage'] = table['memory_usage'].apply(get_size)
    if 'write_bytes' in table.columns:
        table['write_bytes'] = table['write_bytes'].apply(get_size)
    if 'read_bytes' in table.columns:
        table['read_bytes'] = table['read_bytes'].apply(get_size)
    return table

# apply a nice view to the bytes specified
def get_size(bytes):
    for i in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{i}B"
        bytes /= 1024

def main():
    # parser initialization
    parser = argparse.ArgumentParser()
    # parser arguments
    parser.add_argument("-v", "--verbose", action="store_true", dest='verbose', help="show the processes table")
    # get parser arguments
    parse_args = parser.parse_args()
    verbose = parse_args.verbose
    # get config data
    sort_by = verbose_config['sort_by']
    ascending = verbose_config['ascending']
    n = verbose_config['rows']
    columns =verbose_config['columns']

    if verbose:
        # keep updating processes data
        while True:
            # get all processes and their detail
            processes_list = get_processes(*columns)
            # clear the window
            os.system("cls") if "nt" in os.name else os.system("clear")
            # create process dataframe
            table = construct_table(processes_list, sort_by, ascending)
            print(table.head(n).to_string(index=False))
            print("CPU: %.3f%%\nMEMORY: %.3f%%" % (psutil.cpu_percent(), psutil.virtual_memory().used/psutil.virtual_memory().total*100))
            time.sleep(3)

            # ADD REPORT WITH VERBOSE

    # report system
    else:
        # get report configuration
        max_cpu = report_config['max_cpu_percent']
        max_memory = report_config['max_memory_percent']
        print('process manager running. See detail in report.log')
        while True:
            current_cpu_usage = psutil.cpu_percent()
            current_memory_usage = psutil.virtual_memory().used/psutil.virtual_memory().total * 100
            if max_cpu < current_cpu_usage:
                # get processes and their cpu usage
                processes_list = get_processes('name', 'cpu_usage')
                # create process dataframe
                table = construct_table(processes=processes_list, sort_by='cpu_usage', ascending=False)
                # make a report
                logger.info('max_cpu exceeded : %.2f%%\nprocesses:\n %s\n' % (current_cpu_usage, table.head(5).to_string(index=False)))

            if max_memory < current_memory_usage:
                # get processes and their memory usage
                processes_list = get_processes('name', 'memory_usage')
                # create process dataframe
                table = construct_table(processes=processes_list, sort_by='memory_usage', ascending=False)
                # make a report
                logger.info('max_memory exceeded : %.2f%%\nprocesses:\n %s\n' % (current_memory_usage, table.head(5).to_string(index=False)))
            time.sleep(3)

if __name__ == '__main__':
    log()
    config()
    main()
