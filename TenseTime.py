import maya.cmds as cmds
import xml.etree.ElementTree as ET

#Tense Time is a script that reads an XML with symbols of speed and tension, then applies it to a primitive object

#Define some variables
rotationDirection = 1
xmlFilePath = open(r"C:\Users\55135783\OneDrive - MMU\02_Research\LabanProceduralAnimation\Scripts\TenseTime_Phrasing1.xml")
               
#Funtion to read an xml file and return an array of phrases. These phrases will be stored as (speed, tension) tuples where each value can go from 1 to 10.
def getXMLSpeedTensionList(path):
    xmlFile = ET.parse(path)
    xmlRoot = xmlFile.getroot()
    numberOfPhrases = len(xmlRoot)
    speedTensionList =  [[0 for x in range(2)] for y in range(numberOfPhrases)] 
    
    for p in range(numberOfPhrases): #goes through phrases
        speedTensionList [p][0] = xmlRoot[p][0].text    
        speedTensionList [p][1] = xmlRoot[p][1].text                                
    print (speedTensionList)
    return speedTensionList

def processSpeed(_speed):
    #Values of speed should be capped at [1, 10] (low to high)
    #High speed means timing is fast => 10 would mean keyframe every 2 frames, 1 would mean keyframe every 30 frames
    a = 1
    b = 10
    c = 2 #minimum frame rate
    d = 30 #maximum frame rate
    
    if _speed >= 10:
        return c
    elif _speed <= 1:
        return d
    else:
        val = round(((_speed - a)*(d-c) / (b - a)) + c)
        return val
        

def processTension(_tension):
    #Tension is described as relaxed vs strong
    #It can be linked to spacing and jittering
    #Large tension means large spacing, and large jittering
    a = 1
    b = 10
    c = 0.5 #minimum translation rate
    d = 7 #maximum translation rate
    e = 0 #minmum rotation
    f = 5 #maximum rotation
    
    tensionArray = [0, 0]
    global rotationDirection
    
    if _tension >= 10:
        tensionArray = [d, rotationDirection * f]
    elif _tension <= 1:
        tensionArray = [c, rotationDirection * e]
    else:
        valTranslationX = round(((_tension - a)*(d-c) / (b - a)) + c)
        valRotationX = rotationDirection * round((_tension - a)*(f-e) / (b - a))
        tensionArray = [valTranslationX, valRotationX]
    
    rotationDirection = rotationDirection * -1
        
    return tensionArray

#Keyframes speed and tension properties based on current phrase
def keyframeSpeedTension(_speed, _tension, _currentFrame):
    #Tension indicates spacing => Strong = large spacing at ends, Light = tight spacing at ends
    #Process speed and tension and translate them into timing and spacing
    tensionArray = processTension(int(_tension))
    frameRate = processSpeed (int(_speed))
    
    #X translation
    oldTranslationX = cmds.getAttr('movingObject.translateX')
    currentTranslationX = oldTranslationX + tensionArray[0]
    
    #X Rotation
    oldRotationX = cmds.getAttr ('movingObject.rotateX')
    currentRotationX = tensionArray[1]
    
    #Select moving object
    cmds.select( 'movingObject', visible=True )
    if _currentFrame <= 1:
        cmds.currentTime( _currentFrame, edit=True )
        cmds.setKeyframe( v = oldTranslationX, at='translateX' )
        cmds.setKeyframe( v = oldRotationX, at='rotateX')
        
    #Current frame
    currentFrame = _currentFrame + frameRate    
   
    #Set key to current key    
    cmds.currentTime(currentFrame, edit=True )
    cmds.setAttr('movingObject.translateX', currentTranslationX)
    cmds.setKeyframe( v=currentTranslationX, at='translateX' ) 
    cmds.setAttr('movingObject.rotateX', currentRotationX)
    cmds.setKeyframe( v=currentRotationX, at='rotateX' ) 
     
    return currentFrame

    
    
def wrap_fnct_keyframeSpeedTension(_speedTensionList):
    def wrapper1(_): #Overlook False input
        #Use speed tension list to move the object and keyframe its position
        numberOfPhrases = len(_speedTensionList)
        currentFrame = 1
        for x in range (numberOfPhrases):
            speed = _speedTensionList[x][0]
            tension = _speedTensionList[x][1]
            currentFrame = keyframeSpeedTension(speed, tension, currentFrame)
    return wrapper1

#Create a mesh to move through the scene    
def wrap_fnct_createObject(typeOfObjectString):
    def wrapper2(_): #Overlook False input
        #Create an object depending on the type
        if typeOfObjectString == 'cube':
            cmds.polyCube( width=5, height=5, depth=5, name='movingObject')
        elif typeOfObjectString == 'sphere':
            cmds.polySphere( radius=5, name='movingObject')
        elif typeOfObjectString == 'cone':
            cmds.polyCone( radius=5, height = 8, name='movingObject')
    return wrapper2
      
#Wrapping the UI into a function
def tenseTime_UIWindow():    
    #Get Speed and Tension values from XML file
    mySpeedTensionList = getXMLSpeedTensionList(xmlFilePath)   
    
    # Make a new window
    window = cmds.window( title="Time and Tension", iconName='Time Tension', widthHeight=(250, 80), sizeable=False)
    
    #Column layout will accept widgets
    cmds.columnLayout( adjustableColumn=True )
    
    #Buttons in a row (testing purposes)
    cmds.rowLayout(adjustableColumn = 2, numberOfColumns = 2)
    cmds.button(label='Create Object', command=wrap_fnct_createObject('cone'))
    cmds.button(label='Create Phrasing', command = wrap_fnct_keyframeSpeedTension(mySpeedTensionList))
    cmds.setParent( '..' )
    
    #Closes the window
    cmds.button( label='Close', command=('cmds.deleteUI(\"' + window + '\", window=True)') )
    
    cmds.showWindow( window )


tenseTime_UIWindow()
