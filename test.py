import http.client
import json
import csv
from dotenv import load_dotenv
import os
from main import Graph
from main import TMDBAPIUtils


if __name__ == "__main__":

    #Create an instance of the Graph class
    graph = Graph()

    # Load environment variables from the .env file in the root directory
    load_dotenv()

    # Access the API key
    api_key = os.getenv("API_KEY")

    # Create an instance of the TMDBAPIUtils class using the api key
    tmdb_api = TMDBAPIUtils(api_key = api_key)

    iteration_actors = ['5064']

    # Add the Meryl Streep node in the graph
    graph.add_node(('5064', 'Meryl Streep'))

    for x in range(0,3):

        new_actors = []

        for actor in iteration_actors:
            movie_credits = tmdb_api.get_movie_credits_for_person(actor, vote_avg_threshold= 8.0)

            co_actors = []
            for movie_credit in movie_credits:
                co_actors.append(tmdb_api.get_movie_cast(movie_credit['id'], 3, [actor]))
            for co_actor in co_actors:
                node = str(co_actor['id'], co_actor['name'].replace(",", ""))
                if node not in graph.nodes:
                    new_actors.append(co_actor['id'])
                    graph.add_node((str(co_actor['id'], co_actor['name'].replace(",", " "))))
                graph.add_edge((co_actor['id']), actor)
        iteration_actors = new_actors
    
    graph.write_nodes_file("nodes.csv")
    graph.write_edges_file("edges.csv")








