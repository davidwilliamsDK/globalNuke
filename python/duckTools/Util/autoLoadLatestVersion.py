import nuke
import os
import re

class autoLoadLatestVersion:
  def __init__(self):
    nodes = self.getReaders()
    for node in nodes:
      path = node.knob('file').getValue()
      newPath = self.getNewPath(path)	
      if newPath != None:
	node.knob('file').setValue(newPath)
		
  def getReaders(self):
    nodes = nuke.selectedNodes('Read')
    if nodes == []:
      nodes = nuke.allNodes('Read')	

    return nodes

  def getNewPath(self, path):
    directory = os.path.dirname(path) + "/"
    fileName = os.path.basename(path)
    highestVersion = 0

    pattern = re.match("(\D*)(\d{2})(\D*\d*\D*)", fileName)
    try:
      name = pattern.group(1)
      version = pattern.group(2)	
      extension = pattern.group(3)
    except:
      return None	
	    
    if name == None or version == None or extension == None:
      return None
		    
    files = os.listdir(directory)

    for file in files:
      pattern2 = re.match("(\D*)(\d{2})(\D*\d*\D*)", file)
      try:
	name2 = pattern2.group(1)
	version2 = pattern2.group(2)	
	extension2 = pattern2.group(3)
      except:
	continue		
      
      if name != name2:
	continue
      
      if version2 > highestVersion:
	highestVersion = version2

    if highestVersion == version or highestVersion == 0:
      return None

    newVersion = str(highestVersion)
    if len(newVersion) < 2:
      newVersion = "0" + newVersion

    return (directory + name + newVersion + extension)	

def addToMenu():
  if nuke.env['gui']:
    nukeMenu = nuke.menu('Nuke')
    menu = nukeMenu.addMenu('DuckTools')

    toolbar = nuke.menu("Nodes")
    m = toolbar.addMenu("DuckTools", "Duckling.png")

    menu.addCommand("Python/Util/Load Latest Version", "python.autoLoadLatestVersion()", "")
    m.addCommand("Python/Util/Load Latest Version", "python.autoLoadLatestVersion()", "")
					    		
addToMenu()

