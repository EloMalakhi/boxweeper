class BoxNode(object):
    def __init__(self):
        self.open = None            # the amount of non-mine boxes that have been discovered   
        self.closed = None          # the amount of untouched blocks
        self.unfound_mines =  None  # the amount of not found mines, (a mine isn't found until the confirmation button is clicked and guessed mines are 1000)
        self.found_mines = None     # the amount of guessed mines

    def set(self, open, closed, unfound, found):
        self.open  = open
        self.closed = closed
        self.unfound_mines = unfound
        self.guessed = found


class PuzzleNode(object):
    def __init__(self):
        pass

    def set(self, x, y, z):
        self.xv = x # length from left to right in box units
        self.yv = y # height in box units
        self.zv = z # depth in box units
        # pre-done products to assist in programming
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
        self.total = PuzzleNode() # total of units in all three dimensions
        self.view = PuzzleNode() # view dimensions in units
        self.centerLLim = PuzzleNode() # lowest allowed 3-D position for center
        self.centerGLim = PuzzleNode()  # highest allowed 3-D position for cent
        self.boxes = BoxNode()  # useful information about all the boxes in the gamee
        self.death = None # Dead or not
        self.usercenter = PuzzleNode() # 3-D position of where the user leaves off
        self.pinkboxnumber = None # if the dimensions aren't 3 by 3 by 3 then the pinkboxnumber indicates what is the improvised center
        self.ViewCubeCoordTranslate = {} # A translating dictionary for the button number clicked on translating to the 3-D position adjustment
        self.AllCubes = {} #
        #         {(x: int, y: int, z: int): [description_of_box: str, mark_status: str],
# #                (x: int, y: int, z: int): [description_of_box: str, mark_status: str],
# #                (x: int, y: int, z: int): [description_of_box: str, mark_status: str],
#                  (x: int, y: int, z: int): [description_of_box: str, mark_status: str], etc} # all the keys corresponding to all the points


# There are closed boxes with cavities
# there are closed boxes with mines
# there are closed boxes with numbers
# there are open boxes with cavities
# there are open boxes with numbers
# there are labeled boxes

# there are cavities (statuses: closed, open)
# there are mines (statuses: )
# there are numbers
# 