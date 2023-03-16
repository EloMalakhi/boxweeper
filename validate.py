def presets_of_type_1(request, error):
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
    elif not int(request.form.get('v9')) > 2:
        error += "The viewbox height must be greater than 2\n"
        EnoughInformation = False
    
    if not request.form.get('v11').isdigit():
        error += "You didn't add a proper number for the viewbox width\n"
        EnoughInformation = False
    elif not int(request.form.get('v11')) > 2:
        error += "The viewbox width must be greater than 2\n"
        EnoughInformation = False

    if not request.form.get('v13').isdigit():
        error += "You didn't add a proper number for the viewbox length\n"
        EnoughInformation = False
    elif not int(request.form.get('v13')) > 2:
        error += "The viewbox length must be greater than 2\n"
        EnoughInformation = False
    return error, EnoughInformation

def presets_of_type_2(request, error):
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