from app import db
from app.tours.models.models import Tour


def create_new_tour(data):
    logo = data[u'logo']
    number_of_stops = data[u'number_of_stops']
    miles_in_mins = data[u'miles_in_mins']
    welcome_message = data[u'welcome_message']
    status = data[u'status']
   
    if(logo != None and number_of_stops != None and miles_in_mins != None and welcome_message != None and status != None ):
        # try:
       
        data = Tour( logo = logo, number_of_stops = number_of_stops, miles_in_mins = miles_in_mins, welcome_message = welcome_message, status = status)
        print("hello======>",data.to_dict())       
        db.collection(u'Tours').add(data.to_dict())
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



    