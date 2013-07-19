import nuke

def reloadAllReads():
    [i.knob('reload').execute() for i in nuke.allNodes() if i.Class()=='Read']
    