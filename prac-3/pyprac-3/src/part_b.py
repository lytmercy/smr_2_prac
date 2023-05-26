import PySimpleGUI as sg

from src.utils import convert_to_bytes, open_resize, add_number_to_colour_component


def run():
    """"""

    sg.theme("DarkBlack")

    # Define right column of content
    right_col = [[sg.Text("Image from: "), sg.In("Choose file", size=(25, 1), enable_events=True, k="file-path"),
                  sg.FileBrowse(initial_folder="../input")],
                 [sg.Text("Choose colour parameters")],
                 [sg.Text("Colour:"), sg.In(k="clr", size=(5, 1)),
                  sg.Text("Add number:"), sg.In(k="clr-num", size=(5, 1)),
                  sg.Button("Paint image", k="add-clr-act")]]

    img_size = (500, 300)
    # Define image column of content of this part
    image_col = [[sg.Text("Original image")],
                 [sg.Image(size=img_size, k="origin-image")],
                 [sg.Text("Edited image")],
                 [sg.Image(size=img_size, k="painted-image")]]

    # Construct full layout from all columns
    b_layout = [[sg.Column(image_col, element_justification='c', size=(500, 650)),
                 sg.VSeparator(),
                 sg.Column(right_col, element_justification='c')]]

    b_window = sg.Window("Prac-3 -- part-b", b_layout, resizable=False, size=(900, 650))

    while True:
        event, values = b_window.read()
        print(event, values)
        if event in (sg.WIN_CLOSED, "Exit"):
            break
        if event == "file-path":
            image_path = values["file-path"]
            image = open_resize(image_path, resize=img_size)
            b_window["origin-image"].update(data=convert_to_bytes(image))
            b_window["painted-image"].update()
        if event == "add-clr-act":
            image_path = values["file-path"]
            image = open_resize(image_path, resize=img_size)
            color, clr_num = values["clr"], values["clr-num"]
            re_color_image = add_number_to_colour_component(image, color, int(clr_num))
            b_window["painted-image"].update(data=convert_to_bytes(re_color_image))

    b_window.close()
