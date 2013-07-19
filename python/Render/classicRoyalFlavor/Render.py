import nuke, ntpath, subprocess, os, random, time, re
try:
    import assetManager
except:
    print 'failed to import assetManager...'

def Render():
    getRR_Root()
    rrSubmit()
    
def write_tmp():
    list = nuke.filename(nuke.thisNode(), nuke.REPLACE).split(' ')
    for filename in list:
        if filename.endswith('.exr'):
            nuke_script_path = assetManager.change_path(nuke.root().name())
            nuke_script_dir, nuke_script_filename =  os.path.split( nuke_script_path )
            script_path = '/dsPantry/Python/dsToolbox/Nuke/dsOnliner.py'
            sh_path = '%s/online_%s_%s.sh' % ('/pipe/pantry/tmp/_bake', os.path.splitext(nuke_script_filename)[0],str( time.time()).split('.')[0])
            f = open(sh_path, 'w')
            f.write('python %s %s\n' % ( script_path, filename))
            f.close()
            break
            return sh_path
    
def process(cmd_line):
    cmd = cmd_line.split(' ')
    proc = subprocess.Popen(cmd, 
                        shell=False,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        )
    return proc

def getRR_Root():
    if os.environ.has_key('RR_ROOT'):
        return os.environ['RR_ROOT']
    HCPath="%"
    if ((sys.platform.lower() == "win32") or (sys.platform.lower() == "win64")):
        HCPath="%RRLocationWin%"
    elif (sys.platform.lower() == "darwin"):
        HCPath="%RRLocationMac%"
    else:
        HCPath="%RRLocationLx%"
    if HCPath[0]!="%":
        return HCPath
    nuke.message("This plugin was not installed via rrWorkstationInstaller!")

def submit(cmd_line):
    try:
        #print os.popen(cmd_line).read()
        #os.system(cmd_line)
        print process(cmd_line)
        return True
    except:
        return False
    
def rrSubmit():
    nuke.scriptSave()
    rootNode = nuke.toNode('root')
    CompName = rootNode.name()
    rrRoot = getRR_Root()
    value = random.randint(0,225)
    if ((CompName==None) or (len(CompName)==0)):
        return
    if ((sys.platform.lower() == "win32") or (sys.platform.lower() == "win64")):
        cmd = rrRoot+"\\win__rrSubmitter.bat  "+CompName
        print 'cmd', cmd
        #os.system(rrRoot+"\\win__rrSubmitter.bat  "+CompName)
        print process(cmd).communicate()[0]
    elif (sys.platform.lower() == "darwin"):
        os.system(rrRoot+"/bin/mac/rrSubmitter.app/Contents/MacOS/rrSubmitter  "+CompName)
    else:
            print process('%s/lx__rrSubmitter.sh %s -PreID %s' % (rrRoot,CompName, value)).communicate()[0]
            cmd = '/mnt/rrender/bin/lx64/rrSubmitterconsole %s -WaitForPreID %s' % (write_tmp(), value)
            print process(cmd).communicate()[0]


        
