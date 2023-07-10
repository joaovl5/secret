import networkx as nx
import matplotlib.pyplot as plt

# G = nx.connected_caveman_graph(3, 3)

sizes = [2, 2, 3]
probs = [[0.25, 0.05, 0.02], [0.05, 0.35, 0.07], [0.02, 0.07, 0.40]]
G = nx.davis_southern_women_graph()
	


#G = nx.ring_of_cliques(2, 5)

# explicitly set positions


nx.draw_networkx(G)

# Set margins for the axes so that nodes aren't clipped

pos = nx.spring_layout(G, seed=3068)
print(pos)
nx.draw(G, pos=pos, with_labels=True)
plt.show()