import maya.cmds as mc
import pymel.core as pm  
from os import listdir   
  
def main(*arg):
    selectionList = pm.ls(sl=True)

    basicFilter = "Image Files (*.TGA *.tga *.DDS *.dds *.PNG *.png)"
    global path
    path = pm.fileDialog2(fileFilter=basicFilter, dialogStyle=2, fm=3)
    files = listdir(path[0])
    global ddsFiles
    ddsFiles = []
    print (ddsFiles)
    for item in files:
        fileEndings = ('.TGA', '.tga', '.DDS', '.dds', '.PNG', '.png')
        if (item.endswith(fileEndings)):
            ddsFiles.append(item)
    mat()    

def applyMaterial(node):
    if mc.objExists(node):
                
        # base
        shd = mc.shadingNode('aiStandardSurface', name = "%s_aiStandardSurface " % node, asShader=True)
        shdSG = mc.sets(name='%sSG' % shd, empty=True, renderable=True, noSurfaceShader=True)
        mc.connectAttr('%s.outColor' % shd, '%s.surfaceShader' % shdSG)
        mc.sets(node, e=True, forceElement=shdSG)
        # basecolor
        fileBaseColor = mc.shadingNode('file', name="%s_fileBasseColor" % node, asTexture=True )
        mc.setAttr(fileBaseColor + '.colorSpace', 'sRGB', type='string')
        mc.connectAttr('%s.outColor' % fileBaseColor, '%s.baseColor' % shd)  
        mc.setAttr('%s.fileTextureName' % fileBaseColor, path[0] + '/' + str(ddsFiles[0]), type="string")
        # roughness
        fileRoughness = mc.shadingNode('file', name="%s_fileRoughness" % node, asTexture=True )
        mc.setAttr(fileRoughness + '.colorSpace', 'Raw', type='string')
        #mc.setAttr(fileRoughness + '.colorSpace', 'Raw', type='bool')
        mc.connectAttr('%s.outColorR' % fileRoughness, '%s.specularRoughness' % shd)
        mc.setAttr('%s.fileTextureName' % fileRoughness, path[0] + '/' + str(ddsFiles[4]), type="string")
        # metalic
        fileMetalic = mc.shadingNode('file', name="%s_fileMetalic" % node, asTexture=True )
        mc.setAttr(fileMetalic + '.colorSpace', 'Raw', type='string')
        mc.connectAttr('%s.outColorR' % fileMetalic, '%s.metalness' % shd)
        mc.setAttr('%s.fileTextureName' % fileMetalic, path[0] + '/' + str(ddsFiles[2]), type="string")    
        #normal   
        fileNormal = mc.shadingNode('file', name="%s_fileNormal" % node, asUtility=True)
        bump = mc.shadingNode('bump2d', name="%s_bump2d" % node, asTexture=True)
        mc.setAttr(fileNormal + '.colorSpace', 'Raw', type='string')
        mc.setAttr(bump + ".bumpInterp", 1)
        mc.connectAttr('%s.outAlpha' % fileNormal, '%s.bumpValue' % bump)
        mc.connectAttr(bump + ".outNormal", shd + ".normalCamera")
        mc.setAttr('%s.fileTextureName' % fileNormal, path[0] + '/' + str(ddsFiles[3]), type="string")
        #ambient
        fileAmbient = mc.shadingNode('file', name="%s_fileAmbient" % node, asTexture=True)
        mc.setAttr(fileAmbient + '.colorSpace', 'sRGB', type='string')
        #mc.connectAttr(fileAmbient + ".outAlpha", shd + ".base")        

def mat(*arg):
    selection = cmds.ls(sl=True)
    myObjectName = selection[0]
    
    for myObjectNames in selection:  
        applyMaterial(myObjectName)   
        
#pm.window(title='Auto ShaderLab', width=200)
#pm.columnLayout(adjustableColumn=True)

#pm.button(label = 'applyMaterial', command=main)
#pm.showWindow()

main()