import http.client
import json
import csv
import os
from dotenv import load_dotenv
from collections import defaultdict
from graph import Graph
from tmdb_api import TMDBAPIUtils



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
# We are interested in a co-actor network of highly rated movies; specifically,
# we only want the top 3 co-actors in each movie credit of an actor having a vote average >= 8.0.
#
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

#
# Exception handling and best practices
# - You should use the param 'language=en-US' in all API calls to avoid encoding issues when writing data to file.
# - If the actor name has a comma char ',' it should be removed to prevent extra columns from being inserted into the .csv file
# - Some movie_credits may actually be collections and do not return cast data. Handle this situation by skipping these instances.
# - While The TMDb API does not have a rate-limiting scheme in place, consider that making hundreds / thousands of calls
#   can occasionally result in timeout errors. It may be necessary to insert periodic sleeps when you are building your graph.

if __name__ == "__main__":
    #Create an instance of the Graph class
    graph = Graph()

    # Load environment variables from the .env file in the root directory
    load_dotenv()

    # Access the API key
    api_key = os.getenv("API_KEY")

    # Create an instance of the TMDBAPIUtils class using the api key
    tmdb_api_utils = TMDBAPIUtils(api_key = api_key)

    iteration_actor_ids = ['5064']

    # Get the total movie_credits for Meryl Streep to initialize the node
    movie_credits = tmdb_api_utils.get_movie_credits_for_person("5064", 8.0)
    graph.add_node(id = '5064', name = 'Meryl Streep', total_movies = str(len(movie_credits)))
    for x in range(0, 2):
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
                cast_total_movies = str(len(tmdb_api_utils.get_movie_credits_for_person(str(cast['id']), 8.0)))
                node = (str(cast['id']), cast['name'].replace(',', ''), cast_total_movies)
                if node not in graph.nodes:
                    new_actor_ids.append(str(cast['id']))
                    graph.add_node(str(cast['id']), cast['name'].replace(',', ''), cast_total_movies)
                graph.add_edge(actor_id, str(cast['id']))
        iteration_actor_ids = new_actor_ids
    print("Graph Size")
    print(len(graph.nodes))

    # call functions or place code here to build graph (graph building code not graded)

    graph.write_edges_file()
    graph.write_nodes_file()
    graph.write_graph_to_json()
