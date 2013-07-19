import nuke


def createBackdropSetup():
    nuke.nodes.BackdropNode(bdwidth = 800, bdheight = 400, label = '3dRender&Scans', ) #@UndefinedVariable
    nuke.nodes.BackdropNode(bdwidth = 125, bdheight = 125, label = 'Btys', tile_color = 1000000,) #@UndefinedVariable
    nuke.nodes.BackdropNode(bdwidth = 125, bdheight = 125, label = 'Masks', tile_color = 2000000) #@UndefinedVariable
    nuke.nodes.BackdropNode(bdwidth = 125, bdheight = 125, label = 'Util', tile_color = 5000000) #@UndefinedVariable
    nuke.nodes.BackdropNode(bdwidth = 125, bdheight = 125, label = 'Passes', tile_color = 8000000) #@UndefinedVariable
    nuke.nodes.BackdropNode(bdwidth = 125, bdheight = 125, label = 'MBVectors', tile_color = 10000000) #@UndefinedVariable
    nuke.nodes.BackdropNode(bdwidth = 125, bdheight = 125, label = 'Scans', tile_color = 30000000) #@UndefinedVariable
