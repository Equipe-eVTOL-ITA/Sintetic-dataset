import os
import cv2
import matplotlib.pyplot as plt

RECT_THICKNESS = 2
CENT_THICNESS = 2

def show_detection(image, box, color, show_center = True):
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
    x = box[1]*image.shape[1]
    y = box[2]*image.shape[0]
    width = box[3]*image.shape[1]
    height = box[4]*image.shape[0]
    if width == 0.0 or height == 0.0:
        return
    top_left = (int(x - width/2), int(y - height/2))
    bottom_right = (int(x + width/2), int(y + height/2))
    cv2.rectangle(image, top_left, bottom_right, color, RECT_THICKNESS)
    if show_center:
        cv2.circle(image, (int(x), int(y)), CENT_THICNESS, color, -1)

labels_file_name = 'img_'
images_name = 'img_'
labels_file_path = 'Labels\\'
images_file_path = 'dataset\\'

if not os.path.exists(labels_file_path):
    raise FileNotFoundError(f"Arquivo não encontrado: {labels_file_path}")

num_images = 30

labels = [ ]
images = [cv2.imread(f"{images_file_path}{images_name}{n}.png") for n in range(num_images)]

for i in range(num_images):

    boxes = [ ]

    with open(f"{labels_file_path}{labels_file_name}{i}.txt", 'r') as set_file:

        line = set_file.readline( ).strip( )
        
        box = [ ]

        if line != "":
            box = [float(f) for f in line.split( )]
        
        boxes.append(box)

        line = set_file.readline( )

    labels.append(boxes)
    
    image = images[i]
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    for box in boxes:
        if box:
            show_detection(image, box, (0, 255, 0), show_center = False)

    plt.figure( )
    plt.imshow(image)
    plt.show( )


