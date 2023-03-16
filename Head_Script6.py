
############ Necessary for the skeleton of this script ############
from flask import Flask, session, redirect, render_template, request, abort, escape, url_for
import re
import validate
import define
# the globalization of these variables is to deter the creation of a new variable for the same purpose every function call
TheMasterList = []





# all the variables above have to be put into classes


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

class ConstructNode(object):
    def __init__(self):
        pass

    def set(self, base, changeByZ, changeByItself, viewDim):
        self.base = base
        self.Zchange = changeByZ
        self.self_change = changeByItself
        self.ob = 12/viewDim

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


class Construct(object):
    def __init__(self):
        self.x = ConstructNode()
        self.y = ConstructNode()
        self.font_size = None

class Caption(object):
    def __init__(self):
        self.confirmation = None
        self.hoveroverelement = {}
        self.hoverovertext = {}

class Setup(object):
    def __init(self):
        pass

    def set(self, Matrix, error, EnoughInformation, pf, IF, mode):
        self.FileMatrix = Matrix
        self.error = error
        self.EnoughInformation = EnoughInformation
        self.PresetFile = pf
        self.indexFile = IF
        self.mode = mode

GamePuzzle = Puzzle()
GameStruct = Construct()
GameCaptions = Caption()
GameSetup = Setup()
# presetPuzzleHeight, presetPuzzleLength, presetPuzzleWidth define the total scope of the height, length, and width of the puzzle

# presetViewBoxX, presetViewBoxY, presetViewBoxZ define the viewed scope of the puzzle

# PinkBoxNumber, when the box doesn't have the dimensions 3x3x3 then the center has to be determined otherwise, also it must
# be indicated to the user which box carries the coordinates displayed in the text field, so during unusual presets that
# box will be colored pink

# C1 - C6 are constants calculated before the calling of the web pages and used to assist flask in correctly spacing the buttons in the index html files





def check_for_direction(Cx, Cy, Cz):
    List = {}
    count = -1
    if Cx > GamePuzzle.centerLLim.xv:
        count += 1
        List[count] = 'left'
    if Cx < GamePuzzle.centerGLim.xv:
        count += 1
        List[count] = 'right'
    if Cy > GamePuzzle.centerLLim.yv:
        count += 1
        List[count] = 'down'
    if Cy < GamePuzzle.centerGLim.yv:
        count += 1
        List[count] = 'up'
    if Cz > GamePuzzle.centerLLim.zv:
        count += 1
        List[count] = 'backward'
    if Cz < GamePuzzle.centerGLim.zv:
        count += 1
        List[count] = 'forward'
    return List

def check_in_bounds(x, y, z):
    TorF = False
    if isINTEGER(x) and isINTEGER(y) and isINTEGER(z):
        x = int(x)
        y = int(y)
        z = int(z)
        if x <= GamePuzzle.centerGLim.xv and x >= GamePuzzle.centerLLim.xv:
            if y <= GamePuzzle.centerGLim.yv and y >= GamePuzzle.centerLLim.yv:
                if z <= GamePuzzle.centerGLim.zv and z >= GamePuzzle.centerLLim.zv:
                    TorF = True
    print(f'{x} {y} {z}')
    print(TorF)
    return TorF

def isINTEGER(num):
    if re.findall("^-\d*\.\d+$", num):
        return True
    elif re.findall("^-\d+$", num):
        return True
    elif re.findall("^\d*\.\d+$", num):
        return True
    elif re.findall("^\d+$", num):
        return True
    else:
        return False

def remove_cavity(Cavity_for_removal, PointsRecord):
    for i in PointsRecord:
        if PointsRecord[i][0] == Cavity_for_removal:
            PointsRecord[i] = [" ", "unmarkable"]
            GamePuzzle.boxes.open += 1

def Check_For_Mines(PosX, PosY, PosZ):
    count = 0
    for i in range(3):
        y = i - 1
        for k in range(3):
            x = k - 1
            for j in range(3):
                z = j - 1
                if GamePuzzle.AllCubes.get((x+PosX,y+PosY, z+PosZ)):
                    if GamePuzzle.AllCubes[(x+PosX,y+PosY, z+PosZ)][0] == "mine closed":
                        count += 1
    return count

