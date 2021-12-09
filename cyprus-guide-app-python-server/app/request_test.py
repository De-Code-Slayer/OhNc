import requests as re
import json
url = "http://127.0.0.1:5000/"
route = "api/auth/email_signup"


data={"email":"example@mail.com", "password":"examplepassword", "display_name":"John Doe", "photo_url":"url of a photo"}
act = re.post(url+route, json=json.dumps(data) )
print(act)
print(type(data))


        # pos: {
        #     geohash: pos.position.geohash,
        #     geopoint: new firebase.firestore.GeoPoint(pos.position.geopoint._latitude, pos.position.geopoint._longitude )
        #     },
        # features: data.features,
        # address: data.address,
        # contact: data.contact,
        # open_hours: data.open_hours,
        # category: data.category,
        # title: data.title,
        # images: data.images,
        # services : data.services,
        # public_opinion : data.public_opinion,
        # meta : data.meta,
        # description : data.description,
        # parent_category_id: data.parent_category_id,
        # sub_category_id: data.sub_category_id