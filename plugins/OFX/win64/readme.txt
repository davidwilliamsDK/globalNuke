-----------------------------------
---==Lenscare V1.44 for OpenFX==---
-----------------------------------

	This software has been programmed to work in OpenFX compatible hosts like
	Nuke, Digital Fusion and Maya Composite aka Toxik. Lenscare has been tested in the
	named hosts and has been verified to work properly. There are some known problems
	however. Please read about them below.
	
	Other OpenFX hosts should work as well but have not been explicitly tested.
	If you encounter problems in any hosts please send a mail to:
	support (at) frischluft.com


Installation:
-------------
1) install files
	Move all files and folders to the following folder on your machine.
	If you have previous vesions installed please delete them first.

	Linux:   /usr/OFX/Plugins/
	Mac:     /Library/OFX/Plugins/
	Windows: c:\Programm Files\Common Files\Ofx\Plugins\
	 or c:\Programm Files (x86)\Common Files\Ofx\Plugins\
	 if on a 64Bit system
	
	Alternativly you can point the environment variabel OFX_PLUGIN_PATH
	to a folder of your choice and install the plugins there.
	Additionally mosts hosts have their own custom install folders.
	Please consult your hosts documentation for those.

2) install license file
	If you have purchased this software you have received a license file.
	Place that key into the same folder the Lenscare plugins sit in to
	remove the demo restrictions! Removing the demo licenses (demo.lic) is
	not necessary but recommended.

3) restart host
	After you have installed filters and key file please restart your host program.


Finding the plugins:
--------------------
Digital Fusion:
	The plugins will show up in the tools menu under the name 'Frischluft'.

Nuke:
	The plugins will show up in the node menu named 'Frischluft'.

Maya Composite aka Toxik:
	The plugins will show up in the tools palette under an Entry named 'OFX Frischluft'.


Known Problems:
---------------
Toxik:
	- the alpha value of outside color will not work and is always assumed 1.
	- If in the future there is a new plugin versions with a changed or removed
	  parameter that might break your projects and you may have to replace all
	  instances in the old projects. If that should be necessary there will
	  be more detailed information.


Premultiplied / Unpremultiplied:
--------------------------------
Digital Fusion:
	Assumes premultiplied data and we return premultiplied images.
	If your input is unpremultiplied please use a tool with 'post multiply'
	in advance.

Nuke:
	Assumes premultiplied data and we return premultiplied images.
	If your input is unpremultiplied please use the 'Merge/Premultiplication"
	node in advance.

Toxik:
	Assumes unpremultiplied data and we return unpremultiplied images.
	If your input footage is premultiplied you can use the Unpremuliply button in
	the image importer or the node 'Formating/Umpremultiply'.



Change log:
-----------
V1.4.4
    - added custom iris to depth of field (beta status)
    - using host threading now instead of own.
	- improved stability

V1.4.3:
	- changed naming scheme to 'FL Plugin Name' to avoid confusion with existing plugins

V1.4.2:
	- improved stability

V1.4.1:
	- added 64Bit Linux support
	- added Macintosh PowerPC support.
	- Depth of Field: fixed some artefacts that occured depending on a "bad"
					 radius, iris shape and depth buffer combination
	- Depth of Field: fixed potential crash with many cores in low memory conditions
	- Depth of Field: improved behaviour with large and odd core count.
					  3 Core cpus for example will be used more efficiently now. 
	- fixed an aligment problem with the Blend layer
	- fixed a problem where OfxImageEffectActionGetRegionsOfInterest caused
	  a bug and log output on some hosts. It didn't do any harm but was annoying.

	Compatibility updates:
	
	Digital Fusion:
	- worked around a problem where connecting the Blend Input upset Fusion so
	  it would crash or behave in weired ways. Worked around it by renaming the
	  Blend layer to "Blend Clip" only in Digital Fusion.


V1.4: Initial release


-------------------------------------------
Lenscare is a product of frischluft.com
Copyright © 2010. All rights reserved.

website: www.frischluft.com
contact:  info (at) frischluft.ocm
-------------------------------------------