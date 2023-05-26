from PIL import Image, ImageOps
import numpy as np
from scipy import signal
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


def invert_image(image):
    """
    Invert colour gama in image
    :param image: opened image in pillow image instance
    :type image: (PIL.Image())
    :return: Inverted image
    :rtype: (PIL.Image())
    """
    inverted_image = ImageOps.invert(image)

    return inverted_image


def add_number_to_colour_component(image, color, number):
    """

    :param image:
    :type image: (PIL.Image())
    :param color:
    :param number:
    :return:
    """
    img_array = np.array(image)
    match color:
        case 'r':
            img_array[:, :, 0] += number
        case 'g':
            img_array[:, :, 1] += number
        case 'b':
            img_array[:, :, 2] += number

    return Image.fromarray(img_array)


def get_colour_from_image(image, color):
    """

    :param image:
    :param color:
    :return:
    """
    img_array = np.array(image)
    match color:
        case 'r':
            img_array[:, :, 1] = 0
            img_array[:, :, 2] = 0
        case 'g':
            img_array[:, :, 0] = 0
            img_array[:, :, 2] = 0
        case 'b':
            img_array[:, :, 0] = 0
            img_array[:, :, 1] = 0

    return Image.fromarray(img_array)


def merging_images(image_one, image_two, alpha):
    """

    :param image_one:
    :param image_two:
    :param alpha:
    :return:
    """

    if alpha > 1:
        return "incrt alpha"
    elif alpha < 0:
        return "incrt alpha"

    frst_image = np.array(image_one)
    scnd_image = np.array(image_two)

    frst_alpha = alpha
    scnd_alpha = 1 - alpha

    new_image = np.sum([np.dot(frst_alpha, frst_image), np.dot(scnd_alpha, scnd_image)], axis=0)
    new_image = new_image.astype(np.uint8)

    return Image.fromarray(new_image)


def blur_image(image):
    """

    :param image:
    :return:
    """
    mu, sigma = 0, 0.1  # mean and standard deviation
    matrix_size = (5, 5)
    seed = 17

    blur_matrix = np.random.default_rng(seed).normal(mu, sigma, matrix_size)

    signal.windows.gaussian()





def res_up_image():
    """"""
    pass


def median_image():
    """"""
    pass


def erosion_image():
    """"""
    pass


def build_up_image():
    """"""
    pass


def sobel_image():
    """"""
    pass




