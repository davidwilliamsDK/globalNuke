'''
Nuke Footage Collector v1.1

Created on 04.06.2010 

This script collects the footage from your read nodes and save them in a directory 
in the same structure where your current nuke script lives.
update to previous version:
- ask to save script in another location and then save the footage
	where you last saved
- about info box
Fell free to use and change this script to match your needs,
the author isn't responsable for any damage made by the script 
for more info or improvements feel free to contact me

Copyright (c) 2010 abdallah huballah [abdhub@googlemail.com]
'''


import os
import string
import shutil
import fnmatch
import nuke

def ahFootColInfo():
    nuke.message('''Footage Collector Ver 1.1

This script collects the footage from your read nodes and save them in a 
directory in the same structure where your current nuke script lives.

Copyright (c) 2010 abdallah huballah [abdhub@googlemail.com]''')
 
def ahFootCol():
    nuke.scriptSaveAs()
    
#### Getting Filepaths, StartFrame and EndFrame from ReadNodes
    nuke.selectAll()
    tmpDir =[]
    rs = []
    stF = []
    edF = []
    for elm in nuke.selectedNodes('Read'):
        rs.append(elm.knob('name').value())
        stF.append(elm.knob('first').value())
        edF.append(elm.knob('last').value())
        tmpDir.append(elm.knob('file').value())
    tmpF = []
    tmpD = []
    for el in tmpDir:
        tp = os.path.dirname(el)
        tmpD.append(tp + '/')
        lp = len (tp)+1
        tmpF.append(el[lp:])
        
#### Setting the Directory to save to 
    sc = nuke.Root().name()
    scPath = os.path.dirname(nuke.Root().name())
    pl = len(os.path.dirname(nuke.Root().name())) +1
    scName = sc[pl:-3]
    fdir = scName + '_Footage'
    fd = scPath +'/' + fdir
    os.mkdir(fd)
    ftdir = fd + '/' 
    rdir = []
    for n in rs:   
        os.mkdir(ftdir + n)
        rdir.append(ftdir+n+'/')

#### Checking the Footage and then Copy
    for i in range (0,len(rdir)):
        if ('%' in tmpF[i]):
            ind = string.find(tmpF[i],'%',0,len(tmpF[i]))
            fname = tmpF[i][0:ind]
            enum = tmpF[i][ind:-4]
            ext = tmpF[i][-4:]
            seq = []
            for file in os.listdir(tmpD[i]):
                if fnmatch.fnmatch(file, fname + '*'):
                    for j in range (stF[i],edF[i]):
                        if fnmatch.fnmatch(file, '*'+str(j) + ext):
                            filelist = list(file)
                            filelist1 = string.join(filelist,"")
                            seq.append(filelist1)
            for elm in seq: shutil.copy(tmpD[i] + elm, rdir[i] +elm)
        else: shutil.copy(tmpDir[i], rdir[i]+ tmpF[i])

#### Creating the menu in nuke
menu = nuke.menu('Nuke')
n =  menu.addMenu('ah_scripts')
n.addCommand('Footage_Collector v1.1','ahFootCol()')
n.addCommand('About','ahFootColInfo()')