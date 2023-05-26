import PySimpleGUI as sg

from src.utils import convert_to_bytes, open_resize, invert_image


def run():
    """"""

    sg.theme("DarkBlack")

    # Define right column of content
    right_col = [[sg.Text("Image from: "), sg.In("Choose file", size=(25, 1), enable_events=True, k="file-path"),
                  sg.FileBrowse(initial_folder="../input")],
                 [sg.Button("Invert image", k="invert-act")]]

    img_size = (500, 300)
    # Define image column of content of this part
    image_col = [[sg.Text("Original image")],
                 [sg.Image(size=img_size, k="origin-image")],
                 [sg.Text("Inverted image")],
                 [sg.Image(size=img_size, k="inverted-image")]]

    # Construct full layout from all columns
    a_layout = [[sg.Column(image_col, element_justification='c', size=(500, 650)),
                 sg.VSeparator(),
                 sg.Column(right_col, element_justification='c')]]

    a_window = sg.Window("Prac-3 -- part-a", a_layout, resizable=False, size=(900, 650))

    while True:
        event, values = a_window.read()
        print(event, values)
        if event in (sg.WIN_CLOSED, "Exit"):
            break
        if event == "file-path":
            image_path = values["file-path"]
            image = open_resize(image_path, resize=img_size)
            a_window["origin-image"].update(data=convert_to_bytes(image))
            a_window["inverted-image"].update()
        if event == "invert-act":
            image_path = values["file-path"]
            image = open_resize(image_path, resize=img_size)
            inverted_image = invert_image(image)
            a_window["inverted-image"].update(data=convert_to_bytes(inverted_image))

    a_window.close()