def ValidateLabels():
    for i in GamePuzzle.AllCubes:
        if GamePuzzle.AllCubes[i][0] == "mine closed" and GamePuzzle.AllCubes[i][1] == "marked":
            GamePuzzle.boxes.unfound_mines
    if GamePuzzle.boxes.unfound_mines == 0:
        return True
    else:
        return False

def D3_Minesweeper_Post2(request):
    GameSetup.EnoughInformation = True
    if request.form.get('v14'):
        GameSetup.error, GameSetup.EnoughInformation = validate.presets_of_type_2(request, "")

    if GameSetup.EnoughInformation:
        GamePuzzle.total.set(int(request.form.get('v1')), int(request.form.get('v3')), int(request.form.get('v5')))
        GamePuzzle.boxes.set(0, GamePuzzle.total.xy*GamePuzzle.total.zv - int(request.form.get('v7')), int(request.form.get('v7')), 0)
        GamePuzzle.view.set(3, 3, 3)
        GamePuzzle.death = 0

        GamePuzzle.boxes.open = 1
        GameCaptions.confirmation = ""
        GameStruct.x.set(
            34 - 12/GamePuzzle.view.zv - 12/GamePuzzle.view.xv - 12/(GamePuzzle.view.xv - 1),
            12/GamePuzzle.view.zv,
            12/GamePuzzle.view.xv + 12/(GamePuzzle.view.xv - 1),
            GamePuzzle.view.xv)

        GameStruct.y.set(
            56 + 24/GamePuzzle.view.yv + 24/(GamePuzzle.view.yv - 1),
            24/GamePuzzle.view.yv,
            -24/GamePuzzle.view.yv - 24/(GamePuzzle.view.yv - 1),
            GamePuzzle.view.yv/2)

        #C1 = 34 - (1/(presetViewBoxZ - 1) + 1/(presetViewBoxX - 1))*(24 - 12/presetViewBoxX)

        GameStruct.font_size = (60/(GamePuzzle.view.zy * GamePuzzle.view.xv)**(1/3))
        # define the center of the displayed cube:
        GamePuzzle.centerGLim.set(GamePuzzle.total.xv - 2, GamePuzzle.total.yv - 2, GamePuzzle.total.zv - 2)
        GamePuzzle.centerLLim.set(GamePuzzle.view.xv - 2, GamePuzzle.view.yv - 2, GamePuzzle.view.zv - 2)
        GamePuzzle.usercenter.set(GamePuzzle.total.xv - 2, GamePuzzle.total.yv - 2, GamePuzzle.total.zv - 2)
        GamePuzzle.boxes.guessed = 0
        GamePuzzle.pinkboxnumber = (GamePuzzle.view.yv - 2)*GamePuzzle.view.xz + GamePuzzle.centerLLim.xv*GamePuzzle.view.zv + (GamePuzzle.view.zv - 1)
        # the globalization is used to make one data instance for memory purposes
        # and set the type of  these:

        GameCaptions.hoverovertext = {}


        # get the Large Cube that is the game
        import test4
        GamePuzzle.AllCubes = test4.MakeSweeperGame(GamePuzzle.total.yv, GamePuzzle.total.xv, GamePuzzle.total.zv, GamePuzzle.boxes.unfound_mines)

        # here is how a hover over works
        # in a style tag you have the following
        # a div CLASSNAME that has a display: block; attribute
        # a CLASSNAME2.caption that sets attributes of the hover over text
        # a div CLASSNAME:hover + CLASSNAME2 that indicates other attributes of the hover over text
        # 
        # now you are out of the style tag
        # in the div class=block tag you put your two custom tags CLASSNAME and CLASSNAME2
        # in the CLASSNAME tag you put your elements
        # and in the CLASSNAME2 tag you put the hover over text


        # an item has 27 points of contact including itself
        for i in range(GamePuzzle.view.yv):
            for j in range(GamePuzzle.view.xv):
                for k in range(GamePuzzle.view.zv):
                    # dwmio = do when mouse is over
                    GameCaptions.hoveroverelement[i*GamePuzzle.view.xz + j*GamePuzzle.view.zv + k + 1] = 'dwmio' + str(i*GamePuzzle.view.xz + j*GamePuzzle.view.zv + k)
                    # posie is short for position
                    GameCaptions.hoverovertext[i*GamePuzzle.view.xz + j*GamePuzzle.view.zv + k + 1] = 'posie' + str(i*GamePuzzle.view.xz + j*GamePuzzle.view.zv + k)
                    # while running through these numbers it makes a hash to convert from number to coordinate
                    GamePuzzle.ViewCubeCoordTranslate[i*GamePuzzle.view.xz + j*GamePuzzle.view.zv + k + 1] = [j + 2 - GamePuzzle.view.xv, i + 2 - GamePuzzle.view.yv, k + 2 - GamePuzzle.view.zv]
        NoZero = True
        while NoZero:
            for i in GamePuzzle.AllCubes:
                if Check_For_Mines(i[0], i[1], i[2]) == 0:
                    NoZero = False
                    GamePuzzle.AllCubes[i][1] = "unmarkable"
                    GamePuzzle.AllCubes[i][0] = 0
                    tryX, tryY, tryZ = i[0], i[1], i[2]
                    break
        if tryX < GamePuzzle.centerLLim.xv:
            GamePuzzle.usercenter.xv = GamePuzzle.centerLLim.xv
        elif tryX > GamePuzzle.centerGLim.xv:
            GamePuzzle.usercenter.xv = GamePuzzle.centerGLim.xv
        else:
            GamePuzzle.usercenter.xv = tryX
        if tryY < GamePuzzle.centerLLim.yv:
            GamePuzzle.usercenter.yv = GamePuzzle.centerLLim.yv
        elif tryY > GamePuzzle.centerGLim.yv:
            GamePuzzle.usercenter.yv = GamePuzzle.centerGLim.yv
        else:
            GamePuzzle.usercenter.yv = tryY
        if tryZ < GamePuzzle.centerLLim.zv:
            GamePuzzle.usercenter.zv = GamePuzzle.centerLLim.zv
        elif tryZ > GamePuzzle.centerGLim.zv:
            GamePuzzle.usercenter.zv = GamePuzzle.centerGLim.zv
        else:
            GamePuzzle.usercenter.zv = tryZ
        return redirect(url_for('Minesweeper_play'))
    else:
        return render_template(GameSetup.PresetFile, error=GameSetup.error)

