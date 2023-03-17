class BoxNode(object):
    def __init__(self):
        self.open = None
        self.closed = None
        self.unfound_mines =  None
        self.found_mines = None

    def set(self, open, closed, unfound, found):
        self.open  = open
        self.closed = closed
        self.unfound_mines = unfound
        self.guessed = found


class PuzzleNode(object):
    def __init__(self):
        pass

    def set(self, x, y, z):
        self.xv = x
        self.yv = y
        self.zv = z
        self.xx = x*x
        self.xy = x*y
        self.xz = x*z
        self.yx = y*x
        self.yy = y*y
        self.yz = y*z
        self.zx = z*x
        self.zy = z*y
        self.zz = z*z
 

class Puzzle(object):
    def __init__(self):
        self.total = PuzzleNode()
        self.view = PuzzleNode()
        self.centerLLim = PuzzleNode()
        self.centerGLim = PuzzleNode()
        self.boxes = BoxNode()
        self.death = None
        self.usercenter = PuzzleNode()
        self.pinkboxnumber = None
        self.ViewCubeCoordTranslate = {}
        self.AllCubes = {}