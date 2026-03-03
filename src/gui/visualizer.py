import matplotlib.pyplot as plt
import networkx as nx


def draw_network(adj_list):
    G = nx.Graph()
    for u, neighbors in adj_list.graph.items():
        for v in neighbors:
            G.add_edge(u, v)

    plt.figure(figsize=(8, 6))
    nx.draw(G, with_labels=True, node_color='skyblue', edge_color='gray', node_size=800, font_size=10)
    plt.title("社交网络关系拓扑图")
    plt.show()