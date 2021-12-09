from app import firestore

class Tour:
    def __init__(self, logo={}, number_of_stops = {}, miles_in_mins = {}, welcome_message = {}, status = {}):
        self.logo = logo
        self.number_of_stops = number_of_stops
        self.miles_in_mins = miles_in_mins
        self.welcome_message = welcome_message
        self.status = status

    @staticmethod
    def from_dict( source ):
        if source == None:
            return

        place = Tour() 

        if u'logo' in source:
            place.logo = source[u'logo']

        if u'number_of_stops' in source:
            place.number_of_stops = source[u'number_of_stops']

        if u'miles_in_mins' in source:
            place.miles_in_mins = source[u'miles_in_mins']

        if u'welcome_message' in source:
            place.welcome_message = source[u'welcome_message']

        if u'status' in source:
            place.status = source[u'status']
    
        return place


    
    def to_dict(self):
        return {
            u'logo' : self.logo,
            u'number_of_stops' : self.number_of_stops,
            u'miles_in_mins' : self.miles_in_mins,
            u'welcome_message' : self.welcome_message,
            u'status' : self.status
             }

    def __repr__(self):
        return ('Tour(\
            logo = {self.logo},\
            number_of_stops = {self.number_of_stops},\
            miles_in_mins = {self.miles_in_mins},\
            welcome_message = {self.welcome_message},\
            status = {self.status},\
             )')



