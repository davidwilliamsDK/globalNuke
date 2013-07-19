#import ShotGunDropper
#reload(ShotGunDropper)
#nukescripts.dropData = ShotGunDropper.dropData


if __name__ == '__main__':
  # Just in case they didn't use the supplied init.py
  gizManager = globals().get('gizManager', None)
  ppManager = globals().get('ppManager',None)
  if gizManager is None:
      print 'Problem finding GizmoPathManager - check that init.py was setup correctly'
  else:
      gizManager.addGizmoMenuItems()
      # Don't need it no more...
      del gizManager

  if ppManager is None:
      print 'Problem finding PPPathManager - check that init.py was setup correctly'
  else:
      pluginManager = ppManager()
      #pluginManager.loadPython()
      # Don't need it no more...
      del pluginManager