def D3_Minesweeper_Post1(request):
    



    GameSetup.EnoughInformation = True
    if request.form.get('v14'):
        import validate
        GameSetup.error, GameSetup.EnoughInformation = validate.presets_of_type_1(request, "")

    if GameSetup.EnoughInformation:
        GamePuzzle.total.set(int(request.form.get('v1')), int(request.form.get('v3')), int(request.form.get('v5')))
        GamePuzzle.boxes.unfound_mines = int(request.form.get('v7'))
        GamePuzzle.view.set(int(request.form.get('v9')), int(request.form.get('v11')), int(request.form.get('v13')))

        GamePuzzle.boxes.unfound_mines = int(request.form.get('v7'))
        GamePuzzle.death = 0

        GamePuzzle.boxes.open = 1
        GameCaptions.confirmation = ""

        GameStruct.x.set(
            34 - 12/GamePuzzle.view.zv - 12/GamePuzzle.view.xv - 12/(GamePuzzle.view.xv - 1),
            12/GamePuzzle.view.zv,
            12/GamePuzzle.view.xv + 12/(GamePuzzle.view.xv - 1),
            GamePuzzle.view.xv
            )

        GameStruct.y.set(
            56 + 24/GamePuzzle.view.yv + 24/(GamePuzzle.view.yv - 1),
            24/GamePuzzle.view.yv,
            -24/GamePuzzle.view.yv - 24/(GamePuzzle.view.yv - 1),
            GamePuzzle.view.yv/2)


        GameStruct.font_size = (60/(GamePuzzle.view.xy*GamePuzzle.view.zv)**(1/3))
        # define the center of the displayed cube:
        GamePuzzle.centerGLim.xv = GamePuzzle.total.xv - 2
        GamePuzzle.centerGLim.yv = GamePuzzle.total.yv - 2
        GamePuzzle.centerGLim.zv = GamePuzzle.total.zv - 2
        GamePuzzle.centerLLim.xv  = GamePuzzle.view.xv - 2
        GamePuzzle.centerLLim.yv  = GamePuzzle.view.yv - 2
        GamePuzzle.centerLLim.zv  = GamePuzzle.view.zv - 2
        GamePuzzle.usercenter.xv = GamePuzzle.centerGLim.xv
        GamePuzzle.usercenter.yv = GamePuzzle.centerGLim.yv
        GamePuzzle.usercenter.zv = GamePuzzle.centerGLim.zv
        GamePuzzle.boxes.guessed = 0
        GamePuzzle.pinkboxnumber  = (GamePuzzle.view.yv - 2)*GamePuzzle.view.xz + GamePuzzle.centerLLim.xv*GamePuzzle.view.zv + (GamePuzzle.view.zv - 1)

        # the globalization is used to make one data instance for memory purposes
        # and set the type of  these:
        GameCaptions.hoveroverelement = {}
        GameCaptions.hoverovertext = {}

        # get the Large Cube that is the game
        import test4
        GamePuzzle.AllCubes = test4.MakeSweeperGame(GamePuzzle.total.yv, GamePuzzle.total.xv, GamePuzzle.total.zv, GamePuzzle.boxes.unfound_mines)

        # here is how a hover over works
        # in a style tag you have the following
        # a div CLASSNAME that has a display: block; attribute
        # a CLASSNAME2.caption that sets attributes of the hover over text
        # a div CLASSNAME:hover + CLASSNAME2 that indicates other attributes of the hover over text
        # 
        # now you are out of the style tag
        # in the div class=block tag you put your two custom tags CLASSNAME and CLASSNAME2
        # in the CLASSNAME tag you put your elements
        # and in the CLASSNAME2 tag you put the hover over text



        # an item has 27 points of contact including itself
        for i in range(GamePuzzle.view.yv):
            for j in range(GamePuzzle.view.xv):
                for k in range(GamePuzzle.view.zv):
                    # dwmio = do when mouse is over
                    GameCaptions.hoveroverelement[i*GamePuzzle.view.xz + j*GamePuzzle.view.zv + k + 1] = 'dwmio' + str(i*GamePuzzle.view.xz + j*GamePuzzle.view.zv + k)
                    # posie is short for position
                    GameCaptions.hoverovertext[i*GamePuzzle.view.xz + j*GamePuzzle.view.zv + k + 1] = 'posie' + str(i*GamePuzzle.view.xz + j*GamePuzzle.view.zv + k)
                    # while running through these numbers it makes a hash to convert from number to coordinate
                    GamePuzzle.ViewCubeCoordTranslate[i*GamePuzzle.view.xz + j*GamePuzzle.view.zv + k + 1] = [j + 2 - GamePuzzle.view.xv, i + 2 - GamePuzzle.view.yv, k + 2 - GamePuzzle.view.zv]
 
        
        NoZero = True
        while NoZero:
            for i in GamePuzzle.AllCubes:
                if Check_For_Mines(i[0], i[1], i[2]) == 0:
                    NoZero = False
                    GamePuzzle.AllCubes[i][1] = "unmarkable"
                    GamePuzzle.AllCubes[i][0] = "0"
                    tryX, tryY, tryZ = i[0], i[1], i[2]
                    break
        if tryX < GamePuzzle.centerLLim.xv:
            GamePuzzle.usercenter.xv = GamePuzzle.centerLLim.xv
        elif tryX > GamePuzzle.centerGLim.xv:
            GamePuzzle.usercenter.xv = GamePuzzle.centerGLim.xv
        else:
            GamePuzzle.usercenter.xv = tryX
        if tryY < GamePuzzle.centerLLim.yv:
            GamePuzzle.usercenter.yv = GamePuzzle.centerLLim.yv
        elif tryY > GamePuzzle.centerGLim.yv:
            GamePuzzle.usercenter.yv = GamePuzzle.centerGLim.yv
        else:
            GamePuzzle.usercenter.yv = tryY
        if tryZ < GamePuzzle.centerLLim.zv:
            GamePuzzle.usercenter.zv = GamePuzzle.centerLLim.zv
        elif tryZ > GamePuzzle.centerGLim.zv:
            GamePuzzle.usercenter.zv = GamePuzzle.centerGLim.zv
        else:
            GamePuzzle.usercenter.zv = tryZ
        return redirect(url_for('Minesweeper_play'))
    else:
        
        return render_template(GameSetup.PresetFile, error=GameSetup.error)









