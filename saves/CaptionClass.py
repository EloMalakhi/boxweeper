class Caption(object):
    def __init__(self):
        self.confirmation = None  # a string that contains whether the user completed the game or not
        self.hoveroverelement = {} # a set of keys going from 1 to total x units * total y units * total z units translating to tags used in the flask script for each button hover over event
        self.hoverovertext = {} # a set of keys going from 1 to total x units * total y units * total z units translating to tags used in the flask script for each button hover over display
