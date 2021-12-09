from app import db, session, abort, firestore,os, config, make_response
from app.places.models.place_model import Places
from app.utils.helper_funcs import get_guide_filtered_places, get_node_nearby_places
import datetime


def create_new_place(data):
    pos = data[u'pos']
    features = data[u'features']
    address = data[u'address']
    contact = data[u'contact']
    open_hours = data[u'open_hours']
    category = data[u'category']
    title = data[u'title']
    images = data[u'images']
    services = data[u'services']
    public_opinion = data[u'public_opinion']
    meta = data[u'meta']
    description = data[u'description']
    parent_category_id = data[u'parent_category_id']
    sub_category_id = data[u'sub_category_id']

   
    if(pos != None and features != None and address != None and contact != None and open_hours != None and category != None and title != None and images != None and services != None and public_opinion != None and meta != None and description != None and parent_category_id != None and sub_category_id != None ):
        # try:
        data = Places( pos = pos, features = features, address = address, contact = contact, open_hours = open_hours, category = category, title = title, images = images, services = services, public_opinion = public_opinion, meta = meta, description = description, parent_category_id = parent_category_id, sub_category_id = sub_category_id )
        _data = data.to_dict()
        db.collection(u'Places').add({
            u'pos' : { 
                u'geohash': _data[u'pos'][u'geohash'],
                u'geopoint': firestore.GeoPoint(_data[u'pos'][u'geopoint'][u'latitude'], _data[u'pos'][u'geopoint'][u'longitude'])
                 },
            u'features' : _data[u'features'],
            u'address' : _data[u'address'],
            u'contact' : _data[u'contact'],
            u'open_hours' : _data[u'open_hours'],
            u'category' : _data[u'category'],
            u'title' : _data[u'title'],
            u'images' : _data[u'images'],
            u'services' : _data[u'services'],
            u'public_opinion' : _data[u'public_opinion'],
            u'meta' : _data[u'meta'],
            u'description' : _data[u'description'],
            u'parent_category_id' : _data[u'parent_category_id'],
            u'sub_category_id' : _data[u'sub_category_id'],
            u'created_at': datetime.datetime.now(),

        })
        # data.to_dict()
        print("=======> added to database")
        return data.to_dict()
        # except Exception as err:
        #     return {
        #         "error": err
        #     }


def read_place(data, method="all"):
    if(method == "all"):
        
        place = db.collection(data[u'option']).stream()
        for i in place:
            return(f'{i.id} : {i.to_dict()}')

    elif(method == 1):
        place = db.collection(data[u'option']).document(data["id"]).get()
        return place.to_dict()

def get_places_in_radius( data ):
    houses = get_node_nearby_places( data )
    return houses

def get_filtered_data (data):
    result = get_guide_filtered_places(data)
    return result


def update_place(data, method="rating"):

    if(method=="rating"):
        id = data["id"]
        print(id)
        new_update = {"rating":data["rating"]}
        print(new_update)
        rating = db.collection(u'Places').document(id).update(new_update)
        print(new_update)
        return "Updated"
     
            #  return {
            #      "error": err,
            #      "suggest":"make sure the incoming data has the correct expected fields"
            # } 



    