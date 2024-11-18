import http.client
import json
import csv
import os
from dotenv import load_dotenv


#############################################################################################################################
#
# All instructions, code comments, etc. contained within this notebook are part of the assignment instructions.
# Portions of this file will auto-graded in Gradescope using different sets of parameters / data to ensure that values are not
# hard-coded.
#
# Instructions:  Implement all methods in this file that have a return
# value of 'NotImplemented'. See the documentation within each method for specific details, including
# the expected return value
#
# Helper Functions:
# You are permitted to write additional helper functions/methods or use additional instance variables within
# the `Graph` class or `TMDbAPIUtils` class so long as the originally included methods work as required.
#
# Use:
# The `Graph` class  is used to represent and store the data for the TMDb co-actor network graph.  This class must
# also provide some basic analytics, i.e., number of nodes, edges, and nodes with the highest degree.
#
# The `TMDbAPIUtils` class is used to retrieve Actor/Movie data using themoviedb.org API.  We have provided a few necessary methods
# to test your code w/ the API, e.g.: get_move_detail(), get_movie_cast(), get_movie_credits_for_person().  You may add additional
# methods and instance variables as desired (see Helper Functions).
#
# The data that you retrieve from the TMDb API is used to build your graph using the Graph class.  After you build your graph using the
# TMDb API data, use the Graph class write_edges_file & write_nodes_file methods to produce the separate nodes and edges
# .csv files for use with the Argo-Lite graph visualization tool.
#
# While building the co-actor graph, you will be required to write code to expand the graph by iterating
# through a portion of the graph nodes and finding similar artists using the TMDb API. We will not grade this code directly
# but will grade the resulting graph data in your Argo-Lite graph snapshot.
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

    def add_node(self, id: str, name: str) -> None:
        """
        add a tuple (id, name) representing a node to self.nodes if it does not already exist
        The graph should not contain any duplicate nodes
        """
        node = (id, name)
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
        reverse_edge = (target, source)
        if edge not in self.edges and reverse_edge not in self.edges:
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

        nodes_file.write("id,name" + "\n")
        for n in self.nodes:
            nodes_file.write(n[0] + "," + n[1] + "\n")
        nodes_file.close()
        print("finished writing nodes to csv")


