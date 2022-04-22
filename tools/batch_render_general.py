import bpy
import os
from math import radians
from math import degrees
from mathutils import Matrix


#NOTE:
    #    Output set-up in compositer is essential to defining what this script renders/outputs.

increments_deg  = -15
increments_rad  = radians(increments_deg)
    #We have 24 angles that we want to render, because each is an increment of 15, and 360/15 = 24
angles          = 360/abs(increments_deg) 
curr_angle      = 0
    #Amount of frames to render
render_frames_length = 1

    #Start at frame 0
bpy.context.scene.frame_current = 0 
#default_path = '/Volumes/MISC/Senior Project/Visual Art/3D/Renders/Rig Test/Animation_Rotation_Test_10fps/walk_loop'
default_path = '/Volumes/MISC/Synced/Senior Project/Visual Art/3D/Renders/gun-depth-normal-test'
bpy.data.scenes["Scene"].node_tree.nodes["File Output"].base_path = default_path
    #Set rotation of camera parent to 0 before we begin rendering
bpy.data.scenes["Scene"].objects['CameraCenter'].rotation_euler[2] = 0
    #Set the original base path before we start messin with it
orig_base_path = bpy.data.scenes["Scene"].node_tree.nodes["File Output"].base_path 
 
viewport_state = False 
 
#Messy fix to solve the weird way Blender doesn't let you rearrange view later orders in the GUI
#if bpy.data.scenes["Scene"].view_layers.items()[2][0] == 'Body':
#  
#    init_body_layer = bpy.data.scenes["Scene"].view_layers.items()[2]
#    init_head_layer = bpy.data.scenes["Scene"].view_layers.items()[3]

#    bpy.data.scenes["Scene"].view_layers.items()[2] = init_head_layer
#    bpy.data.scenes["Scene"].view_layers.items()[3] = init_body_layer


#finding active render passes:
#render_passes = []
#for attr in dir(bpy.context.view_layer):
#    if attr.startswith("use_pass") and getattr(bpy.context.view_layer, attr) == True:
#        render_passes.append(attr)
    

for i in range(int(angles)):
    #Reset the variable each time, so that we aren't adding numbers each time
    base_path = orig_base_path
        #Start at frame 0 every time we rotate the camera
    bpy.context.scene.frame_current = 0 
    
    base_path += ("/" + str(int(i) * abs(increments_deg)))
    print(base_path)
    try:
        os.mkdir(base_path)
        bpy.data.scenes["Scene"].node_tree.nodes["File Output"].base_path = base_path
    except FileExistsError:
        print("directories already exist :)")
        bpy.data.scenes["Scene"].node_tree.nodes["File Output"].base_path = base_path
     
    
    #Makes sure each layer gets rendered
    for j in bpy.data.scenes["Scene"].view_layers.items():
           
            #Since body is the only animated layer:
        if j[0] == "Body":
             #Renders frames determined by render_frames_length    
            for k in range(render_frames_length):
                bpy.data.scenes["Scene"].node_tree.nodes["File Output"].file_slots[0].path = j[0]
                bpy.data.scenes["Scene"].node_tree.nodes["Render Layers"].layer = j[0]
                bpy.ops.render.render(animation=False,write_still=True,use_viewport=viewport_state,layer='Body',scene="Scene")
                bpy.context.scene.frame_current += 1
        else:
            bpy.context.scene.frame_current = 0
            bpy.data.scenes["Scene"].node_tree.nodes["File Output"].file_slots[0].path = j[0]
            bpy.data.scenes["Scene"].node_tree.nodes["Render Layers"].layer = j[0]
                #Renders whatever we have set up in the compositer to render
            bpy.ops.render.render(animation=False,write_still=True,use_viewport=viewport_state,layer=j[0],scene="Scene")
    
    
    
            #Rotate the camera parent by our increment value in radians
    bpy.data.scenes["Scene"].objects['CameraCenter'].rotation_euler[2] += increments_rad

        #Print current degrees of rotator (for debugging)
    curr_angle = degrees(bpy.data.scenes["Scene"].objects['CameraCenter'].rotation_euler[2])
    print(str(curr_angle))
    
    #print(3 * '\n')        
    
          


 #bpy.ops.transform.rotate(value=increments_rad, orient_axis='Z', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1.67, use_proportional_connected=False, use_proportional_projected=False)