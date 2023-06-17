from PIL import Image
import numpy as np
import cv2
import itertools
import io


def open_resize(image_path, resize=None):
    """
    Open image from file path and optionally resize.
    :param image_path: image file path for opening
    :type image_path: (str)
    :param resize: optional new size
    :type resize: (tuple[int, int] or None)
    :return: pillow image instance
    :rtype: (PIL.Image())
    """
    img = Image.open(image_path)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        # scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((new_width, new_height), Image.ANTIALIAS)

    return img


def convert_to_bytes(image):
    """
    Will convert into bytes and optionally resize an image that is a file or a base64 bytes object.
    Turns into PNG format in the process so that can be displayed by tkinter.
    :param image: image instance
    :type image: (PIL.Image())
    :return: (bytes) a byte-string object
    :rtype: (bytes)
    """
    bio = io.BytesIO()
    image.save(bio, format="PNG")
    del image
    return bio.getvalue()


def viola_jones_algo(frame: Image) -> Image:
    """"""

    color_image = np.array(frame)
    grey_image = frame.convert('L')

    frame_array = np.array(grey_image)
    frame_shape = frame_array.shape

    haara_cascades_path = "../input/haarcascade_frontalface_default.xml"

    face_detector = cv2.CascadeClassifier(haara_cascades_path)

    detected_faces = face_detector.detectMultiScale(frame_array, scaleFactor=1.05, minNeighbors=5,
                                                    minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

    # Loop over the faces bounding boxes
    for (fx, fy, fw, fh) in detected_faces:
        # draw the face bounding box on the frame
        cv2.rectangle(color_image, (fx, fy), (fx + fw, fy + fh),
                      (0, 255, 0), 2)

    return Image.fromarray(color_image)
