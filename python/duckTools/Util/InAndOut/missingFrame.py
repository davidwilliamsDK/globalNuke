import nuke


def SetMissingFrameToChecker():
    
    allReads = []
    [allReads.append(reads) for reads in nuke.allNodes() if reads.Class()=='Read']
    print allReads
        
    
    for changeMe in allReads:
         missingFrames = changeMe.knob('on_error').setValue('nearest frame')
    
    print missingFrames