class TMDBAPIUtils:

    # Do not modify
    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_movie_cast(self, movie_id: str, limit: int = None, exclude_ids: list = None) -> list:
        """
        Get the movie cast for a given movie id, with optional parameters to exclude an cast member
        from being returned and/or to limit the number of returned cast members
        documentation url: https://developers.themoviedb.org/3/movies/get-movie-credits

        :param integer movie_id: a movie_id
        :param integer limit: number of returned cast members by their 'order' attribute
            e.g., limit=5 will attempt to return the 5 cast members having 'order' attribute values between 0-4
            If there are fewer cast members than the specified limit or the limit not specified, return all cast members
        :param list exclude_ids: a list of ints containing ids (not cast_ids) of cast members  that should be excluded from the returned result
            e.g., if exclude_ids are [353, 455] then exclude these from any result.
        :rtype: list
            return a list of dicts, one dict per cast member with the following structure:
                [{'id': '97909' # the id of the cast member
                'character': 'John Doe' # the name of the character played
                'credit_id': '52fe4249c3a36847f8012927' # id of the credit, ...}, ...]
                Note that this is an example of the structure of the list and some of the fields returned by the API. The result of the API call will include many more fields for each cast member.
        Important: the exclude_ids processing should occur prior to limiting output.
        """

        domain_name = 'api.themoviedb.org'
        request_uri = '/3/movie/' + movie_id + '/credits?api_key=' + self.api_key + '&language=en-US'

        # Use http client to invoke API
        conn = http.client.HTTPSConnection(domain_name, 443)
        conn.request('GET', request_uri)
        resp = conn.getresponse()
        decoded_resp = resp.read().decode('UTF-8')
        data = json.loads(decoded_resp)
        cast_list = data.get('cast')

        # limit results
        #if limit:
        #    cast_list = cast_list[:limit]

        if limit:
            cast_list = list(filter(lambda x: x['order'] < limit, cast_list))

        # exclude_ids
        if exclude_ids:
            cast_list = list(filter(lambda x: x.get('id') not in exclude_ids, cast_list))
        return cast_list

    def get_movie_credits_for_person(self, person_id: str, vote_avg_threshold: float = None) -> list:
        """
        Using the TMDb API, get the movie credits for a person serving in a cast role
        documentation url: https://developers.themoviedb.org/3/people/get-person-movie-credits

        :param string person_id: the id of a person
        :param vote_avg_threshold: optional parameter to return the movie credit if it is >=
            the specified threshold.
            e.g., if the vote_avg_threshold is 5.0, then only return credits with a vote_avg >= 5.0
        :rtype: list
            return a list of dicts, one dict per movie credit with the following structure:
                [{'id': '97909' # the id of the movie credit
                'title': 'Long, Stock and Two Smoking Barrels' # the title (not original title) of the credit
                'vote_avg': 5.0 # the float value of the vote average value for the credit}, ... ]
        """

        domain_name = 'api.themoviedb.org'
        request_uri = '/3/person/' + person_id + '/movie_credits?api_key=' + self.api_key + '&language=en-US'

        # Use http client to invoke API
        conn = http.client.HTTPSConnection(domain_name, 443)
        conn.request('GET', request_uri)
        resp = conn.getresponse()
        decoded_resp = resp.read().decode('UTF-8')
        data = json.loads(decoded_resp)

        # Some movie_credits may actually be collections and do not return cast data.
        # Handle this situation by skipping these instances.
        cast_list = []
        if 'cast' in data:
            cast_list = data['cast']

        if vote_avg_threshold and cast_list:
            cast_list = list(filter(lambda x: x['vote_average'] >= vote_avg_threshold, cast_list))

        mov_credits = [{'id': str(data['id']), 'title': data['title'], 'vote_avg': data['vote_average']} for data in
                       cast_list]
        return mov_credits

    """
    def __read_data(self, url):
        domain_name = 'api.themoviedb.org'
        api_url = 'https://api.themoviedb.org/3/movie/' + movie_id + '/credits/?api_key=' + self.api_key

        request_uri = '/3/movie/' + movie_id + '/credits?api_key=' + self.api_key

        ## Use http client to invoke API
        payload = {"api_key": self.api_key}
        conn = http.client.HTTPSConnection(domain_name, 443)
        conn.request('GET', request_uri)
        resp = conn.getresponse()
        decoded_resp = resp.read().decode('UTF-8')
        data = json.loads(decoded_resp)
    """





