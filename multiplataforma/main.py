import bpy
import colorsys
import numpy as np
from scipy.stats import norm
from mathutils import Vector
import sys
import os
import utils
import conf

diretorio = os.path.dirname(bpy.data.filepath)

# Cria o diretório, caso já não exista
if not diretorio in sys.path:
    sys.path.append(diretorio)


# Classe para representar o Drone e a câmera em um só objeto
class Drone:
    def __init__(self, drone_obj, camera_obj):
        self.drone_obj = drone_obj
        self.camera_obj = camera_obj
    
    def move(self, x:float, y:float, z:float) -> None:
        self.camera_obj.location = (x, y, z)
        delta = conf.DRONE_RAND_POS_FROM_CAMERA
        self.drone_obj.location = (
            x+np.random.uniform(-delta, delta),
            y+np.random.uniform(-delta, delta),
            z
        )
    
    def rotate(self, alpha:float, beta:float, gama:float) -> None:
        self.camera_obj.rotation = (alpha, beta, gama)
        self.drone_obj.rotation = self.camera_obj.rotation

# Obtendo os objetos da cena
scene = bpy.context.scene
light = bpy.data.objects[conf.LIGHT_NAME]
origin = bpy.data.objects[conf.ORIGIN_NAME]
camera = bpy.data.objects[conf.CAMERA_NAME]

drone = Drone(bpy.data.objects[conf.DRONE_NAME], camera)

plataformas = []
for tipo in conf.PLATAFORMA_TYPES:
    i = 0
    while True:
        try:
            name = f"{conf.PLATAFORMA_PREFIX}{tipo}.{i:03d}"
            plataformas.append(bpy.data.objects[name])
            print(f"{name} adicionado à lista!")
            i+=1
        except:
            continue

for rodada_de_foto in range(conf.NUMERO_DE_IMAGENS):
    light.data.energy = np.random.uniform(conf.MIN_LIGHT_SCALE, conf.MAX_LIGHT_SCALE)
    light.data.color = colorsys.hsv_to_rgb(*[np.random.uniform(*conf.HSV_RAND_INTERVAL[i]) for i in range(3)])

    drone.move(
        np.random.uniform(*conf.RADIUS_VECTOR_CAMERA_INTERVAL[0]),
        np.random.uniform(*conf.RADIUS_VECTOR_CAMERA_INTERVAL[1]),
        np.random.normal(conf.Z0_FOR_CAMERA_SURROUND, conf.RADIUS_Z/norm.ppf((1+conf.CONFIDENCE_NORMAL_DISTRIBUTION_FOR_Z)/2))
    )

    vec = Vector((0, -camera.location[1], -camera.location[2]))
    dtheta_y = -np.pi - np.arctan2(vec[1], vec[2])
    drone.rotate(
        utils.clamp(dtheta_y, -np.pi/24, np.pi/24),
        np.random.uniform(-np.pi/24, np.pi/24),
        np.random.uniform(-np.pi, np.pi)
    )

    camera.data.lens = np.random.random_integers(*conf.CAMERA_LENS_RAND)

    scene.render.filepath = os.path.join(conf.DIR_IMAGENS, f"{conf.NAME_PREFIX}{rodada_de_foto}.png")
    bpy.ops.render.render(write_still = True)

    cam = utils.Cam(camera, scene)

    with open(os.path.join(conf.DIR_LABELS, f"{conf.NAME_PREFIX}{rodada_de_foto}.txt"), 'a') as file:
        for plataforma in plataformas:
            plat = utils.Image_object(plataforma, cam) # criando um objeto que sera utilizado para julgar se o objeto esta, ou nao, dentro da imagem
            plat.set_bounding_box()

            bbox_plat = plat.get_bounding_box()
            if bbox_plat is None:
                continue

            if bbox_plat[2] != .0 and bbox_plat[3] != .0:
                file.write(f"{plataforma["id"]} {bbox_plat[0]} {bbox_plat[1]} {bbox_plat[2]} {bbox_plat[3]}")