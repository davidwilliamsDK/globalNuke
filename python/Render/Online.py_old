import os, sys, subprocess, glob, re, platform,time
from PySide import QtGui, QtCore
print 'hmhm'
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(300, 300)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.onlineButton = QtGui.QPushButton(self.centralwidget)
        self.onlineButton.setObjectName("onlineButton")
        self.gridLayout.addWidget(self.onlineButton, 3, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.toolButton = QtGui.QToolButton(self.centralwidget)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout.addWidget(self.toolButton)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 306, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.table = QtGui.QTableWidget(self.centralwidget)
        self.table.setObjectName("table")
        self.checkBox = QtGui.QCheckBox(self.centralwidget)
        self.checkBox.setText('LOCAL')
        self.gridLayout.addWidget(self.checkBox, 4, 0, 1, 1)
        self.table.setObjectName("table")
        self.table.setColumnCount(2)
        self.table.setRowCount(0)
        self.gridLayout.addWidget(self.table, 2, 0, 1, 1)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Onliner", None, QtGui.QApplication.UnicodeUTF8))
        self.onlineButton.setText(QtGui.QApplication.translate("MainWindow", "Online", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))


class Onliner(Ui_MainWindow, QtGui.QMainWindow):
    def __init__(self, parent=None):
        """ Setup UI """
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        """"""
        
        self.onlineButton.setEnabled(False)
        self.table.setSizePolicy(QtGui.QSizePolicy.Expanding,  QtGui.QSizePolicy.Expanding)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.dirpath = ''
        self.nuke_filename = nuke.filename(nuke.thisNode(), nuke.REPLACE)
        self.nuke_scriptname= nuke.root().name()
        
        self.table.verticalHeader().hide()
        self.table.setShowGrid(False)
        
        self.table.horizontalHeader().hide()
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.table.setSortingEnabled(True)
        
        self.lineEdit.returnPressed.connect(self.add_framestacks_from_line)
        self.table.itemClicked.connect(self.set_filepath)
        self.toolButton.clicked.connect(self.open_filepath)
        self.table.itemDoubleClicked.connect(self.open_filepath)
        
        """ If not a new nuke script """
        if not self.nuke_scriptname == 'Root':
            self.add_framestacks_to_list()
        
        """ Setting up some windows and linux paths """
        self.batch_onliner = '/dsGlobal/dsCore/nuke/online/dsOnliner.py'
        self.python_path = 'python'
        
        if sys.platform == "linux2":
           self.rrPath = r'/mnt/rrender/bin/lx64/rrSubmitterconsole'
           self.tmp_dir = '/dsGlobal/tmp/_bake'
           
        elif sys.platform == 'win32':
            self.rrPath = r'\\vfx-render-manager\royalrender\bin\win\rrSubmitterconsole.exe'
            self.tmp_dir = r'\\vfx-data-server\dsGlobal\tmp\_bake'  

        self.onlineButton.clicked.connect(self.submit)
    
    def set_filepath(self):
        """ Setting the filepath for lineEdit and enable the Online Button """
        current_filename = self.table.item( self.table.currentRow(),0)
        current_version = self.table.item( self.table.currentRow(),1)
        self.dirpath = '%s/%s' % (self.nuke_compout, current_version.text())
        self.filepath = '%s/%s' % (self.dirpath, current_filename.text())
        self.lineEdit.setText(self.filepath)
        if self.lineEdit.text():
            self.onlineButton.setEnabled(True)

    def add_framestacks_from_line(self):
        """ 
        This was made so you can write a path in the lineEdit and it will add the framestack from the paths.
        Add framestacks from the lineEdit.
        If its a window path its gona replace the \\ with /  
        """
        text = self.lineEdit.text().replace("\\","/")
        self.table.clear()
        self.lineEdit.setText(text)
        
        
        if not os.path.isdir(text):
            dir, file = os.path.split(text)
            text = dir
        
        """ loop throug text until it finds comp and then join everything infront and comp together to form a path"""
        if os.path.exists(text):
            tmp =  text.split('/')
            for i in range(len(tmp)):
                if tmp[i].lower() == 'comp':
                    numb = i
        else:
            print text, 'doesnt exist'
        
        nuke_comp = '/'.join(text.split('/')[:numb+1])
        for dir in os.listdir(nuke_comp):
            if dir.lower() == 'compout':
                self.nuke_compout = '%s/%s' % ( nuke_comp, dir)
        
        """ List all dirs in nuke_compout which will be the versions """
        for dir in os.listdir(self.nuke_compout):
            
            
            """ All dirs that matches v0 """
            if dir[0].lower() == 'v' and dir[1].isdigit():
                nuke_version = '%s/%s' % (self.nuke_compout,dir)
                
                for file in self.get_image_sequences(nuke_version):
                    """ For all frames with the extension of EXR will get added to the list """
                    if file.endswith('.exr'):
                        
                        item_name = QtGui.QTableWidgetItem(file)
                        item_name.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

                        item_version = QtGui.QTableWidgetItem(dir)
                        item_version.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)

                        self.table.insertRow(0)
                        self.table.setRowHeight(0, 14)
                        self.table.setItem(0, 0, item_name)
                        self.table.setItem(0, 1, item_version)
        """ Resizing the collemns to the contens of the table"""
        self.table.resizeColumnsToContents()
        
    def add_framestacks_to_list(self):
        """ 
        Adds framestacks from the nuke_scriptname.
        Clear the table 
        """
        self.table.clear()
        
        """ loop throug text until it finds comp and then join everything infront and comp together to form a path """
        tmp =  self.nuke_scriptname.split('/')
        for i in range(len(tmp)):
            if tmp[i].lower() == 'comp':
                numb = i
        
        nuke_comp = '/'.join(self.nuke_scriptname.split('/')[:numb+1])
        for dir in os.listdir(nuke_comp):
            if dir.lower() == 'compout':
                self.nuke_compout = '%s/%s' % ( nuke_comp, dir)
        for dir in os.listdir(self.nuke_compout):
            
            """ All dirs that matches v0 """
            #print dir
            if dir[0].lower() == 'v' and dir[1].isdigit():
                #print 'in',  dir
                nuke_version = '%s/%s' % (self.nuke_compout,dir)
                for file in self.get_image_sequences(nuke_version):
                    
                    """ For all frames with the extension of EXR will get added to the list """
                    if file.endswith('.exr'):
                        
                        item_name = QtGui.QTableWidgetItem(file)
                        item_name.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled)

                        item_version = QtGui.QTableWidgetItem(dir)
                        item_version.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsUserCheckable)
                        
                        #item_time = QtGui.QTableWidgetItem(time.ctime(os.path.getmtime('%s/%s/%s' % (self.nuke_compout,dir, file))))
                        
                        self.table.insertRow(0)
                        self.table.setRowHeight(0, 14)
                        self.table.setItem(0, 0, item_name)
                        self.table.setItem(0, 1, item_version)
                        #self.table.setItem(0, 2, item_time)
                        
        #self.list.sortItems(QtCore.Qt.DescendingOrder)
        self.table.resizeColumnsToContents()
        
    def submit(self):
        if self.checkBox.checkState():
            path = self.run_locally().strip()
            
            online_folder = '%s/publish2D/compOut/DPX' % self.get_shot_dir(path)
            print online_folder
            if not os.path.exists(online_folder):
                os.makedirs(online_folder)
                
            source_dir, source_file = os.path.split(path)
            name, number, extension = source_file.split('.')
            
            file_path = '%s/%s.%s.%s' % (source_dir, name, '%04d', extension)
            destination = '%s/%s.%s.dpx' % (online_folder, name, '%04d')
            #rv = r'C:\Program Files\Tweak\RV-3.12.12-32/bin/rvio.exe'
            cmd = 'C:\Program Files (x86)\Tweak\RV-3.12.15-32/bin/rvio.exe -v //vfx-data-server%s -outsrgb -o //vfx-data-server%s' % (file_path, destination)
            cmd = r'%s' % cmd.replace('/', '\\')
            #cmd = r'\\vfx-data-server\dsPantry\Install\RV_Player\Win\WIN64-XFORCE\bin\rvio.exe -v -strictlicense //vfx-data-server%s -outsrgb -o %s' % (path, destination)
            print cmd, '\n'
            #print self.process(cmd).communicate()[0]
            
            
        else:
            """ 
            Submit is getting called when you hit the online button.
            Its going to add the job to Online user in rr and prio 89.
            
            Calling dsOnline on dsPantry
            """
            tmp = self.write_tmp()
            cmd = '%s %s DefaulClientGroup=1~RV UserName=0~Online Priority=2~89' % ( self.rrPath, tmp)
            print cmd
            print self.process(cmd).communicate()[0]
            ##self.close()
            
    def run_locally(self):
        """ 
        Writing a tmp file which is getting submitted to the farm.
        It has one line in the tmp file that tells rr to run a curtain command
        """
        filename = self.lineEdit.text()
        
        if filename and filename.endswith('.exr'):
            cleaned_path = self.clean_path(filename)
            return cleaned_path

                
    def get_shot_dir(self,path):
        '''
        Takes path and looks for s0000 and strips everything after the s0000 and returns it. 
        '''
        dir, file = os.path.split( path )
        dir_list = dir.split('/')
        for i in range(len(dir_list)):
            if dir_list[i] and dir_list[i][0].lower() == 's' and dir_list[i][1:4].isdigit():
                string =  '%s' % '/'.join(dir_list[0:i+1])
                return string
            
    def write_tmp(self):
        """ 
        Writing a tmp file which is getting submitted to the farm.
        It has one line in the tmp file that tells rr to run a curtain command
        """
        filename = self.lineEdit.text()
        
        if filename and filename.endswith('.exr'):
            cleaned_path = self.clean_path(filename)
            dir, file = os.path.split(filename)
            name, numb, extension = file.split('.')

            if sys.platform == "linux2":
                sh_path = '%s/online_%s_%s.sh' % (self.tmp_dir, name, str( time.time()).split('.')[0] )
               
            elif sys.platform == 'win32':
                sh_path = '%s\online_%s_%s.sh' % (self.tmp_dir, name, str( time.time()).split('.')[0] )

            f = open(sh_path, 'w')
            f.write('%s %s %s %s\n' % ( self.python_path, self.batch_onliner, cleaned_path, nuke.root()['fps'].getValue() ))
            f.close()
            
            return sh_path
        
    def open_filepath(self):
        '''Open the directory of the clicked tableitem'''
        if sys.platform == "linux2":
            path = self.lineEdit.text()
            if os.path.exists(path):
                cmd = "gnome-open " + str(path)
                
        if sys.platform == "win32":
            path = self.lineEdit.text()
            cmd = "explorer " + str(path.replace("/","\\"))
        
        try:
            print cmd
            self.process(cmd)
        except:
            pass
    
    def process(self, cmd_line):
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

    def clean_path(self, path):
        '''
        Takes a string, which it cleans to the system your on. 
        '''
        if path[:2].lower() == 'p:':
            path = '/dsPipe/%s' % path[3:]
    
        string = None

        if '\\' not in path:
            path = path.split('/')
            for i in range(len(path)):
                if path[i] == 'dsPipe':
                    string =  '/%s' % '/'.join(path[i:len(path)])
                    break
        else:
            path = path.split('\\')
            for i in range(len(path)):
                if path[i] == 'dsPipe':
                    string =  '/%s' % '/'.join(path[i:len(path)])
                    break
        return string

    def get_shot_dir(self, path):
        '''
        Takes path and looks for s0000 and strips everything after the s0000 and returns it. 
        '''
        dir, file = os.path.split( path )
        dir_list = dir.split('/')
        for i in range(len(dir_list)):
            if dir_list[i] and dir_list[i][0].lower() == 's' and dir_list[i][1:4].isdigit():
                string =  '%s' % '/'.join(dir_list[0:i+1])
                return string
            
    def get_image_sequences(self, path):
        '''
        Takes a directory.
        '''
        if os.path.isdir(path):
            source_dir = path
        else:
            source_dir = os.path.dirname(path)
        
        list = []
        name_list = []
        '''
        for all the paths that fits the pattern, append name and extension to a list
        '''
        for glob_path in  glob.glob('%s/*.*.*' % (source_dir)):
            #print glob_path
            dir, file = os.path.split(glob_path)
            
            if not file.endswith('.tmp'):
                name, number, extension = file.split('.')
            
                if (name, extension) not in name_list: 
                    num_list=[]
                    
                    name_list.append((name, extension))
                    '''
                    get the number from the file sequence and append that to its own list
                    '''
                    for _file in glob.glob('%s/%s.*.%s' % (source_dir, name, extension)):
                        _name, number, _extension = _file.split('.')
                        num_list.append(number)
                    '''
                    finally make the list with string 'filename.start-end.extension'
                    '''
                    if min(num_list) == max(num_list):
                        list.append( '%s.%s.%s' %(name, min(num_list), extension))
                    else:
                        list.append( '%s.%s-%s.%s' %(name, min(num_list), max(num_list), extension))
        '''
        return list with 'filename.start-end.extension'
        '''
        return list

def Online():
    pass

if __name__ == "__main__":
    inst = Onliner()
    inst.show()
