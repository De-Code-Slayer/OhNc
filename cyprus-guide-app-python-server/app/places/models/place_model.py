from app import firestore

class Places:
    def __init__(self, pos={}, features = {}, address = {}, contact = {}, open_hours = [], category = [], title = {}, images = [], services = [], public_opinion = {}, meta = {}, description = {}, parent_category_id = {}, sub_category_id = {}):
        self.pos = pos
        self.features = features
        self.address = address
        self.contact = contact
        self.open_hours = open_hours
        self.category = category
        self.title = title
        self.images = images
        self.services = services
        self.public_opinion = public_opinion
        self.meta = meta
        self.description = description
        self.parent_category_id = parent_category_id
        self.sub_category_id = sub_category_id

    @staticmethod
    def from_dict( source ):
        if source == None:
            return

        place = Places() 

        if u'pos' in source:
            place.pos = source[u'pos']

        if u'features' in source:
            place.features = source[u'features']

        if u'address' in source:
            place.address = source[u'address']

        if u'contact' in source:
            place.contact = source[u'contact']

        if u'open_hours' in source:
            place.open_hours = source[u'open_hours']

        if u'category' in source:
            place.category = source[u'category']

        if u'title' in source:
            place.title = source[u'title']

        if u'images' in source:
            place.images = source[u'images']

        if u'services' in source:
            place.services = source[u'services']

        if u'public_opinion' in source:
            place.public_opinion = source[u'public_opinion']

        if u'meta' in source:
            place.meta = source[u'meta']

        if u'description' in source:
            place.description = source[u'description']

        if u'parent_category_id' in source:
            place.parent_category_id = source[u'parent_category_id']

        if u'sub_category_id' in source:
            place.sub_category_id = source[u'sub_category_id']
        
        return place


    
    def to_dict(self):
        return {
            u'pos' : self.pos,
            u'features' : self.features,
            u'address' : self.address,
            u'contact' : self.contact,
            u'open_hours' : self.open_hours,
            u'category' : self.category,
            u'title' : self.title,
            u'images' : self.images,
            u'services' : self.services,
            u'public_opinion' : self.public_opinion,
            u'meta' : self.meta,
            u'description' : self.description,
            u'parent_category_id' : self.parent_category_id,
            u'sub_category_id' : self.sub_category_id,
        }

    def __repr__(self):
        return ('Places(\
            pos = {self.pos},\
            features = {self.features},\
            address = {self.address},\
            contact = {self.contact},\
            open_hours = {self.open_hours},\
            category = {self.category},\
            title = {self.title},\
            images = {self.images},\
            services = {self.services},\
            public_opinion = {self.public_opinion},\
            meta = {self.meta},\
            description = {self.description},\
            parent_category_id = {self.parent_category_id},\
            sub_category_id = {self.sub_category_id},\
        )')



