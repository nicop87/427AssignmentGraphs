import networkx as nx
import matplotlib.pyplot as plt
import argparse

def main(argv= None):
    parser = argparse.ArgumentParser(description="Graph generation, analysis, BFS, and visualization tool.")


    parser.add_argument('--input', type=str, help='Input .gml graph file to load')
    parser.add_argument('--create_random_graph', nargs=2, metavar=('n', 'c'),
    help='Create ER random graph with n nodes and parameter c (p = (c * ln(n)) / n)')
    parser.add_argument('--multi_BFS', nargs='+', help='One or more BFS root node ids (space separated)')
    parser.add_argument('--analyze', action='store_true', help='Perform structural analysis')
    parser.add_argument('--plot', action='store_true', help='Plot the graph and analysis')
    parser.add_argument('--output', type=str, help='Write out enriched graph to .gml file')


    args = parser.parse_args(argv)

    # temp variables and make a erdos renyi graph
    n = 12
    p = 0.3
    root = 0
    G = nx.erdos_renyi_graph(n, p)

    # a dict that assigns each node's distance from the root of the bfs
    levels = dict(nx.single_source_shortest_path_length(G, root))

    print(levels)

    # test code for breadth first search
    bfs_tree = nx.bfs_tree(G, root)

    # Assign "subset" attribute = level
    nx.set_node_attributes(bfs_tree, levels, "subset")

    # --- Step 4: Layout & Draw ---
    pos = nx.multipartite_layout(bfs_tree, subset_key="subset")

    plt.figure(figsize=(8, 6))
    nx.draw(
        bfs_tree, pos,
        with_labels=True,
        node_color="skyblue",
        node_size=800,
        edge_color="gray",
        arrows=False,
        font_size=10
    )
    plt.title(f"BFS Tree from root {root}")
    plt.show()

if __name__ == "__main__":
    main()