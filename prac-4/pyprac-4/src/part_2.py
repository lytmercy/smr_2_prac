import PySimpleGUI as sg

from utils import open_resize, convert_to_bytes, seamless_image_in_image_insertion


def run():
    """"""

    sg.theme("DarkBlack")

    # Define right column of content
    right_col = [[sg.Text("Parent image from: "), sg.In("Choose file", size=(25, 1), enable_events=True, k="first-path"),
                  sg.FileBrowse(initial_folder="../input")],
                 [sg.Text("Embeddable image from: "), sg.In("Choose file", size=(25, 1), enable_events=True, k="second-path"),
                  sg.FileBrowse(initial_folder="../input")],
                 [sg.Button("Run inception", k="inception-act")]]

    img_size = (500, 300)
    embed_size = (100, 100)
    new_img_size = (500, 300)

    # Define image column of content of this part
    image_col = [[sg.Text("Parent image | Embeddable image")],
                 [sg.Image(size=img_size, k="parent-image"), sg.Image(size=embed_size, k="embeddable-image")],
                 [sg.Text("New image")],
                 [sg.Image(size=new_img_size, k="new-image")]]

    # Construct full layout from all columns
    second_layout = [[sg.Column(image_col, element_justification='c', size=(830, 700)),
                      sg.VSeparator(),
                      sg.Column(right_col, element_justification='c')]]

    second_window = sg.Window("Prac-4 -- part-2", second_layout, resizable=False, size=(1330, 700))

    while True:
        event, values = second_window.read()
        print(event, values)
        if event in (sg.WIN_CLOSED, "Exit"):
            break
        if event == "first-path":
            image_path = values["first-path"]
            image = open_resize(image_path, resize=img_size)
            second_window["parent-image"].update(data=convert_to_bytes(image))
            second_window["new-image"].update()

        if event == "second-path":
            image_path = values["second-path"]
            image = open_resize(image_path, resize=embed_size)
            second_window["embeddable-image"].update(data=convert_to_bytes(image))
            second_window["new-image"].update()

        if event == "inception-act":
            frst_image_path = values["first-path"]
            scnd_image_path = values["second-path"]

            frst_image = open_resize(frst_image_path, resize=img_size)
            scnd_image = open_resize(scnd_image_path, resize=embed_size)

            new_image = seamless_image_in_image_insertion(frst_image, scnd_image, (50, 50), (150, 150))
            new_image.save("../output/part-2-res.png", format="PNG")

            second_window["new-image"].update(data=convert_to_bytes(new_image))

    second_window.close()
