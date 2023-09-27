import cv2
import numpy as np
import imutils
from imutils.perspective import four_point_transform
from imutils import contours


def extrairMaiorCtn(frame):
    imgCinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgTh = cv2.adaptiveThreshold(imgCinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 12)
    kernel = np.ones((2, 2), np.uint8)
    imgDil = cv2.dilate(imgTh, kernel)
    contours, _ = cv2.findContours(imgDil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if contours:  # Verifica se a lista de contornos não está vazia
        maiorCtn = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(maiorCtn)
        margin = 10
        x, y, w, h = x - margin, y - margin, w + 2 * margin, h + 2 * margin
        x, y, w, h = max(x, 0), max(y, 0), max(w, 0), max(h, 0)
        bbox = [x, y, w, h]
        recorte = frame[y:y+h, x:x+w]
        # recorte = cv2.resize(recorte, (300, 550))
        return recorte, bbox
    else:
        return None, None  # Retorna valores nulos quando não há contornos


def perspectivaCB(img): # aplicar uma transformação de perspectiva ao exame, obtendo uma visão de cima para baixo.
    cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(cinza, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    bbox2 = None

    if len(cnts) > 0:
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        for c in cnts:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            if len(approx) == 4:
                bbox2 = approx
                corte = four_point_transform(img, bbox2.reshape(4, 2))
                warped = four_point_transform(cinza, bbox2.reshape(4, 2))
                corte = cv2.resize(corte, (300, 550))
    if bbox2 is not None:
        return corte, bbox2
    else:
        return None, None


def questoes(gabTh, tipoGabarito):
    # gabTh = cv2.threshold(gabTh, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(
        gabTh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    questaoCnts = []
    if tipoGabarito == True:
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            ar = w / float(h)
            if w >= 13 and h >= 13 and ar >= 0.9 and ar <= 3.3:
                questaoCnts.append(c)
    else:
        for c in cnts:
            (x, y, w, h) = cv2.boundingRect(c)
            ar = w / float(h)
            if w >= 6 and h >= 6 and ar >= 0.0 and ar <= 9.3:
                questaoCnts.append(c)
                
    questaoCnts = contours.sort_contours(questaoCnts,method="top-to-bottom")[0]
    correto = 0
    for (q, i) in enumerate(np.arange(0, len(questaoCnts), 4)):
        cnts = contours.sort_contours(questaoCnts[i:i + 4])[0]
        bubbled = None
    return questaoCnts
