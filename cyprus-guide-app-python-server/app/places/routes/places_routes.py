from flask.helpers import make_response
from app import app, auth, session, request, url_for, redirect, Resource, api, reqparse
from app.houses.controllers.houses_controllers import get_filtered_data
from app.places.controllers.places_controller import create_new_place, get_places_in_radius, read_place, update_place

class places(Resource):
    def post(self):

         self.args = request.json
         place = create_new_place(self.args)
         return place

    def get(self):
        self.args = request.json
        print(self.args)
        if self.args == "None":

           place = read_place(self.args, method="all")
           return place
        else:
            place = read_place(self.args)
            return place
    
    def put(self):
        self.args = request.json
        update_data = update_place(self.args)
        return update_data

class ReadSinglePlace(Resource):
    def __init__(self):
        self.data = request.json 

    def post(self):
        item = read_place(self.data, method=1)
        return item


class GetPlaces(Resource):
    def post(self):
        self.args = request.json
        print(self.args)
        place = get_places_in_radius(self.args)
        return place

class GetFilteredPlaces(Resource):
    def post(self):
        self.args = request.json
        print(self.args)
        place = get_filtered_data(self.args)
        return place





api.add_resource(ReadSinglePlace, '/api/user/place', endpoint="ReadSinglePlace")
api.add_resource(places, '/api/user/places', endpoint="places")
api.add_resource(GetPlaces, '/api/user/get_places', endpoint="GetPlaces")
api.add_resource(GetFilteredPlaces, '/api/user/get_filtered_places', endpoint="GetFilteredPlaces")