# -*- coding: utf-8 -*-
__author__ = 'antonio'

import pp
import sys
import datetime

# Количество процессов
proc_num = 2

try:
    filename = sys.argv[1]
except IndexError:
    print 'example: python script.py cities.txt'
    sys.exit()

city_array = []
for line in open(filename):
    city_array.append(line.strip().decode('utf-8'))

exclude = [u'Ь',u'Ъ',u'Ы']
total = {}
orgraph = {}

for city in city_array:
    edge = []
    for c in [x for x in city_array if x != city]:
        if city[-1:].upper() in exclude:
            if c[0].upper() == city[-2:-1].upper():
                edge.insert(1, c)
        else:
            if c[0].upper() == city[-1:].upper():
                edge.insert(1, c)
    orgraph.update({city: edge})

def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if not graph.has_key(start):
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths

job_server = pp.Server(proc_num, ppservers=())
print u'Старт поиска. Процессов: ', job_server.get_ncpus()

start = datetime.datetime.now()

for city in city_array:
#    print '---------------------------------------'
#    print u'поиск для города: %s' % city
#    print '---------------------------------------'
    jobs = [(x, job_server.submit(find_all_paths,(orgraph, city, x))) for x in city_array if x != city]
    for input, job in jobs:
#        print u'Закончен поиск до города: %s' % input
        for j in job():
            total.update({len(j) : j})
#    job_server.print_stats()
stop = datetime.datetime.now()

result = total.get(max(total))
print u'Результат:'
print ' -> '.join(result)
print u'Максимальная цепочка: %d' % len(result)
print u'Время работы: %s' % str(stop - start)