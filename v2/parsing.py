import sys
import re
import process as p

def get_stock_process(stocks, process):
    visited = []
    count = len(stocks)
    for key in stocks:
        visited.append(key)
    for i in range(len(process)):
        if process[i][2] != None:
            for key in process[i][2]:
                if key not in visited:
                    visited.append(key)
                    count += 1
    return count

def create_furniture_list(raw):
    list_s = {}
    if ';' in raw:
        first = raw.split(';')
        for elem in first:
            pars = elem.split(':')
            pars[1] = pars[1].replace('\n', '')
            list_s[pars[0]] = int(pars[1])
    else:
        pars = raw.split(':')
        pars[1] = pars[1].replace('\n', '')
        list_s[pars[0]] = int(pars[1])
    return list_s

def parse_process(name, raw, cycle):
    needed = None
    result = None
    i = raw.find('(')
    j = raw.find(')')
    if raw[i] == '(' and raw[j] == ')':
        needed = raw[i + 1:j]
        needed = create_furniture_list(needed)
    next = raw[j + 1::]
    i = next.find('(')
    j = next.find(')')
    if next[i] == '(' and next[j] == ')':
        result = next[i + 1:j]
        result = create_furniture_list(result)
    return [name, needed, result, int(cycle.replace('\n', ''))]

def get_optimized(optimize, str):
    tmp = str.split(';')
    for elem in tmp:
        optimize.append(re.sub('[^a-zA-Z_]', '', elem))
    return optimize

def init_stocks(ressource):
    """Parsing du fichier source et initialisation des stocks"""
    stock = {}
    process = []
    optimize = []
    try :
        test = open(ressource, 'r')
        test.close()
    except:
        print("Please give a valid file")
        exit(1)
    with open(ressource, 'r') as file:
        tmp = file.readline()
        while tmp:
            pars = tmp.split(':') if tmp[0] != '#' else ''
            if (len(pars) == 2) and pars[0] != 'optimize':
                pars[1] = pars[1].replace('\n', '')
                stock[pars[0]] = int(pars[1])
            elif (len(pars) > 2):
                process.append(parse_process(pars[0], tmp, pars[-1]))
            if len(pars) >= 2 and pars[0] == 'optimize':
                optimize = get_optimized(optimize, pars[1])
            tmp = file.readline()
    if not optimize:
        print("Optimize info missing, stopping now.")
        sys.exit()
    if len(stock) == 0:
        print("There is no stock available, stopping now.")
        sys.exit()
    if len(process) == 0:
        print("There is no process to optimize, stopping now.")
        sys.exit()
    return stock, process, optimize

def init_instances_processes(ressource):
    list_node = []
    stock, process, optimize = init_stocks(ressource)
    for elem in process:
        node = p.Process(elem[0], elem[3])
        node.req = elem[1]
        node.results = elem[2]
        list_node.append(node)
    return stock, list_node, optimize
