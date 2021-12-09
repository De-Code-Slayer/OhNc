from flask.helpers import make_response
from app import app, auth, session, request, url_for, redirect, Resource, api, reqparse
from app.houses.controllers.houses_controllers import create_new_house, get_filtered_data, get_house_in_radius, read_house, update_house

class houses(Resource):
    def post(self):
         self.args = request.json
         house = create_new_house(self.args)
         return house

    def get(self):
        self.args = request.json
        place = get_house_in_radius(self.args)
        return place
        
    def put(self):
        self.args = request.json
        update_data = update_house(self.args)
        return update_data


class FetchHouses (Resource):
    def __init__(self):
        self.args = request.json

    def post(self):
        # print(self.args)
        place = get_house_in_radius(self.args)
        return place

class GetHouses(Resource):
    def post(self):
        self.args = request.json
        print(self.args)
        place = get_house_in_radius(self.args)
        print(place)
        return place

class GetFilteredHouses(Resource):
    def post(self):
        self.args = request.json
        # print(self.args)
        place = get_filtered_data(self.args)
        return place






api.add_resource(houses, '/api/user/houses', endpoint="houses")
api.add_resource(GetHouses, '/api/user/get_houses', endpoint="GetHouses")
api.add_resource(GetFilteredHouses, '/api/user/get_filtered_houses', endpoint="GetFilteredHouses")