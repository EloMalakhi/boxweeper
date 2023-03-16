
############ Necessary for the skeleton of this script ############
from flask import Flask, session, redirect, render_template, request, abort, escape, url_for
import re
import validate
# the globalization of these variables is to deter the creation of a new variable for the same purpose every function call
TheMasterList = []
global presetPuzzleHeight, presetPuzzleLength, presetPuzzleWidth, presetPuzzleMines, Cx, Cy, Cz, MineHitter
global presetViewBoxX, presetViewBoxY, presetViewBoxZ,  GPx, GPy, GPz, LPx, LPy, LPz, PinkBoxNumber
global C1, C2, C3, C4, C5, C6, WidthOfButton, HeightOfButton, FS, LabeledBoxes, AmountOfReleasedBoxes
global Confirmation, TotalB, PRESETFILE, error, mode, IndexFiles, Num_to_Coord, hoverover_elementtags, hoverover_texttags







def check_for_direction(Cx, Cy, Cz):
    global GPx, GPy, GPz, LPx, LPy, LPz
    List = {}
    count = -1
    if Cx > LPx:
        count += 1
        List[count] = ['/static/Left.png', 'left']
    if Cx < GPx:
        count += 1
        List[count] = ['/static/Right.png', 'right']
    if Cy > LPy:
        count += 1
        List[count] = ['/static/Down.png', 'down']
    if Cy < GPy:
        count += 1
        List[count] = ['/static/Up.png', 'up']
    if Cz > LPz:
        count += 1
        List[count] = ['/static/Backward.png', 'backward']
    if Cz < GPz:
        count += 1
        List[count] = ['/static/Forward.png', 'forward']
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
    global presetPuzzleHeight, presetPuzzleLength, presetPuzzleWidth, presetPuzzleMines, Cx, Cy, Cz, MineHitter
    global presetViewBoxX, presetViewBoxY, presetViewBoxZ,  GPx, GPy, GPz, LPx, LPy, LPz, PinkBoxNumber
    global C1, C2, C3, C4, C5, C6, WidthOfButton, HeightOfButton, FS, LabeledBoxes, AmountOfReleasedBoxes, hoverover_texttags
    global Confirmation, TotalB, PRESETFILE, hoverover_elementtags, Num_to_Coord, PinkBoxNumber
    EnoughInformation = True
    if request.form.get('v14'):
        error, EnoughInformation = validate.presets_of_type_2(request, "")

    if EnoughInformation:
        global presetPuzzleHeight, presetPuzzleWidth, presetPuzzleLength, presetPuzzleMines
        presetPuzzleWidth = int(request.form.get('v1'))
        presetPuzzleHeight = int(request.form.get('v3'))
        presetPuzzleLength = int(request.form.get('v5'))
        presetPuzzleMines = int(request.form.get('v7'))
        presetViewBoxY = 3
        presetViewBoxX = 3
        presetViewBoxZ = 3
        MineHitter = 0
        AmountOfReleasedBoxes = 1
        Confirmation = ""
        TotalB = presetPuzzleHeight*presetPuzzleLength*presetPuzzleWidth

        C1 = 34 - 12/presetViewBoxZ - 12/presetViewBoxX - 12/(presetViewBoxX - 1)
        C2 = 12/presetViewBoxZ
        C3 = 12/presetViewBoxX + 12/(presetViewBoxX - 1)
        C4 = 56 + 24/presetViewBoxY + 24/(presetViewBoxY - 1)
        C5 = 24/presetViewBoxY
        C6 = -24/presetViewBoxY - 24/(presetViewBoxY - 1)

        #C1 = 34 - (1/(presetViewBoxZ - 1) + 1/(presetViewBoxX - 1))*(24 - 12/presetViewBoxX)

        WidthOfButton = 12/presetViewBoxX
        HeightOfButton = 24/presetViewBoxY
        FS = (60/(presetViewBoxX*presetViewBoxY*presetViewBoxZ)**(1/3))
        # define the center of the displayed cube:
        GPx = presetPuzzleWidth - 2
        GPy = presetPuzzleHeight - 2
        GPz = presetPuzzleLength - 2
        LPx  = presetViewBoxX - 2
        LPy  = presetViewBoxY - 2
        LPz  = presetViewBoxZ - 2
        Cx = GPx
        Cy = GPy
        Cz = GPz
        LabeledBoxes = 0
        PinkBoxNumber  = (presetViewBoxY - 2)*presetViewBoxX*presetViewBoxZ + (presetViewBoxX - 2)*presetViewBoxZ + (presetViewBoxZ - 1)
        # the globalization is used to make one data instance for memory purposes
        global hoverover_elementtags, hoverover_texttags, Num_to_Coord
        # and set the type of  these:
        hoverover_elementtags = {}
        hoverover_texttags = {}
        Num_to_Coord = {}

        # get the Large Cube that is the game
        global PointsRecord
        import test4
        PointsRecord = test4.MakeSweeperGame(presetPuzzleHeight, presetPuzzleWidth, presetPuzzleLength, presetPuzzleMines)

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
        for i in range(presetViewBoxY):
            for j in range(presetViewBoxX):
                for k in range(presetViewBoxZ):
                    # dwmio = do when mouse is over
                    hoverover_elementtags[i*presetViewBoxX*presetViewBoxZ + j*presetViewBoxZ + k + 1] = 'dwmio' + str(i*presetViewBoxX*presetViewBoxZ + j*presetViewBoxZ + k)
                    # posie is short for position
                    hoverover_texttags[i*presetViewBoxX*presetViewBoxZ + j*presetViewBoxZ + k + 1] = 'posie' + str(i*presetViewBoxX*presetViewBoxZ + j*presetViewBoxZ + k)
                    # while running through these numbers it makes a hash to convert from number to coordinate
                    Num_to_Coord[i*presetViewBoxX*presetViewBoxZ + j*presetViewBoxZ + k + 1] = [j + 2 - presetViewBoxX, i + 2 - presetViewBoxY, k + 2 - presetViewBoxZ]
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
    
    global presetPuzzleHeight, presetPuzzleLength, presetPuzzleWidth, presetPuzzleMines, Cx, Cy, Cz, MineHitter
    global presetViewBoxX, presetViewBoxY, presetViewBoxZ,  GPx, GPy, GPz, LPx, LPy, LPz, PinkBoxNumber
    global C1, C2, C3, C4, C5, C6, WidthOfButton, HeightOfButton, FS, LabeledBoxes, AmountOfReleasedBoxes
    global Confirmation, TotalB, Num_to_Coord, hoverover_elementtags, hoverover_texttags, PinkBoxNumber

    EnoughInformation = True
    if request.form.get('v14'):
        import validate
        error, EnoughInformation = validate.presets_of_type_1(request, "")

    if EnoughInformation:
        global presetPuzzleHeight, presetPuzzleWidth, presetPuzzleLength, presetPuzzleMines
        presetPuzzleWidth = int(request.form.get('v1'))
        presetPuzzleHeight = int(request.form.get('v3'))
        presetPuzzleLength = int(request.form.get('v5'))
        presetPuzzleMines = int(request.form.get('v7'))
        presetViewBoxY = int(request.form.get('v9'))
        presetViewBoxX = int(request.form.get('v11'))
        presetViewBoxZ = int(request.form.get('v13'))
        MineHitter = 0
        AmountOfReleasedBoxes = 1
        Confirmation = ""
        TotalB = presetPuzzleHeight*presetPuzzleLength*presetPuzzleWidth

        C1 = 34 - 12/presetViewBoxZ - 12/presetViewBoxX - 12/(presetViewBoxX - 1)
        C2 = 12/presetViewBoxZ
        C3 = 12/presetViewBoxX + 12/(presetViewBoxX - 1)
        C4 = 56 + 24/presetViewBoxY + 24/(presetViewBoxY - 1)
        C5 = 24/presetViewBoxY
        C6 = -24/presetViewBoxY - 24/(presetViewBoxY - 1)

        #C1 = 34 - (1/(presetViewBoxZ - 1) + 1/(presetViewBoxX - 1))*(24 - 12/presetViewBoxX)

        WidthOfButton = 12/presetViewBoxX
        HeightOfButton = 24/presetViewBoxY
        FS = (60/(presetViewBoxX*presetViewBoxY*presetViewBoxZ)**(1/3))
        # define the center of the displayed cube:
        GPx = presetPuzzleWidth - 2
        GPy = presetPuzzleHeight - 2
        GPz = presetPuzzleLength - 2
        LPx  = presetViewBoxX - 2
        LPy  = presetViewBoxY - 2
        LPz  = presetViewBoxZ - 2
        Cx = GPx
        Cy = GPy
        Cz = GPz
        LabeledBoxes = 0
        PinkBoxNumber  = (presetViewBoxY - 2)*presetViewBoxX*presetViewBoxZ + (presetViewBoxX - 2)*presetViewBoxZ + (presetViewBoxZ - 1)
        # the globalization is used to make one data instance for memory purposes
        global hoverover_elementtags, hoverover_texttags, Num_to_Coord
        # and set the type of  these:
        hoverover_elementtags = {}
        hoverover_texttags = {}
        Num_to_Coord = {}

        # get the Large Cube that is the game
        global PointsRecord
        import test4
        PointsRecord = test4.MakeSweeperGame(presetPuzzleHeight, presetPuzzleWidth, presetPuzzleLength, presetPuzzleMines)

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
        for i in range(presetViewBoxY):
            for j in range(presetViewBoxX):
                for k in range(presetViewBoxZ):
                    # dwmio = do when mouse is over
                    hoverover_elementtags[i*presetViewBoxX*presetViewBoxZ + j*presetViewBoxZ + k + 1] = 'dwmio' + str(i*presetViewBoxX*presetViewBoxZ + j*presetViewBoxZ + k)
                    # posie is short for position
                    hoverover_texttags[i*presetViewBoxX*presetViewBoxZ + j*presetViewBoxZ + k + 1] = 'posie' + str(i*presetViewBoxX*presetViewBoxZ + j*presetViewBoxZ + k)
                    # while running through these numbers it makes a hash to convert from number to coordinate
                    Num_to_Coord[i*presetViewBoxX*presetViewBoxZ + j*presetViewBoxZ + k + 1] = [j + 2 - presetViewBoxX, i + 2 - presetViewBoxY, k + 2 - presetViewBoxZ]
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
    global presetViewBoxX, presetViewBoxY, presetViewBoxZ
    global C1, C2, C3, C4, C5, C6, WidthOfButton, HeightOfButton
    global LabeledBoxes, AmountOfReleasedBoxes, Confirmation
    global PointsRecord, presetPuzzleMines, presetPuzzleHeight
    global presetPuzzleLength, presetPuzzleWidth, mode, IndexFiles
    global Num_to_Coord, hoverover_elementtags, hoverover_texttags
    global PinkBoxNumber
    print(IndexFiles[mode])
    if request.method == 'GET':
        if MineHitter < 3:
            return render_template(IndexFiles[mode],
            hoverover_elementtags=hoverover_elementtags,
            xX = presetPuzzleLength, yY = presetPuzzleHeight, zZ = presetPuzzleWidth,
            hoverover_texttags=hoverover_texttags, TB=TotalB,
            Num_to_Coord=Num_to_Coord, x=Cx, y=Cy, z=Cz, FS=FS, Strikes=MineHitter,
            MineHitter=MineHitter, px=presetViewBoxX, py=presetViewBoxY, pz=presetViewBoxZ,
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
            savefile.write("presetPuzzleHeight = " + str(presetPuzzleHeight) + "\n")
            savefile.write("presetPuzzleLength = " + str(presetPuzzleLength) + "\n")
            savefile.write("presetPuzzleWidth = " + str(presetPuzzleWidth) + "\n")
            savefile.write("presetPuzzleMines = " + str(presetPuzzleMines) + "\n")
            savefile.write("presetViewBoxX = " + str(presetViewBoxX) + "\n")
            savefile.write("presetViewBoxY = " + str(presetViewBoxY) + "\n")
            savefile.write("presetViewBoxZ = " + str(presetViewBoxZ) + "\n")
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
            from savefile import presetPuzzleHeight, presetPuzzleWidth,  presetPuzzleLength, presetViewBoxX, presetViewBoxY,  presetViewBoxZ, presetPuzzleMines,  MineHitter
            from savefile import AmountOfReleasedBoxes, TotalB, LabeledBoxes, Num_to_Coord, Cx, Cy, Cz, hoverover_elementtags, hoverover_texttags
            from savefile import PinkBoxNumber, WidthOfButton, HeightOfButton
            return redirect(url_for('Minesweeper_play'))
        else:
            Confirmation = ""
            print("6")
            print(request.form)
            for i in range(presetViewBoxX * presetViewBoxY * presetViewBoxZ):
                buttonPressed = i + 1
                if request.form.get(str(i+1)):
                    print("7")
                    if PointsRecord[(Cx + Num_to_Coord[buttonPressed][0], Cy + Num_to_Coord[buttonPressed][1], Cz + Num_to_Coord[buttonPressed][2])][1] == 'markable' and request.form.get(str(i+1)) == "  ":
                        print("1")
                        LabeledBoxes += 1
                        PointsRecord[(Cx + Num_to_Coord[buttonPressed][0], Cy + Num_to_Coord[buttonPressed][1], Cz + Num_to_Coord[buttonPressed][2])][1] = 'marked'
                    elif PointsRecord[(Cx + Num_to_Coord[buttonPressed][0], Cy + Num_to_Coord[buttonPressed][1], Cz + Num_to_Coord[buttonPressed][2])][1] == 'marked' and request.form.get(str(i+1)) == " ":
                        print("2")
                        LabeledBoxes -= 1
                        PointsRecord[(Cx + Num_to_Coord[buttonPressed][0], Cy + Num_to_Coord[buttonPressed][1], Cz + Num_to_Coord[buttonPressed][2])][1] = 'markable'
                    elif PointsRecord[(Cx + Num_to_Coord[buttonPressed][0], Cy + Num_to_Coord[buttonPressed][1], Cz + Num_to_Coord[buttonPressed][2])][1] == 'markable' and request.form.get(str(i+1)) == " ":
                        if PointsRecord[(Cx + Num_to_Coord[buttonPressed][0], Cy + Num_to_Coord[buttonPressed][1], Cz + Num_to_Coord[buttonPressed][2])][0] == "mine closed":
                            print("  3")
                            MineHitter += 1
                        elif PointsRecord[(Cx + Num_to_Coord[buttonPressed][0], Cy + Num_to_Coord[buttonPressed][1], Cz + Num_to_Coord[buttonPressed][2])][0] == "block":
                            print("  4")
                            AmountOfReleasedBoxes += 1
                            PointsRecord[(Cx + Num_to_Coord[buttonPressed][0], Cy + Num_to_Coord[buttonPressed][1], Cz + Num_to_Coord[buttonPressed][2])] = [Check_For_Mines(Cx + Num_to_Coord[buttonPressed][0], Cy + Num_to_Coord[buttonPressed][1], Cz + Num_to_Coord[buttonPressed][2]), 'unmarkable']
                        elif 'cavity' in PointsRecord[(Cx + Num_to_Coord[buttonPressed][0], Cy + Num_to_Coord[buttonPressed][1], Cz + Num_to_Coord[buttonPressed][2])][0]:
                            print("  5")
                            remove_cavity(PointsRecord[(Cx + Num_to_Coord[buttonPressed][0], Cy + Num_to_Coord[buttonPressed][1], Cz + Num_to_Coord[buttonPressed][2])][0], PointsRecord)


        return redirect(url_for('Minesweeper_play'))
       
 




app.secret_key = 'oetc2802w?ih,i!MkdC>IC.l?<IH'
if __name__ == "__main__":
    app.run(port=4500)

