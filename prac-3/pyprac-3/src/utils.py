from PIL import Image, ImageOps
import numpy as np
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


def blur_image(image, div=1):
    """

    :param image:
    :param div:
    :return:
    """
    mu, sigma = 0.03, 0.001  # mean and standard deviation
    blur_kernel_size = (5, 5)
    seed = 17

    blur_kernel = np.random.default_rng(seed).normal(mu, sigma, blur_kernel_size)

    image_array = np.array(image)
    pad_image = np.pad(image_array, pad_width=((2, 2), (2, 2), (0, 0)), mode="symmetric")

    blured_image = image_array.copy()

    # Iter through all pixels in image
    for i in range(image_array.shape[0]):
        for j in range(image_array.shape[1]):
            for clr in range(image_array.shape[2]):

                image_patch = pad_image[i:i + blur_kernel_size[0], j:j + blur_kernel_size[1], clr]

                blured_image[i, j, clr] = np.sum(np.multiply(image_patch, blur_kernel))\
                                            .clip(min=0, max=255) * (1/div)

    return Image.fromarray(blured_image)


def res_up_image(image, div=1):
    """

    :param image:
    :param div:
    :return:
    """
    res_up_kernel = np.array([[-1, -1, -1],
                              [-1, 9, -1],
                              [-1, -1, -1]])

    image_array = np.array(image)
    pad_image = np.pad(image_array, pad_width=((1, 1), (1, 1), (0, 0)), mode="symmetric")

    res_up_image = image_array.copy()

    # Iter through all pixels in image
    for i in range(image_array.shape[0]):
        for j in range(image_array.shape[1]):
            for clr in range(image_array.shape[2]):

                image_patch = pad_image[i:i + res_up_kernel.shape[0], j:j + res_up_kernel.shape[1], clr]

                res_up_image[i, j, clr] = np.sum(np.multiply(image_patch, res_up_kernel)).clip(min=0, max=255) * (1/div)

    return Image.fromarray(res_up_image)


def median_image(image, kernel_size):
    """

    :param image:
    :param kernel_size:
    :return:
    """
    # Set kernel size for median filter
    median_kernel_size = ()
    match kernel_size:
        case 3:
            median_kernel_size = (3, 3)
        case 4:
            median_kernel_size = (4, 4)
        case 5:
            median_kernel_size = (5, 5)

    image_array = np.array(image)
    pad_image = np.pad(image_array, pad_width=((1, 1), (1, 1), (0, 0)), mode="symmetric")

    # Iter through all pixels in image
    for i in range(image_array.shape[0]):
        for j in range(image_array.shape[1]):
            for clr in range(image_array.shape[2]):

                median_kernel = pad_image[i:i + median_kernel_size[0], j:j + median_kernel_size[1], clr]

                median_value = int(np.median(median_kernel))

                image_array[i, j, clr] = median_value

    return Image.fromarray(image_array)


def erosion_image(image):
    """"""
    erosion_filter = np.array([[0, 0, 1, 0, 0],
                               [0, 1, 1, 1, 0],
                               [1, 1, 1, 1, 1],
                               [0, 1, 1, 1, 0],
                               [0, 0, 1, 0, 0]])

    image_array = np.array(image)
    pad_image = np.pad(image_array, pad_width=((2, 2), (2, 2), (0, 0)), mode="symmetric")

    erosioned_image = image_array.copy()

    # Iter through all pixels in image
    for i in range(image_array.shape[0]):
        for j in range(image_array.shape[1]):
            for clr in range(image_array.shape[2]):

                image_patch = pad_image[i:i + erosion_filter.shape[0], j:j + erosion_filter.shape[1], clr]

                erosion_patch = np.multiply(image_patch, erosion_filter)

                erosioned_image[i, j, clr] = np.min(erosion_patch[np.nonzero(erosion_patch)])

    return Image.fromarray(erosioned_image)


