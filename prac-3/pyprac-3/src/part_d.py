import PySimpleGUI as sg

from src.utils import convert_to_bytes, open_resize, merging_images


def run():
    """"""

    sg.theme("DarkBlack")

    # Define right column of content
    right_col = [[sg.Text("First image from: "), sg.In("Choose file", size=(25, 1), enable_events=True, k="first-path"),
                  sg.FileBrowse(initial_folder="../input")],
                 [sg.Text("Second image from: "), sg.In("Choose file", size=(25, 1), enable_events=True, k="second-path"),
                  sg.FileBrowse(initial_folder="../input")],
                 [sg.Text("Choose alpha parameter (0 < alpha < 1)")],
                 [sg.Text("Alpha:"), sg.In(k="alpha", size=(5, 1)), sg.Button("Merge images", k="mrg-img-act")],
                 [sg.Text("Or Slider alpha parameter (0 < alpha < 1)")],
                 [sg.Text("First Image"),
                  sg.Slider(range=(0, 20), default_value=10, orientation='h', disable_number_display=True,
                            size=(25, 15), enable_events=True, k="alpha-slider"),
                  sg.Text("Second Image")]]

    frst_img_size = (500, 300)
    scnd_img_size = (500, 300)
    new_img_size = (500, 300)
    # Define image column of content of this part
    image_col = [[sg.Text("Original images")],
                 [sg.Image(size=frst_img_size, k="first-image"), sg.Image(size=scnd_img_size, k="second-image")],
                 [sg.Text("New image")],
                 [sg.Image(size=new_img_size, k="new-image")]]

    # Construct full layout from all columns
    d_layout = [[sg.Column(image_col, element_justification='c', size=(1030, 650)),
                 sg.VSeparator(),
                 sg.Column(right_col, element_justification='c')]]

    d_window = sg.Window("Prac-3 -- part-d", d_layout, resizable=False, size=(1500, 650))

    while True:
        event, values = d_window.read()
        print(event, values)
        if event in (sg.WIN_CLOSED, "Exit"):
            break
        if event == "first-path":
            frst_image_path = values["first-path"]
            frst_image = open_resize(frst_image_path, resize=frst_img_size)
            d_window["first-image"].update(data=convert_to_bytes(frst_image))
            d_window["new-image"].update()
        if event == "second-path":
            scnd_image_path = values["second-path"]
            scnd_image = open_resize(scnd_image_path, resize=scnd_img_size)
            d_window["second-image"].update(data=convert_to_bytes(scnd_image))
            d_window["new-image"].update()
        if event == "mrg-img-act":
            frst_image_path = values["first-path"]
            scnd_image_path = values["second-path"]
            frst_image = open_resize(frst_image_path, resize=frst_img_size)
            scnd_image = open_resize(scnd_image_path, resize=scnd_img_size)
            alpha = float(values["alpha"])
            new_image = merging_images(frst_image, scnd_image, alpha)

            if new_image == "incrt alpha":
                sg.popup("Alpha is incorrect!", title="Bad parameter")
                continue

            d_window["new-image"].update(data=convert_to_bytes(new_image))
        if event == "alpha-slider":
            frst_image_path = values["first-path"]
            scnd_image_path = values["second-path"]

            frst_image = open_resize(frst_image_path, resize=frst_img_size)
            scnd_image = open_resize(scnd_image_path, resize=scnd_img_size)

            alpha = float(values["alpha-slider"]/20)

            new_image = merging_images(frst_image, scnd_image, alpha)

            if new_image == "incrt alpha":
                sg.popup("Alpha is incorrect!", title="Bad parameter")
                continue

            d_window["alpha"].update(alpha)
            d_window["new-image"].update(data=convert_to_bytes(new_image))

    d_window.close()
