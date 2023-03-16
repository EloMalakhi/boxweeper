
############ Necessary for the skeleton of this script ############
from flask import Flask, session, redirect, render_template, request, abort, escape, url_for
import re
import validate
import define
# the globalization of these variables is to deter the creation of a new variable for the same purpose every function call
TheMasterList = []

global presetPuzzleMines, Cx, Cy, Cz, MineHitter
global GPx, GPy, GPz, LPx, LPy, LPz, PinkBoxNumber
global C1, C2, C3, C4, C5, C6, WidthOfButton, HeightOfButton, FS, LabeledBoxes, AmountOfReleasedBoxes
global Confirmation, TotalB, PRESETFILE, error, mode, IndexFiles, Num_to_Coord, hoverover_elementtags, hoverover_texttags

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
        

class ConstructNode(object):
    def __init__(self):
        pass

    def set(self, base, changeByZ, changeByItself):
        self.base = base
        self.Zchange = changeByZ
        self.self_change = changeByItself

class Puzzle(object):
    def __init__(self):
        self.total = PuzzleNode()
        self.view = PuzzleNode()
        self.centerLLim = PuzzleNode()
        self.centerGLim = PuzzleNode()
        self.mines = None
        self.death = None

class Construct(object):
    def __init__(self):
        self.x = ConstructNode()
        self.y = ConstructNode()

GamePuzzle = Puzzle()
# presetPuzzleHeight, presetPuzzleLength, presetPuzzleWidth define the total scope of the height, length, and width of the puzzle

# presetViewBoxX, presetViewBoxY, presetViewBoxZ define the viewed scope of the puzzle

# GPx, GPy, GPz, LPx, LPy, LPz, these define the greatest and lowest allowable x, y, z points for the center of the view box

# PinkBoxNumber, when the box doesn't have the dimensions 3x3x3 then the center has to be determined otherwise, also it must
# be indicated to the user which box carries the coordinates displayed in the text field, so during unusual presets that
# box will be colored pink

# C1 - C6 are constants calculated before the calling of the web pages and used to assist flask in correctly spacing the buttons in the index html files





def check_for_direction(Cx, Cy, Cz):
    global GPx, GPy, GPz, LPx, LPy, LPz
    List = {}
    count = -1
    if Cx > LPx:
        count += 1
        List[count] = 'left'
    if Cx < GPx:
        count += 1
        List[count] = 'right'
    if Cy > LPy:
        count += 1
        List[count] = 'down'
    if Cy < GPy:
        count += 1
        List[count] = 'up'
    if Cz > LPz:
        count += 1
        List[count] = 'backward'
    if Cz < GPz:
        count += 1
        List[count] = 'forward'
    return List

def check_in_bounds(x, y, z):
    TorF = False
    global GPx, GPy, GPz, LPx, LPy, LPz
    if isINTEGER(x) and isINTEGER(y) and isINTEGER(z):
        x = int(x)
        y = int(y)
        z = int(z)
        if x <= GPx and x >= LPx:
            if y <= GPy and y >= LPy:
                if z <= GPz and z >= LPz:
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
    global AmountOfReleasedBoxes
    for i in PointsRecord:
        if PointsRecord[i][0] == Cavity_for_removal:
            PointsRecord[i] = [" ", "unmarkable"]
            AmountOfReleasedBoxes += 1

def Check_For_Mines(PosX, PosY, PosZ):
    count = 0
    for i in range(3):
        y = i - 1
        for k in range(3):
            x = k - 1
            for j in range(3):
                z = j - 1
                if PointsRecord.get((x+PosX,y+PosY, z+PosZ)):
                    if PointsRecord[(x+PosX,y+PosY, z+PosZ)][0] == "mine closed":
                        count += 1
    return count

def ValidateLabels():
    global presetPuzzleMines
    Mines = presetPuzzleMines
    for i in PointsRecord:
        if PointsRecord[i][0] == "mine closed" and PointsRecord[i][1] == "marked":
                Mines -= 1
    if Mines == 0:
        return True
    else:
        return False

