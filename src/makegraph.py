# -*- coding: utf-8 -*-

import requestpage, pickle, json

# This script is responsible for building the graph using BFS.

# Define a list of starting pages for BFS. In this case, we request all module pages from API
# and filter it using custom rules
# 
# This list can also be self-defined!
# For example, using just ["Pet"], the BFS will give 88 modules!
# If there are any pages that are not "dependency-linked" with existing starting pages,
# append those items to the following list so that they can be BFS-ed
startFromPages = requestpage.requestListOfAllPages(828, "Module:")

print(f"Number of starting pages: {len(startFromPages)}")

# Fetch each page content: detect require(), mw.loadData(), loader.require(), and loader.loadData()
# Using BFS, build dependencies graph
queue = []
dependenciesGraph = {}
dataPages = []
externalPages = []

for pg in startFromPages:
    name = pg.replace("Module:", "")
    queue.append(name)

while len(queue) > 0:
    name = queue.pop(0).strip()
    name = name if len(name) < 1 else name[0].upper() + name[1:]
    if name != "" and not name in dependenciesGraph:
        print("Finding dependencies for", name)
        dependencies, dataDependencies, isExternal = requestpage.findDependencies(name)
        combinedDependencies = [name[0].upper() + name[1:] for name in filter(lambda page: page.strip() != "", dependencies + dataDependencies)]
        dependenciesGraph[name] = combinedDependencies
        queue += combinedDependencies
        dataPages += dataDependencies
        print("External" if isExternal else combinedDependencies)
        if isExternal:
            externalPages.append(name)

dataPages = list(set(dataPages))

print(dependenciesGraph)
print(len(dependenciesGraph))

with open("dependencies-graph.txt", "w") as f:
    f.write(json.dumps(dependenciesGraph, indent=4))
    f.close()

with open('dependencies-graph.pickle', 'wb') as f:
    pickle.dump(dependenciesGraph, f)

with open("datapages.txt", "w") as f:
    f.write(json.dumps(dataPages, indent=4))
    f.close()

with open('datapages.pickle', 'wb') as f:
    pickle.dump(dataPages, f)

with open("externalpages.txt", "w") as f:
    f.write(json.dumps(externalPages, indent=4))
    f.close()

with open('externalpages.pickle', 'wb') as f:
    pickle.dump(externalPages, f)
