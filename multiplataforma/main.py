import bpy
import colorsys
import numpy as np
from scipy.stats import norm
from mathutils import Vector
import sys
import os
import time

diretorio = os.path.dirname(bpy.data.filepath)

# Cria o diretório, caso já não exista
if not diretorio in sys.path:
    sys.path.append(diretorio)

import utils
import conf

os.makedirs(conf.DIR_IMAGENS, exist_ok=True)

labels_path = os.path.join(diretorio, conf.DIR_IMAGENS)
imagens_path = os.path.join(diretorio, conf.DIR_IMAGENS)
chao_assets = os.path.join(diretorio, conf.DIR_CHAO_ASSETS)

# Obtendo a lista de arquivos de imagens para o chao
imagens_chao = [f for f in os.listdir(chao_assets) if f.endswith('.jpg') or f.endswith('.png') or f.endswith('.jpeg')]
print(f"Imagens de chão encontradas: {len(imagens_chao)}")

# Funcao para alterar a textura do material do chao
def alterar_textura_material(material, new_image_path=None):
    nodes = material.node_tree.nodes
    image_texture_node = None

    # Tenta encontrar um nó de textura de imagem existente
    for node in nodes:
        if node.type == 'TEX_IMAGE':
            image_texture_node = node
            break
    
    if image_texture_node is None: # Se ainda assim não conseguiu o nó
        print(f"Erro: Não foi possível obter ou criar um nó 'Image Texture' para o material '{material.name}'.")
        return False

    if not os.path.exists(new_image_path):
        print(f"Erro: Arquivo de imagem não encontrado em: {new_image_path}")
        return False

    try:
        new_image = bpy.data.images.load(new_image_path)
    except RuntimeError as e:
        print(f"Erro ao carregar a imagem '{new_image_path}': {e}")
        print("Verifique se o caminho está correto e se o arquivo é uma imagem válida.")
        return False

    image_texture_node.image = new_image
    print(f"Material '{material.name}' atualizado com a imagem: {new_image.name}")
    return True

# Classe para representar o Drone e a câmera em um só objeto
class Drone:
    def __init__(self, drone_obj, camera_obj):
        self.drone_obj = drone_obj
        self.camera_obj = camera_obj
    
    def move(self, x:float, y:float, z:float) -> None:
        self.camera_obj.location = (x, y, z+0.1)
        delta = conf.DRONE_RAND_POS_FROM_CAMERA
        self.drone_obj.location = (
            x+np.random.uniform(-delta, delta),
            y+np.random.uniform(-delta, delta),
            z+conf.DELTA_Z_FROM_CAMERA_TO_DRONE
        )
    
    def rotate(self, alpha:float, beta:float, gama:float) -> None:
        self.camera_obj.rotation_euler = (alpha, beta, gama)
        self.drone_obj.rotation_euler = self.camera_obj.rotation_euler

# Obtendo os objetos da cena
print("Obtendo os objetos da cena")
scene = bpy.context.scene
light = bpy.data.objects[conf.LIGHT_NAME]
origin = bpy.data.objects[conf.ORIGIN_NAME]
camera = bpy.data.objects[conf.CAMERA_NAME]
material_chao = bpy.data.materials.get(conf.MATERIAL_CHAO_NAME)
drone = Drone(bpy.data.objects[conf.DRONE_NAME], camera)

plataformas = []
for tipo in conf.PLATAFORMA_TYPES:
    i = 1
    print(f"Procurando objetos do tipo {tipo}...")
    try:
        name = f"{conf.PLATAFORMA_PREFIX}{tipo}"
        plataformas.append(bpy.data.objects[name])
        print(f"{name} adicionado à lista!")
    except:
        print("Nenhum objeto do tipo", tipo, "sem numeracao encontrado...")
    while True:
        try:
            name = f"{conf.PLATAFORMA_PREFIX}{tipo}.{i:03d}"
            plataformas.append(bpy.data.objects[name])
            print(f"{name} adicionado à lista!")
            i+=1
        except:
            print("Parando por aqui...")
            break

print("Iniciando as rodadas de fotos...")
for rodada_de_foto in range(conf.NUMERO_DE_IMAGENS):
    print(f"Rodada atual: {rodada_de_foto}/{conf.NUMERO_DE_IMAGENS-1}")
    if rodada_de_foto % 10 == 0:
        print("Alterando textura do chão... Rodada:", rodada_de_foto)
        alterar_textura_material(material=material_chao, new_image_path=os.path.join(chao_assets, np.random.choice(imagens_chao)))
    time.sleep(0.3)  # Espera um pouco para evitar problemas de travamento
    light.data.energy = np.random.uniform(conf.MIN_LIGHT_SCALE, conf.MAX_LIGHT_SCALE)
    light.data.color = colorsys.hsv_to_rgb(*[np.random.uniform(*conf.HSV_RAND_INTERVAL[i]) for i in range(3)])

    quadrante_index = np.random.choice(conf.N_QUADRANTES)
    quadrante = conf.QUADRANTES[quadrante_index]

    drone.move(
        quadrante[0]+np.random.uniform(*conf.RADIUS_VECTOR_CAMERA_INTERVAL[0]),
        quadrante[1]+np.random.uniform(*conf.RADIUS_VECTOR_CAMERA_INTERVAL[1]),
        np.random.normal(conf.Z0_FOR_CAMERA_SURROUND, conf.RADIUS_Z/norm.ppf((1+conf.CONFIDENCE_NORMAL_DISTRIBUTION_FOR_Z)/2))
    )

    vec = Vector((0, -camera.location[1], -camera.location[2]))
    dtheta_y = -np.pi - np.arctan2(vec[1], vec[2])
    drone.rotate(
        utils.clamp(dtheta_y, -conf.ANGLE_LIMIT, conf.ANGLE_LIMIT),
        np.random.uniform(-conf.ANGLE_LIMIT, conf.ANGLE_LIMIT),
        np.random.uniform(-conf.ANGLE_LIMIT, conf.ANGLE_LIMIT)
    )
    
    camera.data.lens = np.random.random_integers(*conf.CAMERA_LENS_RAND)

    scene.render.filepath = os.path.join(imagens_path, f"{conf.NAME_PREFIX}{rodada_de_foto+conf.START_INDEX}.png")
    bpy.ops.render.render(write_still = True)

    cam = utils.Cam(camera, scene)

    with open(os.path.join(labels_path, f"{conf.NAME_PREFIX}{rodada_de_foto+conf.START_INDEX}.txt"), 'w') as file:
        for plataforma in plataformas:
            plat = utils.Image_object(plataforma, cam) # criando um objeto que sera utilizado para julgar se o objeto esta, ou nao, dentro da imagem
            plat.set_bounding_box()

            bbox_plat = plat.get_bounding_box()
            if bbox_plat is None:
                continue

            if bbox_plat[2] != .0 and bbox_plat[3] != .0:
                file.write(f"{plataforma['id']} {bbox_plat[0]} {bbox_plat[1]} {bbox_plat[2]} {bbox_plat[3]}\n")