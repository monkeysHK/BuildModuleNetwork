# -*- coding: utf-8 -*-

import requestpage, pickle

# This script is responsible for building the graph using BFS.

# Define a list of starting pages for BFS.
# If there are any pages that are not "dependency-linked" with existing starting pages,
# append those items to the following list so that they can be BFS-ed
startFromPages = [
    "Pet"
]

# Fetch each page content: detect require(), mw.loadData(), loader.require(), and loader.loadData()
# Using BFS, build dependencies graph
queue = []
dependenciesGraph = {}

for pg in startFromPages:
    name = pg.replace("Module:", "")
    queue.append(name)

while len(queue) > 0:
    name = queue.pop(0)
    if name.strip() != "" and not name in dependenciesGraph:
        print("Finding dependencies for", name)
        dependencies = requestpage.findDependencies(name)
        print(dependencies)
        dependenciesGraph[name] = dependencies
        queue += dependencies

print(dependenciesGraph)

with open("dependencies-graph.txt", "w") as f:
    f.write(str(dependenciesGraph))
    f.close()

with open('dependencies-graph.pickle', 'wb') as f:
    pickle.dump(dependenciesGraph, f)
