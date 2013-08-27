import os, sys, shutil, subprocess
from PySide import QtGui
import nuke
import myNameParser as fileNameParser
import _duckFunctions as df

sys.path.append("//vfx-data-server/dsGlobal/globalNuke/python/Render")

import dsSubmit_ui
reload(dsSubmit_ui)

def process( cmd_line):
    '''
    Subprocessing, Returning the process.
    '''
    cmd = cmd_line.split(' ')
    proc = subprocess.Popen(cmd, 
                        shell=False,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        )
    return proc

class MyForm(QtGui.QWidget):
    def __init__(self, parent=None):
        #Setup Window
        QtGui.QWidget.__init__(self)
        self.ui = dsSubmit_ui.Ui_MainWindow()
        self.ui.setupUi(self)

        self.rrPath = r"\\vfx-render-server\royalrender\bin\win\rrSubmitterconsole.exe"        
        
        #defining knobs
        self.compName = nuke.root().name()
        self.nameParser = fileNameParser.nameParser(nuke.root().name())
        self.startFrame =nuke.Root().firstFrame()
        self.lastFrame =nuke.Root().lastFrame()
        self.nodeFormat = nuke.Root().format()
        self.format = "%s %dx%d %d" % (self.nodeFormat.name(),self.nodeFormat.width(),self.nodeFormat.height(),self.nodeFormat.pixelAspect()) 
        self.frameStep = "1"

        self.ui.compName_LE.setText(self.nameParser.fileName)
        self.ui.initals_LE.setText(self.nameParser.sig)

        self.fileName = "%s_%s_%s" % (self.nameParser.product,self.nameParser.seqName, self.nameParser.shotName)
        self.ui.fileName_LE.setText(self.fileName)

        self.ui.frameFormat_LE.setText(str(self.format))
        
        self.ui.startFrame_LE.setText(str(self.startFrame))
        self.ui.endFrame_LE.setText(str(self.lastFrame))
        self.ui.minPackage_LE.setText("2")
        self.ui.maxPackage_LE.setText("24")        

        self.ui.deleteRange_LE.setText(str(self.startFrame) + "-" + str(self.lastFrame))
        
        ##Buttons and actions
        self.ui.ok_B.clicked.connect(self.submitRender)
        self.ui.deleteRange_CB.currentIndexChanged.connect(self.deleteRange)

    def deleteRange(self):
        dr = self.ui.deleteRange_CB.currentText()
        if dr == "All":
            print "delete all"
            self.ui.deleteRange_LE.setEnabled(False)
            self.ui.deleteRange_LE.setText(str(self.startFrame) + "-" + str(self.lastFrame))
            
        if dr == "Custom":
            print "delete custom ranges"
            self.ui.deleteRange_LE.setEnabled(True)
            
        if dr == "None":
            print "delete No Frames"
            self.ui.deleteRange_LE.setText(" ")
            self.ui.deleteRange_LE.setEnabled(False)
       
    def createIcon(self):
        df.createIcon()
        
    def submitRender(self):
        print "do it"
        
        self.sig = self.ui.initals_LE.text()
        self.startFrame = self.ui.startFrame_LE.text()
        self.lastFrame = self.ui.endFrame_LE.text()
        self.minPackage = self.ui.minPackage_LE.text()
        self.maxPackage = self.ui.maxPackage_LE.text()
        self.prio = self.ui.priority_CB.currentText()
        
        if self.prio == "DOITNOW":self.prio == "99"
        
        self.basePath = ""
        self.writeOutName = ""
        self.compOutPath = ""
        COMPname = self.nameParser.fileName
        
       #check nuke script type to determine render out path
        if self.nameParser.type == "comp":
            self.basePath = "%s" % (self.nameParser.renderPath)
            print 'this is my basePath ' + self.basePath
            self.writeOutName = "%s_%s_%s" % (self.nameParser.product,self.nameParser.seqName, self.nameParser.shotName)
            print 'if comp type is comp this my writeOutName ' +  self.writeOutName

            compPath = r"%s/%s" % (self.basePath,self.nameParser.version)
            print 'this is my compOutPath depending on name' + compPath
            
        COMPcompDir = os.path.dirname(self.nameParser.scriptDir)
        print 'this is my compDir ' + COMPcompDir
        nukeScriptPath =  r"%s/%s/%s"% (COMPcompDir,'nukeScripts',COMPname)
        print nukeScriptPath
        #if comppdir not exist create
        os.path.dirname(nukeScriptPath)
        
        if not os.path.exists(nukeScriptPath):
            os.makedirs(nukeScriptPath)     

        #using delete in df to delete old renders on user choice
        self.deleteRangeArray = []
        
        for i in self.ui.deleteRange_LE.text().split(","):
            rangeMatch = i.split('-')
            if len(rangeMatch) == 2:
                min = int(rangeMatch[0])
                max = int(rangeMatch[1])
                if min < max:
                    for number in range(min,max+1):
                        self.deleteRangeArray.append(number)
            elif len(rangeMatch) == 1:
                number = int(rangeMatch[0])
                self.deleteRangeArray.append(number)
        print self.deleteRangeArray

        #load from duckfunctions
        if df.updateSavers():
            df.deleteFrames(self.deleteRangeArray)
            nuke.scriptSave(self.nameParser.filePath)
            #Copy script to comp folder
            shutil.copy(self.nameParser.filePath, compPath)
            #RR commands
            rrCommand = "%s %s -SeqStart %d -SeqEnd %d UserName=0~%s DefaultClientGroup=0~nuke Priority=0~%d SeqDivMIN=0~%d SeqDivMAX=0~%d " % (self.rrPath, nukeScriptPath, int(self.startFrame), int(self.lastFrame), self.sig, int(self.prio),int(self.minPackage),int(self.maxPackage))
            print rrCommand
            print process(rrCommand).communicate()[0]
            print("Success")
        else:
            print("Fail")        
        #self.createIcon()
        
def dsSubmit():
    nuke.tprint("custom submitter")
    
s = MyForm()
s.show()
    