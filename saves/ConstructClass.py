class ConstructNode(object):
    def __init__(self):
        pass

    def set(self, base, changeByZ, changeByItself, viewDim):
        # calculation of button position based on self's position is as follows:
        # base + changebyZ*(z numbered unit) + changeByItself*(button numbered unit in this dimension)
        self.base = base
        self.Zchange = changeByZ
        self.self_change = changeByItself
        # x or y of button based on the view dimension units
        self.ob = 12/viewDim




class Construct(object):
    def __init__(self):
        self.x = ConstructNode()
        self.y = ConstructNode()
        # the font size of the button
        self.font_size = None

