# -*- coding: utf-8 -*-
import googlemaps, json

from flask.views import View
from models import UserModel


class UserUploadGps(View):

    def dispatch_request(self, user_id, gps):
        # Replace the API key below with a valid API key.
        #return "dafsdfsd"
        try:
            gmaps = googlemaps.Client(key='AIzaSyCNcSw3hYO2wes__ZHHp_emc7v8vsHkaM0')

            # Geocoding and address
            #"geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
            # Look up an address with reverse geocoding
            reverse_geocode_result = gmaps.reverse_geocode(gps)

            types = ["food", "gym", "cafe", "book_store", "health", "shopping_mall", "library", "park", "university"]

            places = gmaps.nearest(gps, types=types)

            res = {}
            if places and len(places["results"]) > 0:
                for t in places["results"][0]["types"]:
                    if t in types:
                        res["location_type"] = t

            user = UserModel.get_by_id(int(user_id))
            user.where = reverse_geocode_result[0]["formatted_address"]
            user.gps = gps + ": " + res["location_type"]
            user.put()
        except Exception as e:
            return json.dumps(places["results"])


        return json.dumps(res)
