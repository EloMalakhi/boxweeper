from flask import render_template
from LowerLevel.data_methods import call_bymethod

def check_for_direction(Cx, Cy, Cz, GamePuzzle):
    # INPUT in sequential order:
    # Cx: integer: the x location of the center of the view
    # Cy: integer: the y location of the center of the view
    # Cz: integer: the z location of the center of the view
    # GamePuzzle: class: structure found in saves/PuzzleClass.py
    
    # OUTPUT:
    # List: type List: has the list of possible directions user can move

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

def call_html_form(GameSetup, GameCaptions, GamePuzzle, GameStruct):
    # INPUTS (in sequential order):
    # GameSetup: class: structure is found in saves/SetupClass.py
    # GameCaptions: class: structure is found in saves/CaptionClass.py
    # GamePuzzle: class: structure is found in saves/PuzzleClass.py
    # GameStruct: class: structure is found in saves/ConstructClass.py

    # OUTPUT:
    # a flask render_template of GameSetup.FileMatrix[1][GameSetup.mode] (the Game Content File) with all the parameters called by that html form
    Quadruple = call_bymethod(GamePuzzle)
    return render_template("index.html",
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
            Available_directions=check_for_direction(GamePuzzle.usercenter.xv, GamePuzzle.usercenter.yv, GamePuzzle.usercenter.zv, GamePuzzle),
            Pink=GamePuzzle.pinkboxnumber, 
            amount_of_directions=len(check_for_direction(GamePuzzle.usercenter.xv, GamePuzzle.usercenter.yv, GamePuzzle.usercenter.zv, GamePuzzle)),
            c1=GameStruct.x.base, c2=GameStruct.x.Zchange, c3=GameStruct.x.self_change, c4=GameStruct.y.base, c5=GameStruct.y.Zchange, c6=GameStruct.y.self_change,
            wob=GameStruct.x.ob, hob=GameStruct.y.ob,
            CF=GameCaptions.confirmation,
            MM=Quadruple[0], 
            LL=Quadruple[1], 
            RB=Quadruple[2],
            PointsRecord = Quadruple[3])