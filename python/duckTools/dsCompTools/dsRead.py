

import os, sys, shutil, subprocess
from PySide import QtGui,QtCore
from PySide.QtCore import Qt
import nuke
#import myNameParser as fileNameParser
import _duckFunctions as df
reload(df)


sys.path.append("//vfx-data-server/dsGlobal/globalNuke/python/duckTools/dsCompTools")

import dsReader_ui
reload(dsReader_ui)

class MyForm(QtGui.QWidget):
    def __init__(self, parent=None):
        #Setup Window
        QtGui.QWidget.__init__(self)
        self.ui = dsReader_ui.Ui_dsReader()
        self.ui.setupUi(self)
        
        ### Extra ui fixes...
        self.ui.tableWidget.setColumnWidth(0,80)
        self.ui.tableWidget.setColumnWidth(1,25)
        self.ui.tableWidget.setColumnWidth(2,40)
        self.ui.tableWidget.setColumnWidth(3,350)
        self.ui.tableWidget.setColumnWidth(4,20)
        
        self.redButton = "U:/globalNuke/python/duckTools/dsCompTools/red_Button.png"
        self.greenButton = "U:/globalNuke/python/duckTools/dsCompTools/green_Button.png"
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(self.redButton), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.red_RB.setIcon(icon)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(self.greenButton), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.green_RB.setIcon(icon1)
        ### Extra ui fixes...
        
        self.rnlN = df.getReadNodes()
        path = nuke.root().name()
        rnlFP = df.get3dPublish(path)
        
        for f in rnlFP:
            compare = df.compare(f,self.rnlN)
            print compare
            if compare:
                self.rnlN.append(f)
        
        x = 0
        for rnl in self.rnlN:
            self.ui.tableWidget.setRowCount(x+1)

            item = QtGui.QTableWidgetItem(str(rnl['nodeName']))
            self.ui.tableWidget.setVerticalHeaderItem(x,item)
            
            iconPath = r"\\xserv2.duckling.dk\dsComp\Lego_Ninjago\film\2013_Fall_Ninjago_014601\q0010\s0010\comp\published3D\FG_Beauty\v004\.FG_Beauty_RL.1270.jpg"
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(iconPath), QtGui.QIcon.Normal, QtGui.QIcon.Off)

            item = QtGui.QTableWidgetItem()
            item.setIcon(icon)
            self.ui.tableWidget.setItem(x, 0, item)
            
            if rnl["nodeName"] == "None":
                button = self.redButton
            else:
                button = self.compareVer(rnl)
            
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(button), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            
            item = QtGui.QTableWidgetItem()
            item.setIcon(icon)
            self.ui.tableWidget.setItem(x, 1, item)
            
            item = QtGui.QTableWidgetItem(rnl['currentVer'])
            self.ui.tableWidget.setItem(x, 2, item)
            
            seq =  re.search("q[0-9][0-9][0-9][0-9]",rnl['rlPath']).group()
            pathend = ".../" + seq + rnl['rlPath'].split(seq)[-1]
            pathStart = rnl['rlPath'].split(seq)[0]
            
            item = QtGui.QTableWidgetItem(pathend)
            self.ui.tableWidget.setItem(x, 3, item)
            
            item = QtGui.QTableWidgetItem(pathStart)
            self.ui.tableWidget.setItem(x, 4, item)

            item = QtGui.QTableWidgetItem(rnl['rl'])
            self.ui.tableWidget.setItem(x, 5, item)

            x = x + 1
            
        self.ui.update_B.clicked.connect(self.updateToLatest)
    
    def updateToLatest(self):
        print "update Selected"
        nodes = self.ui.tableWidget.selectionModel().selectedRows()
        for n in nodes:
            row = n.row()
            
            readNode = self.ui.tableWidget.verticalHeaderItem(row).text()
            item = self.ui.tableWidget.horizontalHeaderItem(3).text()
            pathEnd = self.ui.tableWidget.item(int(row),3).text()
            
            pathEnd = pathEnd.replace(".../","")
            pathStart = self.ui.tableWidget.item(int(row),4).text()

            self.currentPath = pathStart + pathEnd

            for nodeName in self.rnlN:
                if nodeName['nodeName'] == "None":
                    fileName = nodeName['fileName']
                    padding = nodeName['padding']
                    ext = nodeName['ext']
                    break

            curVer = re.search("v[0-9][0-9][0-9]",self.currentPath).group()            
            path = self.currentPath.replace("/" + curVer,"")
            tmpList = os.listdir(path)

            for t in tmpList:
                if re.search("v[0-9][0-9][0-9]",t):
                    newVer = t
            
            if readNode != "None":
                n = nuke.toNode(readNode)
                filePath = n['file'].value()
   
                self.newPath = filePath.replace(curVer,newVer)
                
                if filePath == "self.newPath":
                    pass
                else:
                    n['file'].setValue(str(self.newPath))
            else:
                n = nuke.createNode('Read',)
                self.newPath = self.currentPath + "/" + fileName + "." + padding + "." + ext
                
                n['file'].setValue(str(self.newPath))
                
    def compareVer(self,rnl):

        curVer = re.search("v[0-9][0-9][0-9]",rnl['rlPath']).group()     
        path = rnl['rlPath'].replace("/" + curVer,"")

        tmpList = os.listdir(path)        
        for t in tmpList:
            if re.search("v[0-9][0-9][0-9]",t):
                ver = t

        if int(ver[1:]) > int(rnl['currentVer'][1:]):
            return self.redButton
        else:
            return self.greenButton

def dsRead():
    nuke.tprint("ds read tool v0.1")
    
s = MyForm()
s.show()
