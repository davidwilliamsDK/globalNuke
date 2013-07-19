import nuke


def setMissingFrameToChecker():
    
    allReads = []
    [allReads.append(reads) for reads in nuke.allNodes() if reads.Class()=='Read']
    print allReads
        
    
    for changeMe in allReads:
         missingFrames = changeMe.knob('on_error').setValue('checkerboard')
    
    print missingFrames