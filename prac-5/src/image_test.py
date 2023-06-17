import PySimpleGUI as sg

from src.utils import open_resize, convert_to_bytes, viola_jones_algo


def run():
    """"""

    sg.theme("DarkBlack")

    # Define right column of content
    right_col = [[sg.Text("Image from: "), sg.In("Choose file", size=(25, 1), enable_events=True, k="file-path"),
                  sg.FileBrowse(initial_folder="../input")],
                 [sg.Button("Detect Face", k="detect-act")]]

    img_size = (350, 400)
    res_size = (350, 400)
    # Define image column of content of this part
    image_col = [[sg.Text("Original image")],
                 [sg.Image(size=img_size, k="origin-image")],
                 [sg.Text("Detected Face on Resulted image")],
                 [sg.Image(size=res_size, k="resulted-image")]]

    # Construct full layout from all columns
    first_layout = [[sg.Column(image_col, element_justification='c', size=(450, 890)),
                     sg.VSeparator(),
                     sg.Column(right_col, element_justification='c')]]

    first_window = sg.Window("Prac-5 -- Image test", first_layout, resizable=False, size=(850, 890))

    while True:
        event, values = first_window.read()
        print(event, values)
        if event in (sg.WIN_CLOSED, "Exit"):
            break
        if event == "file-path":
            image_path = values["file-path"]
            image = open_resize(image_path, resize=img_size)
            first_window["origin-image"].update(data=convert_to_bytes(image))
            first_window["resulted-image"].update()

        if event == "detect-act":
            image_path = values["file-path"]
            image = open_resize(image_path, resize=img_size)

            resulted_image = viola_jones_algo(image)

            first_window["resulted-image"].update(data=convert_to_bytes(resulted_image))

    first_window.close()