def build_up_image(image):
    """"""
    build_up_filter = np.array([[0, 0, 1, 0, 0],
                                [0, 1, 1, 1, 0],
                                [1, 1, 1, 1, 1],
                                [0, 1, 1, 1, 0],
                                [0, 0, 1, 0, 0]])

    image_array = np.array(image)
    pad_image = np.pad(image_array, pad_width=((2, 2), (2, 2), (0, 0)), mode="symmetric")

    builded_up_image = image_array.copy()

    # Iter through all pixels in image
    for i in range(image_array.shape[0]):
        for j in range(image_array.shape[1]):
            for clr in range(image_array.shape[2]):

                image_patch = pad_image[i:i + build_up_filter.shape[0], j:j + build_up_filter.shape[1], clr]

                erosion_patch = np.multiply(image_patch, build_up_filter)

                builded_up_image[i, j, clr] = np.max(erosion_patch[np.nonzero(erosion_patch)])

    return Image.fromarray(builded_up_image)


def sobel_image(image):
    """"""
    sobel_gy_filter = np.array([[-1, -2, -1],
                                [0, 0, 0],
                                [1, 2, 1]])
    sobel_gx_filter = np.array([[-1, 0, 1],
                                [-2, 0, 2],
                                [-1, 0, 1]])

    image_array = np.array(image)

    image_grey = image_array[:, :, 0]/3 + image_array[:, :, 1]/3 + image_array[:, :, 2]/3
    # image_grey = image_array[:, :, 0] * 0.07 + image_array[:, :, 1] * 0.72 + image_array[:, :, 2] * 0.21

    pad_image = np.pad(image_grey, pad_width=((1, 1), (1, 1)), mode="symmetric")

    sobel_image_array = np.zeros(image_grey.shape, dtype=np.uint8)

    # Iter through all pixels in image
    for i in range(image_grey.shape[0]):
        for j in range(image_grey.shape[1]):

            y_image_patch = pad_image[i:i + sobel_gy_filter.shape[0], j:j + sobel_gy_filter.shape[1]]
            x_image_patch = pad_image[i:i + sobel_gx_filter.shape[0], j:j + sobel_gx_filter.shape[1]]

            gy_patch = np.multiply(y_image_patch, sobel_gy_filter)
            gx_patch = np.multiply(x_image_patch, sobel_gx_filter)

            gy_power = np.power(np.sum(gy_patch), 2)
            gx_power = np.power(np.sum(gx_patch), 2)

            gxy_sqrt = np.sqrt(gx_power + gy_power)

            sobel_image_array[i, j] = gxy_sqrt.clip(min=0, max=255)

    return Image.fromarray(sobel_image_array)


def embed_extract_watermark(image, watermark, pixel_bit=-1):
    """"""
    image_array = np.array(image)

    watermark_array = np.array(watermark)
    watermark_array = watermark_array >= 128
    watermark_array = np.array(watermark_array[:, :, 0], dtype=np.uint8)

    im_height, im_width = image_array.shape[:2]
    wm_height, wm_width = watermark_array.shape

    if im_height == wm_height and im_width == wm_width:
        for i in range(0, im_height):
            for j in range(0, im_width):
                image_pixel = image_array[i, j, 2]
                # Binary operations
                bin_pixel = list(np.binary_repr(image_pixel, 8))
                # print(bin_pixel)
                bin_xor_pixel = np.bitwise_xor([int(bin_pixel[pixel_bit])], [int(watermark_array[i, j])])
                # print(bin_pixel[-1], watermark_array[i, j])
                # print(bin_xor_pixel)
                bin_pixel[pixel_bit] = str(bin_xor_pixel[0])
                # print(''.join(bin_pixel))
                # Set new pixel value to image
                new_image_pixel = int(''.join(bin_pixel), 2)
                print(image_pixel, new_image_pixel)
                image_array[i, j, 2] = new_image_pixel
    elif im_height > wm_height or im_width > wm_width:
        pass
    elif im_height < wm_height or im_width < wm_width:
        pass

    return Image.fromarray(image_array)
