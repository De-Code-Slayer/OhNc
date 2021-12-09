from app import request, Resource, api
from app.tours.controllers.tour_stops_controller import create_new_tour_stop, read_tour_stop, update_tour_stop

class TourStops(Resource):
    def post(self):

         self.args = request.json
         tour = create_new_tour_stop(self.args)
         return tour

    def get(self):
        self.args = request.json
        print(self.args)
        tour = read_tour_stop(self.args)
        return tour
    
    def put(self):
        self.args = request.json
        update_data = update_tour_stop(self.args)
        return update_data

api.add_resource(TourStops, '/api/user/tourstop', endpoint="Tourstop")