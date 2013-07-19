###    Sends the sequence of the selected node to Mocha
###    ---------------------------------------------------------
###    send2mocha.py v1.0
###    Created: 10/01/2010
###    Modified: 10/01/2010
###    Written by Diogo Girondi
###    diogogirondi@gmail.com

import os
import platform
import subprocess
import nuke

def send2mocha():
    
    '''Sends the currently selected Read or Write node sequence to Mocha for further work'''

    if platform.system() in ( 'Windows', 'Microsoft' ):
        if nuke.env['WIN32']:
            mocha_path = 'C:/Program Files/Imagineer Systems Ltd/mocha Pro V2/bin/mochapro.exe'
        else:
            mocha_path = 'C:/Program Files (x86)/Imagineer Systems Ltd/Mocha V1/bin/Mocha.exe'
        cmd = []
    elif platform.system() in ( 'Darwin', 'Apple' ):
        ps_path = '/Applications/Imagineer Systems Ltd/Mocha V1/Mocha.app'
        cmd = ['open', '-a']
    else:
        nuke.message( 'This script only works for Windows and OSX' )
        return

    sn = nuke.selectedNode()

    if sn.Class() in ( 'Read', 'Write' ):
        first = sn.firstFrame()
        file = sn['file'].value() % first
        cmd = '"%s" "%s"' % ( mocha_path, file )
        subprocess.Popen( cmd )

    else:
        nuke.message( 'Select a Read or Write node' )
        return
        
        
        