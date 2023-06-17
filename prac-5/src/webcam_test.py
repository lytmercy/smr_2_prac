import PySimpleGUI as sg
from PIL import Image
import cv2

from src.utils import open_resize, convert_to_bytes, viola_jones_algo


def run():
    """"""

    sg.theme("DarkBlack")

    # Define right column of content
    right_col = [[sg.Button("Run WebCam", k="run-act")],
                 [sg.Button("Stop WebCam", k="stop-act")]]

    video_size = (650, 530)

    # Define image column of content of this part
    image_col = [[sg.Text("WebCam Live")],
                 [sg.Image(size=video_size, k="webcam-video")]]

    # Construct full layout from all columns
    second_layout = [[sg.Column(image_col, element_justification='c', size=(650, 530)),
                      sg.VSeparator(),
                      sg.Column(right_col, element_justification='c')]]

    second_window = sg.Window("Prac-4 -- WebCam Test", second_layout, resizable=False, size=(810, 530))

    vc = cv2.VideoCapture(0)

    while (True):

        event, values = second_window.read(timeout=3)
        print(event, values)

        if event in (sg.WIN_CLOSED, "Exit"):
            vc.release()
            break

        if event == "run-act":
            second_window["webcam-video"].unhide_row()

        if event == "stop-act":
            second_window["webcam-video"].hide_row()

        _, v_frame = vc.read()
        v_frame = cv2.cvtColor(v_frame, cv2.COLOR_BGR2RGB)
        v_frame = Image.fromarray(v_frame)
        resulted_frame = viola_jones_algo(v_frame)
        second_window["webcam-video"](data=convert_to_bytes(resulted_frame))

    second_window.close()
