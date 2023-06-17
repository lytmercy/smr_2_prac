from PIL import Image
import numpy as np
import itertools
import io
import time


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


def derivative_calculation(dx, dy, input_x, input_y, height, width, color_ch):
    """

    :param array:
    :param height:
    :param width:
    :param color_ch:
    :return:
    """
    for x, y, clr in itertools.product(range(1, height - 2),
                                       range(1, width - 2),
                                       range(color_ch)):
        dx[x, y, clr] = input_x[x + 1, y, clr] - input_x[x, y, clr]
        dy[x, y, clr] = input_y[x, y + 1, clr] - input_y[x, y, clr]

    return dx, dy


def recover_image_from_gradient_field(image: Image) -> tuple[Image, Image, Image]:
    """"""

    image_array = np.array(image, dtype=np.float32)
    height, width, color = image_array.shape

    vx = np.zeros((height, width, color), dtype=np.float32)
    vy = np.zeros((height, width, color), dtype=np.float32)

    dvx = np.zeros((height, width, color), dtype=np.float32)
    dvy = np.zeros((height, width, color), dtype=np.float32)

    vx, vy = derivative_calculation(vx, vy, image_array, image_array, height, width, color)

    dvx, dvy = derivative_calculation(dvx, dvy, vx, vy, height, width, color)

    f_xyc = dvx + dvy

    recovered_image = np.zeros((height, width, color), dtype=np.float32)

    recovered_image[:, 0, :] = image_array[:, 0, :]
    recovered_image[:, width - 1, :] = image_array[:, width - 1, :]
    recovered_image[0, :, :] = image_array[0, :, :]
    recovered_image[height - 1, :, :] = image_array[height - 1, :, :]

    for clr in range(color):

        print(f"Color: {clr}")
        print("=============")

        error = 1
        eps = 1e-7

        iter_count = 0
        start_clr = time.time()
        start = start_clr

        while error > eps:
            error = 0
            for x, y in itertools.product(range(1, height - 2),
                                          range(1, width - 2)):

                temp = (recovered_image[x + 1, y, clr] + recovered_image[x - 1, y, clr] +
                        recovered_image[x, y + 1, clr] + recovered_image[x, y - 1, clr] - f_xyc[x, y, clr]) / 4

                div = abs(temp - recovered_image[x, y, clr])
                recovered_image[x, y, clr] = temp

                if div > error:
                    error = div

            iter_count += 1
            if iter_count % 5000 == 0:
                print(f"iter error: {error}")
                print("iter time: %.1f" % (time.time() - start))
                start = time.time()

        # print("Final score")
        # print(f"Iterations: {iter_count}")
        # print(f"error: {error}")
        # print("time: %.1f" % (time.time() - start_clr))

    recovered_image = recovered_image.clip(min=0, max=255)
    recovered_image = recovered_image.astype(np.uint8)
    vx = vx.astype(np.uint8)
    vy = vy.astype(np.uint8)

    return Image.fromarray(recovered_image), Image.fromarray(vx), Image.fromarray(vy)


def seamless_image_in_image_insertion(image_field: Image, image_object: Image,
                                      xy_coord: tuple, nxny_coord: tuple) -> Image:
    """"""

    image_field_array = np.array(image_field, dtype=np.float32)
    image_object_array = np.array(image_object, dtype=np.float32)
    image_object_array = np.pad(image_object_array, pad_width=((1, 1), (1, 1), (0, 0)),
                                mode="constant", constant_values=0)

    field_shape = image_field_array.shape
    object_shape = image_object_array.shape

    image_object_array[:, 0, :] = image_field_array[xy_coord[0]-1:nxny_coord[0]+1, xy_coord[1]-1, :]
    image_object_array[:, object_shape[1]-1, :] = image_field_array[xy_coord[0]-1:nxny_coord[0]+1, nxny_coord[1]+1, :]
    image_object_array[0, :, :] = image_field_array[xy_coord[0]-1, xy_coord[1]-1:nxny_coord[1]+1, :]
    image_object_array[object_shape[0]-1, :, :] = image_field_array[nxny_coord[0]+1, xy_coord[1]-1:nxny_coord[1]+1, :]

    vx = np.zeros(object_shape, dtype=np.float32)
    vy = np.zeros(object_shape, dtype=np.float32)

    dvx = np.zeros(object_shape, dtype=np.float32)
    dvy = np.zeros(object_shape, dtype=np.float32)

    vx, vy = derivative_calculation(vx, vy, image_object_array, image_object_array,
                                    object_shape[0], object_shape[1], object_shape[2])

    dvx, dvy = derivative_calculation(dvx, dvy, vx, vy,
                                      object_shape[0], object_shape[1], object_shape[2])

    f_xyc = dvx + dvy

    for clr in range(object_shape[2]):

        print(f"Color: {clr}")
        print("=============")

        error = 1
        eps = 1e-7

        iter_count = 0
        start_clr = time.time()
        start = start_clr

        while error > eps:
            error = 0
            for x, y in itertools.product(range(1, object_shape[0] - 2),
                                          range(1, object_shape[1] - 2)):

                temp = (image_object_array[x + 1, y, clr] + image_object_array[x - 1, y, clr] +
                        image_object_array[x, y + 1, clr] + image_object_array[x, y - 1, clr] - f_xyc[x, y, clr]) / 4

                div = abs(temp - image_object_array[x, y, clr])
                image_object_array[x, y, clr] = temp

                if div > error:
                    error = div

            iter_count += 1
            if iter_count % 5000 == 0:
                print(f"iter error: {error}")
                print("iter time: %.1f" % (time.time() - start))
                start = time.time()

        print("Final score")
        print(f"Iterations: {iter_count}")
        print(f"error: {error}")
        print("time: %.1f" % (time.time() - start_clr))

    image_object_array = image_object_array.clip(min=0, max=255)

    image_field_array[xy_coord[0]-1:nxny_coord[0]+1, xy_coord[1]-1:nxny_coord[1]+1, :] = image_object_array

    return Image.fromarray(image_field_array.astype(np.uint8))
