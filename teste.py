import os
import cv2
import matplotlib.pyplot as plt

RECT_THICKNESS = 3
CENT_THICNESS = 3

def show_detection(image, boxes, color, show_center = True):
    """
    Shows an object detection.

    :param image: image used for object detection.
    :type image: OpenCV's image.
    :param detection: detection as a 5-dimensional tuple: (probability, x, y, width, height).
    :type detection: 5-dimensional tuple.
    :param color: color used to show the detection (RGB value).
    :type color: 3-dimensional tuple.
    :param show_center: if the center of the detection should be shown in the image.
    :type show_center: bool.
    """
    x = boxes[1]*image.shape[1]
    y = boxes[2]*image.shape[0]
    width = boxes[3]*image.shape[1]
    height = boxes[4]*image.shape[0]
    if width == 0.0 or height == 0.0:
        return
    top_left = (int(x - width/2), int(y - height/2))
    bottom_right = (int(x + width/2), int(y + height/2))
    cv2.rectangle(image, top_left, bottom_right, color, RECT_THICKNESS)
    if show_center:
        cv2.circle(image, (int(x), int(y)), CENT_THICNESS, color, -1)

num_targets = 5

labels_file_name = 'img_3'
images_name = 'img_'
labels_file_path = 'Labels\\img_3.txt'

if not os.path.exists(labels_file_path):
    raise FileNotFoundError(f"Arquivo não encontrado: {labels_file_path}")

num_images = 1

labels = [ ]

with open(labels_file_path, 'r') as set_file:

    for i in range(num_images):

        lines = [set_file.readline( ).strip( ) for n in range(num_targets)]
        
        boxes = [[float(f) for f in line.split( )] for line in lines]
        
        labels.append(boxes)

        line = set_file.readline( )

images = [cv2.imread(f"dataset\\{images_name}{3}.png") for n in range(num_images)]

for i in range(num_images):

    image = images[i]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    for j in range(num_targets):
        show_detection(image, labels[i][j], (0, 255, 0), show_center = False)

    plt.figure( )
    plt.imshow(image)
    plt.show( )