app = Flask(__name__)

#  these three lines are the home page of the game
@app.route('/', methods=['GET', 'POST'])
def Modes():
    """ defines the amount of playable modes
        makes a dictionary attaching the mode number to the necessary web pages
        loops through the modes until 
    """

    modes = 4
    GameSetup.set([{0: "Presets.html", 1: "Presets3.html", 2: "Presets3.html", 3: "Presets3.html"}, 
                   {0: "index5.html", 1: "index7.html", 2: "index8.html", 3: "index9.html"}],
                   "", "", "", "", 0)
    if request.method == 'GET':
        return render_template('Modes.html', modes=modes)
    else:
        for i in range(modes):
            if request.form.get(str(i)):
                GameSetup.PresetFile = GameSetup.FileMatrix[0][i]
                GameSetup.mode = i
    return redirect(url_for('D3_Minesweeper'))
            

@app.route('/D3_Minesweeper', methods=['GET', 'POST'])
def D3_Minesweeper():
    global mode
    if request.method == 'GET':
        return render_template(GameSetup.PresetFile)
    else:
        
        if GameSetup.mode == 0:
            
            return D3_Minesweeper_Post1(request)
        else:
            return D3_Minesweeper_Post2(request)

# this is where everything happens

@app.route('/Minesweeper_play', methods=['GET', 'POST'])
def Minesweeper_play():
    if request.method == 'GET':
        if GamePuzzle.death < 3:
            return render_template(GameSetup.FileMatrix[1][GameSetup.mode],
            hoverover_elementtags=GameCaptions.hoveroverelement,
            xX = GamePuzzle.total.xv, 
            yY = GamePuzzle.total.yv, 
            zZ = GamePuzzle.total.zv,
            hoverover_texttags=GameCaptions.hoverovertext, TB=GamePuzzle.total.xy*GamePuzzle.total.zv,
            Num_to_Coord=GamePuzzle.ViewCubeCoordTranslate, x=GamePuzzle.usercenter.xv, y=GamePuzzle.usercenter.yv, z=GamePuzzle.usercenter.zv, FS=GameStruct.font_size, Strikes=GamePuzzle.death,
            MineHitter=GamePuzzle.death, 
            px = GamePuzzle.view.xv,
            py = GamePuzzle.view.yv,
            pz = GamePuzzle.view.zv,
            PointsRecord=GamePuzzle.AllCubes, 
            Available_directions=check_for_direction(GamePuzzle.usercenter.xv, GamePuzzle.usercenter.yv, GamePuzzle.usercenter.zv),
            Pink=GamePuzzle.pinkboxnumber, 
            amount_of_directions=len(check_for_direction(GamePuzzle.usercenter.xv, GamePuzzle.usercenter.yv, GamePuzzle.usercenter.zv)),
            c1=GameStruct.x.base, c2=GameStruct.x.Zchange, c3=GameStruct.x.self_change, c4=GameStruct.y.base, c5=GameStruct.y.Zchange, c6=GameStruct.y.self_change,
            wob=GameStruct.x.ob, hob=GameStruct.y.ob,
            MM=GamePuzzle.boxes.unfound_mines, LL=GamePuzzle.boxes.guessed, RB=GamePuzzle.boxes.open, CF=GameCaptions.confirmation)
        else:
            return render_template('MinesweeperDeath.html')
    else:
        # go through the squares and see which ones have a value of 1 or 2 spaces to indicate labelness
        if request.form.get('up'):
            GamePuzzle.usercenter.yv += 1
        elif request.form.get('down'):
            GamePuzzle.usercenter.yv -= 1
        elif request.form.get('left'):
            GamePuzzle.usercenter.xv -= 1
        elif request.form.get('right'):
            GamePuzzle.usercenter.xv += 1
        elif request.form.get('forward'):
            GamePuzzle.usercenter.zv += 1
        elif request.form.get('backward'):
            GamePuzzle.usercenter.zv -= 1
        elif request.form.get('position'):
            position = request.form.get('positionString')
            position = re.sub("\s+", " ", position)
            if len(position.split(' ')) == 3 and check_in_bounds(position.split(' ')[0], position.split(' ')[1], position.split(' ')[2]): 
                List = position.split(' ')
                GamePuzzle.usercenter.xv = int(List[0])
                GamePuzzle.usercenter.yv = int(List[1])
                GamePuzzle.usercenter.zv = int(List[2])
        elif request.form.get('CM'):
            if GamePuzzle.boxes.guessed == GamePuzzle.boxes.unfound_mines:
                if ValidateLabels():
                    GameCaptions.confirmation = "You got all of them, you win!"
                    return redirect(url_for('Minesweeper_play'))
                else:
                    GameCaptions.confirmation = "You didn't get all of them yet, keep trying!"
                    return redirect(url_for('Minesweeper_play'))
            else:
                GameCaptions.confirmation = "You didn't get all of them yet, keep trying!"
                return redirect(url_for('Minesweeper_play'))
        elif request.form.get('save'):
            savefile = open('savefile.py', 'w')
            savefile.write("PointsRecord = " + str(GamePuzzle.AllCubes) + "\n")
            savefile.write("T_H = " + str(GamePuzzle.total.yv) + "\n")
            savefile.write("T_L = " + str(GamePuzzle.total.zv) + "\n")
            savefile.write("T_W = " + str(GamePuzzle.total.xv) + "\n")
            savefile.write("V_X = " + str(GamePuzzle.view.xv) + "\n")
            savefile.write("V_Y = " + str(GamePuzzle.view.yv) + "\n")
            savefile.write("V_Z = " + str(GamePuzzle.view.zv) + "\n")
            savefile.write(f"P_M = {GamePuzzle.boxes.unfound_mines}\n")
            savefile.write("MineHitter = " + str(GamePuzzle.death) + "\n") 
            savefile.write("AmountOfReleasedBoxes = " + str(GamePuzzle.boxes.open) + "\n")
            savefile.write("LabeledBoxes = " + str(GamePuzzle.boxes.guessed) + "\n")
            savefile.write(f"mode = {GameSetup.mode}")
            savefile.write("Num_to_Coord = " + str(GamePuzzle.ViewCubeCoordTranslate) + "\n")
            savefile.write("Cx = " + str(GamePuzzle.usercenter.xv) + "\n")
            savefile.write("Cy = " + str(GamePuzzle.usercenter.yv) + "\n")
            savefile.write("Cz = " + str(GamePuzzle.usercenter.zv) + "\n")
            savefile.write("PinkBoxNumber = " + str(GamePuzzle.pinkboxnumber) + "\n")
            savefile.write("hoverover_elementtags = " + str(GameCaptions.hoveroverelement) + "\n")
            savefile.write("hoverover_texttags = " + str(GameCaptions.hoverovertext) + "\n")
            savefile.write("HeightOfButton = " + str(GameStruct.y.ob) + "\n")
            savefile.write("WidthOfButton = " + str(GameStruct.x.ob) + "\n")
            savefile.write(f"GLX = {GamePuzzle.centerGLim.xv}\n")
            savefile.write(f"GLY = {GamePuzzle.centerGLim.yv}\n")
            savefile.write(f"GLZ = {GamePuzzle.centerGLim.zv}\n")
            savefile.write(f"LLX = {GamePuzzle.centerLLim.xv}\n")
            savefile.write(f"LLY = {GamePuzzle.centerLLim.yv}\n")
            savefile.write(f"LLZ = {GamePuzzle.centerLLim.zv}\n")
            savefile.write(f"C1 = {GameStruct.x.base}\n")
            savefile.write(f"C2 = {GameStruct.x.Zchange}\n")
            savefile.write(f"C3 = {GameStruct.x.self_change}\n")
            savefile.write(f"C4 = {GameStruct.y.base}\n")
            savefile.write(f"C5 = {GameStruct.y.Zchange}\n")
            savefile.write(f"C6 = {GameStruct.y.self_change}\n")
            savefile.write(f"Confirmation = '{GameCaptions.confirmation}'\n")
            savefile.close()
            return redirect(url_for('Minesweeper_play'))
        elif request.form.get('open'):
            from savefile import PointsRecord as Poi
            GamePuzzle.AllCubes = Poi
            from savefile import T_H, T_W, T_L, V_X, V_Y, V_Z, P_M, C1, C2, C3, C4, C5, C6, MineHitter
            from savefile import AmountOfReleasedBoxes, LabeledBoxes, Num_to_Coord, Cx, Cy, Cz, hoverover_elementtags, hoverover_texttags
            from savefile import PinkBoxNumber, WidthOfButton, HeightOfButton, Confirmation
            from savefile import GLX, GLY, GLZ, LLX, LLY, LLZ, mode
            GamePuzzle.total.set(T_W, T_H, T_L)
            GamePuzzle.view.set(V_X, V_Y, V_Z)
            GamePuzzle.centerGLim.set(GLX, GLY, GLZ)
            GamePuzzle.centerLLim.set(LLX, LLY, LLZ)
            GamePuzzle.boxes.unfound_mines = P_M
            GamePuzzle.usercenter.set(Cx, Cy, Cz)
            GamePuzzle.death = MineHitter
            GamePuzzle.pinkboxnumber = PinkBoxNumber
            GameStruct.x.set(C1, C2, C3, 12/WidthOfButton)
            GameStruct.y.set(C4, C5, C6, 12/HeightOfButton)
            GamePuzzle.boxes.guessed = LabeledBoxes
            GamePuzzle.boxes.open = AmountOfReleasedBoxes
            GameCaptions.confirmation = Confirmation
            GameCaptions.hoveroverelement = hoverover_elementtags
            GameCaptions.hoverovertext = hoverover_texttags
            GamePuzzle.ViewCubeCoordTranslate =  Num_to_Coord
            GameSetup.mode = mode
            return redirect(url_for('Minesweeper_play'))
        else:
            GameCaptions.confirmation = ""
            print(request.form)
            for i in range(GamePuzzle.view.xy*GamePuzzle.view.zv):
                buttonPressed = i + 1
                if request.form.get(str(i+1)):
                    if GamePuzzle.AllCubes[(GamePuzzle.usercenter.xv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][0], GamePuzzle.usercenter.yv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][1], GamePuzzle.usercenter.zv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][2])][1] == 'markable' and request.form.get(str(i+1)) == "  ":
                        GamePuzzle.boxes.guessed += 1
                        GamePuzzle.AllCubes[(GamePuzzle.usercenter.xv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][0], GamePuzzle.usercenter.yv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][1], GamePuzzle.usercenter.zv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][2])][1] = 'marked'
                    elif GamePuzzle.AllCubes[(GamePuzzle.usercenter.xv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][0], GamePuzzle.usercenter.yv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][1], GamePuzzle.usercenter.zv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][2])][1] == 'marked' and request.form.get(str(i+1)) == " ":
                        GamePuzzle.boxes.guessed -= 1
                        GamePuzzle.AllCubes[(GamePuzzle.usercenter.xv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][0], GamePuzzle.usercenter.yv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][1], GamePuzzle.usercenter.zv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][2])][1] = 'markable'
                    elif GamePuzzle.AllCubes[(GamePuzzle.usercenter.xv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][0], GamePuzzle.usercenter.yv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][1], GamePuzzle.usercenter.zv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][2])][1] == 'markable' and request.form.get(str(i+1)) == " ":
                        if GamePuzzle.AllCubes[(GamePuzzle.usercenter.xv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][0], GamePuzzle.usercenter.yv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][1], GamePuzzle.usercenter.zv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][2])][0] == "mine closed":
                            GamePuzzle.death += 1
                        elif GamePuzzle.AllCubes[(GamePuzzle.usercenter.xv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][0], GamePuzzle.usercenter.yv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][1], GamePuzzle.usercenter.zv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][2])][0] == "block":
                            GamePuzzle.boxes.open += 1
                            GamePuzzle.AllCubes[(GamePuzzle.usercenter.xv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][0], GamePuzzle.usercenter.yv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][1], GamePuzzle.usercenter.zv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][2])] = [Check_For_Mines(GamePuzzle.usercenter.xv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][0], GamePuzzle.usercenter.yv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][1], GamePuzzle.usercenter.zv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][2]), 'unmarkable']
                        elif 'cavity' in GamePuzzle.AllCubes[(GamePuzzle.usercenter.xv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][0], GamePuzzle.usercenter.yv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][1], GamePuzzle.usercenter.zv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][2])][0]:
                            remove_cavity(GamePuzzle.AllCubes[(GamePuzzle.usercenter.xv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][0], GamePuzzle.usercenter.yv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][1], GamePuzzle.usercenter.zv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][2])][0], GamePuzzle.AllCubes)


        return redirect(url_for('Minesweeper_play'))
       
 




app.secret_key = 'oetc2802w?ih,i!MkdC>IC.l?<IH'
if __name__ == "__main__":
    app.run(port=4500)

