from pyvis.network import Network
import pickle

# This script is responsible for doing statistics and building the graph visualization

with open('dependencies-graph.pickle', 'rb') as f:
    dependenciesGraph = pickle.load(f)

with open('datapages.pickle', 'rb') as f:
    dataPages = pickle.load(f)

with open('externalpages.pickle', 'rb') as f:
    externalPages = pickle.load(f)

dependentGraph = {} # this is the reverse of dependencies graph

nodeIndexMap = {}

net = Network(directed=True, neighborhood_highlight=True, filter_menu=True)

for node, dependencies in dependenciesGraph.items():
    dependentGraph[node] = []

for node, dependencies in dependenciesGraph.items():
    for dep in dependencies:
        dependentGraph[dep].append(node)

nodeList = list(dependentGraph.items())

for index, value in enumerate(nodeList):
    node, dependents = value
    nodeIndexMap[node] = index
    net.add_node(index,
        label=node,
        value=len(dependents),
        title=f"Name: {node}\nID: {str(index)}\nDependent modules (indegree): {str(len(dependents))}\nDependencies (outdegree): {str(len(dependenciesGraph[node]))}",
        color=node in dataPages and "#dd4b39" or node in externalPages and "#63b833" or None)

for index, value in enumerate(nodeList):
    node, dependents = value
    for dep in dependents:
        net.add_edge(nodeIndexMap[dep], index)

net.repulsion()
net.show_buttons()
net.show('nodes.html')
