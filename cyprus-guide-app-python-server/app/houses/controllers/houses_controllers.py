from app import db, session, abort, firestore,os, config, make_response
from app.houses.models.house_model import House
from app.utils.helper_funcs import get_guide_filtered_places, get_guide_nearby_places
import datetime


def create_new_house(data):
    # print(data)

    try:
        pos = data[u'pos']
        price = data[u'price']
        features = data[u'features']
        address = data[u'address']
        contact = data[u'contact']
        services = data[u'services']
        living_space = data[u'living_space']
        title = data[u'title']
        images = data[u'images']
        public_opinion = data[u'public_opinion']
        meta = data[u'meta']
        description = data[u'description']
        parent_category_id = data[u'parent_category_id']
        sub_category_id = data[u'sub_category_id']
    
        if(pos != None, features != None, address != None, contact != None, title != None, images != None, services != None, public_opinion != None, meta != None, description != None, parent_category_id != None, sub_category_id != None ):
            # try:
            data = House( price=price, living_space=living_space, pos=pos, features=features, address=address, contact=contact, title=title, images=images, services=services, public_opinion=public_opinion, meta=meta, description=description, parent_category_id=parent_category_id, sub_category_id=sub_category_id )
            _data = data.to_dict()
            db.collection(u'Apartments').add({
                u'pos' : { 
                    u'geohash': _data[u'pos'][u'geohash'],
                    u'geopoint': firestore.GeoPoint(_data[u'pos'][u'geopoint'][u'latitude'], _data[u'pos'][u'geopoint'][u'longitude'])
                    },
                u'features': _data[u'features'],
                u'address': _data[u'address'],
                u'contact': _data[u'contact'],
                u'title': _data[u'title'],
                u'price': _data[u'price'],
                u'images': _data[u'images'],
                u'services': _data[u'services'],
                u'public_opinion': _data[u'public_opinion'],
                u'meta': _data[u'meta'],
                u'living_space': _data[u'living_space'],
                u'description': _data[u'description'],
                u'parent_category_id': _data[u'parent_category_id'],
                u'sub_category_id': _data[u'sub_category_id'],
                u'created_at': datetime.datetime.now(),
                u'status': _data[u'status']
            })
            print("=======> added to database")
            return data.to_dict()
    except Exception as e:
        return {
            "error": e,
            "suggestion":"make sure the incoming data has the correct expected fields"
        } 
       


def read_house(data, method="all"):
    try:
        if(method == "all"):
            
            house = db.collection(u'Apartments').stream()
            for i in house:
                return(f'{i.id} : {i.to_dict()}')

        elif(method == 1):
            house = db.collection(u'Apartments').document(data["id"]).get()
            print(data)
            return house.to_dict()
    except Exception as e:
        return {
            "error": e,
            "suggest":"make sure the incoming data has the correct expected fields"
        } 

def get_house_in_radius( data ):
    houses = get_guide_nearby_places( data )
    return houses

def get_filtered_data (data):
    result = get_guide_filtered_places(data)
    return result



def update_house(data, method="rating"):
    try:
        if(method=="rating"):
            id = data["id"]
            print(f'Rating Before : {data["count"]}')

            new_update_star = data["rating"]
            apartment_rating = data["count"][data["value"]]
            update_rating = int(apartment_rating) + int(1)

            data["count"][data["value"]] = update_rating
            data["score"] = "calc_rating"(data["count"])


            new_update = {"rating": {
               " count": data["count"],
               " score": data["score"]
            }}

            print(f'Rating Before : {data["count"]}')

            db.collection(u'Apartments').document(id).update(new_update)
            return "Updated"

        if(method == "status"):
   
            id = data["id"]
            status = {"status":data["status"]}
            db.collection(u'Apartments').document(id).update(status)

    except Exception as e:
        return {
            "error": e,
            "suggest":"make sure the incoming data has the correct expected fields"
        } 
