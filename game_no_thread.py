# -*- encoding: utf-8 -*-
__author__ = 'antonio'

import datetime
import sys

city_array = []

try:
    filename = sys.argv[1]
except IndexError:
    print 'example: python script.py cities.txt'
    sys.exit()

for line in open(filename):
    city_array.append(line.strip().decode('utf-8'))

exclude = [u'Ь',u'Ъ',u'Ы']
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

total = {}
start = datetime.datetime.now()
for city in city_array:
    for c in [x for x in city_array if x != city]:
        res = find_all_paths(orgraph, city, c)
        for r in res:
            total.update({len(r) : r})
stop = datetime.datetime.now()

result = total.get(max(total))
print u'Результат:'
print ' -> '.join(result)
print u'Максимальная цепочка: %d' % len(result)
print u'Время работы: %s' % str(stop - start)