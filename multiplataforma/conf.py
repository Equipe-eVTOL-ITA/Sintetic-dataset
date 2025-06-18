from numpy import pi

START_INDEX = 4345

# Constantes sobre os arquivos
DIR_IMAGENS = "imagens/"
DIR_LABELS = "labels/"
DIR_CHAO_ASSETS = "assets/ChaoAssets2/"
NAME_PREFIX = "img_"

# Constante sobre o treino
NUMERO_DE_IMAGENS = 2000

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
MIN_LIGHT_SCALE = 0.5
MAX_LIGHT_SCALE = 1

HSV_RAND_INTERVAL = ((0, 1), (0, 0.8), (1, 1))

RADIUS_VECTOR_CAMERA_INTERVAL = ((0, 22), (0, 22))
RADIUS_Z = 0.3
Z0_FOR_CAMERA_SURROUND = 0.8
CONFIDENCE_NORMAL_DISTRIBUTION_FOR_Z = 0.95

DRONE_RAND_POS_FROM_CAMERA = 1

CAMERA_LENS_RAND = (4, 9)
