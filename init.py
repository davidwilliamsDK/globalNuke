CUSTOM_GIZMO_LOCATION = r''
try:
	import assetManager
except:
	pass

import os,re,sys,platform

def filenameFix(filename):
	if platform.system() in ("Windows", "Microsoft"):
		if filename.replace("dsComp/","S:\\"):
			return filename.replace( "/dsComp/", "S:\\" )
		
		if filename.replace("dsPipe/","P:\\"):
			filename.replace("dsPipe/","P:\\")
		nuke.tprint(filename)
	else:
		if filename.replace( "S:\\", "/dsComp/" ):
			return filename.replace( "S:\\", "/dsComp/" )
		
		if filename.replace( "P:\\", "/dsPipe/" ):
			return filename.replace( "P:\\", "/dsPipe/" )
		nuke.tprint(filename)
		
	return filename
	nuke.tprint(filename)

#WILL CREATE FOLDER ON THE FLY
nuke.knobDefault( 'Write.beforeRender', 'assetManager.createOutDirs()')

class GizmoPathManager(object):
	def __init__(self, exclude=r'^\.', searchPaths=None):
		
		if isinstance(exclude, basestring):
			exclude = re.compile(exclude)
		self.exclude = exclude
		if searchPaths is None:
			searchPaths = os.environ.get('NUKE_GIZMO_PATH', '').split(os.pathsep)
			if not searchPaths:
				import inspect
				thisFile = inspect.getsourcefile(lambda: None)
				if thisFile:
					searchPaths = [os.path.dirname(os.path.abspath(thisFile))]
				else:
					searchPaths = list(nuke.pluginPath())
		self.searchPaths = searchPaths
		self.reset()
		
	def canonical_path(cls, path):
		return os.path.normcase(os.path.normpath(os.path.realpath(os.path.abspath(path))))

	def reset(self):
		self._crawlData = {}

	def addGizmoPaths(self):
		self.reset()
		self._visited = set()
		for gizPath in self.searchPaths:
			self._recursiveAddGizmoPaths(gizPath, self._crawlData,foldersOnly=True)

	def _recursiveAddGizmoPaths(self, folder, crawlData, foldersOnly=False):
		if not os.path.isdir(folder):
			return
		if nuke.GUI:
			if 'files' not in crawlData:
				crawlData['gizmos'] = []
			if 'dirs' not in crawlData:
				crawlData['dirs'] = {}
		canonical_path = self.canonical_path(folder)
		if canonical_path in self._visited:
			return
		self._visited.add(canonical_path)
		
		for subItem in sorted(os.listdir(canonical_path)):
			if self.exclude and self.exclude.search(subItem):
				continue
			subPath = os.path.join(canonical_path, subItem)
			if os.path.isdir(subPath):
				nuke.pluginAppendPath(subPath)
				subData = {}
				if nuke.GUI:
					crawlData['dirs'][subItem] = subData
				self._recursiveAddGizmoPaths(subPath, subData)
			elif nuke.GUI and (not foldersOnly) and os.path.isfile(subPath):
				name, ext = os.path.splitext(subItem)
				if ext == '.gizmo':
					crawlData['gizmos'].append(name)
					nuke.tprint("pathAdded " + subPath)
					
	def addGizmoMenuItems(self, toolbar=None, defaultTopMenu=None): 
		if not self._crawlData:
			self.addGizmoPaths()
		if toolbar is None:
			toolbar = nuke.menu("Nodes")
		elif isinstance(toolbar, basestring):
			toolbar = nuke.menu(toolbar)
		self._recursiveAddGizmoMenuItems(toolbar, self._crawlData, defaultSubMenu=defaultTopMenu, topLevel=True)

	def _recursiveAddGizmoMenuItems(self, toolbar, crawlData,defaultSubMenu=None, topLevel=False):
		for name in crawlData.get('gizmos', ()):
			niceName = name
			if niceName.find('_v')==len(name) - 4:
				niceName = name[:-4]
			toolbar.addCommand(niceName,"nuke.createNode('%s')" % name)

		for folder, data in crawlData.get('dirs', {}).iteritems():
			subMenu = toolbar.findItem(folder)
			if subMenu is None:
				if defaultSubMenu:
					subMenu = toolbar.findItem(defaultSubMenu)
				else:
					#subMenu = toolbar.addMenu(folder)
					subMenu = toolbar.addMenu(folder, icon='%s.png' % folder)
				nuke.tprint("menu Created " + folder)
			self._recursiveAddGizmoMenuItems(subMenu, data) 

