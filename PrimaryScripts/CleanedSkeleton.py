from flask import Flask, redirect, render_template, request, url_for, abort, escape, session
import PrimaryScripts.vitals as vitals

import re
import PrimaryScripts.define as define
from AppClasses.CaptionClass import Caption
from AppClasses.PuzzleClass import Puzzle
from AppClasses.SetupClass import Setup
from AppClasses.ConstructClass import Construct
from PrimaryScripts.call import call_html_form

global GameSetup, GamePuzzle, GameStruct, GameCaptions, openError




app = Flask(__name__)




# Home page
@app.route('/', methods=['GET', 'POST'])
def HomePage():
    global GameSetup, GamePuzzle, GameStruct, GameCaptions, openError

    if vitals.user_typed_homepage_url(request):
        return vitals.HomePage2user(render_template)
    
    elif vitals.user_is_choosing_to_walk_into_the_next_room(request):
        if vitals.user_wants_to_open_a_previous_game(request.form):
            
            GamePuzzle, GameStruct, GameCaptions, GameSetup, ToSender, openError = vitals.try_to_open_game_or_fail()
            return ToSender
        
        else:

            GamePuzzle, GameStruct, GameCaptions, GameSetup = vitals.load_undefined_game()
            GameSetup.PresetFile = "Presets.html"

            if vitals.incoming_preset_input(request.form):
            # check to see if all the information being received from the preset page is valid
                GameSetup.error, GameSetup.EnoughInformation = vitals.preset_inspection(request, "")

                if GameSetup.EnoughInformation:
                    # if it is then send it to define to calculate the correct data components of the game
                    define.Stats(GamePuzzle, GameStruct, GameCaptions, request)
                    return redirect(url_for('Minesweeper_play'))
                
        return render_template(GameSetup.PresetFile, error=GameSetup.error)


@app.route('/Minesweeper_play', methods=['GET', 'POST'])
def Minesweeper_play():
    # OUTPUT: type: flask redirect to decorator | flask render_template html_form
    if request.method == 'GET':
        if GamePuzzle.death < 3:
            return call_html_form(GameSetup, GameCaptions, GamePuzzle, GameStruct)
        else:
            return render_template('MinesweeperDeath.html')
    else:
        return vitals.main_decision_base(request.form, GamePuzzle, GameCaptions, GameStruct, GameSetup)


app.secret_key = 'oetc2802w?ih,i!MkdC>IC.l?<IH'
if __name__ == "__main__":
    app.run( port=4200)