def D3_Minesweeper_Post2(request):
    global presetPuzzleMines, Cx, Cy, Cz, MineHitter
    global GPx, GPy, GPz, LPx, LPy, LPz, PinkBoxNumber
    global C1, C2, C3, C4, C5, C6, WidthOfButton, HeightOfButton, FS, LabeledBoxes, AmountOfReleasedBoxes, hoverover_texttags
    global Confirmation, TotalB, PRESETFILE, hoverover_elementtags, Num_to_Coord, PinkBoxNumber
    EnoughInformation = True
    if request.form.get('v14'):
        error, EnoughInformation = validate.presets_of_type_2(request, "")

    if EnoughInformation:
        GamePuzzle.total.set(int(request.form.get('v1')), int(request.form.get('v3')), int(request.form.get('v5')))
        GamePuzzle.mines = int(request.form.get('v7'))
        GamePuzzle.view.set(3, 3, 3)
        presetPuzzleMines = int(request.form.get('v7'))






        
        GamePuzzle.death = 0
        MineHitter = 0
        AmountOfReleasedBoxes = 1
        Confirmation = ""
        TotalB = GamePuzzle.total.xy * GamePuzzle.total.zv

        C1 = 34 - 12/GamePuzzle.view.zv - 12/GamePuzzle.view.xv - 12/(GamePuzzle.view.xv - 1)
        C2 = 12/GamePuzzle.view.zv
        C3 = 12/GamePuzzle.view.xv + 12/(GamePuzzle.view.xv - 1)
        C4 = 56 + 24/GamePuzzle.view.yv + 24/(GamePuzzle.view.yv - 1)
        C5 = 24/GamePuzzle.view.yv
        C6 = -24/GamePuzzle.view.yv - 24/(GamePuzzle.view.yv - 1)

        #C1 = 34 - (1/(presetViewBoxZ - 1) + 1/(presetViewBoxX - 1))*(24 - 12/presetViewBoxX)

        WidthOfButton = 12/GamePuzzle.view.xv
        HeightOfButton = 24/GamePuzzle.view.yv
        FS = (60/(GamePuzzle.view.zy * GamePuzzle.view.xv)**(1/3))
        # define the center of the displayed cube:
        GPx = GamePuzzle.total.xv - 2
        GPy = GamePuzzle.total.yv - 2
        GPz = GamePuzzle.total.zv - 2
        LPx  = GamePuzzle.view.xv - 2
        LPy  = GamePuzzle.view.yv - 2
        LPz  = GamePuzzle.view.zv - 2
        Cx = GPx
        Cy = GPy
        Cz = GPz
        LabeledBoxes = 0
        PinkBoxNumber  = (GamePuzzle.view.yv - 2)*GamePuzzle.view.xz + LPx*GamePuzzle.view.zv + (GamePuzzle.view.zv - 1)
        # the globalization is used to make one data instance for memory purposes
        global hoverover_elementtags, hoverover_texttags, Num_to_Coord
        # and set the type of  these:
        hoverover_elementtags = {}
        hoverover_texttags = {}
        Num_to_Coord = {}

        # get the Large Cube that is the game
        global PointsRecord
        import test4
        PointsRecord = test4.MakeSweeperGame(GamePuzzle.total.yv, GamePuzzle.total.xv, GamePuzzle.total.zv, presetPuzzleMines)

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
        # PinkBoxNumber = (PVY - 2)*PVX*PVZ + (PVX - 2)*PVZ + (PVZ - 2)


        # an item has 27 points of contact including itself
        for i in range(GamePuzzle.view.yv):
            for j in range(GamePuzzle.view.xv):
                for k in range(GamePuzzle.view.zv):
                    # dwmio = do when mouse is over
                    hoverover_elementtags[i*GamePuzzle.view.xz + j*GamePuzzle.view.zv + k + 1] = 'dwmio' + str(i*GamePuzzle.view.xz + j*GamePuzzle.view.zv + k)
                    # posie is short for position
                    hoverover_texttags[i*GamePuzzle.view.xz + j*GamePuzzle.view.zv + k + 1] = 'posie' + str(i*GamePuzzle.view.xz + j*GamePuzzle.view.zv + k)
                    # while running through these numbers it makes a hash to convert from number to coordinate
                    Num_to_Coord[i*GamePuzzle.view.xz + j*GamePuzzle.view.zv + k + 1] = [j + 2 - GamePuzzle.view.xv, i + 2 - GamePuzzle.view.yv, k + 2 - GamePuzzle.view.zv]
        NoZero = True
        while NoZero:
            for i in PointsRecord:
                if Check_For_Mines(i[0], i[1], i[2]) == 0:
                    NoZero = False
                    PointsRecord[i][1] = "unmarkable"
                    PointsRecord[i][0] = 0
                    tryX, tryY, tryZ = i[0], i[1], i[2]
                    break
        if tryX < LPx:
            Cx = LPx
        elif tryX > GPx:
            Cx = GPx
        else:
            Cx = tryX
        if tryY < LPy:
            Cy = LPy
        elif tryY > GPy:
            Cy = GPy
        else:
            Cy = tryY
        if tryZ < LPz:
            Cz = LPz
        elif tryZ > GPz:
            Cz = GPz
        else:
            Cz = tryZ
        return redirect(url_for('Minesweeper_play'))
    else:
        return render_template(PRESETFILE, error=error)

