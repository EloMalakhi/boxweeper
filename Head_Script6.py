
############ Necessary for the skeleton of this script ############
from flask import Flask, session, redirect, render_template, request, abort, escape, url_for
import re
import validate
import define
from saves.CaptionClass import Caption
from saves.PuzzleClass import Puzzle
from saves.SetupClass import Setup
from saves.ConstructClass import Construct
from call import call_html_form
global GameSetup, GamePuzzle, GameStruct, GameCaptions



# presetPuzzleHeight, presetPuzzleLength, presetPuzzleWidth define the total scope of the height, length, and width of the puzzle

# presetViewBoxX, presetViewBoxY, presetViewBoxZ define the viewed scope of the puzzle

# PinkBoxNumber, when the box doesn't have the dimensions 3x3x3 then the center has to be determined otherwise, also it must
# be indicated to the user which box carries the coordinates displayed in the text field, so during unusual presets that
# box will be colored pink

# C1 - C6 are constants calculated before the calling of the web pages and used to assist flask in correctly spacing the buttons in the index html files

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

def Check_For_Mines(PosX, PosY, PosZ, GamePuzzle):
    count = 0
    for i in range(3):
        y = i - 1
        for k in range(3):
            x = k - 1
            for j in range(3):
                z = j - 1
                if GamePuzzle.AllCubes.get((x+PosX, y+PosY, z+PosZ)):
                    if GamePuzzle.AllCubes[(x+PosX, y+PosY, z+PosZ)][0] == "mine closed":
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
    # the request for only a 3 x 3 x 3 box
    GameSetup.EnoughInformation = True
    if request.form.get('v14'):
        # check to see if all the information being received from the preset page is valid
        GameSetup.error, GameSetup.EnoughInformation = validate.presets_of_type_2(request, "")

    if GameSetup.EnoughInformation:
         # if it is then send it to define to calculate the correct data components of the game
        define.Stats(GamePuzzle, GameStruct, GameCaptions, "cubic", request)
        return redirect(url_for('Minesweeper_play'))
    else:
        # otherwise skip back to the preset entering page
        return render_template(GameSetup.PresetFile, error=GameSetup.error)

def D3_Minesweeper_Post1(request):
    # the request for an irregular box
    GameSetup.EnoughInformation = True
    if request.form.get('v14'):
        import validate

        # check to see if all the information being received from the preset page is valid
        GameSetup.error, GameSetup.EnoughInformation = validate.presets_of_type_1(request, "")

    if GameSetup.EnoughInformation:
        # if it is then send it to define to calculate the correct data components of the game
        define.Stats(GamePuzzle, GameStruct, GameCaptions, "exotic", request)
        return redirect(url_for('Minesweeper_play'))
    else:
        # otherwise skip back to the preset entering page
        return render_template(GameSetup.PresetFile, error=GameSetup.error)

app = Flask(__name__)

#  these three lines are the home page of the game
@app.route('/', methods=['GET', 'POST'])
def Modes(): # 18 lines
    global GamePuzzle,  GameStruct, GameCaptions, GameSetup
    """ defines the amount of playable modes
        makes a dictionary attaching the mode number to the necessary web pages
        loops through the modes until 
    """
    modes = 4
    
    if request.method == 'GET':
        return render_template('Modes.html', modes=modes)
    else:
        if request.form.get("open"):
            from saves.puzzle import GamePuzzle as savedPU
            GamePuzzle = savedPU
            from saves.struct import GameStruct  as savedST
            GameStruct = savedST
            from saves.captions import GameCaptions as savedCA
            GameCaptions = savedCA
            from saves.setup import GameSetup as savedSE
            GameSetup = savedSE
            return redirect(url_for('Minesweeper_play'))
        else:
            GamePuzzle = Puzzle()
            GameStruct = Construct()
            GameCaptions = Caption()
            GameSetup = Setup()
            GameSetup.set([{0: "Presets.html", 1: "Presets3.html", 2: "Presets3.html", 3: "Presets3.html"}, 
            {0: "index5.html", 1: "index7.html", 2: "index8.html", 3: "index9.html"}], "", "", "", "", 0)
            for i in range(modes):
                if request.form.get(str(i)):
                    GameSetup.PresetFile = GameSetup.FileMatrix[0][i]
                    GameSetup.mode = i
    return redirect(url_for('D3_Minesweeper'))
            

@app.route('/D3_Minesweeper', methods=['GET', 'POST'])
def D3_Minesweeper(): # 11 lines
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
def Minesweeper_play(): # 92 lines
    if request.method == 'GET':
        if GamePuzzle.death < 3:
            return call_html_form(GameSetup, GameCaptions, GamePuzzle, GameStruct)
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
            import save
            save.saveClasses(GamePuzzle, GameStruct, GameCaptions, GameSetup)
            return redirect(url_for('Minesweeper_play'))
        # elif request.form.get('open'):
        #     from saves.puzzle import GamePuzzle as savedPU
        #     GamePuzzle = savedPU
        #     from saves.struct import GameStruct  as savedST
        #     GameStruct = savedST
        #     from saves.captions import GameCaptions as savedCA
        #     GameCaptions = savedCA
        #     from saves.setup import GameSetup as savedSE
        #     GameSetup = savedSE
        #     return redirect(url_for('Minesweeper_play'))
        
        else:
            GameCaptions.confirmation = ""
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
                            GamePuzzle.AllCubes[(GamePuzzle.usercenter.xv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][0], GamePuzzle.usercenter.yv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][1], GamePuzzle.usercenter.zv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][2])] = [Check_For_Mines(GamePuzzle.usercenter.xv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][0], GamePuzzle.usercenter.yv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][1], GamePuzzle.usercenter.zv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][2], GamePuzzle), 'unmarkable']
                        elif 'cavity' in GamePuzzle.AllCubes[(GamePuzzle.usercenter.xv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][0], GamePuzzle.usercenter.yv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][1], GamePuzzle.usercenter.zv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][2])][0]:
                            remove_cavity(GamePuzzle.AllCubes[(GamePuzzle.usercenter.xv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][0], GamePuzzle.usercenter.yv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][1], GamePuzzle.usercenter.zv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][2])][0], GamePuzzle.AllCubes)


        return redirect(url_for('Minesweeper_play'))
       


app.secret_key = 'oetc2802w?ih,i!MkdC>IC.l?<IH'
if __name__ == "__main__":
    app.run(port=4000)

# 328 lines

