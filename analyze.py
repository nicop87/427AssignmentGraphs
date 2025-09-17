import networkx as nx


def analyze(graph):
    
    # Results of each check
    results = {}

    # Connected Components
    components = list(nx.weakly_connected_components(graph))
    # Puts the results into our results dict
    results["connected components"] = components


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
    isolated = []
    for n in graph.nodes:
        # Checks every node if there are no incoming or outgoing edges
        if graph.in_degree(n) == 0 and graph.out_degree(n):
            isolated.append(n)
    results["isolated nodes"] == isolated

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


    return results

