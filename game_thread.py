# -*- encoding: utf-8 -*-
__author__ = 'antonio'

import Queue
import threading
import sys
import datetime

# Количество потоков
thread_num = 2

try:
    filename = sys.argv[1]
except IndexError:
    print 'example: python script.py cities.txt'
    sys.exit()

city_array = []
for line in open(filename):
    city_array.append(line.strip().decode('utf-8'))

exclude = [u'Ь',u'Ъ',u'Ы']
exit_flag = False
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

class CityFinder(threading.Thread):
    def run(self):
        while not city_pool.empty():
            city = city_pool.get()
            for x in [x for x in city_array if x != city]:
                res = find_all_paths(orgraph, city, x)
                for r in res:
                    total.update({len(r) : r})
            city_pool.task_done()

city_pool = Queue.Queue()
for item in city_array:
    city_pool.put(item)

print u'Старт поиска. Потоков: ', thread_num

start = datetime.datetime.now()
for x in xrange(thread_num):
    CityFinder().start()
city_pool.join()
stop = datetime.datetime.now()

result = total.get(max(total))

print u'Результат:'
print ' -> '.join(result)
print u'Максимальная цепочка: %d' % len(result)
print u'Время работы: %s' % str(stop - start)