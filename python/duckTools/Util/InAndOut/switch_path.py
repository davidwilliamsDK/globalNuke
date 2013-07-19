import sys, re
try:
    import nuke
except:
    print 'couldnt import nuke'
    

def changePath(path, arg):
    if arg == 'dsComp':
        if sys.platform == 'win32':
            if path[0].lower() == 'p':
                path = path.replace('%s:' % (path[0]), '//xserv2/VFXSAN/dsComp')
            else:
                path = path.replace('//vfx-data-server/dsPipe', '//xserv2/VFXSAN/dsComp')
        else:
            path = path.replace('//xserv2/VFXSAN/dsComp', '/mounts/san/dsComp')
            
   
    if arg == 'dsRender':
        if sys.platform == 'win32':
            if path[0].lower() == 'p':
                path = path.replace('%s:' % (path[0]), '//framestore/pipeline/dsRender')
            else:
                path = path.replace('//vfx-data-server/dsPipe', '//framestore/pipeline/dsRender')
        else:
            path = path.replace('/dsPipe', '/mnt/vfxpipe/dsRender')
    return path

def determinPath(path):
    
    if sys.platform == 'win32':
        match = re.search('([vV]\d\d\d)', path)
        if match:
            print match.group()
        pass
    elif sys.platform == 'linux2':
        pass
    else:
        print 'MAC SUCKS'
    
def switch_path():
    for node in nuke.allNodes():
        if node.Class().lower() == 'read':
            file = node.knob('file')
            file.setValue(changePath(file.getValue(), 'dsComp'))
            print "%s[%s] :\t '%s...'" % (node.name(), node.Class(), file.getValue()[:len(file.getValue())/2])
            
        elif node.Class().lower() == 'write':
            file = node.knob('file')
            file.setValue(changePath(file.getValue(), 'dsComp'))
            print "%s[%s] :\t '%s...'" % (node.name(), node.Class(),  file.getValue()[:len(file.getValue())/2])

list = ['//vfx-data-server/dsPipe','/mnt/vfxpipe/dsRender', '//xserv2/VFXSAN/dsComp', '/mounts/san/dsComp', '/dsPipe']
for path in list:
    print determinPath(path)