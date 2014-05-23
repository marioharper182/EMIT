__author__ = 'tonycastronova'


"""
commandline help documentation
"""


def help_function(function):
    """
    returns the help doc for a specific function
    """

    if function == 'save':
        pass
    elif function == 'open':
        pass
    elif function =='add':
        pass
    elif function =='remove':
        pass
    elif function == 'link':
        pass
    elif function == 'display':
        pass
    elif function == 'run':
        pass
    else:
        return '> [error] function "%s" not recognized. ' % function

def info():
    """
    returns software info
    """
    return  '  Environmental Model InTegration (EMIT) Project \n' +\
            '  Released: 7/1/2014 \n' +\
            '  Version: 0.1 \n' +\
            '  Author: Anthony Castronova \n'

def help():
    """
    returns commandline help string
    """
    return  '> Basic Commands \n'+\
            '  help - displays EMIT commands \n' + \
            '  exit - closes the application \n' + \
            '  info - displays EMIT software information \n' +\
            '\n> Advanced Functions \n' +\
            '> (for more function information use the command "help {function name} )" \n'+\
            '  save    - saves model configuration \n'+\
            '  open    - opens existing configuration \n'+\
            '  add     - adds a model to the configuration \n' + \
            '  remove  - removes a model from the configuration \n'+\
            '  link    - creates link between two models \n' +\
            '  display - displays the configuration \n' +\
            '  run     - executes the simulation \n'