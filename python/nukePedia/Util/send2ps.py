###    Sends the current frame of the selected node to
###    Photoshop, or renders one if necessary.
###    ---------------------------------------------------------
###    send2ps.py v3.2
###    Created: 27/06/2009
###    Modified: 04/01/2010
###    Written by Diogo Girondi
###    diogogirondi@gmail.com

import os
import platform
import subprocess
import nuke

def send2ps():
    selNode = nuke.selectedNode()
    doSend2ps(selNode)


def doSend2ps( node, over_original = False ):

    '''Sends the current frame from the selected node to Photoshop'''

    if platform.system() in ( 'Windows', 'Microsoft' ):
        if nuke.env['WIN32']:
            ps_path = 'c:/Program Files/Adobe/Adobe Photoshop CS5.1 (64 Bit)/Photoshop.exe'
        else:
            ps_path = 'C:/Program Files (x86)/Adobe/Adobe Photoshop CS3/Photoshop.exe'
        cmd = []
    elif platform.system() in ( 'Darwin', 'Apple' ):
        ps_path = '/Applications/Adobe Photoshop CS4/Adobe Photoshop CS4.app'
        cmd = ['open', '-a']
    else:
        nuke.message( 'This script only works for Windows and OSX' )
        return
        
    if nuke.root()['name'].value() is '':
        nuke.scriptSave()
    
    if over_original and node.Class() in ['Read',  'Write']:    
        if node['file'] is not '':
            try:
                file_path = os.path.normpath( node['file'].value() % frame )
            except:
                file_path = os.path.normpath( node['file'].value() )
                
            if os.path.isfile( file_path ) is None:
                nuke.tprint( ">>> send2ps: The file path on %s it's not a file" ) % node.name()
                return
            else:
                cmd.append(ps_path)
                cmd.append(file_path)
                subprocess.Popen(cmd)
        else:
            raise RuntimeError('No frame on %s') % node.name()
    else:
        frame = nuke.frame()
        name = node.name()
        pos = ( node['xpos'].value(), node['ypos'].value() )
        script_path = nuke.root()['name'].value()
        script_root = os.path.dirname( script_path ) + '/'
        script_name = '.'.join( os.path.basename( script_path ).split( '.' )[:-1] )
        store_path = script_root + 'sent_to_ps/' + script_name + '/'
        ps_file = 'ps_' + name + '.%04d.exr' % frame
        
        if os.path.isdir( store_path ):
            file_path = store_path + ps_file
        else:
            try:
                os.makedirs( store_path )
                file_path = store_path + ps_file
            except:
                file_path = script_root + ps_file
                
        
    #===========================================================================
    #    #Exr
    # ghostSMain = nuke.createNode("Write")
    # ghostSMain.knob('channels').setValue('rgb')
    # ghostSMain.knob('name').setValue('exrGSaver')
    # ghostSMain.knob('file_type').setValue('exr')
    #===========================================================================
    
                
        w = nuke.createNode("Write")
        w.knob('channels').setValue('rgba')
        
        w.knob('file_type').setValue('exr')
        
        w['file'].setValue( file_path )
        
        nuke.tprint( '>>> send2ps: Rendering frame for %s' % name )
        nuke.execute( w.name(), frame, frame, 1 )        
        nuke.tprint( '>>> send2ps: %s - Done!' % w['file'].value() )
        cmd.append(os.path.normpath( ps_path ))
        cmd.append(os.path.normpath( file_path ))
        subprocess.Popen(cmd)
        if nuke.NUKE_VERSION_MAJOR >= 5 and nuke.NUKE_VERSION_MINOR >= 2:
            w['reading'].setValue( False )
            w['postage_stamp'].setValue( True )
            w['icon'].setValue( 'PS.png' )
        else:
            r = nuke.createNode( 'Read', 'file {' + w['file'].value() + '} colorspace sRGB tile_color 91291647', inpanel=False )
            r['xpos'].setValue( pos[0] )
            r['ypos'].setValue( pos[1]+50 )
            r['icon'].setValue( 'PS.png' )
            nuke.delete( w )
        
            
            
            