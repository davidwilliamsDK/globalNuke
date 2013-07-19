def projectionCam():
    f = nuke.frame()
    p = nuke.Panel( "Projection Frame" )
    p.addSingleLineInput( "Frame:", f )
    result = p.show()
    if result == 1:
        nuke.frame( int( nuke.expression( p.value( "Frame:" ) ) ) )
    
        selCam = nuke.selectedNode()
        verStr = nuke.NUKE_VERSION_STRING
        if verStr[0] == 6:
            if verStr[2] == 1:
                knobs = [ 'xform_order', 'rot_order', 'scaling', 'uniform_scale', 'skew', 'pivot', 'useMatrix', 'matrix', 'world_matrix', 'projection_mode', 'focal', 'haperture', 'vaperture', 'near', 'far', 'win_translate', 'win_scale', 'winroll', 'focal_point' ]
        else:
            knobs = [ 'xform_order', 'rot_order', 'scaling', 'uniform_scale', 'skew', 'pivot', 'projection_mode', 'focal', 'haperture', 'vaperture', 'near', 'far', 'win_translate', 'win_scale', 'winroll', 'focal_point' ]
        nuke.selectAll()
        nuke.invertSelection()
        projCam = nuke.createNode( 'Camera2' )


        frameTab = nuke.Tab_Knob( 'Frame' )
        frameVal = nuke.Int_Knob( 'frameValue', 'Frame:' )

        frameVal.setValue( int( nuke.expression( p.value( "Frame:" ) ) ) )

        for k in [ frameTab, frameVal ]:
            projCam.addKnob( k )
    
        for x in [ 'translate','rotate' ]:
          for y in [0,1,2]:
             projCam[ x ].setExpression( '%s.%s( frameValue )' % ( selCam[ 'name' ].value(), x ), y )
        
        if selCam[ 'focal' ].isAnimated() == True:
            projCam[ 'focal' ].setExpression( '%s.%s( frameValue )' % ( selCam[ 'name' ].value(), 'focal' ) )

        projCam[ 'read_from_file' ].setValue( False )
        projCam[ 'label' ].setValue( 'projCam\nframe [ value frameValue ]' )

        for each in knobs:
            projCam[ each ].setExpression( '%s.%s' % ( selCam[ 'name' ].value(), each ) )

        r = 0
        g = .5
        b = 1
        
        hexColour = int( '%02x%02x%02x%02x' % ( r*255, g*255, b*255, 1 ), 16 )
        projCam[ 'tile_color' ].setValue( hexColour )

