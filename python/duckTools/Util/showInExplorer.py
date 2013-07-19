import nuke
import os



def showInExplorer():
    "Little script that  will open your selected read/write in winExplore"
    
    selectedNode=nuke.selectedNode()

    filePath=selectedNode['file'].value()

    myPath=os.path.split(filePath)[0]

    myPath = os.path.normpath(myPath)


    print myPath
    cmd = 'explorer "%s"' % (myPath)
    print cmd
    os.system(cmd)
























