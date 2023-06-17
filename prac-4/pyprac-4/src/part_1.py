import PySimpleGUI as sg

from utils import open_resize, convert_to_bytes, recover_image_from_gradient_field


def run():
    """"""

    sg.theme("DarkBlack")

    # Define right column of content
    right_col = [[sg.Text("Image from: "), sg.In("Choose file", size=(25, 1), enable_events=True, k="file-path"),
                  sg.FileBrowse(initial_folder="../input")],
                 [sg.Button("Recover image", k="recover-act")]]

    img_size = (150, 100)
    grad_size = (150, 100)
    # Define image column of content of this part
    image_col = [[sg.Text("Original image")],
                 [sg.Image(size=img_size, k="origin-image")],
                 [sg.Text("Vx Grad | Recovered image | Vy Grad")],
                 [sg.Image(size=grad_size, k="vx-image"),
                  sg.Image(size=img_size, k="recovered-image"),
                  sg.Image(size=grad_size, k="vy-image")]]

    # Construct full layout from all columns
    first_layout = [[sg.Column(image_col, element_justification='c', size=(1030, 590)),
                     sg.VSeparator(),
                     sg.Column(right_col, element_justification='c')]]

    first_window = sg.Window("Prac-4 -- part-1", first_layout, resizable=False, size=(1430, 590))

    while True:
        event, values = first_window.read()
        print(event, values)
        if event in (sg.WIN_CLOSED, "Exit"):
            break
        if event == "file-path":
            image_path = values["file-path"]
            image = open_resize(image_path, resize=img_size)
            first_window["origin-image"].update(data=convert_to_bytes(image))
            first_window["vx-image"].update()
            first_window["vy-image"].update()
            first_window["recovered-image"].update()

        if event == "recover-act":
            image_path = values["file-path"]
            image = open_resize(image_path, resize=img_size)
            image.save("../output/original_img.png", format="PNG")

            recovered_image, vx_grad, vy_grad = recover_image_from_gradient_field(image)
            recovered_image.save("../output/recovered_img.png", format="PNG")

            first_window["vx-image"].update(data=convert_to_bytes(vx_grad))
            first_window["vy-image"].update(data=convert_to_bytes(vy_grad))
            first_window["recovered-image"].update(data=convert_to_bytes(recovered_image))

    first_window.close()
