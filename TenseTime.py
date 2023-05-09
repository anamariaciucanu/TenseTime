import maya.cmds as cmds

#Tense Time is a script that reads an XML with symbols of speed and tension, then applies it to a primitive object

#Wrapping the UI into a function
def tenseTime_UIWindow():
    # Make a new window
    window = cmds.window( title="Time and Tension", iconName='Time Tension', widthHeight=(200, 100), sizeable=False)
    
    #Column layout will accept widgets
    cmds.columnLayout( adjustableColumn=True )
    
    #Buttons will be parented to column layout
    cmds.button( label='Do Nothing' )
    
    #Buttons in a row (testing purposes)
    cmds.rowLayout(adjustableColumn = 2, numberOfColumns =4)
    cmds.button(label='Cube', command="cmds.polyCube()")
    cmds.button(label='Sphere', command = "cmds.polySphere()")
    cmds.button(label='Torus', command = "cmds.polyTorus()")
    cmds.setParent( '..' )
    
    #Closes the window
    cmds.button( label='Close', command=('cmds.deleteUI(\"' + window + '\", window=True)') )
    
    cmds.showWindow( window )

tenseTime_UIWindow()