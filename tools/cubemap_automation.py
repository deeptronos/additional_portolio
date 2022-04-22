import bpy
import math
import os

myCamera = ""
originalSceneCamera = ""

originalFilepath = bpy.context.scene.render.filepath

for i in range(len(bpy.data.objects)): # try and set myCamera
    if bpy.data.objects[i].name == "cubemap_renderer":
        myCamera = bpy.data.objects[i]

if myCamera == "": #if myCamera is not set, raise ValueError
    raise ValueError("Create and position a camera named 'cubemap_renderer' before attempting to use this script.")       

myCamera.rotation_euler =(0.0, 0.0, 0.0) # zero-out camera rotation

if bpy.data.scenes["Scene"].camera != myCamera:
    originalSceneCamera =  bpy.data.scenes["Scene"].camera # save original camera
    bpy.data.scenes["Scene"].camera = myCamera # set scene camera



def renderCubemapFace(direction): # Render a "face" of the cubemap, in the specified direction
    
    bpy.context.scene.render.filepath = originalFilepath + direction + ".png" # set filepath
    
    # Rotate camera according to direction:
    if direction == "forward":
        myCamera.rotation_euler = (math.radians(90), 0.0, 0.0)
    elif direction == "backward":
        myCamera.rotation_euler = (math.radians(90), 0.0, math.radians(180))
    elif direction == "down":
        myCamera.rotation_euler = (0.0, 0.0, 0.0)
    elif direction == "up":
        myCamera.rotation_euler = (math.radians(180), 0.0, 0.0)
    elif direction == "left":
        myCamera.rotation_euler = (math.radians(90), 0.0, math.radians(90))
    elif direction == "right":
        myCamera.rotation_euler = (math.radians(90), 0.0, math.radians(270))
    else:
        raise ValueError("renderCubemapFace called with invalid direction.")
        return '0'
        #continue
    
    bpy.ops.render.render(write_still=True) # render and save output
    
# comment the below lines as is needed: 
#for d in ["forward", "backward", "down", "up", "left", "right"]: 
for d in ["up", "left", "right"]:
    renderCubemapFace(d)                     
      
    