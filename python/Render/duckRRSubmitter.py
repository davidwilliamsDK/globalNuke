import nuke
import nukescripts
import myNameParser as fileNameParser
import _duckFunctions as df
import os
import sys
import shutil
import subprocess
os.umask(0)
reload(fileNameParser)


        
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

class duckRRSubmitter(nukescripts.PythonPanel):
    def __init__(self):
        nukescripts.PythonPanel.__init__(self, 'Duckling Nuke Submitter', 'com.duckling.ducklingRRSubmitter')
        
        self.nameParser = fileNameParser.nameParser
        #defining knobs
        self.compName = nuke.String_Knob('compName', 'Comp Name')
        self.updateCompName() 
        self.fileName = nuke.String_Knob('fileName', 'File Name')
        self.updateFileName()
        self.format = nuke.Format_Knob('format', 'Frame Format')
        self.updateFormat()
        self.rrPath = r"\\vfx-render-server\royalrender\bin\win\rrSubmitterconsole.exe"
        #self.rrPath = self.nameParser.windowRender
        
        if sys.platform == "linux2":
            self.rrPath = self.nameParser.linuxRender
            
        
         
        self.frameStart = nuke.Int_Knob('startFrame', 'Start Frame')
        self.frameStart.setValue(nuke.Root().firstFrame())
        self.frameEnd = nuke.Int_Knob('startFrame', 'End Frame')
        self.frameEnd.setValue(nuke.Root().lastFrame())
        self.frameStep = nuke.Int_Knob('stepFrame', 'Step Size')
        self.frameStep.setValue(1)
        self.deleteRangeEnum = nuke.Enumeration_Knob('deleteRangeEnum', 'Delete Range', ('All', 'Custom', 'None'))
        self.deleteRange = nuke.String_Knob('deleteRange', '')
        self.deleteRange.setValue("%d-%d" % (nuke.Root().firstFrame(), nuke.Root().lastFrame()))
        self.deleteRange.setEnabled(False)
        self.priority = nuke.Range_Knob('priority', 'Priority')
        self.priority.setRange(1, 100)
        self.priority.setValue(95)
        
        # creating knobs
        self.addKnob(self.compName)
        self.addKnob (self.fileName)
        self.addKnob(self.format)
        self.addKnob(self.frameStart)
        self.addKnob(self.frameEnd)
        self.addKnob(self.frameStep)
        self.addKnob(self.deleteRangeEnum)
        self.addKnob(self.deleteRange)
        self.addKnob(self.priority)
        self.showModalDialog()
        
        
    def knobChanged(self, knob):
        if knob == self.deleteRangeEnum:
            if self.deleteRangeEnum.value() == 'All':
                self.deleteRange.setEnabled(False)
                self.deleteRange.setValue("%d-%d" % (self.frameStart.value(), self.frameEnd.value()))
            if self.deleteRangeEnum.value() == 'Custom':
                self.deleteRange.setEnabled(True)
            if self.deleteRangeEnum.value() == 'None':
                self.deleteRange.setEnabled(False)
                self.deleteRange.setValue("")
            
        if knob.name() == "OK":
            self.submitRender()
        

    # RENDER SUBMITTER
    def submitRender(self):
        nameParser = self.nameParser
        
        self.basePath = ""
        self.writeOutName = ""
        self.compOutPath = ""
        COMPname = nameParser.fileName
        
       #check nuke script type to determine render out path
        if nameParser.type == "comp":
            self.basePath = "%s" % (nameParser.renderPath)
            print ''
            print 'this is my basePath ' + self.basePath
            print ''
            self.writeOutName = "%s_%s_%s_%s" % (nameParser.vendor,nameParser.product,nameParser.seqName, nameParser.shotName)
            print ''
            print 'if comp type is comp this my writeOutName ' +  self.writeOutName
            print ''
            #to be used with an if depending on comptype
            #this is my compOutPath depending on name//VFX-DATA-SERVER/DSPIPE/LEGO_TEST/FILM/TESTEPISODE/Q0010/S0010/COMP

            compPath = r"%s/%s" % (self.basePath,nameParser.version)
            print ''
            print 'this is my compOutPath depending on name' + compPath
            
        
        COMPcompDir = os.path.dirname(nameParser.scriptDir)
        print ''
        print 'this is my compDir ' + COMPcompDir
        print ''
        nukeScriptPath =  r"%s/%s/%s"% (COMPcompDir,'nukeScripts',COMPname)
        print ''
        print nukeScriptPath
        print ''
        #if comppdir not exist create
        os.path.dirname(nukeScriptPath)
        
        if not os.path.exists(nukeScriptPath):
            os.makedirs(nukeScriptPath)     
            
        #using delete in df to delete old renders on user choice
        self.deleteRangeArray = []
        for i in self.deleteRange.value().split(','):
            rangeMatch = i.split('-')
            if len(rangeMatch) == 2:
                min = int(rangeMatch[0])
                max = int(rangeMatch[1])
                if min < max:
                    for number in range(min, max + 1):
                        self.deleteRangeArray.append(number)
            elif len(rangeMatch) == 1:
                number = int(rangeMatch[0])
                self.deleteRangeArray.append(number)
                
        #load from duckfunctions
        if df.updateSavers():
            df.deleteFrames(self.deleteRangeArray)
            nuke.scriptSave(self.nameParser.filePath)
            #Copy script to comp folder
            shutil.copy(self.nameParser.filePath, compPath)
            #RR commands
            rrCommand = "%s %s -SeqStart %d -SeqEnd %d -SeqStep %d DefaultClientGroup=0~Nuke6 Priority=0~%d" % (self.rrPath, nukeScriptPath, self.frameStart.value(), self.frameEnd.value(), self.frameStep.value(), self.priority.getValue())
            #rrCommand = "%s %s -SeqStart %d -SeqEnd %d -SeqStep %d Priority=0~%d" % (self.rrPath, nukeScriptPath, self.frameStart.value(), self.frameEnd.value(), self.frameStep.value(), self.priority.getValue())
            print rrCommand
            print process(rrCommand).communicate()[0]
            print("Success")
        else:
            print("Fail")   

    # locking format            
    def updateFormat(self):
        self.format.setValue(nuke.Root()['format'].value())
        self.format.setEnabled(False)
        
    
    def updateCompName(self):
        self.nameParser = fileNameParser.nameParser(nuke.root().name())
        self.compName.setValue(self.nameParser.fileName)

    def updateFileName(self):
        nameParser = self.nameParser
        self.writeOutName = ""
        if nameParser.type == "comp":
            self.writeOutName = "%s_%s_%s_%s" % (nameParser.vendor,nameParser.product,nameParser.seqName, nameParser.shotName)
            self.fileName.setValue(self.writeOutName)
        

        
        
#duckRRSubmitter()