class ppManager(object):
	def __init__(self):
		toolbar = nuke.toolbar('Nodes')
		for root, dirs, files in os.walk(NUKE_PYTHON_PATH):
			if platform.system() == "Windows":
				rootBase = root.split("%s%spython%s" % (NUKE_PATH, os.sep, os.sep))
				rootbase = rootBase[0].replace("\\", "/")
				baseList = rootbase.split("python")
				toolBoxList = baseList[-1].split("/")
				
			if platform.system() == "Linux":
				rootBase = [root]
				rootbase = root
				baseList = rootbase.split("python")
				toolBoxList = baseList[-1].split("/")
				
			if len(toolBoxList) > 1:
				base = baseList[-1]
				for file in files:
					if not re.search("ui",file):
						match = re.match("(^[^_].*)\.py$", file)
						if match:
							menuItem = match.group(1)
							shortCut = ""
							shortCutFile = "%s/%s.txt" % (root, menuItem)
							if os.path.exists(shortCutFile):
								shortCut = open(shortCutFile, 'r').read()
							toolbar.addCommand("%s/%s" % (base[1:], menuItem), "nuke.load('%s/%s'), %s()" % (root.replace("\\", "/"), menuItem, menuItem), "%s" % shortCut)
							#nuke.tprint("%s/%s" % (base[1:], menuItem), "nuke.load('%s/%s'), %s()" % (root.replace("\\", "/"), menuItem, menuItem), "%s" % shortCut)
							
		toolbar = nuke.toolbar('Nodes')
		pluginType = {'win32': 'dll', 'linux2': 'so', 'darwin': 'dylib','win64': 'dll'}
		for root, dirs, files in os.walk(NUKE_PLUGINS_PATH):
			rootBase = root.split("%s%splugins%s" % (NUKE_PATH, os.sep, os.sep))
			rootbase = rootBase[0].replace("\\", "/")
			baseList = rootbase.split("plugins")
			toolBoxList = baseList[-1].split("/")
			if len(toolBoxList) > 1:
				base = baseList[-1]
				for file in files:
					if re.match(".*\.%s$" % (pluginType[sys.platform]), file):
						menuItem = file.rstrip('.%s' % pluginType[sys.platform])
						shortCut = ""
						shortCutFile = "%s/%s.txt" % (root, menuItem)
						if os.path.exists(shortCutFile):
							shortCut = open(shortCutFile, 'r').read()
							toolbar.addCommand("%s/%s" % (base[1:], menuItem), "nuke.createNode('%s')" % (menuItem), "%s" % shortCut)
		nuke.tprint("added all PP")

class farmStuff(object):
	''' For Farm DO NOT TOUCH... if NUKE_PATH needs to change it will need to change here...'''
	def __init__(self, exclude=r'^\.'):
		NUKE_PATH = '/dsGlobal/globalNuke' 
		for root, dirs, files in os.walk(NUKE_PATH):
			if files:
				for file in files:
					""" Adds all gizmos and plugins directories to nuke.pluginPath """
					if file.endswith('.gizmo') or file.endswith('.so') or file.endswith('.bundle'):
						if not root in nuke.pluginPath():
							nuke.pluginAddPath(root,addToSysPath=False)
					""" Adds all python directories to sys.path """
					if file.endswith('.py'):
						if not root in sys.path:
							sys.path.append(root)
							
if __name__ == '__main__':

	nuke.pluginAddPath('./icons', addToSysPath=False)
	nuke.pluginAddPath('./fonts', addToSysPath=False)
	nuke.pluginAddPath('//vfx-data-server/dsGlobal/dsCore/nuke')
	
	NUKE_PYTHON_PATH = os.environ['NUKE_PYTHON_PATH']
	NUKE_PATH = os.environ['NUKE_PATH']
	NUKE_PLUGINS_PATH = os.environ['NUKE_PLUGINS_PATH']
	
	if CUSTOM_GIZMO_LOCATION and os.path.isdir(CUSTOM_GIZMO_LOCATION):
		gizManager = GizmoPathManager(searchPaths=[CUSTOM_GIZMO_LOCATION])
	else:
		gizManager = GizmoPathManager()

	gizManager.addGizmoPaths()

	if not nuke.GUI:
		# We're not gonna need it anymore, cleanup...
		del gizManager
		farmManager = farmStuff()