def D3_Minesweeper_Post1(request):
    
    global presetPuzzleMines, Cx, Cy, Cz, MineHitter
    global GPx, GPy, GPz, LPx, LPy, LPz, PinkBoxNumber
    global C1, C2, C3, C4, C5, C6, WidthOfButton, HeightOfButton, FS, LabeledBoxes, AmountOfReleasedBoxes
    global Confirmation, TotalB, Num_to_Coord, hoverover_elementtags, hoverover_texttags, PinkBoxNumber

    EnoughInformation = True
    if request.form.get('v14'):
        import validate
        error, EnoughInformation = validate.presets_of_type_1(request, "")

    if EnoughInformation:
        GamePuzzle.total.set(int(request.form.get('v1')), int(request.form.get('v3')), int(request.form.get('v5')))
        GamePuzzle.mines = int(request.form.get('v7'))
        GamePuzzle.view.set(int(request.form.get('v9')), int(request.form.get('v11')), int(request.form.get('v13')))

        presetPuzzleMines = int(request.form.get('v7'))
        MineHitter = 0
        AmountOfReleasedBoxes = 1
        Confirmation = ""
        TotalB = GamePuzzle.total.xy * GamePuzzle.total.zv

        C1 = 34 - 12/GamePuzzle.view.zv - 12/GamePuzzle.total.xv - 12/(GamePuzzle.total.xv - 1)
        C2 = 12/GamePuzzle.total.zv
        C3 = 12/GamePuzzle.total.xv + 12/(GamePuzzle.total.xv - 1)
        C4 = 56 + 24/GamePuzzle.total.yv + 24/(GamePuzzle.total.yv - 1)
        C5 = 24/GamePuzzle.total.yv
        C6 = -24/GamePuzzle.total.yv - 24/(GamePuzzle.total.yv - 1)

        WidthOfButton = 12/GamePuzzle.total.xv
        HeightOfButton = 24/GamePuzzle.total.yv
        FS = (60/(GamePuzzle.total.xy*GamePuzzle.total.zv)**(1/3))
        # define the center of the displayed cube:
        GPx = GamePuzzle.total.xv - 2
        GPy = GamePuzzle.total.yv - 2
        GPz = GamePuzzle.total.zv - 2
        LPx  = GamePuzzle.view.xv - 2
        LPy  = GamePuzzle.view.yv - 2
        LPz  = GamePuzzle.view.zv - 2
        Cx = GPx
        Cy = GPy
        Cz = GPz
        LabeledBoxes = 0
        PinkBoxNumber  = (GamePuzzle.view.yv - 2)*GamePuzzle.view.xz + LPx*GamePuzzle.view.zv + (GamePuzzle.view.zv - 1)
        # the globalization is used to make one data instance for memory purposes
        global hoverover_elementtags, hoverover_texttags, Num_to_Coord
        # and set the type of  these:
        hoverover_elementtags = {}
        hoverover_texttags = {}
        Num_to_Coord = {}

        # get the Large Cube that is the game
        global PointsRecord
        import test4
        PointsRecord = test4.MakeSweeperGame(GamePuzzle.total.yv, GamePuzzle.total.xv, GamePuzzle.total.zv, presetPuzzleMines)

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
        # PinkBoxNumber = (PVY - 2)*PVX*PVZ + (PVX - 2)*PVZ + (PVZ - 2)


        # an item has 27 points of contact including itself
        for i in range(GamePuzzle.view.yv):
            for j in range(GamePuzzle.view.xv):
                for k in range(GamePuzzle.view.zv):
                    # dwmio = do when mouse is over
                    hoverover_elementtags[i*GamePuzzle.view.xz + j*GamePuzzle.view.zv + k + 1] = 'dwmio' + str(i*GamePuzzle.view.xz + j*GamePuzzle.view.zv + k)
                    # posie is short for position
                    hoverover_texttags[i*GamePuzzle.view.xz + j*GamePuzzle.view.zv + k + 1] = 'posie' + str(i*GamePuzzle.view.xz + j*GamePuzzle.view.zv + k)
                    # while running through these numbers it makes a hash to convert from number to coordinate
                    Num_to_Coord[i*GamePuzzle.view.xz + j*GamePuzzle.view.zv + k + 1] = [j + 2 - GamePuzzle.view.xv, i + 2 - GamePuzzle.view.yv, k + 2 - GamePuzzle.view.v.z]
 
        
        NoZero = True
        while NoZero:
            for i in PointsRecord:
                if Check_For_Mines(i[0], i[1], i[2]) == 0:
                    NoZero = False
                    PointsRecord[i][1] = "unmarkable"
                    PointsRecord[i][0] = "0"
                    tryX, tryY, tryZ = i[0], i[1], i[2]
                    break
        if tryX < LPx:
            Cx = LPx
        elif tryX > GPx:
            Cx = GPx
        else:
            Cx = tryX
        if tryY < LPy:
            Cy = LPy
        elif tryY > GPy:
            Cy = GPy
        else:
            Cy = tryY
        if tryZ < LPz:
            Cz = LPz
        elif tryZ > GPz:
            Cz = GPz
        else:
            Cz = tryZ
        return redirect(url_for('Minesweeper_play'))
    else:
        
        return render_template(PRESETFILE, error=error)









