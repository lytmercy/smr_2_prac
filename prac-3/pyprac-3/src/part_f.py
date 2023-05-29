import PySimpleGUI as sg

from src.utils import convert_to_bytes, open_resize, merging_images


def run():
    """"""

    sg.theme("DarkBlack")

    # Define right column of content
    right_col = [[sg.Text("First image from: "), sg.In("Choose file", size=(25, 1), enable_events=True, k="image-path"),
                  sg.FileBrowse(initial_folder="../input")],
                 [sg.Text("Watermark from: "), sg.In("Choose file", size=(25, 1), enable_events=True, k="watermark-path"),
                  sg.FileBrowse(initial_folder="../input")],
                 [sg.Text("Choose alpha parameter (0 < alpha < 1)")],
                 [sg.Button("Merge images", k="mrg-img-act")]]

    img_size = (500, 300)
    watermark_size = (500, 300)
    new_img_size = (500, 300)
    # Define image column of content of this part
    image_col = [[sg.Text("Original image"), sg.Text("Watermark")],
                 [sg.Image(size=img_size, k="origin-image"), sg.Image(size=watermark_size, k="watermark-image")],
                 [sg.Text("New image")],
                 [sg.Image(size=new_img_size, k="new-image")]]

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
            f_window["new-image"].update()

        if event == "watermark-path":
            watermark_path = values["watermark-path"]
            watermark_image = open_resize(watermark_path, resize=watermark_size)
            f_window["watermark-image"].update(data=convert_to_bytes(watermark_image))
            f_window["new-image"].update()

        if event == "mrg-img-act":
            origin_image_path = values["image-path"]
            watermark_path = values["watermark-path"]

            origin_image = open_resize(origin_image_path, resize=img_size)
            watermark_image = open_resize(watermark_path, resize=watermark_size)

            new_image = merging_images(origin_image, watermark_image)

            f_window["new-image"].update(data=convert_to_bytes(new_image))

    f_window.close()
