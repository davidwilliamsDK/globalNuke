import nuke

def followReadRange():
    
#===============================================================================
# #    Will set the Scene frame range to that of the selected Node
#===============================================================================
    
    selNode = nuke.selectedNode()
    scene = nuke.root()
    #read range
    
    newStart = selNode.knob('first').getValue()
    newEnd = selNode.knob('last').getValue()
    

    #scene range
    scene.knob('first_frame').setValue(newStart)
    
    scene.knob('last_frame').setValue(newEnd)
    
    