#############################################################################################################################
#
# BUILDING YOUR GRAPH
#
# Working with the API:  See use of http.request: https://docs.python.org/3/library/http.client.html#examples
#
# Using TMDb's API, build a co-actor network for the actor's/actress' highest rated movies
# In this graph, each node represents an actor
# An edge between any two nodes indicates that the two actors/actresses acted in a movie together
# i.e., they share a movie credit.
# e.g., An edge between Samuel L. Jackson and Robert Downey Jr. indicates that they have acted in one
# or more movies together.
#
# For this assignment, we are interested in a co-actor network of highly rated movies; specifically,
# we only want the top 3 co-actors in each movie credit of an actor having a vote average >= 8.0.
#
# You will need to add extra functions or code to accomplish this.  We will not directly call or explicitly grade your
# algorithm. We will instead measure the correctness of your output by evaluating the data in your argo-lite graph
# snapshot.
#
# Build your co-actor graph on the actress 'Meryl Streep' w/ person_id 5064.
# Initialize a Graph object with a single node representing Meryl Streep
# Find all of Meryl Streep's movie credits that have a vote average >= 8.0
#
# 1. For each movie credit:
#   get the movie cast members having an 'order' value between 0-2 (these are the co-actors)
#   for each movie cast member:
#       using graph.add_node(), add the movie cast member as a node (keep track of all new nodes added to the graph)
#       using graph.add_edge(), add an edge between the Meryl Streep (actress) node
#       and each new node (co-actor/co-actress)
#
#
# Using the nodes added in the first iteration (this excludes the original node of Meryl Streep!)
#
# 2. For each node (actor / actress) added in the previous iteration:
#   get the movie credits for the actor that have a vote average >= 8.0
#   for each movie credit:
#       try to get the 3 movie cast members having an 'order' value between 0-2
#       for each movie cast member:
#           if the node doesn't already exist:
#               add the node to the graph (track all new nodes added to the graph)
#               if the edge does not exist:
#                   add an edge between the node (actor) and the new node (co-actor/co-actress)
#
#
# - Repeat the steps from # 2. until you have iterated 3 times to build an appropriately sized graph.
# - Your graph should not have any duplicate edges or nodes
# - Write out your finished graph as a nodes file and an edges file using
#   graph.write_edges_file()
#   graph.write_nodes_file()
#
# Exception handling and best practices
# - You should use the param 'language=en-US' in all API calls to avoid encoding issues when writing data to file.
# - If the actor name has a comma char ',' it should be removed to prevent extra columns from being inserted into the .csv file
# - Some movie_credits may actually be collections and do not return cast data. Handle this situation by skipping these instances.
# - While The TMDb API does not have a rate-limiting scheme in place, consider that making hundreds / thousands of calls
#   can occasionally result in timeout errors. It may be necessary to insert periodic sleeps when you are building your graph.


def return_name() -> str:
    """
    Return a string containing your GT Username
    e.g., gburdell3
    Do not return your 9 digit GTId
    """
    return 'asadshafqat8'


def return_argo_lite_snapshot() -> str:
    """
    Return the shared URL of your published graph in Argo-Lite
    """
    return 'https://poloclub.github.io/argo-graph-lite/#adabc728-dd66-4b4f-b0d0-5396b6b80c78'




if __name__ == "__main__":
    graph = Graph()


    # tmdb_api_utils = TMDBAPIUtils(api_key='99999999999999999999999')

    # print("On a good day!!!")
    # graph.add_node(id='5065', name='Bradley')
    # graph.add_edge('5064', '5065')
    # print(graph.max_degree_nodes())

    tmdb_api_utils = TMDBAPIUtils(api_key='cd9295864be300cdb3ff2241f572d103')

    parent_id = []
    iteration_actor_ids = ['5064']
    graph.add_node(id='5064', name='Meryl Streep')
    for x in range(0, 3):
        print("Iteration " + str(x))
        print("Iteration Node Size: " + str(len(iteration_actor_ids)))

        new_actor_ids = []
        for actor_id in iteration_actor_ids:
            movie_credits = tmdb_api_utils.get_movie_credits_for_person(actor_id, 8.0)
            # print(movie_credits)
            print("Movie Credits")
            print(len(movie_credits))

            cast_members = [cast for movie_credit in movie_credits for cast in tmdb_api_utils.get_movie_cast(movie_credit['id'], 3, [int(actor_id)])]
            print("Cast Members")
            print(len(cast_members))
            for cast in cast_members:
                node = (str(cast['id']), cast['name'].replace(',', ''))
                if node not in graph.nodes:
                    new_actor_ids.append(str(cast['id']))
                    graph.add_node(str(cast['id']), cast['name'].replace(',', ''))
                graph.add_edge(actor_id, str(cast['id']))
        iteration_actor_ids = new_actor_ids
    print("Graph Size")
    print(len(graph.nodes))

    # call functions or place code here to build graph (graph building code not graded)

    graph.write_edges_file()
    graph.write_nodes_file()