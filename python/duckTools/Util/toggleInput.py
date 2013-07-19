'''
Created on 19 nov 2010

@author: danielt
'''

import nuke
import nukescripts

def hideInput():
    
    for nodes in nuke.selectedNodes():
        nukescripts.toggle('hide_input')
        return 
    
print hideInput()

