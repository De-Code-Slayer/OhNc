from datetime import datetime
# from app import dba
# from flask_login import UserMixin

class House:
    def __init__(self, status="available", price={}, living_space=[], pos={}, features={}, address={}, contact={}, open_hours=[], category=[], title={}, images=[], services=[], public_opinion={}, meta={}, description={}, parent_category_id=[], sub_category_id=[] ):
        self.pos = pos
        self.features = features
        self.address = address
        self.contact = contact
        self.open_hours = open_hours
        self.category = category
        self.title = title
        self.price = price
        self.living_space = living_space
        self.images = images
        self.services = services
        self.public_opinion = public_opinion
        self.meta = meta
        self.status = status
        self.description = description
        self.parent_category_id = parent_category_id
        self.sub_category_id = sub_category_id

    @staticmethod
    def from_dict(source):

        if source is None:
            return {}

        house = House()

        if u'pos' in source:
            house.pos = source=[u'pos']

        if u'pos' in source:
            house.pos = source[u'pos']

        if u'features' in source:
            house.features = source[u'features']

        if u'address' in source:
            house.address = source[u'address']

        if u'contact' in source:
            house.contact = source[u'contact']

        if u'open_hours' in source:
            house.open_hours = source[u'open_hours']

        if u'status' in source:
            house.status = source[u'status']

        if u'living_space' in source:
            house.living_space = source[u'living_space']

        if u'category' in source:
            house.category = source[u'category']

        if u'title' in source:
            house.title = source[u'title']

        if u'images' in source:
            house.images = source[u'images']

        if u'services' in source:
            house.services = source[u'services']

        if u'public_opinion' in source:
            house.public_opinion = source[u'public_opinion']

        if u'meta' in source:
            house.meta = source[u'meta']

        if u'description' in source:
            house.description = source[u'description']

        if u'price' in source:
            house.price = source[u'price']

        if u'parent_category_id' in source:
            house.parent_category_id = source[u'parent_category_id']

        if u'sub_category_id' in source:
            house.sub_category_id = source[u'sub_category_id']


        return house
    

    def to_dict(self):
        house = {
            u'pos': self.pos,
            u'features': self.features,
            u'address': self.address,
            u'contact': self.contact,
            u'open_hours': self.open_hours,
            u'category': self.category,
            u'title': self.title,
            u'images': self.images,
            u'status': self.status,
            u'services': self.services,
            u'public_opinion': self.public_opinion,
            u'meta': self.meta,
            u'living_space': self.living_space,
            u'price': self.price,
            u'description': self.description,
            u'parent_category_id': self.parent_category_id,
            u'sub_category_id': self.sub_category_id
        }

        
        

        return house

    def __repr__(self):
        return (
            f'City(\
                display_name = {self.display_name}, \
                pos = {self.pos}, \
                features = {self.features}, \
                address = {self.address}, \
                contact = {self.contact}, \
                open_hours = {self.open_hours}, \
                category = {self.category}, \
                title = {self.title}, \
                price = {self.price}, \
                status = {self.status}, \
                living_space = {self.living_space}, \
                images = {self.images}, \
                services = {self.services}, \
                public_opinion = {self.public_opinion}, \
                meta = {self.meta}, \
                description = {self.description}, \
                parent_category_id = {self.parent_category_id}, \
                sub_category_id = {self.sub_category_id}, \
            )'
        )

