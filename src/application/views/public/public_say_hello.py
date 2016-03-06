# -*- coding: utf-8 -*-
import googlemaps, json

from flask.views import View


class PublicSayHello(View):

    def dispatch_request(self, username, gps):
        # Replace the API key below with a valid API key.
        gmaps = googlemaps.Client(key='AIzaSyCNcSw3hYO2wes__ZHHp_emc7v8vsHkaM0')

        # Geocoding and address
        #"geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

        # Look up an address with reverse geocoding
        reverse_geocode_result = gmaps.reverse_geocode(gps)

        return json.dumps(reverse_geocode_result)
        #return "Hello {}".format(username)
