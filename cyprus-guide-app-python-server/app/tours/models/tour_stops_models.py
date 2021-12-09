

class TourStop:
    def __init__(self, images={}, description = {}, address = {}, id = {}):
        self.images = images
        self.description = description
        self.address = address
        self.id = id

    @staticmethod
    def from_dict( source ):
        if source == None:
            return

        place = TourStop() 

        if u'images' in source:
            place.images = source[u'images']

        if u'description' in source:
            place.description = source[u'description']

        if u'address' in source:
            place.address = source[u'address']

        if u'id' in source:
            place.id = source[u'id']
    
        return place


    
    def to_dict(self):
        return {
            u'images' : self.images,
            u'description' : self.description,
            u'address' : self.address,
            u'id' : self.id
             }

    def __repr__(self):
        return ('Tour(\
            images = {self.images},\
            description = {self.description},\
            address = {self.address},\
            id = {self.id},\
             )')



