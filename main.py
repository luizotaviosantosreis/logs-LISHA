from customprocess import CustomProcess
import psutil, time, os, argparse
import pandas as pd

def get_processes():
    processes = []
    for process in psutil.process_iter():
        with process.oneshot():
            cp = CustomProcess(process)
            cp_data = cp.get_data()
            processes.append(cp_data)
    return processes

def construct_table(processes, sort_by, ascending):
    table = pd.DataFrame(processes)
    table.set_index('pid', inplace=True)
    table.sort_values(sort_by, inplace=True, ascending=ascending)
    table['memory_usage'] = table['memory_usage'].apply(get_size)
    table['write_bytes'] = table['write_bytes'].apply(get_size)
    table['read_bytes'] = table['read_bytes'].apply(get_size)
    return table

def get_size(bytes):
    for i in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{i}B"
        bytes /= 1024

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", dest="sort_by", help="Column to sort by.", default="cpu_usage")
    ## ADD A COLUMN FILTER
    parser.add_argument("--ascending", action="store_true", help="sort in ascending order.")
    parser.add_argument("-n", help="Number of processes to show.", default=25)
    parser.add_argument("-u", "--update", action="store_true", dest='update', help="keep the program running and updating each second")

    parse_args = parser.parse_args()
    sort_by = parse_args.sort_by
    ascending = parse_args.ascending
    n = int(parse_args.n)
    update = parse_args.update
    
    if update:
        while update:
            processes_list = get_processes()
            os.system("cls") if "nt" in os.name else os.system("clear")
            table = construct_table(processes_list, sort_by, ascending)
            print(table.head(n).to_string())
            time.sleep(1)
    else:
        processes_list = get_processes()
        table = construct_table(processes_list, sort_by, ascending)
        print(table.to_string())

if __name__ == '__main__':
    main()
