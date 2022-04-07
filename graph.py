import networkx as nx
import matplotlib.pyplot as plt
G = nx.Graph()
G.add_edges_from([('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'A'),
                 ('B', 'E'), ('E', 'F'), ('F', 'G'), ('G', 'E')])
# pos = nx.planar_layout(G) #choose layout for graph
print(nx.is_connected(G))
A = nx.adjacency_matrix(G)
print(A.todense())
print(list(nx.bridges(G)))
nx.draw(G, with_labels=True)
plt.show()
