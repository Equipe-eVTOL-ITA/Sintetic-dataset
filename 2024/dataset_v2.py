# Run in Blender

import bpy
import colorsys
import numpy as np
import sys
import os

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import blender#_vx as blender

# Setting files params

labels_file_name = 'Labels\\img_'
set_len = 5
num_targets = 5

# Getting the scene

scene = bpy.context.scene
light = bpy.data.objects['Light']
camera = bpy.data.objects['Camera']

xy_radius = 13/4
light_scale = 1000

# Creating the random dataset to training the CNN

for i in range(set_len):

    light.data.energy = np.random.uniform(0.05*light_scale, 3.5*light_scale)
    light.data.color = colorsys.hsv_to_rgb(np.random.uniform(0, 1), np.random.uniform(0, 0.5), 1)

    camera.location = (np.random.uniform(-xy_radius, xy_radius), np.random.uniform(-xy_radius, xy_radius), np.random.uniform(1.5, 6.5))
    camera.rotation_euler = (np.random.uniform(-np.pi/9, np.pi/9), np.random.uniform(-np.pi/9, np.pi/9), np.random.uniform(-np.pi, np.pi))
    camera.data.lens = np.random.random_integers(18, 22)

    scene.render.filepath = "//dataset/" + "img_" + str(i) + ".png"

    bpy.ops.render.render(write_still = True)

    cam = blender.Cam(camera, scene)

    image_objects = [blender.Image_object(bpy.data.objects['Base_' + str(n + 1)], cam) for n in range(num_targets)]

    with open(labels_file_name + str(i) + '.txt', 'a') as file:

        for n in range(num_targets):

            image_objects[n].set_bounding_box()
            bbox = image_objects[n].get_bounding_box()
            
            if bbox[2] != .0 and bbox[3] != .0:

                file.write("0 %f %f %f %f\n" % bbox)
                # file.write(' '.join(map(str, bbox)))
                # file.write('\n')

