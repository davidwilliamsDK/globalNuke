import nuke
import os
import time
import shutil
import nukescripts
import re, sys

vortex_root = '/mounts/vfxstorage/vortex/vortex'
if not  vortex_root in sys.path:
    sys.path.append(vortex_root)



'''def collect(path):
    #nuke.filename(nuke.thisNode(), nuke.REPLACE)
    for file in os.listdir(path):
        source = '%s/%s' % (path, file)
        if not os.path.isdir(source):
            link_dir = path.replace('/Comp/CompOut', '/Online')
            if not os.path.exists( link_dir):
                os.makedirs(link_dir)
            destination = '%s/%s' % (link_dir, file)
            if not os.path.exists( destination):
                os.symlink(source, destination)'''

def createOutDirs():
    trgDir = os.path.dirname(nuke.filename(nuke.thisNode()))
    
    if not os.path.isdir(trgDir):
        try:
            os.makedirs(trgDir)
        except: 
            pass  
        
def getCurrentScriptDir():
    #GET CURRENT SCRIPT DIR
    scriptDir =  os.path.dirname ( nuke.root().knob("name").getValue() )
    #print scriptDir
    
       
def get_comp_path():
    try:
        nuke_script_path = nuke.root().name()
    except:
        nuke_script_path = None
        
    if nuke_script_path:
        nuke_script_dir, nuke_script_filename =  os.path.split( nuke_script_path )
        return nuke_script_path, nuke_script_dir, nuke_script_filename
    
    
def magicWrite():

    #GET CURRENT SCRIPT DIR
    scriptDir =  os.path.dirname ( nuke.root().knob("name").getValue() )
    #print scriptDir
    
    #GET CURRENT COMPNAME AND COMPPATH
    compPath, compName = os.path.split(nuke.root().name())
    print compPath
    print compName

    #USE REG EXPR TO CHECK SCRIPTNAME AND POPULATE
    match = re.match('^(\w+)_(\w+)_(\w+)_(\w+)_(v\d+)_(\w+)_(\w+)\.nk', compName)
    if match:
        projectShort, film, sequenceName, shotName, version, note, initials = match.groups()
        #print match.groups()
        
    #CREATE COMP WRITE NAME
    folderVersion = version
    #writeOutName = projectShort + '_' + film + '_' + sequenceName + '_' + shotName + '.' + padding + '.' + fileFormat 
    writeOutName = projectShort + '_' + film + '_' + sequenceName + '_' + shotName
    #print writeOutName
    
    #GET RENDER DIR /compOut
    renderPath = scriptDir.replace("NukeScript", "compOut")
    #print renderPath
    
    #CREATE COMP OUT PATH AND FOLDER TO BE CREATED BEFORE RENDER AS CALLBACK
    compOut = renderPath +  '/' + folderVersion + '/' + writeOutName
    
    #nuke.tprint(compOut)
    
    return compOut




def copyNukeScript():
    
    #GET CURRENT SCRIPT DIR
    scriptDir =  os.path.dirname ( nuke.root().knob("name").getValue() )
    #GET CURRENT COMPNAME AND COMPPATH
    compPath, compName = os.path.split(nuke.root().name())
    print compPath
    print compName
    #USE REG EXPR TO CHECK SCRIPTNAME AND POPULATE
    match = re.match('^(\w+)_(\w+)_(\w+)_(\w+)_(v\d+)_(\w+)_(\w+)\.nk', compName)
    if match:
        projectShort, film, sequenceName, shotName, version, note, initials = match.groups()
    #CREATE COMP WRITE NAME
    folderVersion = version
    writeOutName = projectShort + '_' + film + '_' + sequenceName + '_' + shotName
    #GET RENDER DIR /compOut
    renderPath = scriptDir.replace("NukeScript", "compOut")
    #CREATE COMP OUT PATH AND FOLDER TO BE CREATED BEFORE RENDER AS CALLBACK
    compOut = renderPath +  '/' + folderVersion + '/' + writeOutName       
    #COPY LATEST TO FOLDER
    fromPath, fromName = os.path.split(nuke.root().name())
    dest = renderPath +  '/' + folderVersion 
    shutil.copy2(os.path.join(fromPath, fromName),dest)
    return


def dirName():

    #GET CURRENT SCRIPT DIR
    scriptDir =  os.path.dirname ( nuke.root().knob("name").getValue() )
    #print scriptDir
    
    #GET CURRENT COMPNAME AND COMPPATH
    compPath, compName = os.path.split(nuke.root().name())
    print compPath
    print compName

    #USE REG EXPR TO CHECK SCRIPTNAME AND POPULATE
    match = re.match('^(\w+)_(\w+)_(\w+)_(\w+)_(v\d+)_(\w+)_(\w+)\.nk', compName)
    if match:
        projectShort, film, sequenceName, shotName, version, note, initials = match.groups()
        #print match.groups()
        
    #CREATE COMP WRITE NAME
    folderVersion = version
    #writeOutName = projectShort + '_' + film + '_' + sequenceName + '_' + shotName + '.' + padding + '.' + fileFormat 
    writeOutName = projectShort + '_' + film + '_' + sequenceName + '_' + shotName
    #print writeOutName
    
    #GET RENDER DIR /compOut
    renderPath = scriptDir.replace("NukeScript", "compOut")
    #print renderPath
    
    #CREATE COMP OUT PATH AND FOLDER TO BE CREATED BEFORE RENDER AS CALLBACK
    outPath = renderPath +  '/' + folderVersion + '/' + writeOutName
    
    #nuke.tprint(compOut)
    
    return outPath

