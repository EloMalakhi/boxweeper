class ConstructNode(object):
    def __init__(self):
        pass

    def set(self, base, changeByZ, changeByItself, viewDim):
        self.base = base
        self.Zchange = changeByZ
        self.self_change = changeByItself
        self.ob = 12/viewDim




class Construct(object):
    def __init__(self):
        self.x = ConstructNode()
        self.y = ConstructNode()
        self.font_size = None

