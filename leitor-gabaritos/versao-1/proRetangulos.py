from imutils.perspective import four_point_transform
from imutils import contours 
import numpy as np
import imutils
import cv2

# Função para processar retângulos em uma imagem
def proRetangulos(edged, image, gray):
    bbox2 = None
    # Encontra os contornos na imagem binária
    cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]  # Lida com diferentes versões do OpenCV
    
    ct = 0  # Inicialização de uma variável de contagem
    docCnt = None  # Inicialização de uma variável para armazenar os contornos de interesse
    
    if len(cnts) > 0:
        # Ordena os contornos pelo tamanho em ordem decrescente
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        
        # Itera pelos contornos encontrados
        for c in cnts:
            peri = 0.02 * cv2.arcLength(c, True)  # Calcula o perímetro do contorno
            approx = cv2.approxPolyDP(c, peri, True)  # Aproxima o contorno por um polígono
            if len(approx) == 4:  # Verifica se o polígono tem 4 vértices (retângulo)
                ct = 1  # Define a variável de contagem como 1
                docCnt = approx  # Armazena o retângulo encontrado
                break
    
    if ct == 1:  # Se um retângulo foi encontrado
        # Aplica a perspectiva para obter uma visão frontal do retângulo
        paper = four_point_transform(image, docCnt.reshape(4, 2))
        warped = four_point_transform(gray, docCnt.reshape(4, 2))
        
        # Define a região de interesse no papel
        altura = paper.shape[0] // 11
        largura = paper.shape[0] // 2.95
        paper = paper[altura:paper.shape[0], largura:paper.shape[1]]
        
        # Aplica um limiar para segmentar as áreas preenchidas no retângulo
        thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        thresh = thresh[altura:thresh.shape[0], largura:thresh.shape[1]] 
        
        if thresh.shape[0] > 0 and thresh.shape[1] > 0:
            # Encontra contornos nas áreas preenchidas
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if imutils.is_cv2() else cnts[1]
            questionCnts = []  # Inicialização de uma lista para contornos de interesse
            
            for c in cnts:
                tamanho = thresh.shape[1] / 5 
                (x, y, w, h) = cv2.boundingRect(c)
                bbox2 = x, y, w, h
                ar = w / float(h)
                approx = cv2.approxPolyDP(c, peri, True)
                
                # Verifica se o contorno atende a certos critérios
                if (w <= tamanho and h < tamanho) and (ar >= 1.6 and ar <= 2.6) and (w > tamanho / 10 and h > tamanho / 10):
                    questionCnts.append(c)  # Adiciona o contorno à lista de interesse
                    
                print(len(questionCnts))  # Imprime o número de contornos de interesse encontrados
                
                if len(questionCnts) == 50:  # Se encontrar 50 contornos de interesse, interrompe a busca
                    break
    return bbox2
