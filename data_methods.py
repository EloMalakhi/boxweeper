def remove_cavity(Cavity_for_removal, PointsRecord, GamePuzzle):
    # INPUT: (in order):
    # Cavity_for_removal: str: the name of the cavity that was discovered
    # Points_Record: 
    # #           {(x: int, y: int, z: int): [description_of_box: str, mark_status: str],
# #                (x: int, y: int, z: int): [description_of_box: str, mark_status: str],
# #                (x: int, y: int, z: int): [description_of_box: str, mark_status: str],
#                  (x: int, y: int, z: int): [description_of_box: str, mark_status: str], etc} # all the keys corresponding to all the points

    # goes through all the points and looks for cavities marked by the uncovered cavity and then removes them
    for i in PointsRecord:
        if PointsRecord[i][0] == Cavity_for_removal:
            PointsRecord[i] = [" ", "unmarkable"]
            GamePuzzle.boxes.open += 1


def Check_For_Mines(PosX, PosY, PosZ, GamePuzzle):
    # INPUT (in sequential order):
    # PosX: int: the x of the 3D location in question
    # PosY: int: the y of the 3D location in question
    # PosZ: int: the z of the 3D location in question
#     GamePuzzle: class: structure is found in saves/PuzzleClass.py

#   OUTPUT:
#       count: int: the amount of mines found around the 3D location
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

def ValidateLabels(GamePuzzle):
    # INPUT: GamePuzzle: class: see saves/PuzzleClass.py for structure of class
    # checks to see if all the mines have been marked if so returns True, otherwise returns False
    for i in GamePuzzle.AllCubes:
        if GamePuzzle.AllCubes[i][0] == "mine closed" and GamePuzzle.AllCubes[i][1] == "marked":
            GamePuzzle.boxes.unfound_mines -= 1
    if GamePuzzle.boxes.unfound_mines == 0:
        return True
    else:
        return False
    
def process_request(GamePuzzle, request, buttonPressed):
    if GamePuzzle.AllCubes[(GamePuzzle.usercenter.xv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][0], GamePuzzle.usercenter.yv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][1], GamePuzzle.usercenter.zv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][2])][1] == 'markable' and request.form.get(str(buttonPressed)) == "  ":
        GamePuzzle.boxes.guessed += 1
        GamePuzzle.AllCubes[(GamePuzzle.usercenter.xv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][0], GamePuzzle.usercenter.yv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][1], GamePuzzle.usercenter.zv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][2])][1] = 'marked'
    elif GamePuzzle.AllCubes[(GamePuzzle.usercenter.xv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][0], GamePuzzle.usercenter.yv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][1], GamePuzzle.usercenter.zv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][2])][1] == 'marked' and request.form.get(str(buttonPressed)) == " ":
        GamePuzzle.boxes.guessed -= 1
        GamePuzzle.AllCubes[(GamePuzzle.usercenter.xv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][0], GamePuzzle.usercenter.yv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][1], GamePuzzle.usercenter.zv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][2])][1] = 'markable'
    elif GamePuzzle.AllCubes[(GamePuzzle.usercenter.xv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][0], GamePuzzle.usercenter.yv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][1], GamePuzzle.usercenter.zv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][2])][1] == 'markable' and request.form.get(str(buttonPressed)) == " ":
        if GamePuzzle.AllCubes[(GamePuzzle.usercenter.xv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][0], GamePuzzle.usercenter.yv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][1], GamePuzzle.usercenter.zv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][2])][0] == "mine closed":
            GamePuzzle.death += 1
        elif GamePuzzle.AllCubes[(GamePuzzle.usercenter.xv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][0], GamePuzzle.usercenter.yv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][1], GamePuzzle.usercenter.zv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][2])][0] == "block":
            GamePuzzle.boxes.open += 1
            GamePuzzle.AllCubes[(GamePuzzle.usercenter.xv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][0], GamePuzzle.usercenter.yv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][1], GamePuzzle.usercenter.zv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][2])] = [Check_For_Mines(GamePuzzle.usercenter.xv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][0], GamePuzzle.usercenter.yv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][1], GamePuzzle.usercenter.zv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][2], GamePuzzle), 'unmarkable']
        elif 'cavity' in GamePuzzle.AllCubes[(GamePuzzle.usercenter.xv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][0], GamePuzzle.usercenter.yv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][1], GamePuzzle.usercenter.zv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][2])][0]:
            remove_cavity(GamePuzzle.AllCubes[(GamePuzzle.usercenter.xv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][0], GamePuzzle.usercenter.yv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][1], GamePuzzle.usercenter.zv + GamePuzzle.ViewCubeCoordTranslate[buttonPressed][2])][0], GamePuzzle.AllCubes)

def PossiblyFound(GamePuzzle):
    if GamePuzzle.boxes.guessed == GamePuzzle.boxes.unfound_mines:
        return True
    else:
        return False
    

def FinishWriting(GamePuzzle):
    h5 = open('saves/puzzle.py', 'a')
    h5.write(f"GamePuzzle.AllCubes, GamePuzzle.ViewCubeCoordTranslate, GamePuzzle.pinkboxnumber = {str(GamePuzzle.AllCubes)}, {str(GamePuzzle.ViewCubeCoordTranslate)}, {str(GamePuzzle.pinkboxnumber)}\n")
    h5.write(f"GamePuzzle.boxes.set({GamePuzzle.boxes.open}, {GamePuzzle.boxes.closed}, {GamePuzzle.boxes.unfound_mines}, {GamePuzzle.boxes.guessed})\n")
    h5.close()


def defineStats_bymethod(Puzzle, request):
    Puzzle.boxes.set(1, Puzzle.total.xy*Puzzle.total.zv - int(request.form.get('v7')), int(request.form.get('v7')), 0)
    Puzzle.boxes.guessed = 0
    import test4
    Puzzle.AllCubes = test4.MakeSweeperGame(Puzzle.total.yv, Puzzle.total.xv, Puzzle.total.zv, Puzzle.boxes.unfound_mines)
    NoZero = True
    while NoZero:
        for i in Puzzle.AllCubes:
            if Check_For_Mines(i[0], i[1], i[2], Puzzle) == 0:
                NoZero = False
                Puzzle.AllCubes[i][1] = "unmarkable"
                Puzzle.AllCubes[i][0] = "0"
                tryX, tryY, tryZ = i[0], i[1], i[2]
                break

def call_bymethod(Puzzle):
    # test4 will need adjusted for every data method
    # also PuzzleClass will need adjusted
    return Puzzle.boxes.unfound_mines, Puzzle.boxes.guessed, Puzzle.boxes.open, Puzzle.AllCubes