app = Flask(__name__)

#  these three lines are the home page of the game
@app.route('/', methods=['GET', 'POST'])
def Modes():
    """ defines the amount of playable modes
        makes a dictionary attaching the mode number to the necessary web pages
        loops through the modes until 
    """
    global PRESETFILE, mode, IndexFiles
    modes = 4
    PresetFiles = {0: "Presets.html", 1: "Presets3.html", 2: "Presets3.html", 3: "Presets3.html"}
    IndexFiles = {0: "index5.html", 1: "index7.html", 2: "index8.html", 3: "index9.html"}
    if request.method == 'GET':
        return render_template('Modes.html', modes=modes)
    else:
        print(request.form)
        for i in range(modes):
            if request.form.get(str(i)):
                PRESETFILE = PresetFiles[i]
                mode = i
    return redirect(url_for('D3_Minesweeper'))
            

@app.route('/D3_Minesweeper', methods=['GET', 'POST'])
def D3_Minesweeper():
    global PRESETFILE, mode
    if request.method == 'GET':
        return render_template(PRESETFILE)
    else:
        
        if mode == 0:
            
            return D3_Minesweeper_Post1(request)
        else:
            return D3_Minesweeper_Post2(request)

# this is where everything happens

@app.route('/Minesweeper_play', methods=['GET', 'POST'])
def Minesweeper_play():
    global Cx, Cy, Cz, MineHitter, PinkBoxNumber, FS, TotalB
    global C1, C2, C3, C4, C5, C6, WidthOfButton, HeightOfButton
    global LabeledBoxes, AmountOfReleasedBoxes, Confirmation
    global PointsRecord, presetPuzzleMines, mode, IndexFiles
    global Num_to_Coord, hoverover_elementtags, hoverover_texttags
    global PinkBoxNumber
    if request.method == 'GET':
        if MineHitter < 3:
            return render_template(IndexFiles[mode],
            hoverover_elementtags=hoverover_elementtags,
            xX = GamePuzzle.total.xv, 
            yY = GamePuzzle.total.yv, 
            zZ = GamePuzzle.total.zv,
            hoverover_texttags=hoverover_texttags, TB=TotalB,
            Num_to_Coord=Num_to_Coord, x=Cx, y=Cy, z=Cz, FS=FS, Strikes=MineHitter,
            MineHitter=MineHitter, 
            px = GamePuzzle.view.xv,
            py = GamePuzzle.view.yv,
            pz = GamePuzzle.view.zv,
            PointsRecord=PointsRecord, Available_directions=check_for_direction(Cx, Cy, Cz),
            Pink=PinkBoxNumber, amount_of_directions=len(check_for_direction(Cx, Cy, Cz)),
            c1=C1, c2=C2, c3=C3, c4=C4, c5=C5, c6=C6, wob=WidthOfButton, hob=HeightOfButton,
            MM=presetPuzzleMines, LL=LabeledBoxes, RB=AmountOfReleasedBoxes, CF=Confirmation)
        else:
            return render_template('MinesweeperDeath.html')
    else:
        # go through the squares and see which ones have a value of 1 or 2 spaces to indicate labelness
        if request.form.get('up'):
            Cy += 1
        elif request.form.get('down'):
            Cy -= 1
        elif request.form.get('left'):
            Cx -= 1
        elif request.form.get('right'):
            Cx += 1
        elif request.form.get('forward'):
            Cz += 1
        elif request.form.get('backward'):
            Cz -= 1
        elif request.form.get('position'):
            print("7")
            position = request.form.get('positionString')
            position = re.sub("\s+", " ", position)
            if len(position.split(' ')) == 3 and check_in_bounds(position.split(' ')[0], position.split(' ')[1], position.split(' ')[2]): 
                List = position.split(' ')
                Cx = int(List[0])
                Cy = int(List[1])
                Cz = int(List[2])
        elif request.form.get('CM'):
            if LabeledBoxes == presetPuzzleMines:
                if ValidateLabels():
                    Confirmation = "You got all of them, you win!"
                    return redirect(url_for('Minesweeper_play'))
                else:
                    Confirmation = "You didn't get all of them yet, keep trying!"
                    return redirect(url_for('Minesweeper_play'))
            else:
                Confirmation = "You didn't get all of them yet, keep trying!"
                return redirect(url_for('Minesweeper_play'))
        elif request.form.get('save'):
            savefile = open('savefile.py', 'w')
            savefile.write("PointsRecord = " + str(PointsRecord) + "\n")
            savefile.write("T_H = " + str(GamePuzzle.total.yv) + "\n")
            savefile.write("T_L = " + str(GamePuzzle.total.zv) + "\n")
            savefile.write("T_W = " + str(GamePuzzle.total.xv) + "\n")
            savefile.write("presetPuzzleMines = " + str(presetPuzzleMines) + "\n")
            savefile.write("V_X = " + str(GamePuzzle.view.xv) + "\n")
            savefile.write("V_Y = " + str(GamePuzzle.view.yv) + "\n")
            savefile.write("V_Z = " + str(GamePuzzle.view.zv) + "\n")
            savefile.write("MineHitter = " + str(MineHitter) + "\n") 
            savefile.write("AmountOfReleasedBoxes = " + str(AmountOfReleasedBoxes) + "\n")
            savefile.write("TotalB  = " + str(TotalB) + "\n")
            savefile.write("LabeledBoxes = " + str(LabeledBoxes) + "\n")
            savefile.write("Num_to_Coord = " + str(Num_to_Coord) + "\n")
            savefile.write("Cx = " + str(Cx) + "\n")
            savefile.write("Cy = " + str(Cy) + "\n")
            savefile.write("Cz = " + str(Cz) + "\n")
            savefile.write("PinkBoxNumber = " + str(PinkBoxNumber) + "\n")
            savefile.write("hoverover_elementtags = " + str(hoverover_elementtags) + "\n")
            savefile.write("hoverover_texttags = " + str(hoverover_texttags) + "\n")
            savefile.write("HeightOfButton = " + str(HeightOfButton) + "\n")
            savefile.write("WidthOfButton = " + str(WidthOfButton) + "\n")
            savefile.close()
            return redirect(url_for('Minesweeper_play'))
        elif request.form.get('open'):
            from savefile import PointsRecord as Poi
            PointsRecord = Poi
            from savefile import T_H, T_W, T_L, V_X, V_Y, V_Z, presetPuzzleMines,  MineHitter
            from savefile import AmountOfReleasedBoxes, TotalB, LabeledBoxes, Num_to_Coord, Cx, Cy, Cz, hoverover_elementtags, hoverover_texttags
            from savefile import PinkBoxNumber, WidthOfButton, HeightOfButton
            GamePuzzle.total.set(T_W, T_H, T_L)
            GamePuzzle.view.set(V_X, V_Y, V_Z)
            return redirect(url_for('Minesweeper_play'))
        else:
            Confirmation = ""
            print(request.form)
            for i in range(GamePuzzle.view.xy*GamePuzzle.view.zv):
                buttonPressed = i + 1
                if request.form.get(str(i+1)):
                    if PointsRecord[(Cx + Num_to_Coord[buttonPressed][0], Cy + Num_to_Coord[buttonPressed][1], Cz + Num_to_Coord[buttonPressed][2])][1] == 'markable' and request.form.get(str(i+1)) == "  ":
                        LabeledBoxes += 1
                        PointsRecord[(Cx + Num_to_Coord[buttonPressed][0], Cy + Num_to_Coord[buttonPressed][1], Cz + Num_to_Coord[buttonPressed][2])][1] = 'marked'
                    elif PointsRecord[(Cx + Num_to_Coord[buttonPressed][0], Cy + Num_to_Coord[buttonPressed][1], Cz + Num_to_Coord[buttonPressed][2])][1] == 'marked' and request.form.get(str(i+1)) == " ":
                        LabeledBoxes -= 1
                        PointsRecord[(Cx + Num_to_Coord[buttonPressed][0], Cy + Num_to_Coord[buttonPressed][1], Cz + Num_to_Coord[buttonPressed][2])][1] = 'markable'
                    elif PointsRecord[(Cx + Num_to_Coord[buttonPressed][0], Cy + Num_to_Coord[buttonPressed][1], Cz + Num_to_Coord[buttonPressed][2])][1] == 'markable' and request.form.get(str(i+1)) == " ":
                        if PointsRecord[(Cx + Num_to_Coord[buttonPressed][0], Cy + Num_to_Coord[buttonPressed][1], Cz + Num_to_Coord[buttonPressed][2])][0] == "mine closed":
                            MineHitter += 1
                        elif PointsRecord[(Cx + Num_to_Coord[buttonPressed][0], Cy + Num_to_Coord[buttonPressed][1], Cz + Num_to_Coord[buttonPressed][2])][0] == "block":
                            AmountOfReleasedBoxes += 1
                            PointsRecord[(Cx + Num_to_Coord[buttonPressed][0], Cy + Num_to_Coord[buttonPressed][1], Cz + Num_to_Coord[buttonPressed][2])] = [Check_For_Mines(Cx + Num_to_Coord[buttonPressed][0], Cy + Num_to_Coord[buttonPressed][1], Cz + Num_to_Coord[buttonPressed][2]), 'unmarkable']
                        elif 'cavity' in PointsRecord[(Cx + Num_to_Coord[buttonPressed][0], Cy + Num_to_Coord[buttonPressed][1], Cz + Num_to_Coord[buttonPressed][2])][0]:
                            remove_cavity(PointsRecord[(Cx + Num_to_Coord[buttonPressed][0], Cy + Num_to_Coord[buttonPressed][1], Cz + Num_to_Coord[buttonPressed][2])][0], PointsRecord)


        return redirect(url_for('Minesweeper_play'))
       
 




app.secret_key = 'oetc2802w?ih,i!MkdC>IC.l?<IH'
if __name__ == "__main__":
    app.run(port=4500)

