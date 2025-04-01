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
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

import blender_ap as blender
from utils import clamp

# Setting files params

### Edit here

labels_files_path = 'Campo_labels\\'
labels_files_name = 'img_'
images_files_path = 'Campo_images\\'
images_files_name = 'img_'

set_len = 5

### No edit here

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
labels_files_path = os.path.join(base_path, labels_files_path)
images_files_path = os.path.join(base_path, images_files_path)

# Getting the scene

scene = bpy.context.scene
light = bpy.data.objects['Light']
camera = bpy.data.objects['Camera']
drone = bpy.data.objects['Drone']
origin = bpy.data.objects['Origin']
baldes = [bpy.data.objects[str(i + 1)] for i in range(3)]
tampos = [bpy.data.objects['T' + str(i + 1)] for i in range(3)]

origin_center = sum((v.co for v in origin.data.vertices), Vector( ))/len(origin.data.vertices)/100

r_x = 15/2
r_y = 2
light_scale = 1

# Creating the random dataset to training the CNN

for i in range(set_len):

    light.data.energy = np.random.uniform(0.3*light_scale, 4*light_scale)
    light.data.color = colorsys.hsv_to_rgb(np.random.uniform(0, 1), np.random.uniform(0, 0.8), 1)

    # np.random.normal(0, r_x/ppf(c))

    camera.location = (origin_center[0] + np.random.uniform(0, 2*r_x), origin_center[1] + np.random.uniform(-r_y, r_y), np.random.uniform(1, 7))
    drone.location = camera.location
    camera.rotation_euler = (np.random.uniform(-np.pi/24, np.pi/24), np.random.uniform(-np.pi/24, np.pi/24), np.random.uniform(-np.pi, np.pi))
    drone.rotation_euler = camera.rotation_euler
    camera.data.lens = np.random.random_integers(4, 9)

    # scene.render.filepath = f"//{images_files_path}{images_files_name}{i}.png"
    scene.render.filepath = os.path.join(images_files_path, f"{images_files_name}{i}.png")

    bpy.ops.render.render(write_still = True)

    cam = blender.Cam(camera, scene)

    with open(os.path.join(labels_files_path, f"{labels_files_name}{i}.txt"), 'a') as file:

        for balde, tampo in zip(baldes, tampos):

            image_balde = blender.Image_object(balde, cam)
            image_tampo = blender.Image_object(tampo, cam)

            image_balde.set_bounding_box( )
            image_tampo.set_bounding_box( )

            bbox_balde = image_balde.get_bounding_box(center = False)
            bbox_tampo = image_tampo.get_bounding_box(center = False)

            x_min = clamp(bbox_balde[0], bbox_tampo[0], bbox_tampo[1])
            x_max = clamp(bbox_balde[1], bbox_tampo[0], bbox_tampo[1])
            y_min = clamp(bbox_balde[2], bbox_tampo[2], bbox_tampo[3])
            y_max = clamp(bbox_balde[3], bbox_tampo[2], bbox_tampo[3])

            bbox = ((x_min + x_max)/2, (y_min + y_max)/2, x_max - x_min, y_max - y_min)
        
            if bbox_balde[2] != .0 and bbox_balde[3] != .0:
                
                file.write("1 %f %f %f %f\n" % bbox)


