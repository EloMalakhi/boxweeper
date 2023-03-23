


def presets_of_type_1(request, error):
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

    if not request.form.get('v9').isdigit():
        error += "You didn't add a proper number for the viewbox height\n"
        EnoughInformation = False
    elif int(request.form.get('v9')) < 3:
        error += "The viewbox height must be greater than 2\n"
        EnoughInformation = False
    elif int(request.form.get('v3')) and int(request.form.get('v9')) > int(request.form.get('v3')):
        error += "The viewbox height should not be greater than the height of the box"
        EnoughInformation = False
    
    if not request.form.get('v11').isdigit():
        error += "You didn't add a proper number for the viewbox width\n"
        EnoughInformation = False
    elif int(request.form.get('v11')) < 3:
        error += "The viewbox width must be greater than 2\n"
        EnoughInformation = False
    elif int(request.form.get('v1')) and int(request.form.get('v11')) > int(request.form.get('v1')):
        error += "The viewbox width should not be greater than the width of the box"
        EnoughInformation = False

    if not request.form.get('v13').isdigit():
        error += "You didn't add a proper number for the viewbox length\n"
        EnoughInformation = False
    elif int(request.form.get('v13')) < 3:
        error += "The viewbox length must be greater than 2\n"
        EnoughInformation = False
    elif int(request.form.get('v5')) and int(request.form.get('v13')) > int(request.form.get('v5')):
        error += "The viewbox length should not be greater than the length of the box"
        EnoughInformation = False 


    return error, EnoughInformation

def presets_of_type_2(request, error):
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