# Coactor Network Graph Visualization
Vast amount of digital data is generated every day, but raw data is often not immediately usable. We are usually more interested in the information content of the data, what pattens are captured?

This repository showcases a project aimed at collecting, preprocessing, and visualizing data using an API from The Movie Database (TMDB) and constructing a graph representation of the data which shows how prolific each actor is and which actors have acted together. The undirected network graph visualization highlights connections between nodes (actors) using D3.js, providing an engaging way to explore relationships and data patterns.



## Motivation
The project serves as a demonstration of:

Data collection and preprocessing skills.
Proficiency in data visualization using modern web technologies.
Effective communication of insights through interactive and dynamic visualizations.
By combining Python for backend processing and D3.js for visualization, this project offers a seamless blend of analytics and presentation.


## Technologies Used
**Backend:**
Python: For data collection, cleaning, and transformation.

**Frontend:**
HTML5 and JavaScript: To structure and power the visualization.
D3.js: A powerful JavaScript library for creating scalable and interactive visualizations.
Canvas API: For efficient rendering of the graph.

## Features
Interactive network graph visualization:
Nodes represent actors, with size scaled by number of highly rated movies to therir credit
Links represent two actors co-starring in a movie, with dynamic scaling for the weigh of the link which represents the number of times the two actors have starred together.

Node interaction:
Hover to display detailed information.
Click to select and highlight nodes.
Drag-and-drop functionality for repositioning nodes.
Optimized rendering using the Canvas API, suitable for large datasets.

## Methodology
**1. Data Collection and Preprocessing**
The TTMDBAPIUtils class is implemented to fetch all the data from the API
Version 3 of the API is used.
To use the API:
- Create a TMDB Account and follow the instructions to obtain an authentication token
- Refer to the [TMDB API DOCUMENTATION](https://developer.themoviedb.org/reference/intro/getting-started) which contains helpful 'try it out' features to get acquainted with the API

The two methods in the class namely:
```python
# Method for getting all the cast members for a movie credit using movie credit_id
    def get_movie_cast(self, movie_id: str, limit: int = None, exclude_ids: list = None) -> list:

# Method for getting all the movies for a specific actor using the actor_id
    def get_movie_credits_for_person(self, person_id: str, vote_avg_threshold: float = None) -> list:
```
Details of these methods are given are included in docstrings within the class



