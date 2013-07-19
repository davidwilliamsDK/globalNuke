#super simple script to play ya nodes in djv, needs to be fixed a bit, happy camping danielT

import nuke
import subprocess


def djMe():
    
    #get the selected node and path
    playThis = nuke.selectedNode()
    file = playThis.knob('file').getValue()

    readerPath = file.replace('%04d', '0000')
    
    subprocess.Popen(args=[r"\\framestore\pipeline\pantry\Nuke6.2v2\djv-0.8.3-pre2_winxp-x86\bin\djv_view.exe", readerPath])
