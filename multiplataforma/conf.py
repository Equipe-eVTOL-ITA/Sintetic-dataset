from numpy import pi
import os

# Constante sobre o treino
NUMERO_DE_IMAGENS = 20

# Constantes sobre os objetos
LIGHT_NAME = "Light"
CAMERA_NAME = "Camera"
DRONE_NAME = "Drone"
ORIGIN_NAME = "Origin"
MATERIAL_CHAO_NAME = "Grama"
PLATAFORMA_PREFIX = "Plat_"
PLATAFORMA_TYPES = ("Casa", "Triangulo", "Quadrado", "Circulo", "Hexagono", "Pentagono", "Estrela", "Cruz")

# Constantes sobre os parâmetros fixos
DELTA_Z_FROM_CAMERA_TO_DRONE = 1.5
ANGLE_LIMIT = pi/60 #pi/24

# Constantes sobre os parâmetros randômicos
MIN_LIGHT_SCALE = 0.75
MAX_LIGHT_SCALE = 1

HSV_RAND_INTERVAL = ((0.1, 0.2), (0, 0.3), (0.9, 1))

#RADIUS_VECTOR_CAMERA_INTERVAL = ((0, 22), (0, 22))
RADIUS_VECTOR_CAMERA_INTERVAL = ((0, 8), (0, 8))
QUADRANTES = ((0, 0), (-20, 0), (20, 0), (0, 20), (-20, 20), (20, 20), (0, -20), (-20, -20), (20, -20))
N_QUADRANTES = len(QUADRANTES)
RADIUS_Z = 0.3
Z0_FOR_CAMERA_SURROUND = 0.8
CONFIDENCE_NORMAL_DISTRIBUTION_FOR_Z = 0.95

DRONE_RAND_POS_FROM_CAMERA = 1

CAMERA_LENS_RAND = (4, 9)

def get_env_start_index():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    start_index = 0
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith('START_INDEX='):
                    try:
                        start_index = int(line.strip().split('=')[1])
                    except Exception:
                        start_index = 0
    # Atualiza o valor no arquivo .env
    new_index = start_index + NUMERO_DE_IMAGENS
    lines = []
    found = False
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith('START_INDEX='):
                    lines.append(f'START_INDEX={new_index}\n')
                    found = True
                else:
                    lines.append(line)
    if not found:
        lines.append(f'START_INDEX={new_index}\n')
    with open(env_path, 'w') as f:
        f.writelines(lines)
    return start_index

START_INDEX = get_env_start_index()

def get_and_update_batch_index():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    batch_index = 0
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith('BATCH_INDEX='):
                    try:
                        batch_index = int(line.strip().split('=')[1])
                    except Exception:
                        batch_index = 0
    # Atualiza o valor no arquivo .env
    new_index = batch_index + 1
    lines = []
    found = False
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith('BATCH_INDEX='):
                    lines.append(f'BATCH_INDEX={new_index}\n')
                    found = True
                else:
                    lines.append(line)
    if not found:
        lines.append(f'BATCH_INDEX={new_index}\n')
    with open(env_path, 'w') as f:
        f.writelines(lines)
    return batch_index

BATCH_INDEX = get_and_update_batch_index()

# Constantes sobre os arquivos
batch_dir = f"batch{BATCH_INDEX}"
os.makedirs(os.path.join(batch_dir, "images"), exist_ok=True)

DIR_IMAGENS = os.path.join(batch_dir, "images/")
DIR_CHAO_ASSETS = "assets/ChaoAssets3/"
NAME_PREFIX = "img_"

# Constantes para o utils
RATIO_OUTSIDE_IMAGE = 0.3
SIZABLE_BBX = 0.1