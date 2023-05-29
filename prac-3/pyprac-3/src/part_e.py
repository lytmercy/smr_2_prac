import PySimpleGUI as sg

from src.utils import convert_to_bytes, open_resize
from src.utils import blur_image, res_up_image, median_image, erosion_image, build_up_image, sobel_image


def run():
    """"""

    sg.theme("DarkBlack")

    # Define right column of content
    right_col = [[sg.Text("Image from: "), sg.In("Choose file", size=(25, 1), enable_events=True, k="file-path"),
                  sg.FileBrowse(initial_folder="../input")],
                 [sg.Button("Blur-Res up image", k="blur-res-up-act")],
                 [sg.Button("Median filter", k="median-act")],
                 [sg.Button("Erosion filter", k="erosion-act")],
                 [sg.Button("Building up filter", k="build-up-act")],
                 [sg.Button("Sobel filter", k="sobel-act")]]

    img_size = (500, 300)
    flt_size = (500, 300)
    # Define image column of content of this part
    image_col = [[sg.Text("Original image")],
                 [sg.Image(size=img_size, k="origin-image")],
                 [sg.Text("Filtered image")],
                 [sg.Image(size=flt_size, k="filtered-0-image"),
                  sg.Image(size=flt_size, k="filtered-1-image"),
                  sg.Image(size=flt_size, k="filtered-2-image")]]

    # Construct full layout from all columns
    e_layout = [[sg.Column(image_col, element_justification='c', size=(1520, 690)),
                 sg.VSeparator(),
                 sg.Column(right_col, element_justification='c')]]

    e_window = sg.Window("Prac-3 -- part-e", e_layout, resizable=False, size=(1920, 690))

    while True:
        event, values = e_window.read()
        print(event, values)
        if event in (sg.WIN_CLOSED, "Exit"):
            break
        if event == "file-path":
            image_path = values["file-path"]
            image = open_resize(image_path, resize=img_size)
            e_window["origin-image"].update(data=convert_to_bytes(image))
            e_window["filtered-0-image"].update()
            e_window["filtered-1-image"].update()
            e_window["filtered-2-image"].update()

        if event == "blur-res-up-act":
            image_path = values["file-path"]
            image = open_resize(image_path, resize=img_size)

            blured_image = blur_image(image)
            bh_res_image = res_up_image(blured_image)
            h_res_image = res_up_image(image)

            e_window["filtered-0-image"].update(data=convert_to_bytes(blured_image))
            e_window["filtered-1-image"].update(data=convert_to_bytes(bh_res_image))
            e_window["filtered-2-image"].update(data=convert_to_bytes(h_res_image))

        if event == "median-act":
            image_path = values["file-path"]
            image = open_resize(image_path, resize=img_size)

            medianed_image = median_image(image, 3)

            e_window["filtered-0-image"].update()
            e_window["filtered-1-image"].update(data=convert_to_bytes(medianed_image))
            e_window["filtered-2-image"].update()

        if event == "erosion-act":
            image_path = values["file-path"]
            image = open_resize(image_path, resize=img_size)

            erosioned_image = erosion_image(image)

            e_window["filtered-0-image"].update(data=convert_to_bytes(erosioned_image))
            e_window["filtered-1-image"].update()
            e_window["filtered-2-image"].update()

        if event == "build-up-act":
            image_path = values["file-path"]
            image = open_resize(image_path, resize=img_size)

            builded_up_image = build_up_image(image)

            e_window["filtered-1-image"].update()
            e_window["filtered-2-image"].update(data=convert_to_bytes(builded_up_image))

        if event == "sobel-act":
            image_path = values["file-path"]
            image = open_resize(image_path, resize=img_size)

            sobeled_image = sobel_image(image)

            e_window["filtered-0-image"].update()
            e_window["filtered-1-image"].update(data=convert_to_bytes(sobeled_image))
            e_window["filtered-2-image"].update()

    e_window.close()
