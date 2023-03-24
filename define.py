from data_methods import *


def Stats(Puzzle, Struct, Captions, caller, request):
    # INPUTS (in sequential order):
    # Puzzle: class: structure is found in saves/PuzzleClass.py
    # Struct: class: structure is found in saves/ConstructClass.py
    # Captions: class: structure is found in saves/CaptionClass.py
    # caller: "exotic" | "cubic", 'exotic' means it carries different dimensions than 3 by 3 by 3
    #                             'cubic' means it carries dimensions 3 by 3 by 3

    Puzzle.total.set(int(request.form.get('v1')), int(request.form.get('v3')), int(request.form.get('v5')))

    if caller == "exotic":
        Puzzle.view.set(int(request.form.get('v9')), int(request.form.get('v11')), int(request.form.get('v13')))
    elif caller == "cubic":
        Puzzle.view.set(3, 3, 3)

    Captions.confirmation = ""

    Puzzle.death = 0

    Struct.x.set(
        34 - 12/Puzzle.view.zv - 12/Puzzle.view.xv - 12/(Puzzle.view.xv - 1),
        12/Puzzle.view.zv,
        12/Puzzle.view.xv + 12/(Puzzle.view.xv - 1),
        Puzzle.view.xv
        )
    
    Struct.y.set(
        56 + 24/Puzzle.view.yv + 24/(Puzzle.view.yv - 1),
        24/Puzzle.view.yv,
        -24/Puzzle.view.yv - 24/(Puzzle.view.yv - 1),
        Puzzle.view.yv/2)
    
    Struct.font_size = (60/(Puzzle.view.xy*Puzzle.view.zv)**(1/3))

    Puzzle.centerGLim.set(Puzzle.total.xv - 2, Puzzle.total.yv - 2, Puzzle.total.zv - 2)
    Puzzle.centerLLim.set(Puzzle.view.xv - 2, Puzzle.view.yv - 2, Puzzle.view.zv - 2)
    Puzzle.usercenter.set(Puzzle.total.xv - 2, Puzzle.total.yv - 2, Puzzle.total.zv - 2)

    Puzzle.pinkboxnumber  = (Puzzle.view.yv - 2)*Puzzle.view.xz + Puzzle.centerLLim.xv*Puzzle.view.zv + (Puzzle.view.zv - 1)
    
    Captions.hoveroverelement = {}

    Captions.hoverovertext = {}


    
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

    # make the hover feature tags
    for i in range(Puzzle.view.yv):
        for j in range(Puzzle.view.xv):
            for k in range(Puzzle.view.zv):
                # dwmio = do when mouse is over
                Captions.hoveroverelement[i*Puzzle.view.xz + j*Puzzle.view.zv + k + 1] = 'dwmio' + str(i*Puzzle.view.xz + j*Puzzle.view.zv + k)
                # posie is short for position
                Captions.hoverovertext[i*Puzzle.view.xz + j*Puzzle.view.zv + k + 1] = 'posie' + str(i*Puzzle.view.xz + j*Puzzle.view.zv + k)
                # while running through these numbers it makes a hash to convert from number to coordinate
                Puzzle.ViewCubeCoordTranslate[i*Puzzle.view.xz + j*Puzzle.view.zv + k + 1] = [j + 2 - Puzzle.view.xv, i + 2 - Puzzle.view.yv, k + 2 - Puzzle.view.zv]

    # find the cube to become the starting point
    defineStats_bymethod(Puzzle, request)

