from flask.helpers import make_response
from app import app, auth, session, request, url_for, redirect, Resource, api, reqparse
from app.tours.controllers.controllers import create_new_tour, read_tour, update_tour

class Tour(Resource):
    def post(self):

         self.args = request.json
         tour = create_new_tour(self.args)
         return tour

    def get(self):
        self.args = request.json
        print(self.args)
        tour = read_tour(self.args)
        return tour
    
    def put(self):
        self.args = request.json
        update_data = update_tour(self.args)
        return update_data

api.add_resource(Tour, '/api/user/tours', endpoint="Tours")