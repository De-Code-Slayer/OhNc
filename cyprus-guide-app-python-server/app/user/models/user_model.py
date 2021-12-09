from datetime import datetime
# from app import dba
# from flask_login import UserMixin

class User:
    def __init__(self, email, phone_number, display_name, photo_url, email_verified=False, disabled=False ):
        self.display_name = display_name
        self.email = email
        self.email_verified = email_verified
        self.phone_number = phone_number
        self.photo_url = photo_url
        self.disabled = disabled
        self.created_at = datetime.now().isoformat(timespec='minutes')
        self.tags = []
        self.attributes = {}


    @staticmethod
    def from_dict(source):

        if source is None:
            return {}

        user = User(source[u'email'], source[u'phone_number'], source[u'display_name'], source[u'photo_url'])

        if u'email_verified' in source:
            user.phone_number = source[u'email_verified']

        if u'disabled' in source:
            user.disabled = source[u'disabled']

        if u'tags' in source:
            user.tags = source[u'tags']
        
        if u'attributes' in source:
            user.attributes = source[u'attributes']

        return user
    

    def to_dict(self):
        user = {
            u'email': self.email,
            u'phone_number': self.phone_number,
            u'display_name': self.display_name,
            u'photo_url': self.photo_url,
            u'email_verified': self.email_verified,
            u'disabled' : self.disabled,
            u'created_at': self.created_at,
            u'tags': self.tags,
            u'attributes': self.attributes
        }

        
        

        return user

    def __repr__(self):
        return (
            f'City(\
                display_name = {self.display_name}, \
                email = {self.email}, \
                email_verified = {self.email_verified}, \
                phone_number = {self.phone_number}, \
                photo_url = {self.photo_url}, \
                disabled = {self.disabled}, \
                created_at = {self.created_at}, \
                tags = {self.tags}, \
                attributes = {self.attributes} \
            )'
        )

class Tags:
    def __init__(self,tag):
        self.tag = tag

    @staticmethod
    def to_list(self):

        tag_list = []
        if type(self.tag is str):
            tags = tag_list.append(self.tag)
        if type( self.tag is list ):
            tags = self.tag

        return tags

    def from_list(source):

        if source is None:
            return []
        
        tags = Tags(tag=source)

        return tags

    def __repr__(self):
        return (
            f'Tags(\
                tag={self.tag}) \
                )'
            )
#___________________________________________________________________________________


class Places:
    def __init__(self, title={}, description={}, cordinates={}, image_url={}, services={}, contact={}, meta={}, rating={} ):
        self.title = title
        self.description = description
        self.services = services
        self.cordinates = cordinates
        self.image_url = image_url
        self.contact = contact
        self.meta = meta
        self.rating = rating
        


    @staticmethod
    def from_dict(source):

        if source is None:
            return {}

        place = Places()

        if u'title' in source:
            place.title = source[u'title']

        if u'description' in source:
            place.description = source[u'description']

        if u'image_url' in source:
            place.image_url = source[u'image_url']
        
        if u'cordinate' in source:
            place.cordinates = source[u'cordinates']

        if u'services' in source:
            place.services = source[u'services']

        if u'meta' in source:
            place.meta = source[u'meta']

        if u'rating' in source:
            place.rating = source[u'rating']

        return place
    
    def to_dict(self):
        place = {
            u'title': self.title,
            u'description': self.description,
            u'cordinates': self.cordinates,
            u'image_url': self.image_url,
            u'services': self.services,
            u'rating' : self.rating,
            u'meta': self.meta,
        }

        return place

    def __repr__(self):
        return (
            f'Places(\
                title = {self.title}, \
                description = {self.description}, \
                cordinates = {self.cordinates}, \
                image_url = {self.image_url}, \
                services = {self.services}, \
                rating = {self.rating}, \
                meta = {self.meta}, \
            )'
        )

