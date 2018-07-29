from geopy import distance, Point
from haystack.query import SearchQuerySet, SQ


class SearchAPIClass:

    def __init__(self, request):
        self.request = request
        self.query = request.query_params

    def get(self):

        search_query = self.query.get('text')
        search_result = SearchQuerySet().filter(
            SQ(title=search_query) | SQ(category=search_query))

        if self.query.get('type').lower() in 'autocomplete':
            result = self.get_search_autocomplete_output(
                search_query, search_result)
        else:
            result = self.get_search_page_output(search_query, search_result)

        return result

    @staticmethod
    def get_search_autocomplete_output(search_query, search_result):

        response = []

        for item in search_result:
            search_item = {}
            if search_query in item.title.lower():
                search_match_word = item.title
            else:
                search_match_word = search_query
            search_item['match'] = search_match_word
            search_item['category'] = item.category
            response.append(search_item)

        return response

    def get_search_page_output(self, search_query, search_result):
        response = []

        for item in search_result:
            search_item = item.objects.__dict__.pop('_state')
            search_item['distance'] = self.get_distance(
                item.objects.location.latitute, item.objects.location.latitute)
            response.append(search_item)

        response = sorted(response, key=lambda k: k.get('distance'))
        return response

    def get_distance(self, latitute, longitute):
        user_latitute = self.request.user.location.latitute
        user_longitute = self.request.user.location.longitute

        point_1_str = '{} {}'.format(user_latitute, user_longitute)
        point_2_str = '{} {}'.format(latitute, longitute)

        point_1 = Point(point_1_str)
        point_2 = Point(point_2_str)
        dist = distance.distance(point_1, point_2)

        return dist
