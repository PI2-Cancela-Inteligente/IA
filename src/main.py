import cv2 as cv
from utils import *

cam = cv.VideoCapture(0)

while True:
    status, frame = cam.read()

    if not status:
        break

    if cv.waitKey(1) & 0xff == ord('q'):
        break
    
    img, detected, topx, topy, bottomx, bottomy = process_image(frame)
    if detected:
        cv.rectangle(frame,(topy,topx),(bottomy,bottomx),(0,255,0), 3)
        cv.putText(frame,"Contorno Encontrado",(0 + 200,0 + 0 + 50), cv.FONT_HERSHEY_COMPLEX,1, (56,142,72), 2, cv.LINE_AA)
        placa = get_text(img)
        cv.putText(frame,placa,(0 + 200,0 + 0 + 50), cv.FONT_HERSHEY_COMPLEX,1, (56,142,72), 2, cv.LINE_AA)
    else:
        prediction = 'SEM CONTORNO'
        cv.putText(frame,prediction,(0 + 200,0 + 0 + 50), cv.FONT_HERSHEY_COMPLEX,1,(0,40,255) , 2, cv.LINE_AA)

    cv.imshow("Screen",frame)