# This script is responsible for building the graph visualization

from pyvis.network import Network
import networkx as nx
import pickle

# Load information

with open('build/dependencies-graph.pickle', 'rb') as f:
    usesRelationsMap: dict[str, list[str]] = pickle.load(f)

with open('build/datapages.pickle', 'rb') as f:
    dataPages: list[str] = pickle.load(f)

with open('build/externalpages.pickle', 'rb') as f:
    externalPages: list[str] = pickle.load(f)

# Initialize the network

# Build the reverse of USES relations

usedByRelationsMap: dict[str, list[str]] = {}

for node, dependencies in usesRelationsMap.items():
    usedByRelationsMap[node] = []

for node, dependencies in usesRelationsMap.items():
    for dep in dependencies:
        usedByRelationsMap[dep].append(node)

# Build the graph

dag = nx.DiGraph() # initialize the graph

# Add nodes

for node in usesRelationsMap.keys():
    # color = None
    # if node in dataPages:
    #     color = None
    # elif node in externalPages:
    #     color = "#63b833"
    # else:
    #     color = "#dd4b39"
    group = 0 if node in dataPages else 1 if node in externalPages else 10
    dag.add_node(node,
        label=node,
        # weight=len(usedByRelationsMap[node]),
        size=70,
        title=f"Name: {node}\nUses (outdegree): {str(len(usesRelationsMap[node]))}\nUsed by (indegree): {str(len(usedByRelationsMap[node]))}",
        # color=color,
        group=group
    )

# Add edges based on USES relation

for node in usesRelationsMap.keys():
    for dep in usesRelationsMap[node]:
        dag.add_edge(node, dep)

pos = nx.drawing.nx_agraph.graphviz_layout(dag, prog='dot', args='-Grankdir=BT -Granksep=3 -Gnodesep=0.02 -Nmargin=0.5')

# Draw the pyvis network

# net = Network(directed=True, neighborhood_highlight=True, select_menu=True, filter_menu=True, layout=True)
net = Network(directed=True, neighborhood_highlight=True, select_menu=True, filter_menu=True)
net.from_nx(dag)
# net.repulsion()
net.show_buttons()

for node in net.get_nodes():
    net.get_node(node)['x']=pos[node][0]
    net.get_node(node)['y']=-pos[node][1] #the minus is needed here to respect networkx y-axis convention 
    net.get_node(node)['physics']=False
    net.get_node(node)['font']={"size": 48, "strokeWidth": 12}
    net.get_node(node)['label']=str(node) #set the node label as a string so that it can be displayed

net.show('docs/nodes.html', notebook=False)
