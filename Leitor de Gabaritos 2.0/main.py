import os
import cv2
import numpy as np
import imutils
from imutils.perspective import four_point_transform

imagem_caminho = 'image/gabarito4.png'


def extrairMaiorCtn(frame):
    imgCinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgTh = cv2.adaptiveThreshold(
        imgCinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 12)
    kernel = np.ones((2, 2), np.uint8)
    imgDil = cv2.dilate(imgTh, kernel)
    contours, _ = cv2.findContours(
        imgDil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if contours:
        maiorCtn = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(maiorCtn)
        margin = 10
        x, y, w, h = x - margin, y - margin, w + 2 * margin, h + 2 * margin
        x, y, w, h = max(x, 0), max(y, 0), max(w, 0), max(h, 0)
        bbox = [x, y, w, h]
        recorte = frame[y:y+h, x:x+w]
        return recorte, bbox
    else:
        return None, None


def perspectivaCB(img):
    cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(cinza, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)

    cnts = cv2.findContours(
        edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    if len(cnts) > 0:
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                bbox2 = approx
                corte = four_point_transform(img, bbox2.reshape(4, 2))
                corte = cv2.resize(corte, (300, 550))
                return corte, bbox2
    return None, None


def questoes(gabTh):
    cnts = cv2.findContours(gabTh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    questaoCnts = []
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        ar = w / float(h)
        if w >= 13 and h >= 13 and 0.1 <= ar <= 3.3:
            questaoCnts.append(c)
    return questaoCnts


def processar_frame(frame):
    zoomGabarito, bbox = extrairMaiorCtn(frame)
    if zoomGabarito is not None:
        contorno, bbox2 = perspectivaCB(zoomGabarito)
        if contorno is not None:
            frame_copy = frame.copy()
            contorno_copy = contorno.copy()
            cv2.drawContours(frame_copy, [bbox2], -1, (255, 0, 0), 2)

            imgCinza = cv2.cvtColor(contorno, cv2.COLOR_BGR2GRAY)
            imgTh = cv2.adaptiveThreshold(
                imgCinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
            imgTh_copy = imgTh.copy()

            questaoCnts = questoes(imgTh)
            for c in questaoCnts:
                cv2.drawContours(contorno_copy, [c], -1, (0, 255, 0), 2)

            return frame_copy, contorno_copy, imgTh_copy
    return frame, None, None


def main():
    os.system("cls")
    usar_webcam = False

    if usar_webcam:
        captura = cv2.VideoCapture(1)
    else:
        img = cv2.imread(imagem_caminho)

    if (usar_webcam and captura.isOpened()) or (not usar_webcam and img is not None):
        while True:
            tecla = cv2.waitKey(1)
            if usar_webcam:
                _, frame = captura.read()
                frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            else:
                frame = img

            frame_copy, contorno_copy, imgTh_copy = processar_frame(frame)

            # Redimensionar as imagens antes de exibir
            frame_copy = cv2.resize(frame_copy, (300, 400))
            cv2.imshow("Video da Webcam", frame_copy)
            cv2.moveWindow("Video da Webcam", 0, 0)

            if contorno_copy is not None:
                contorno_copy = cv2.resize(contorno_copy, (300, 400))
                imgTh_copy = cv2.resize(imgTh_copy, (300, 400))
                cv2.imshow("Video da Webcam Gabarito", contorno_copy)
                cv2.imshow("Video da Webcam Cinza", imgTh_copy)

            if tecla == 27:
                print('Saindo...')
                break

        if usar_webcam:
            captura.release()
        cv2.destroyAllWindows()
    else:
        print('Não foi possível carregar a imagem.')


if __name__ == "__main__":
    main()
