import nuke

def shortCutMe():
    
    selectedReads = []
    [selectedReads.append(reads) for reads in nuke.selectedNodes() if reads.Class()=='Read']
    print selectedReads

    for read in selectedReads:
        read.setSelected(False)

    for read in selectedReads:
        read.setSelected(True)
        shortCutMe = nuke.createNode("PostageStamp")
        shortCutMe.knob('label').setValue('[lindex [split [lindex [split [knob [topnode].file] .] 0] /] end]')
        shortCutMe.knob('postage_stamp').setValue(True)
        shortCutMe.knob('hide_input').setValue(True)
        read.setSelected(False)

