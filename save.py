import time
import data_methods


def saveClasses(GamePuzzle, GameStruct, GameCaptions, GameSetup):
    # INPUTS (in sequential order):
    # GamePuzzle: class: structure is found in saves/PuzzleClass.py
    # GameStruct: class: structure is found in saves/ConstructClass.py
    # GameCaptions: class: structure is found in saves/CaptionClass.py
    # GameSetup: class: structure is found in saves/SetupClass.py
    PuzzleClass(GamePuzzle)
    StructClass(GameStruct)
    CaptionsClass(GameCaptions)
    SetupClass(GameSetup)

def PuzzleClass(GamePuzzle):
    # INPUTS (in sequential order):
    # GamePuzzle: class: structure is found in saves/PuzzleClass.py
    h1 = open('saves/puzzle.py', 'w')
    h1.write("from saves.PuzzleClass import *\n")
    h1.write("GamePuzzle = Puzzle()\n")
    h1.write(f"GamePuzzle.total.set({GamePuzzle.total.xv}, {GamePuzzle.total.yv}, {GamePuzzle.total.zv})\n")
    h1.write(f"GamePuzzle.view.set({GamePuzzle.view.xv}, {GamePuzzle.view.yv}, {GamePuzzle.view.zv})\n")
    h1.write(f"GamePuzzle.usercenter.set({GamePuzzle.usercenter.xv}, {GamePuzzle.usercenter.yv}, {GamePuzzle.usercenter.zv})\n")
    h1.write(f"GamePuzzle.centerGLim.set({GamePuzzle.centerGLim.xv}, {GamePuzzle.centerGLim.yv}, {GamePuzzle.centerGLim.zv})\n")
    h1.write(f"GamePuzzle.centerLLim.set({GamePuzzle.centerLLim.xv}, {GamePuzzle.centerLLim.yv}, {GamePuzzle.centerLLim.zv})\n")
    h1.write(f"GamePuzzle.death = {GamePuzzle.death}\n")
    h1.close()
    time.sleep(.2)
    data_methods.FinishWriting(GamePuzzle)

def StructClass(GameStruct):
    # INPUTS (in sequential order):
    # GameStruct: class: structure is found in saves/ConstructClass.py
    h2 = open('saves/struct.py', 'w')
    h2.write("from saves.ConstructClass import *\n")
    h2.write('GameStruct = Construct()\n')
    h2.write(f'GameStruct.x.set({GameStruct.x.base}, {GameStruct.x.Zchange}, {GameStruct.x.self_change}, {12/GameStruct.x.ob})\n')
    h2.write(f'GameStruct.y.set({GameStruct.y.base}, {GameStruct.y.Zchange}, {GameStruct.y.self_change}, {12/GameStruct.y.ob})')
    h2.close()


def CaptionsClass(GameCaptions):
    # INPUTS (in sequential order):
    # GameCaptions: class: structure is found in saves/CaptionClass.py
    h3 = open('saves/captions.py', 'w')
    h3.write("from saves.CaptionClass import *\n")
    h3.write("GameCaptions = Caption()\n")
    h3.write(f"GameCaptions.hoveroverelement, GameCaptions.hoverovertext, GameCaptions.confirmation = {GameCaptions.hoveroverelement}, {GameCaptions.hoverovertext}, '{GameCaptions.confirmation}'\n")
    h3.close()


def SetupClass(GameSetup):
    # INPUTS (in sequential order):
    # GameSetup: class: structure is found in saves/SetupClass.py
    h4 = open('saves/setup.py', 'w')
    h4.write('from saves.SetupClass import *\n')
    h4.write("GameSetup = Setup()\n")
    h4.write(f'GameSetup.set({str(GameSetup.FileMatrix)}, "{GameSetup.error}", {GameSetup.EnoughInformation}, "{GameSetup.PresetFile}", "{GameSetup.indexFile}", {GameSetup.mode})\n')
    h4.close()

