# Run in Blender

import bpy
import colorsys
import numpy as np
from mathutils import Vector
import sys
import os

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

import blender_v1_linha_linha as blender
from utils import clamp

# Setting files params

labels_file_name = 'Labels\\img_'
set_len = 15
object_name = '1'

# Getting the scene

scene = bpy.context.scene
light = bpy.data.objects['Light']
camera = bpy.data.objects['Camera']
drone = bpy.data.objects['Drone']
balde = bpy.data.objects[object_name]
tampo = bpy.data.objects['T' + object_name]

n = len(balde.data.vertices)
balde_center = sum([balde.data.vertices[i].co for i in range(n)], Vector( ))/n/100

radius = 1
light_scale = 1

# Creating the random dataset to training the CNN

for i in range(set_len):

    light.data.energy = np.random.uniform(0.3*light_scale, 4*light_scale)
    light.data.color = colorsys.hsv_to_rgb(np.random.uniform(0, 1), np.random.uniform(0, 0.8), 1)

    camera.location = (balde_center[0] + np.random.uniform(-radius, radius), balde_center[1] + np.random.uniform(-radius, radius), np.random.uniform(2, 6))
    drone.location = camera.location
    camera.rotation_euler = (np.random.uniform(-np.pi/24, np.pi/24), np.random.uniform(-np.pi/24, np.pi/24), np.random.uniform(-np.pi, np.pi))
    drone.rotation_euler = camera.rotation_euler
    camera.data.lens = np.random.random_integers(5, 9)

    scene.render.filepath = "//dataset/" + "img_" + str(i) + ".png"

    bpy.ops.render.render(write_still = True)

    cam = blender.Cam(camera, scene)

    with open(labels_file_name + str(i) + '.txt', 'a') as file:

        image_balde = blender.Image_object(balde, cam)
        image_balde.set_bounding_box( )
        bbox_balde = image_balde.get_bounding_box(center = False)

        image_tampo = blender.Image_object(tampo, cam)
        image_tampo.set_bounding_box( )
        bbox_tampo = image_tampo.get_bounding_box(center = False)

        x_min = clamp(bbox_balde[0], bbox_tampo[0], bbox_tampo[1])
        x_max = clamp(bbox_balde[1], bbox_tampo[0], bbox_tampo[1])
        y_min = clamp(bbox_balde[2], bbox_tampo[2], bbox_tampo[3])
        y_max = clamp(bbox_balde[3], bbox_tampo[2], bbox_tampo[3])

        bbox = ((x_min + x_max)/2, (y_min + y_max)/2, x_max - x_min, y_max - y_min)
        
        if bbox_balde[2] != .0 and bbox_balde[3] != .0:
            
            file.write("1 %f %f %f %f\n" % bbox)


