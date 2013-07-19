import nuke

def channelShuffling():
    '''
    First get the selection of the read node that you want to split into shuffle nodes
    Clean up the channel list
    Set values of the shufflenodes
    Connect the shuffle to the selection
    '''
    if nuke.selectedNode() and nuke.selectedNode().Class() == 'Read':
        node = nuke.selectedNode()
        dot = nuke.createNode('Dot')
        channelList = []
        
        #print node.name()
        #print node.knob('name').value()
        print node.channels()
        for channel in node.channels():
            cleanChannel = channel.split('.')[0]
            if cleanChannel not in channelList:
                channelList.append(cleanChannel)
        #print node.xpos(),len(channelList)/2
        
        x = node.xpos() - (100 * len(channelList)/2)
        y = node.ypos() + 100
        #print node.Class()
        #print channelList
        lastShuffle = None
        for chan in channelList:
            
            shuffle = nuke.createNode('Shuffle')
            stamp = nuke.createNode('PostageStamp')

            
            if lastShuffle:
                shuffle.setInput(0, lastShuffle)
            
            shuffle.knob('name').setValue('%s_%s' % (node.name(), chan))
            stamp.knob('name').setValue('postage_%s_%s' % (node.name(), chan))
            shuffle.knob('in').setValue(chan)
            shuffle.setXYpos( x, y)
            x += 100
            
            #shuffle.knob('hide_input').setValue('true')
            #stamp.knob('hide_input').setValue('true')
            
            lastShuffle = shuffle