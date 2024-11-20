from collections import defaultdict
import json
#############################################################################################################################
#
# Use:
# The `Graph` class  is used to represent and store the data for the TMDb co-actor network graph.  This class
# also provide some basic analytics, i.e., number of nodes, edges, and nodes with the highest degree.
#
# The `TMDbAPIUtils` class is used to retrieve Actor/Movie data using themoviedb.org API.  We have provided a few necessary methods
# to test your code w/ the API, e.g.: get_move_detail(), get_movie_cast(), get_movie_credits_for_person(). Additional
# methods and instance variables as desired.
#
# The data that is retrieved from the TMDb API is used to build the graph using the Graph class.  After you build your graph using the
# TMDb API data, use the Graph class write_edges_file & write_nodes_file methods to produce the separate nodes and edges
# .csv files as well as graph.json for use with the index.html file to create a network visualization using D3.js.
#
#############################################################################################################################


class Graph:

    # Do not modify
    def __init__(self, with_nodes_file=None, with_edges_file=None):
        """
        option 1:  init as an empty graph and add nodes
        option 2: init by specifying a path to nodes & edges files
        """
        self.nodes = []
        self.edges = []
        if with_nodes_file and with_edges_file:
            nodes_CSV = csv.reader(open(with_nodes_file))
            nodes_CSV = list(nodes_CSV)[1:]
            self.nodes = [(n[0], n[1]) for n in nodes_CSV]

            edges_CSV = csv.reader(open(with_edges_file))
            edges_CSV = list(edges_CSV)[1:]
            self.edges = [(e[0], e[1]) for e in edges_CSV]

    def add_node(self, id: str, name: str, total_movies: str) -> None:
        """
        add a tuple (id, name) representing a node to self.nodes if it does not already exist
        The graph should not contain any duplicate nodes
        """
        node = (id, name, total_movies)
        if node not in self.nodes:
            self.nodes.append(node)
        return None

    def add_edge(self, source: str, target: str) -> None:
        """
        Add an edge between two nodes if it does not already exist.
        An edge is represented by a tuple containing two strings: e.g.: ('source', 'target').
        Where 'source' is the id of the source node and 'target' is the id of the target node
        e.g., for two nodes with ids 'a' and 'b' respectively, add the tuple ('a', 'b') to self.edges
        """
        edge = (source, target)
        self.edges.append(edge)
        return None

    def total_nodes(self) -> int:
        """
        Returns an integer value for the total number of nodes in the graph
        """
        return len(self.nodes)

    def total_edges(self) -> int:
        """
        Returns an integer value for the total number of edges in the graph
        """
        return len(self.edges)

    def max_degree_nodes(self) -> dict:
        """
        Return the node(s) with the highest degree
        Return multiple nodes in the event of a tie
        Format is a dict where the key is the node_id and the value is an integer for the node degree
        e.g. {'a': 8}
        or {'a': 22, 'b': 22}
        """
        degree_dict = {}
        for n in self.edges:
            degree_dict[n[0]] = degree_dict.get(n[0], 0) + 1
            degree_dict[n[1]] = degree_dict.get(n[1], 0) + 1
        max_degree = max(degree_dict.values())

        # max_deg_nodes = {(k, v) for k, v in degree_dict.items() if v == max_degree}
        max_deg_nodes = dict(filter(lambda x: x[1] == max_degree, degree_dict.items()))
        return max_deg_nodes

    def print_nodes(self):
        """
        No further implementation required
        May be used for de-bugging if necessary
        """
        print(self.nodes)

    def print_edges(self):
        """
        No further implementation required
        May be used for de-bugging if necessary
        """
        print(self.edges)

    # Do not modify
    def write_edges_file(self, path="edges.csv") -> None:
        """
        write all edges out as .csv
        :param path: string
        :return: None
        """
        edges_path = path
        edges_file = open(edges_path, 'w')

        edges_file.write("source" + "," + "target" + "\n")

        for e in self.edges:
            edges_file.write(e[0] + "," + e[1] + "\n")

        edges_file.close()
        print("finished writing edges to csv")

    # Do not modify
    def write_nodes_file(self, path="nodes.csv") -> None:
        """
        write all nodes out as .csv
        :param path: string
        :return: None
        """
        nodes_path = path
        nodes_file = open(nodes_path, 'w')

        nodes_file.write("id, name, total_movies" + "\n")
        for n in self.nodes:
            nodes_file.write(n[0] + "," + n[1] + "," + n[2] + "\n")
        nodes_file.close()
        print("finished writing nodes to csv")




    def write_graph_to_json(self, path="graph.json") -> None:
        """
        Writes nodes and edges to a single JSON file with the specified structure.
        :param path: string - path to output JSON file
        :return: None
        """

        # Process nodes to match the required JSON format
        nodes_json = [{"id": n[0], "name": n[1], "movies": n[2]} for n in self.nodes]

        # Process edges to calculate weights and remove duplicate edges
        edge_weights = defaultdict(int)
        for source, target in self.edges:
            # Sort to handle both (source, target) and (target, source) as the same edge
            edge = tuple(sorted((source, target)))
            edge_weights[edge] += 1

        # Convert processed edges to the required JSON format
        links_json = [{"source": src, "target": tgt, "weight": weight}
                    for (src, tgt), weight in edge_weights.items()]

        # Combine nodes and links into a single JSON structure
        graph_json = {"nodes": nodes_json, "links": links_json}

        # Write the JSON data to file
        with open(path, 'w') as json_file:
            json.dump(graph_json, json_file, indent=4)
        
        print(f"Finished writing graph data to {path}")