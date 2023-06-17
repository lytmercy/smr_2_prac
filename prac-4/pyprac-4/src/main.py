import PySimpleGUI as sg

import part_1 as prt_1
import part_2 as prt_2


def main():
    """"""

    sg.theme("DarkBlack")

    main_layout = [[sg.Text("Select part of practice work:")],
                   [sg.Button("Part-1"), sg.Button("Part-2")],
                   [sg.Button("Quit")]]

    main_window = sg.Window("Prac-4 Py-implementation", main_layout, element_justification='c', size=(310, 130))

    while True:
        event, values = main_window.read()
        print(event, values)
        if event in (sg.WIN_CLOSED, "Quit"):
            break
        if event == "Part-1":
            # Show window with result of part a of practice
            main_window.hide()
            prt_1.run()
            main_window.un_hide()
        if event == "Part-2":
            # Show window with result of part b of practice
            main_window.hide()
            prt_2.run()
            main_window.un_hide()

    main_window.close()


if __name__ == '__main__':
    main()

