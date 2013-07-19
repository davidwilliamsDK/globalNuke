import nuke, re

'''/dsComp/Lego_Hollywood/Film/Episode_01/Q0010/S0010/comp/3dExports/Q0010_S0010_camera.nk'''
'''\\xserv2\VFXSAN\dsComp\Lego_Hollywood\Film\Episode_01\Q0630\S0010\comp\nukeScripts'''
class Eye_Fix():
    
    def __init__(self):
        if sys.platform == "linux2":
            self.dsPipe = '/dsPipe'
            self.dsComp = '/dsComp'
        elif sys.platform == 'win32':
            self.dsPipe = '//vfx-data-server/dsPipe'
            self.dsComp = '//xserv2/VFXSAN/dsComp'
        
        self.nuke_fix_eye( self.get_camera() )
        
    def get_camera(self):
        path = nuke.root().knob('name').getValue()
        if path:
                print path
                match = re.search(r'([qQ][0-9][0-9][0-9][0-9])\/([sS][0-9][0-9][0-9][0-9])', path)
                if match:
                    self.sq, self.sh = match.groups()
                    filename = '%s/Lego_Hollywood/Film/Episode_01/%s/%s/comp/3dExports/%s_%s_Camera.nk' % (self.dsComp, self.sq, self.sh, self.sq, self.sh)
                    return filename
                else:
                    return None
                    print 'No match'
                    
        else:
            print 'please save your scene'
            return None
    
    def nuke_fix_eye(self, file):
        if file:
            d = {}
            nuke.nodePaste('//vfx-data-server/dsPantry/Python/dsPublishNukeScript/eye_reflections.nk')
            nuke.nodePaste(file)
            
            node_switch = None
            node_dotA = None
            node_dotB = None
            node_merge = None
            node_camera = None
            node_relight = None
            node_hold = None
            node_read = None
            
            node_merge = nuke.toNode('eyefix_Merge')
            d['node_merge'] = node_merge
            node_camera = nuke.toNode('%s_%s' % (self.sq, self.sh))
            d['node_camera'] = node_camera
            node_relight = nuke.toNode('eyefix_EnvRelight')
            d['node_relight'] = node_relight
            node_dotA = nuke.toNode('eyefix_DOTa')
            d['node_dotA'] = node_dotA
            node_hold = nuke.toNode('eyefix_FrameHold')
            d['node_hold'] = node_hold
            node_read = nuke.toNode('Read1')
            d['node_read'] = node_read

            
            for node in nuke.allNodes('Switch'):
                for input_node in node.dependencies(nuke.INPUTS):
                    if 'Distance_haze' in input_node.name():
                        node_switch = node
                        d['node_switch'] = node_switch
            for node in nuke.allNodes('Dot'):
                for input_node in node.dependencies(nuke.INPUTS):
                    if input_node == node_switch and not node == node_dotA:
                        node_dotB = node
                        d['node_dotB'] = node_dotB
                      
            for key, value in d.items():
                if not value:
                    print 'Couldnt find %s.' % key
                
            if node_read and node_hold:
                node_hold.connectInput(0, node_read)
                
            if node_relight and node_camera:
                node_relight.connectInput(2, node_camera)
                
            if node_switch and node_dotA and node_dotB:
                node_dotA.connectInput(0, node_switch)
                node_dotB.connectInput(0, node_merge)
            else:
                if not node_switch:
                    print 'Couldnt find node switch.'
                elif not node_dotA:
                    print 'Couldnt find node dotA.'
                elif not node_dotB:
                    print 'Couldnt find node dotB.'
                        

#Eye_Fix()