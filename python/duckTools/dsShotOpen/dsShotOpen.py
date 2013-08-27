print "nuke shot Opener"
import os, sys, shutil, subprocess
from PySide import QtGui
import nuke
import _duckFunctions as df

sys.path.append("//vfx-data-server/dsGlobal/globalNuke/python/duckTools/dsShotOpen")
sys.path.append(r'\\vfx-data-server\dsGlobal\dsCore\shotgun')

import dsShotOpen_ui
reload(dsShotOpen_ui)

import sgTools    

class MyForm(QtGui.QWidget):
    def __init__(self, parent=None):
        #Setup Window
        QtGui.QWidget.__init__(self)
        self.ui = dsShotOpen_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.dsComp = "S:"
        self.defaultIcon = "//vfx-data-server/dsGlobal/globalNuke/presetScripts/nkScriptIcon.jpg"
        
        self.home = 'C:%s' % os.getenv("HOMEPATH")
        self.config_dir = '%s/.dsShotOpenNuke' % (self.home)
        self.config_dir = self.config_dir.replace("/","\\")
        self.config_path = '%s/config.ini' % (self.config_dir)
        self.config_path = self.config_path.replace("/","\\")
            
        self.init_user()
        self.init_projects()
        self.init_episodes()

        self.ui.projects_CB.currentIndexChanged.connect(self.init_episodes)
        self.ui.episodes_CB.currentIndexChanged.connect(self.init_sequences)
        self.ui.sequence_LW.itemSelectionChanged.connect(self.init_shots)
        self.ui.shots_LW.itemSelectionChanged.connect(self.init_nkScripts)
        
        #self.ui.icon_B.clicked.connect(self.createIcon)
        self.ui.load_B.clicked.connect(self.openScript)
        
        self.loadTest()

    def loadTest(self):
        if nuke.root().name() == "Root":
            print "default scene use config"
            self.load_config()
        else:
            path = nuke.root().name()
            print "get settings from file"
            self.load_config()

    def createIcon(self):
        df.createIcon()

    def openScript(self):
        
        nk = self.ui.nk_LW.currentItem().text()
        path = self.nkScriptPath + nk

        nuke.scriptClear()
        nuke.scriptOpen(path)

    def init_user(self):
        ##Test and return if Episode exists
        self.ui.user_CB.clear()
        self.userDict = {}
        self.group = {'type': 'Group', 'id': 5}
        self.myPeople = sgTools.sgGetPeople()
        for user in sorted(self.myPeople):
            if str(user['sg_status_list']) == "act":
                userName = str(user['name'])
                self.ui.user_CB.addItem(userName)
                self.userDict['id'] = user['id']
                self.userDict['sg_initials'] = user['sg_initials']

    def init_projects(self):
        '''
        Adds projects to self.projects
        Only if the project contains a /Local/config.xml
        '''
        self.ui.projects_CB.clear()
        
        sg = sgTools.getSG()
        sgProjects = sg.find("Project", [['sg_status', 'is', 'Active']], ['name'])
        for pro in sgProjects:
            self.ui.projects_CB.addItem(pro['name'])
            
    def init_episodes(self):
        '''
        Adds episodes to self.episodes
        '''
        self.ui.episodes_CB.clear()
        pr = self.ui.projects_CB.currentText()
        
        sg = sgTools.getSG()
        sgEpisodes = sg.find("Scene", [['sg_status_list', 'is', 'act'], ['project.Project.name','is', str(pr)]], ['code'])
        for epi in sgEpisodes:
            self.ui.episodes_CB.addItem(epi['code'])
        
    def init_sequences(self):
        '''
        Adds sequences to self.sequences
        Searches after pattern is [qQ][0-9][0-9][0-9][0-9]
        '''
        self.ui.sequence_LW.clear()
        pr = self.ui.projects_CB.currentText()
        ep = self.ui.episodes_CB.currentText()
        
        self.seqRootPath = self.dsComp + "/" + pr + "/film/" + ep + "/"
        tmpList = os.listdir(self.seqRootPath)

        for t in tmpList:
            if t[0] != ".":
                if re.search("q[0-9][0-9][0-9][0-9]",t):
                    self.ui.sequence_LW.addItem(t)

    def init_shots(self):
        
        pr = self.ui.projects_CB.currentText()
        ep = self.ui.episodes_CB.currentText()
        sq = self.ui.sequence_LW.currentItem().text()

        self.ui.shots_LW.clear()
        sg = sgTools.getSG()
        sgShots = sg.find("Shot",[['project.Project.name','is',str(pr)],['sg_scene.Scene.code','is', str(ep)],['sg_sequence.Sequence.code','is',str(sq)]],['code','id','sg_cut_in','sg_cut_out','sg_mayain','sg_mayaout'])
        for shot in sgShots:
            self.ui.shots_LW.addItem(str(shot['code']))

    def init_nkScripts(self):

        self.ui.nk_LW.clear()
        pr = self.ui.projects_CB.currentText()
        ep = self.ui.episodes_CB.currentText()
        sq = self.ui.sequence_LW.currentItem().text()
        sh = self.ui.shots_LW.currentItem().text()
        
        self.nkScriptPath = "%s/%s/film/%s/%s/%s/comp/nukeScripts/"  %(self.dsComp,pr,ep,sq,sh)
        self.nkCompOut = "%s/%s/film/%s/%s/%s/comp/compOut/"  %(self.dsComp,pr,ep,sq,sh)
        
        try:
            tmpList = os.listdir(self.nkScriptPath)
            for s in tmpList:
                if not re.search("~",s):
                    if not re.search("autosave",s):
                        if not os.path.isdir(self.nkScriptPath + s):
                            self.nameParcer(s)
                            try:
                                iconPath = self.nkCompOut + self.nameDict['ver'] + "/"
                            except:
                                iconPath = None
                            icon = self.nkScriptIcon(iconPath)
                            item = QtGui.QListWidgetItem(self.ui.nk_LW)
                            item.setIcon(icon)
                            item.setText(s)
                            self.ui.nk_LW.addItem(item)
        except:
            print "no " + sq + " on file structure but in ShotGun" 

        self.save_config()
        
    def nameParcer(self,nkScript):
        self.nameDict = {}
        try:
            seq = re.search("q[0-9][0-9][0-9][0-9]",nkScript).group()
            self.nameDict['seq'] = seq
        except:
            pass
        try:
            shot = re.search("s[0-9][0-9][0-9][0-9]",nkScript).group()
            self.nameDict['shot'] = shot
        except:
            pass
        try:
            ver =  re.search("v[0-9][0-9][0-9]",nkScript).group()
            self.nameDict['ver'] = ver
        except:
            pass
        try:
            epi = nkScript.split(seq)[0].strip("_")
            self.nameDict['epi'] = epi
        except:
            pass
        try:
            tmpLine = nkScript.split(str(ver))[-1].strip("_")
        except:
            pass
        try:
            comp = tmpLine.split("_")[0]
            self.nameDict['comp'] = comp
        except:
            pass
        try:
            nn = tmpLine.split("_")[1]
            self.nameDict['nn'] = nn
        except:
            pass
        try:
            usr = tmpLine.split("_")[2].split(".")[0]
            self.nameDict['usr'] = usr
        except:
            pass
        
    def testIcon(self,iconPath):
        try:
            tmpList = os.listdir(iconPath)
            for t in tmpList:
                if re.search(".jpg",t):
                    iconPath = iconPath + "/" + t
                    return iconPath
        except:
            return iconPath
            
    def nkScriptIcon(self,iconPath):
        iconPath = self.testIcon(iconPath)
        icon = QtGui.QIcon()
        if iconPath == None:
            iconPath = self.defaultIcon
        if not os.path.isfile(iconPath):
            iconPath = self.defaultIcon
            
        icon.addPixmap(QtGui.QPixmap(iconPath), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        return icon

    def load_config(self):
        '''
        Load config which is a dictionary and applying setting.
        '''
        if os.path.exists(self.config_path):
            config_file = open( '%s' % self.config_path, 'r')
            list = config_file.readlines()
            config_file.close()

            config = {}
            for option in list:
                key, value = option.split('=')
                config[key] = value.strip()
                
            index = [i for i in range(self.ui.user_CB.count()) if self.ui.user_CB.itemText(i) == config.get('USER')][0]
            self.ui.user_CB.setCurrentIndex(index)
            
            index = [i for i in range(self.ui.projects_CB.count()) if self.ui.projects_CB.itemText(i) == config.get('PROJECT')][0]
            self.ui.projects_CB.setCurrentIndex(index)
            
            index = [i for i in range(self.ui.episodes_CB.count()) if self.ui.episodes_CB.itemText(i) == config.get('EPISODE')][0]
            self.ui.episodes_CB.setCurrentIndex(index)
            
            index = [i for i in range(self.ui.sequence_LW.count()) if self.ui.sequence_LW.item(i).text() == config.get('SEQUENCE')][0]
            self.ui.sequence_LW.setCurrentRow(index)
            
            index = [i for i in range(self.ui.shots_LW.count()) if self.ui.shots_LW.item(i).text() == config.get('SHOT')][0]
            self.ui.shots_LW.setCurrentRow(index)
            
    def save_config(self):
        '''
        Save setting to the config file as a dictionary.
        '''
        user = self.ui.user_CB.currentText()
        project = self.ui.projects_CB.currentText()
        episode = self.ui.episodes_CB.currentText()
        sequence = self.ui.sequence_LW.currentItem().text()
        shot = self.ui.shots_LW.currentItem().text()

        if not os.path.exists(self.config_dir):
            #print self.config_dir, self.config_path
            os.mkdir(self.config_dir)
        config = open( '%s' % self.config_path, 'w')
        config.write('USER=%s\n' % (user))
        config.write('PROJECT=%s\n' % (project))
        config.write('EPISODE=%s\n' % (episode))
        config.write('SEQUENCE=%s\n' % (sequence))
        config.write('SHOT=%s\n' % (shot))

        config.close()

        self.load_config()
        return self.config_path

def dsShotOpen():
    nuke.tprint("custom shotOpener")
    
s = MyForm()
s.show()
    