def fileName():

    #GET CURRENT SCRIPT DIR
    scriptDir =  os.path.dirname ( nuke.root().knob("name").getValue() )
    #print scriptDir
    
    #GET CURRENT COMPNAME AND COMPPATH
    compPath, compName = os.path.split(nuke.root().name())
    print compPath
    print compName

    #USE REG EXPR TO CHECK SCRIPTNAME AND POPULATE
    match = re.match('^(\w+)_(\w+)_(\w+)_(\w+)_(v\d+)_(\w+)_(\w+)\.nk', compName)
    if match:
        projectShort, film, sequenceName, shotName, version, note, initials = match.groups()
        #print match.groups()
        
    #CREATE COMP WRITE NAME
    folderVersion = version
    #writeOutName = projectShort + '_' + film + '_' + sequenceName + '_' + shotName + '.' + padding + '.' + fileFormat 
    writeOutName = projectShort + '_' + film + '_' + sequenceName + '_' + shotName
    #print writeOutName
    
    #GET RENDER DIR /compOut
    renderPath = scriptDir.replace("NukeScript", "compOut")
    #print renderPath
    
    #CREATE COMP OUT PATH AND FOLDER TO BE CREATED BEFORE RENDER AS CALLBACK
    compOut = renderPath +  '/' + folderVersion + '/' + writeOutName
    
    #nuke.tprint(compOut)
    
    return writeOutName
    
def clean_path(path):
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
    print 'clean_path:', string
    return string

def change_path(path):
    path = clean_path(path)
    if path:
        if sys.platform == 'linux2':
            pass
        elif sys.platform == 'win32':
            path = '//vfx-data-server%s' % path
    
    return path

def get_comp_path():
    try:
        nuke_script_path = nuke.root().name()
    except:
        nuke_script_path = None
        
    if nuke_script_path:
        nuke_script_dir, nuke_script_filename =  os.path.split( nuke_script_path )
        return nuke_script_path, nuke_script_dir, nuke_script_filename

def collect():
    path =  change_path(nuke.filename(nuke.thisNode(), nuke.REPLACE))
    dir, file = os.path.split( path )
    dir_list = dir.split('/')
    for i in range(len(dir_list)):
        if dir_list[i] and dir_list[i][0].lower() == 's' and dir_list[i][1:4].isdigit():
            #print i, dir_list[i]
            string =  '%s' % '/'.join(dir_list[0:i+1])
            print string
    if os.path.exists(path):
        print '...'
        
def symLinkIt():
    print 'LINKED!'
    return 

def safeChecking():
    try:
        print 'Safe Checking'
        '''
        determinPath('/dsComp/Lego_Hollywood/Film/Episode_01/Q0120/S0060/comp/compIn/PublishedCG/Scene_Beauty/v004/Q0120_S0050_Beauty.####.exr')
        determinPath('/mounts/san/dsComp/Lego_Hollywood/Film/Episode_01/Q0120/S0060/comp/compIn/PublishedCG/Scene_Beauty/v004/Q0120_S0050_Beauty.####.exr')
        determinPath('//xserv2/VFXSAN/dsComp/Lego_Hollywood/Film/Episode_01/Q0120/S0060/comp/compIn/PublishedCG/Scene_Beauty/v004/Q0120_S0050_Beauty.####.exr')
        
        determinPath('/dsPipe/Lego_Hollywood/Film/Episode_01/Q0120/S0060/comp/compIn/PublishedCG/Scene_Beauty/v004/Q0120_S0050_Beauty.####.exr')
        determinPath('/mounts/vfxstoreage/dsPipe/Lego_Hollywood/Film/Episode_01/Q0120/S0060/comp/compIn/PublishedCG/Scene_Beauty/v004/Q0120_S0050_Beauty.####.exr')
        determinPath('//vfx-data-server/dsPipe/Lego_Hollywood/Film/Episode_01/Q0120/S0060/comp/compIn/PublishedCG/Scene_Beauty/v004/Q0120_S0050_Beauty.####.exr')
        '''
        switch_path()
    except:
        print 'Fucked up!'

def switch_path():
    for node in nuke.allNodes():
        if node.Class().lower() == 'read':
            file = node.knob('file')
            file.setValue(determinPath(file.getValue()))
            #print "%s[%s] :\t '%s...'" % (node.name(), node.Class(), file.getValue()[:len(file.getValue())/2])
            
        elif node.Class().lower() == 'write':
            file = node.knob('file')
            file.setValue(determinPath(file.getValue()))
            #print "%s[%s] :\t '%s...'" % (node.name(), node.Class(),  file.getValue()[:len(file.getValue())/2])

def determinPath(path):
    #print 'BEFORE:', path
    '''
    check if its a windows or linux path
    then check if its a comp or a 3d path
    '''
    patterns = ['^(//xserv2/VFXSAN/dsComp)', '^(//vfx-data-server/dsPipe)',  '^(/dsComp)', '^(/mounts/san/dsComp)', '^(/dsPipe)','^(/mounts/vfxstoreage/dsPipe)']
    match = [re.search(pattern, path).group() for pattern in patterns if re.search(pattern, path)]

    if sys.platform == 'win32' and match:
        if match[0] in ['/dsPipe', '/mounts/vfxstoreage/dsPipe']:
            path = path.replace(match[0], '//vfx-data-server/dsPipe')
        elif match[0] in ['/dsComp', '/mounts/san/dsComp']:
            path = path.replace(match[0], '//xserv2/VFXSAN/dsComp')
            
    elif sys.platform == 'linux2' and match:
        if match[0] in ['//vfx-data-server/dsPipe']:
            path = path.replace(match[0], '/dsPipe')
        elif match[0] in ['//xserv2/VFXSAN/dsComp']:
            path = path.replace(match[0], '/dsComp')
    return path
    #print 'AFTER:', path


