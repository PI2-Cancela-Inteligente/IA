import cv2 as cv
import requests
from utils import process_image, get_text, generate_plate
from rasp import open_door, setup

cam = cv.VideoCapture(2)

while True:
    status, frame = cam.read()
    setup()

    if not status:
        break

    if cv.waitKey(1) & 0xFF == ord("q"):
        break

    img, detected, topx, topy, bottomx, bottomy = process_image(frame)
    if detected:
        cv.rectangle(frame, (topy, topx), (bottomy, bottomx), (0, 255, 0), 3)
        cv.putText(
            frame,
            "Contorno Encontrado",
            (0 + 200, 0 + 0 + 50),
            cv.FONT_HERSHEY_COMPLEX,
            1,
            (56, 142, 72),
            2,
            cv.LINE_AA,
        )
        placa = get_text(img)
        cv.putText(
            frame,
            placa,
            (0 + 200, 0 + 0 + 100),
            cv.FONT_HERSHEY_COMPLEX,
            1,
            (56, 142, 72),
            2,
            cv.LINE_AA,
        )

        headers = {"Content-Type": "application/json"}
        placa = placa.upper()
        if len(placa) == 7:
            if "0" not in placa and "Q" not in placa and "G" not in placa:
                response = requests.post(
                    "http://140.238.191.18:5000/estaciona",
                    json={"placa": placa},
                    headers=headers,
                )
                print(response.status_code)

                if response.status_code == 201:
                    text_data = response.json().get("message")
                    cv.putText(
                        frame,
                        text_data,
                        (0 + 200, 0 + 0 + 150),
                        cv.FONT_HERSHEY_COMPLEX,
                        1,
                        (56, 142, 72),
                        2,
                        cv.LINE_AA,
                    )
                    open_door()
            else:
                # print("####################################")
                placas = generate_plate(placa)
                for placa in placas:
                    response = requests.post(
                        "http://140.238.191.18:5000/estaciona",
                        json={"placa": placa},
                        headers=headers,
                    )
                    print(response.status_code)
                    if response.status_code == 201:
                        text_data = response.json().get("message")
                        cv.putText(
                            frame,
                            text_data,
                            (0 + 200, 0 + 0 + 150),
                            cv.FONT_HERSHEY_COMPLEX,
                            1,
                            (56, 142, 72),
                            2,
                            cv.LINE_AA,
                        )
                        open_door()

                        break
    else:
        prediction = "SEM CONTORNO"
        cv.putText(
            frame,
            prediction,
            (0 + 200, 0 + 0 + 50),
            cv.FONT_HERSHEY_COMPLEX,
            1,
            (0, 40, 255),
            2,
            cv.LINE_AA,
        )

    cv.imshow("Screen", frame)
    # sleep(0.5)
