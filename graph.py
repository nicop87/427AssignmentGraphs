import networkx as nx
import matplotlib.pyplot as plt
import argparse
import itertools

def main(argv= None):

    # All the arg parser setup to read the 6 difference command line inputs.
    # Some are optional while others exit the program if left out.
    parser = argparse.ArgumentParser(description="Read command line inputs.")
    parser.add_argument('--input', type=str, help='Input .gml graph file to load')
    parser.add_argument('--create_random_graph', nargs=2, metavar=('n', 'c'), help='Create ER random graph with n nodes and parameter c (p = (c * ln(n)) / n)')
    parser.add_argument('--multi_BFS', nargs='+', help='One or more BFS root node ids (space separated)')
    parser.add_argument('--analyze', action='store_true', help='Perform structural analysis')
    parser.add_argument('--plot', action='store_true', help='Plot the graph and analysis')
    parser.add_argument('--output', type=str, help='Write out enriched graph to .gml file')
    args = parser.parse_args(argv)

    # main graph will be an undirected graph object
    graph = nx.DiGraph()

    # If create_random_graph is set, will generate a new Erdos Renyi graph with parameters
    if args.create_random_graph:
        # Pulls paramters from argparser
        n_str, c_str = args.create_random_graph
        # makes sure they are valid input parameters
        try:
            n = int(n_str)
            c = float(c_str)
        except Exception:
            raise ValueError("--create_random_graph requires integer n and numeric c")
        
        # create graph
        graph = nx.erdos_renyi_graph(n, c)
    
    # If create_random_graph is not flagged, then use input .gml if passed, otherwise exit program
    elif args.input:
        try:
            graph = nx.read_gml(args.input)
        except FileNotFoundError:   # catches and informs user if the file wasn't found
            raise FileNotFoundError("given input file could not be found")
        except Exception:           # catches and informs user if the file found is unusable/malformed
            raise ValueError("file found, contents incompatible with .gml format")
    else:
        print("No input or graph generation specified, please use --input or --create_random_graph. Exiting Program.")
        exit()

    # Will run BFS on all the given root nodes, and display each tree on a graph when the --plot flag is triggered
    if args.multi_BFS:
        print("multiBFS")
        root_count = len(args.multi_BFS)
        # Create a figure with 1 row and 2 columns of plots 
        fig, axes = plt.subplots(1, root_count, figsize=(10, 5))

        # Starts going through each root node
        for i in range(root_count):

            # Finds all the shortest paths and the bfs tree structure
            levels = dict(nx.single_source_shortest_path_length(graph, int(args.multi_BFS[i])))
            bfs_tree = nx.bfs_tree(graph, int(args.multi_BFS[i]))

            # Also adds the bfs to each root node to the metadata of nodes
            nx.set_node_attributes(graph, levels, f"distance_to_rootnode_{args.multi_BFS[i]}")

            # Maps the values to each node, then orders them into a tree structure based on the values
            nx.set_node_attributes(bfs_tree, levels, "subset")
            pos = nx.multipartite_layout(bfs_tree, subset_key="subset")

            # draws all individual bfs trees side-by-side
            nx.draw(
                bfs_tree, pos,
                ax=axes[i],
                with_labels=True,
                node_color="lightblue",
                node_size=200,
                edge_color="gray",
                arrows=False,
                font_size=10
            )

            axes[i].set_title(f"Graph {i} (root={args.multi_BFS[i]})")
        plt.show()

    if args.analyze:
        print("analyze")

    if args.plot:
        # Moves the graph around to be more spacious
        pos = nx.spring_layout(graph, seed=42)

        # Finds a list of the isolated nodes
        isolated_nodes = list(nx.isolates(graph))

        # Draw base graph
        nx.draw(graph, pos, with_labels=True, node_color="lightgray", edge_color="lightgray")

        # Draw isolated nodes
        nx.draw(graph, pos, nodelist=isolated_nodes, with_labels=True, node_color="red", edge_color="lightgray")

        # final check to not put BFS overlays if the flag wasn't set
        if args.multi_BFS:
            roots = [int(x) for x in args.multi_BFS]
            
            # iterate through different colors for each root to use, except red, red is reserved for isolated nodes
            colors = itertools.cycle(["blue", "green", "orange", "purple", "yellow", "brown", "pink"])

            for root, color in zip(roots, colors):
                paths = nx.single_source_shortest_path(graph, root)

                # Highlight each shortest path
                for target, path in paths.items():
                    path_edges = list(zip(path[:-1], path[1:]))
                    nx.draw_networkx_edges(graph, pos, edgelist=path_edges, width=2, edge_color=color)

                # Highlight root node
                nx.draw_networkx_nodes(graph, pos, nodelist=[root], node_color=color, node_size=600)

            plt.title("Highlighted Shortest Paths from Multiple BFS Roots")
        else: 
            plt.title("Graph with no given root nodes")
        plt.show()
    
    # outputs the whole graph to a .gml file, also adds metadata to note if nodes are isolated
    if args.output: 
        # adds metadata for component id's
        components = list(nx.connected_components(graph))
        for component_id, comp in enumerate(components):
            nx.set_node_attributes(graph, {n: component_id for n in comp}, name="component_id")

        # all nodes get indicated true or false for isolation
        isolated_nodes = list(nx.isolates(graph))
        nx.set_node_attributes(graph, "False", name="isolated")
        nx.set_node_attributes(graph, {n: "True" for n in isolated_nodes}, name="isolated")
        nx.write_gml(graph, f"{args.output}")

if __name__ == "__main__":
    main()