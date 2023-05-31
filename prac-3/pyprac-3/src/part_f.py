import PySimpleGUI as sg
import numpy as np
from PIL import Image

from src.utils import convert_to_bytes, open_resize, embed_extract_watermark


def run():
    """"""

    sg.theme("DarkBlack")

    # Define right column of content
    right_col = [[sg.Text("Original image from: "), sg.In("Choose file", size=(25, 1), enable_events=True, k="image-path"),
                  sg.FileBrowse(initial_folder="../input")],
                 [sg.Text("Watermark from: "), sg.In("Choose file", size=(25, 1), enable_events=True, k="watermark-path"),
                  sg.FileBrowse(initial_folder="../input")],
                 [sg.Button("Sign image", k="sign-img-act")],
                 [sg.Button("Unsign image", k="unsign-img-act")]]

    img_size = (500, 300)
    watermark_size = (500, 300)
    new_img_size = (500, 300)
    # Define image column of content of this part
    image_col = [[sg.Text("Original image"), sg.Text("Watermark")],
                 [sg.Image(size=img_size, k="origin-image"), sg.Image(size=watermark_size, k="watermark-image")],
                 [sg.Text("Watermarked image"), sg.Text("Unsigned image")],
                 [sg.Image(size=new_img_size, k="signed-image"), sg.Image(size=new_img_size, k="unsigned-image")]]

    # Construct full layout from all columns
    f_layout = [[sg.Column(image_col, element_justification='c', size=(1030, 650)),
                 sg.VSeparator(),
                 sg.Column(right_col, element_justification='c')]]

    f_window = sg.Window("Prac-3 -- part-d", f_layout, resizable=False, size=(1500, 650))

    while True:
        event, values = f_window.read()
        print(event, values)
        if event in (sg.WIN_CLOSED, "Exit"):
            break
        if event == "image-path":
            origin_image_path = values["image-path"]
            origin_image = open_resize(origin_image_path, resize=img_size)
            f_window["origin-image"].update(data=convert_to_bytes(origin_image))
            f_window["signed-image"].update()
            f_window["unsigned-image"].update()

        if event == "watermark-path":
            watermark_path = values["watermark-path"]
            watermark_image = open_resize(watermark_path, resize=watermark_size)

            # watermark_array = np.array(watermark_image)
            # watermark_array = watermark_array >= 128
            # watermark_array = np.array(watermark_array[:, :, 0], dtype=np.uint8)
            # watermark_image = Image.fromarray(watermark_array)

            f_window["watermark-image"].update(data=convert_to_bytes(watermark_image))
            f_window["signed-image"].update()
            f_window["unsigned-image"].update()

        if event == "sign-img-act":
            origin_image_path = values["image-path"]
            watermark_path = values["watermark-path"]

            origin_image = open_resize(origin_image_path, resize=img_size)
            watermark_image = open_resize(watermark_path, resize=watermark_size)

            signed_image = embed_extract_watermark(origin_image, watermark_image, 4)

            sign_path = "../output/unsigned.png"
            signed_image.save(sign_path, format="PNG")

            f_window["signed-image"].update(data=convert_to_bytes(signed_image))

        if event == "unsign-img-act":
            origin_image_path = values["image-path"]
            watermark_path = values["watermark-path"]

            origin_image = open_resize(origin_image_path, resize=img_size)
            watermark_image = open_resize(watermark_path, resize=watermark_size)

            unsigned_image = embed_extract_watermark(origin_image, watermark_image, 4)

            sign_path = "../output/signed.png"
            signed_image.save(sign_path, format="PNG")

            f_window["unsigned-image"].update(data=convert_to_bytes(unsigned_image))

    f_window.close()
