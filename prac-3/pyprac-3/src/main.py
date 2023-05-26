import PySimpleGUI as sg

import src.part_a as prt_a
import src.part_b as prt_b
import src.part_c as prt_c
import src.part_d as prt_d
import src.part_e as prt_e
import src.part_f as prt_f


def main():
    """"""

    sg.theme("DarkBlack")

    main_layout = [[sg.Text("Select part of practice work:")],
                   [sg.Button("Part-a"), sg.Button("Part-c"), sg.Button("Part-e")],
                   [sg.Button("Part-b"), sg.Button("Part-d"), sg.Button("Part-f")],
                   [sg.Button("Quit")]]

    main_window = sg.Window("Prac-3 Py-implementation", main_layout, size=(310, 130))

    while True:
        event, values = main_window.read()
        print(event, values)
        if event in (sg.WIN_CLOSED, "Quit"):
            break
        if event == "Part-a":
            # Show window with result of part a of practice
            main_window.hide()
            prt_a.run()
            main_window.un_hide()
        if event == "Part-b":
            # Show window with result of part b of practice
            main_window.hide()
            prt_b.run()
            main_window.un_hide()
        if event == "Part-c":
            # Show window with result of part c of practice
            main_window.hide()
            prt_c.run()
            main_window.un_hide()
        if event == "Part-d":
            # Show window with result of part d of practice
            main_window.hide()
            prt_d.run()
            main_window.un_hide()
        if event == "Part-e":
            # Show window with result of part e of practice
            main_window.hide()
            prt_e.run()
            main_window.un_hide()
        if event == "Part-f":
            # Show window with result of part f of practice
            main_window.hide()
            prt_f.run()
            main_window.un_hide()

    main_window.close()


if __name__ == '__main__':
    main()
