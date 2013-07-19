import os,sys
import platform, subprocess


if platform.system() == "Linux":
    os.environ['NUKE_PATH'] = '/dsGlobal/globalNuke'
    os.environ['NUKE_PLUGINS_PATH'] = '/dsGlobal/globalNuke/plugins'
    os.environ['NUKE_GIZMO_PATH'] = '/dsGlobal/globalNuke/gizmos'
    os.environ['NUKE_PYTHON_PATH'] = '/dsGlobal/globalNuke/Python'
    os.environ['OFX_PLUGIN_PATH'] = '/dsGlobal/globalNuke/plugins/OFX/Linux/OFX'
    os.environ['RVL_SERVER'] = '192.168.1.250'
    subprocess.call(["/usr/local/Nuke7.0v6/Nuke7.0"])

if platform.system() == "Windows":
    os.environ['NUKE_PATH'] = '//vfx-data-server/dsGlobal/globalNuke'
    os.environ['NUKE_PLUGINS_PATH'] = '//vfx-data-server/dsGlobal/globalNuke/plugins'
    os.environ['NUKE_GIZMO_PATH'] = '//vfx-data-server/dsGlobal/globalNuke/gizmos'
    os.environ['NUKE_PYTHON_PATH'] = '//vfx-data-server/dsGlobal/globalNuke/python'
    os.environ['OFX_PLUGIN_PATH'] = '//vfx-data-server/dsGlobal/globalNuke/plugins/OFX/win64'
    os.environ['RVL_SERVER'] = '192.168.1.250'
    sys.path.append("//vfx-data-server/dsGlobal/dsCore/nuke")
    cmd = "\"C:/Program Files/Nuke7.0v6/Nuke7.0.exe\" --nukex"
    os.system(cmd)