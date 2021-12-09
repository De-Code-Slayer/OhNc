from app import db
from app.tours.models.tour_stops_models import TourStop


def create_new_tour(data):
    images = data[u'images']
    description = data[u'description']
    address = data[u'address']
    id = data[u'id']
   
    if(images != None and description != None and address != None and id != None  ):
        # try:
       
        data = TourStop( images = images, description = description, address = address, id = id)  
        db.collection(u'TourStops').add(data.to_dict())
        # data.to_dict()
        print("=======> added to database")
        return data.to_dict()



def read_tour(data):
    
        tour = db.collection(data[u'option']).document(data["id"]).get()
        return tour.to_dict()




def update_tour(data):

   
        id = data["id"]
        print(id)
        new_update = data
        # print(new_update)
        tour = db.collection(u'Tour').document(id).update(new_update)
        # print(new_update)
        return tour.to_dict
     
            #  return {
            #      "error": err,
            #      "suggest":"make sure the incoming data has the correct expected fields"
            # } 



    