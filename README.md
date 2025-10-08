# 427AssignmentGraphs
By Leo Pan 030025552 and Nicolas Piker 029966545

## Dependencies
We installed and utilized the python `networkx` and `matplotlib.pyplot` packages, in addition to the base python packages `argparse` and `itertools`.

## Implementations
Utilized functions of `networkx` to generate graphs, conduct BFS', detect cycles, find isolated nodes, group components by ID, calculate graph density, and find average shortest path lengths. `matplotlib` was used in conjunction to visualize the graphs, and hightlight or color points of interest. `argparse` was used to read command line parameters, and `itertools` was used just to cycle through different root node colors (only 7 colors are distinct it will cycle back through if you list more roots, and red is reserved for isolated non-root nodes.) Also `numpy` briefly for list type conversions.

## Running the program
Run `python ./graph.py` with the following parameters:
* `--input` followed by the name of a `.gml` file will make the program take the file as an input graph to analyze and visualize.
* `--create_random_graph` with a size and constant parameter will create a random graph with the size number of nodes and the probability of edges being created determined by the constant from 0.0 to 1.0.
* `--multi_BFS` will run the bfs on the following root nodes given. Needs to be integers and space separated. If an invalid node is given it will ignore it.
* `--analyze` this flag will output analytics about the graph to the console.
* `--plot` this flag will plot the whole graph with highlighted root nodes and their shortest paths, and isolated nodes in red.
* `--output` follow with a file name, will output the .gml and metadata of the current graph to that file name.

Note: If you have the `--multi_BFS` and `--plot` flags set, you will need to close the BFS tree graphs for the plot graph and `--analyze` analytics to appear. and once you close the plot graph the program will print to an output file if the `--output` flag was set.

The following command makes use of all flags except `--input`.

E.g `python ./graph.py --create_random_graph 20 0.5 --multi_BFS 0 5 10 --analyze --plot --output final_graph.gml` 

This will create a random graph with 20 nodes, with a 0.5 constant. Run bfs on the root nodes 0, 5, and 10. Output analytics to the console, plot the graph visually, and finally output the graph to `final_graph.gml` or make one if it doesn't already exist.

E.g `python ./graph.py --input example.gml --analyze --plot` 

This command will instead use a graph stored in `example.gml` as input and post analytics and plot it visually.
