from mathutils import Vector, Matrix
from conf import RATIO_OUTSIDE_IMAGE, SIZABLE_BBX

def clamp(x, minimum, maximum):

    return max(minimum, min(x, maximum))

class Point:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

class BoundingBox:
    """
    Classe para representar uma bounding box na imagem
    """
    def __init__(self, centro_x=None, centro_y=None, width=None, height=None):
        self.centro = Point(centro_x, centro_y)
        self.width = width
        self.height = height

    @property
    def superior_esquerdo(self) -> Point:
        if self.centro.x is not None and self.centro.y is not None and self.width is not None and self.height is not None:
            return Point(self.centro.x - self.width/2.0, self.centro.y - self.height/2.0)
        return Point(None, None)

    @property
    def inferior_direito(self) -> Point:
        if self.centro.x is not None and self.width is not None and self.centro.y is not None and self.height is not None:
            return Point(self.centro.x + self.width/2.0, self.centro.y + self.height/2.0)
        return Point(None, None)

    def __iter__(self):
        yield self.centro.x
        yield self.centro.y
        yield self.width
        yield self.height

    def set_box_from_extremes(self, min_x, min_y, max_x, max_y) -> None:
        """
        Configura o centro, largura e altura da bounding box a partir dos extremos.
        """
        self.centro.x = (min_x + max_x) / 2.0
        self.centro.y = (min_y + max_y) / 2.0
        self.width = max_x - min_x
        self.height = max_y - min_y

    def is_minimally_inside(self, r: float, reso_x: float, reso_y: float) -> bool:
        """
        Retorna True se a bounding box estiver minimamente localizada dentro da figura,
        ou seja, se ela estiver fora da resolução no máximo por uma fração r da sua largura/altura.
        """
        if self.width is None or self.height is None or self.centro.x is None or self.centro.y is None:
            return False

        min_x = self.superior_esquerdo.x
        max_x = self.inferior_direito.x
        min_y = self.superior_esquerdo.y
        max_y = self.inferior_direito.y

        return (
            # obs: todos os valores estao em porcentagens para os seus respectivos eixos coordenados
            max_x > r * self.width and
            min_x < 1 - r * self.width and
            max_y > r * self.height and
            min_y < 1 - r * self.height
        )

    def is_minimally_sizable(self) -> bool:
        """
        Retorna True se a bounding box tiver tamanho minimamente aceitável.
        """
        return self.width is not None and self.height is not None and self.width > SIZABLE_BBX and self.height > SIZABLE_BBX


class Cam():
    """
    An incremental class to represent a camera in the scene
    """

    def __init__(self, camera, scene):
        """
        Constructs the Cam object.
        
        :param camera: camera object that bases the Cam object
        :type camera: bpy.data.objects
        :param scene: scene object that bases the class
        :type scene: bpy.context.scene
        """
        self.camera = camera
        self.scene = scene

        scene.render.resolution_x = 800
        scene.render.resolution_y = 800

        self.x_resolution = scene.render.resolution_x
        self.y_resolution = scene.render.resolution_y

        self.sensor_fit = self.camera.data.sensor_fit
        
        self.sensor_width = self.camera.data.sensor_width if self.sensor_fit != 'VERTICAL' else self.camera.data.sensor_height*self.x_resolution/self.y_resolution
        self.sensor_height = self.camera.data.sensor_height if self.sensor_fit == 'VERTICAL' else self.sensor_width*self.y_resolution/self.x_resolution

        self.K = self.intrinsic_matrix()

    def intrinsic_matrix(self):
        """
        Function that returns the intrinsic matrix of the camera
        
        :return: intrinsic matrix of the camera
        :rtype K: mathutils.Matrix
        """

        f = self.camera.data.lens

        scale = self.scene.render.resolution_percentage/100.0

        pixel_aspect_ratio = self.scene.render.pixel_aspect_y/self.scene.render.pixel_aspect_x

        mx = self.x_resolution/self.sensor_width*scale
        mx = mx if self.sensor_fit != 'VERTICAL' else mx*pixel_aspect_ratio
        my = self.y_resolution/self.sensor_height*scale
        my = my if self.sensor_fit == 'VERTICAL' else my/pixel_aspect_ratio

        cx = self.x_resolution*(0.5 - self.camera.data.shift_x)
        cy = self.y_resolution*(0.5 - self.camera.data.shift_y)

        K = Matrix([
            [mx*f, 0, cx],
            [0, my*f, cy],
            [0, 0, 1]
        ])

        return K

    def to_camera_coord(self, point):
        """
        Auxiliar function that returns a point in the camera coordinate system

        :param point: point in the world coordinate system
        :type point: mathutils.Vector (Vector (float, float, float))
        :return: point in the camera coordinate system
        :rtype point: mathutils.Vector (Vector (float, float, float))
        """

        point_camera_coord = self.camera.matrix_world.inverted() @ point

        return point_camera_coord

class Image_object:
    """
    Class to represents a solid object in the image
    """

    def __init__(self, object, camera):
        """
        Constructs the object.

        :param object: solid object that bases the Image_object object
        :type object: bpy.types.objects
        :param camera: camera object of the scene
        :type camera: Cam
        """

        self.object = object
        self.camera = camera

        self.box = BoundingBox()

    def to_image_coord(self, point):
        """
        Auxiliar function that returns the coordinates of a point in the image coordinate system

        :param point: point in the world coordinate system
        :type point: mathutils.Vector (Vector (float, float, float))
        :return: point in the image coordinate system
        :rtype: mathutils.Vector (Vector(float, float, float))
        """

        point_camera_coord = self.camera.to_camera_coord(point)

        if point_camera_coord[2] > 0:
            return Vector([0.0, 0.0, 1])

        point_image_coord = self.camera.K @ point_camera_coord
        point_image_coord /= point_image_coord[2]

        point_image_coord[0] = 1 - point_image_coord[0]/self.camera.x_resolution
        point_image_coord[1] = point_image_coord[1]/self.camera.y_resolution

        return point_image_coord

    def set_bounding_box(self) -> None:
        """
        Sets the bounding box around the object in the image
        """

        vertices = self.object.data.vertices

        vertices_coord = [self.object.matrix_world @ v.co for v in vertices]

        image_vetices = [self.to_image_coord(c) for c in vertices_coord]

        x_vertices = [v[0] for v in image_vetices]
        max_x = max(x_vertices)
        min_x = min(x_vertices)

        y_vertices = [v[1] for v in image_vetices]
        max_y = max(y_vertices)
        min_y = min(y_vertices)

        self.box.set_box_from_extremes(min_x, min_y, max_x, max_y)

    def get_bounding_box(self) -> tuple:
        """
        Returns the bounding box tuple of the object in the image

        :return: bounding box of the object in the image
        :rtype: tuple(float, float, float, float)
        """

        if self.box.is_minimally_inside(RATIO_OUTSIDE_IMAGE, self.camera.x_resolution, self.camera.y_resolution):
            if self.box.is_minimally_sizable():
                return tuple(self.box)
        
        return None
