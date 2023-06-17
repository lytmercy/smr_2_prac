import PySimpleGUI as sg

from src import image_test, webcam_test


def main():
    """"""

    sg.theme("DarkBlack")

    main_layout = [[sg.Text("Select part of practice work:")],
                   [sg.Button("Image Test"), sg.Button("Webcam Test")],
                   [sg.Button("Quit")]]

    main_window = sg.Window("Prac-5 Py-implementation", main_layout, element_justification='c', size=(310, 130))

    while True:
        event, values = main_window.read()
        print(event, values)
        if event in (sg.WIN_CLOSED, "Quit"):
            break
        if event == "Image Test":
            # Show window with result of part a of practice
            main_window.hide()
            image_test.run()
            main_window.un_hide()
        if event == "Webcam Test":
            # Show window with result of part b of practice
            main_window.hide()
            webcam_test.run()
            main_window.un_hide()

    main_window.close()


if __name__ == '__main__':
    main()

