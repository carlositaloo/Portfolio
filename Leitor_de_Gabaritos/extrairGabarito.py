import cv2
import numpy as np
import imutils
from imutils.perspective import four_point_transform


def extrairMaiorCtn(img):
    imgCinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgTh = cv2.adaptiveThreshold(
        imgCinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 12)
    kernel = np.ones((2, 2), np.uint8)
    imgDil = cv2.dilate(imgTh, kernel)
    contours, _ = cv2.findContours(
        imgDil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if contours:  # Verifica se a lista de contornos não está vazia
        maiorCtn = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(maiorCtn)
        margin = 10
        x, y, w, h = x - margin, y - margin, w + 2 * margin, h + 2 * margin
        x, y, w, h = max(x, 0), max(y, 0), max(w, 0), max(h, 0)
        bbox = [x, y, w, h]
        recorte = img[y:y+h, x:x+w]
        # recorte = cv2.resize(recorte, (300, 550))
        return recorte, bbox
    else:
        return None, None  # Retorna valores nulos quando não há contornos
    
def perspectivaCB(img):
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
        return corte, bbox2, warped
    else:
        return None, None, None

def respostas(warped):
    thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    questaoCnts = []
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)
        if w >= 20 and h >= 20 and ar >= 0.5 and ar <= 2.0:
            questaoCnts.append(c)
            return questaoCnts
        else:
            return None
    