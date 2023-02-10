import cv2
import numpy as np
import imutils
import pytesseract
import matplotlib.pyplot as plt


def process_image(img):
    (H, W) = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 200)
    cnts = cv2.findContours(
        edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
    screenCnt = None
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.018 * peri, True)
        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        detected = False
        # print ("No contour detected")
        return None, detected, None, None, None, None
    else:
        detected = True

        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(
            mask,
            [screenCnt],
            0,
            255,
            -1,
        )
        new_image = cv2.bitwise_and(img, img, mask=mask)
        (x, y) = np.where(mask == 255)

        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        Cropped = gray[topx : bottomx + 1, topy : bottomy + 1]

        return Cropped, detected, topx, topy, bottomx, bottomy


def show_image(img):
    plt.figure(figsize=(10, 10))
    plt.imshow(img, cmap="gray")
    plt.show()


def get_text(img):
    alphanumeric = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    config = f"-c tessedit_char_whitelist={alphanumeric} --tessdata-dir tessdata --psm 8"
    text = pytesseract.image_to_string(img, lang="eng", config=config)
    text = "".join([c for c in text if c.isalnum()])
    return text


def generate_plate(placa: str) -> list:
    placas = []
    placas.append(placa.replace("G", "0"))
    placas.append(placa.replace("G", "Q"))
    placas.append(placa.replace("0", "G"))
    placas.append(placa.replace("0", "Q"))
    placas.append(placa.replace("Q", "G"))
    placas.append(placa.replace("Q", "0"))

    return placas
