import networkx as nx


def analyze(graph):
    
    # Results of each check
    results = {}

    # Connected Components
    components = list(nx.weakly_connected_components(graph))
    # Puts the results into our results dict
    results["connected components"] = len(components)


    # Cycle Determination 
    try:
        # Boolean check to see if a cycle exists
        Ugraph = graph.to_undirected()
        nx.find_cycle(graph, orientation="original")
        has_cycle = True
    except nx.NetworkXNoCycle: 
        #if the cycle check returns an error 
        has_cycle = False
    results['has cycle'] = has_cycle

    # Isolated nodes
    results["isolated nodes"] == list(nx.isolates(graph))

    # Graph density
    results["density"] = nx.density(graph)

    # Average shortest path length
        #checking to see if the graph is connected 
    if nx.is_weakly_connected(graph):
        Ugraph = graph.to_undirected()
        #this allows us to get the shortest path without caring about direction
        avg_short = nx.average_shortest_path_length(Ugraph)
        results["average shortest path length"] = avg_short
    else:
        #this is if there are any isolated nodes
        results["average shortest path length"] = "The graph is not connected"


    print("The results of analyzing the given graph:")
    print(f"There are {results['connected components']} connected components in the graph.")
    if results[has_cycle]:
        print('There is a cycle.')
    else:
        print("There is no cycle.")
    print(f"There are {len(results['isolated nodes'])} isolated nodes in the graph.")
    print(f"The graph has a density of {results['density']}.")
    print(f"The average shortest path of the graph is {results['average shortest path length']}.")

