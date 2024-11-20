import http.client
import json

#############################################################################################################################

# The `TMDbAPIUtils` class is used to retrieve Actor/Movie data using themoviedb.org API.  We have provided a few necessary methods
# to test your code w/ the API, e.g.: get_move_detail(), get_movie_cast(), get_movie_credits_for_person(). Additional
# methods and instance variables as desired.

###############################################################################################################################

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
        
        cast_final_list = []
        for x in cast_list:
            if 'vote_average' in x.keys():
                cast_final_list.append(x)

        if vote_avg_threshold and cast_final_list:
            cast_final_list = list(filter(lambda x: x['vote_average'] >= vote_avg_threshold, cast_final_list))

        mov_credits = [{'id': str(data['id']), 'title': data['title'], 'vote_avg': data['vote_average']} for data in
                       cast_final_list]
        return mov_credits