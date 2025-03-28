from mathutils import Vector, Matrix
from utils import length, clamp

class Bounding_box:
    """
    Class to represent a bounding box in the image
    """

    def __init__(self, x = None, y = None, width = None, height = None):
        """
        Constructs the Bounding_box object.

        :param x: x coordinate of the center of the bounding box, in px
        :type x: float
        :param y: y coordinate of the center of the bounding box, in px
        :type y: float
        :param width: width of the bounding box, in px
        :type width: float
        :param height: height of the bounding box, in px
        :type height: float
        """

        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.set_max_min( )

    def set_max_min(self):
        """
        Function that sets the extreme points of the bounding box
        """

        if self.x is not None and self.width is not None and self.width != 0.0:
            self.max_x = self.x + self.width/2.0
            self.min_x = self.x - self.width/2.0
        else:
            self.max_x = self.min_x = None
        if self.y is not None and self.height is not None and self.height != 0.0:
            self.max_y = self.y + self.height/2.0
            self.min_y = self.y - self.height/2.0
        else:
            self.max_y = self.min_y = None
    
    def set_box(self, min_x, min_y, max_x, max_y):
        """
        Function that sets the bounding box from the extreme points

        :param min_x: minimum x coordinate, in px
        :type min_x: float
        :param min_y: minimum y coordinate, in px
        :type min_y: float
        :param max_x: maximum x coordinate, in px
        :type max_x: float
        :param max_y: maximum y coordinate, in px
        :type max_y: float
        """

        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

        self.x = (min_x + max_x)/2.0
        self.y = (min_y + max_y)/2.0

        self.width = length(min_x, max_x)
        self.height = length(min_y, max_y)

    def tuple(self, x = None, y = None, width = None, height = None):
        """
        Returns the bounding box in the form of a tuple

        :param x: x coordinate of the center of the bounding box
        :type x: float
        :param y: y coordinate of the center of the bounding box
        :type y: float
        :param width: width of the bounding box
        :type width: float
        :param height: height of the bounding box
        :type height: float
        :return: tuple with the bounding box
        :rtype: tuple(float, float, float, float)
        """

        self.x = x if x is not None else self.x
        self.y = y if y is not None else self.y
        self.width = width if width is not None else self.width
        self.height = height if height is not None else self.height

        self.set_max_min( )

        if self.x == None or self.y == None or self.width == 0.0 or self.width == None or self.height == 0.0 or self.height == None:
            return (0.0, 0.0, 0.0, 0.0)
        return (self.x, self.y, self.width, self.height)

class Cam( ):
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

        self.sensor_width = self.camera.data.sensor_width
        self.sensor_height = self.camera.data.sensor_height

        self.x_resolution = scene.render.resolution_x
        self.y_resolution = scene.render.resolution_y
        
        self.K = self.intrinsic_matrix( )

    def intrinsic_matrix(self):
        """
        Function that returns the intrinsic matrix of the camera
        
        :return: intrinsic matrix of the camera
        :rtype K: mathutils.Matrix
        """

        f = self.camera.data.lens
        s = 1.2 # scale factor of y axis (because of camera distortion)

        scale = self.scene.render.resolution_percentage/100.0

        camera_width = self.camera.data.sensor_width
        camera_height = self.camera.data.sensor_height

        aspect_ratio_y = self.scene.render.pixel_aspect_y

        mx = self.x_resolution/camera_width*scale
        my = self.y_resolution/(camera_height*aspect_ratio_y)*scale*s

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

        point_camera_coord = self.camera.matrix_world.inverted( ) @ point

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

        self.box = Bounding_box( )

    def to_image_coord(self, point):
        """
        Auxiliar function that returns the coordinates of a point in the image coordinate system

        :param point: point in the world coordinate system
        :type point: mathutils.Vector (Vector (float, float, float))
        :return: point in the image coordinate system (normalized)
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

    def set_bounding_box(self):
        """
        Sets the bounding box around the object in the image
        """

        vertices = self.object.data.vertices

        vertices_coord = [self.object.matrix_world @ v.co for v in vertices]

        image_vetices = [self.to_image_coord(c) for c in vertices_coord]

        x_vertices = [v[0] for v in image_vetices]
        max_x = clamp(max(x_vertices), 0, 1)
        min_x = clamp(min(x_vertices), 0, 1)

        y_vertices = [v[1] for v in image_vetices]
        max_y = clamp(max(y_vertices), 0, 1)
        min_y = clamp(min(y_vertices), 0, 1)

        self.box.set_box(min_x, min_y, max_x, max_y)

    def get_bounding_box(self):
        """
        Returns the bounding box tuple of the object in the image

        :return: bounding box of the object in the image
        :rtype: tuple(float, float, float, float)
        """

        if self.box.max_x < 1/4*self.box.width or self.box.min_x > 1 - 1/4*self.box.width or self.box.max_y < 1/4*self.box.height or self.box.min_y > 1 - 1/4*self.box.height:
            return (0.0, 0.0, 0.0, 0.0)
        else:
            return self.box.tuple( )

