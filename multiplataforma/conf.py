# Constantes sobre os arquivos
DIR_IMAGENS = "imagens/"
DIR_LABELS = "labels/"
NAME_PREFIX = "img_"

# Constante sobre o treino
NUMERO_DE_IMAGENS = 2000

# Constantes sobre os objetos
LIGHT_NAME = "Light"
CAMERA_NAME = "Camera"
DRONE_NAME = "Drone"
ORIGIN_NAME = "Origin"
PLATAFORMA_PREFIX = "Plat_"
PLATAFORMA_TYPES = ("Casa", "Triangulo", "Quadrado", "Circulo", "Hexagono", "Pentagono", "Estrela", "Cruz")

# Constantes sobre os parâmetros randômicos
MIN_LIGHT_SCALE = 0.3
MAX_LIGHT_SCALE = 4

HSV_RAND_INTERVAL = ((0, 1), (0, 0.8), (1, 1))

RADIUS_VECTOR_CAMERA_INTERVAL = ((0, 10), (0, 10))
RADIUS_Z = 3
Z0_FOR_CAMERA_SURROUND = 3
CONFIDENCE_NORMAL_DISTRIBUTION_FOR_Z = 0.95

DRONE_RAND_POS_FROM_CAMERA = 1

CAMERA_LENS_RAND = (4, 9)