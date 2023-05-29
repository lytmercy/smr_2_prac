import PySimpleGUI as sg

from src.utils import convert_to_bytes, open_resize, get_colour_from_image


def run():
    """"""

    sg.theme("DarkBlack")

    # Define right column of content
    right_col = [[sg.Text("Image from: "), sg.In("Choose file", size=(25, 1), enable_events=True, k="file-path"),
                  sg.FileBrowse(initial_folder="../input")],
                 [sg.Button("Decompose image", k="dec-img-act")]]

    img_size = (500, 300)
    clr_size = (500, 300)
    # Define image column of content of this part
    image_col = [[sg.Text("Original image")],
                 [sg.Image(size=img_size, k="origin-image")],
                 [sg.Text("The colour range of the image")],
                 [sg.Image(size=img_size, k="red-image"),
                  sg.Image(size=img_size, k="green-image"),
                  sg.Image(size=img_size, k="blue-image")]]

    # Construct full layout from all columns
    c_layout = [[sg.Column(image_col, element_justification='c', size=(1500, 650)),
                 sg.VSeparator(),
                 sg.Column(right_col, element_justification='c')]]

    c_window = sg.Window("Prac-3 -- part-c", c_layout, resizable=False, size=(1900, 650))

    while True:
        event, values = c_window.read()
        print(event, values)
        if event in (sg.WIN_CLOSED, "Exit"):
            break
        if event == "file-path":
            image_path = values["file-path"]
            image = open_resize(image_path, resize=img_size)
            c_window["origin-image"].update(data=convert_to_bytes(image))
            c_window["red-image"].update()
            c_window["green-image"].update()
            c_window["blue-image"].update()
        if event == "dec-img-act":
            image_path = values["file-path"]
            image = open_resize(image_path, resize=clr_size)
            c_window["red-image"].update(data=convert_to_bytes(get_colour_from_image(image, 'r')))
            c_window["green-image"].update(data=convert_to_bytes(get_colour_from_image(image, 'g')))
            c_window["blue-image"].update(data=convert_to_bytes(get_colour_from_image(image, 'b')))

    c_window.close()
