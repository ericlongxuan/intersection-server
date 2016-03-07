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

            types = {"food":1, "gym":2, "cafe":3, "book_store":4, "health":5, "shopping_mall":6, "library":7, "park":8, "university":9}

            places = gmaps.nearest(gps, types=types.keys())

            res = {}
            location_type_index = 0 #unknown
            res["location_type"] = "unknown"  #unknown
            if places and len(places["results"]) > 0:
                for t in places["results"][0]["types"]:
                    if t in types.keys():
                        res["location_type"] = t
                        location_type_index = types[t]

            user = UserModel.get_by_id(int(user_id))
            user.where = reverse_geocode_result[0]["formatted_address"]
            user.gps = gps + ": " + res["location_type"]

            if user.locations is None:
                user.locations = str(location_type_index)
            elif len(user.locations) < 12 * 24:
                user.locations += str(location_type_index)
            else:
                user.locations = user.locations[1:] + str(location_type_index)
            user.put()
        except Exception as e:
            return json.dumps(places["results"]) + e.message

        res["locations"] = user.locations
        return json.dumps(res)
