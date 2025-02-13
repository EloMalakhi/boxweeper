from flask import Flask, session, redirect, url_for, request, abort, escape, render_template
from AppClasses.CaptionClass import Caption
from AppClasses.PuzzleClass import Puzzle
from AppClasses.ConstructClass import Construct
from AppClasses.SetupClass import Setup
import LowerLevel.data_methods as data_methods
import re



# Metaphorical Organs
def try_to_open_game_or_fail():
    try:
        from saves.puzzle import GamePuzzle
        from saves.struct import GameStruct
        from saves.captions import GameCaptions
        from saves.setup import GameSetup
        openError = ""
        return GamePuzzle, GameStruct, GameCaptions, GameSetup, redirect(url_for('Minesweeper_play')), openError
    except:
        openError = "One of these files don't have the necessary classes\nto fix that adjustment correct the class in that file or start a new game and save it"
        return GamePuzzle, GameStruct, GameCaptions, GameSetup, redirect(url_for('HomePage')), openError
    
def load_undefined_game():
    return Puzzle(), Construct(), Caption(), Setup()

def preset_inspection(request, error):
#   INPUTS (in sequential order):
#   request = flask processing an html form and giving a html form request  
#   error is an empty string
#
#   OUTPUTS (in sequential order):
#   error: a string that is either "" or a set of lines noting what invalid information was given in the html form
#   EnoughInformation = True if error == "" (hence no invalid data given) or False if invalid data was given  
    
    EnoughInformation = True
    if not request.form.get('v1').isdigit():
        error += "You didn't add a proper number for the width\n"
        EnoughInformation = False
    elif not int(request.form.get('v1')) > 2:
        error += "The width must be greater than 2\n"
        EnoughInformation = False

    if not request.form.get('v3').isdigit():
        error += "You didn't add a proper number for the height\n"
        EnoughInformation = False
    elif not int(request.form.get('v3')) > 2:
        error += "The height must be greater than 2\n"
        EnoughInformation = False

    if not request.form.get('v5').isdigit():
        error += "You didn't add a proper number for the length\n"
        EnoughInformation = False
    elif not int(request.form.get('v5')) > 2:
        error += "The length must be greater than 2\n"
        EnoughInformation = False
    
    if not request.form.get('v7').isdigit():
        error += "You didn't add a proper number for the number of mines\n"
        EnoughInformation = False
    return error, EnoughInformation

def check_in_bounds(x, y, z, GamePuzzle):

    if isinstance(x, int) and isinstance(y, int) and isinstance(z, int):
        if int(x) <= GamePuzzle.centerGLim.xv and int(x) >= GamePuzzle.centerLLim.xv:
            if int(y) <= GamePuzzle.centerGLim.yv and int(y) >= GamePuzzle.centerLLim.yv:
                if int(z) <= GamePuzzle.centerGLim.zv and int(z) >= GamePuzzle.centerLLim.zv:
                    return True
    return False

def main_decision_base(requestform, GamePuzzle, GameCaptions, GameStruct, GameSetup):
    # go through the squares and see which ones have a value of 1 or 2 spaces to indicate labelness

        if requestform.get('up'):
            GamePuzzle.usercenter.yv += 1
        elif requestform.get('down'):
            GamePuzzle.usercenter.yv -= 1
        elif requestform.get('left'):
            GamePuzzle.usercenter.xv -= 1
        elif requestform.get('right'):
            GamePuzzle.usercenter.xv += 1
        elif requestform.get('forward'):
            GamePuzzle.usercenter.zv += 1
        elif requestform.get('backward'):
            GamePuzzle.usercenter.zv -= 1
        elif requestform.get('position'):
            position = requestform.get('positionString')
            position = re.sub("\s+", " ", position)
            if len(position.split(' ')) == 3 and check_in_bounds(position.split(' ')[0], position.split(' ')[1], position.split(' ')[2], GamePuzzle): 
                List = position.split(' ')
                GamePuzzle.usercenter.xv = int(List[0])
                GamePuzzle.usercenter.yv = int(List[1])
                GamePuzzle.usercenter.zv = int(List[2])
        elif request.form.get('CM'):
            if data_methods.PossiblyFound(GamePuzzle):
                if data_methods.ValidateLabels(GamePuzzle):
                    GameCaptions.confirmation = "You got all of them, you win!"
                    return redirect(url_for('Minesweeper_play'))
                else:
                    GameCaptions.confirmation = "You didn't get all of them yet, keep trying!"
                    return redirect(url_for('Minesweeper_play'))
            else:
                GameCaptions.confirmation = "You didn't get all of them yet, keep trying!"
                return redirect(url_for('Minesweeper_play'))
        elif request.form.get('save'):
            import PrimaryScripts.save as save
            save.saveClasses(GamePuzzle, GameStruct, GameCaptions, GameSetup)
            return redirect(url_for('Minesweeper_play'))

        
        else:
            GameCaptions.confirmation = ""
            for i in range(GamePuzzle.view.xy*GamePuzzle.view.zv):
                buttonPressed = i + 1
                if request.form.get(str(i+1)):
                    data_methods.process_request(GamePuzzle, request, buttonPressed)

        return redirect(url_for('Minesweeper_play'))





# Conditionals
def user_typed_homepage_url(param):
    return (param.method == 'GET')

def user_is_choosing_to_walk_into_the_next_room(request):
    return (request.method == 'POST')

def user_wants_to_open_a_previous_game(requestform):
    return requestform.get('open')

def incoming_preset_input(requestform):
    return requestform.get('v14')



# If_then_logic
def HomePage2user(param):
    return param('Presets.html')