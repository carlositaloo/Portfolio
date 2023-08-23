# Importe as bibliotecas necessárias
from imutils.perspective import four_point_transform
from imutils import contours
import numpy as np
import imutils
import cv2
import os

# Limpa o terminal (apenas para sistemas Windows)
os.system("cls")

# Inicializa variáveis
ct = 0
cap = cv2.VideoCapture(1)  # Inicializa a captura de vídeo da câmera (mude para 0 se for a câmera padrão)
correct = 0
gb = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]  # Gabarito

# Loop principal que captura e processa quadros da câmera em tempo real
while True:
    ct = 0
    ret, image = cap.read()  # Captura um quadro da câmera
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Converte para escala de cinza
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)  # Aplica um desfoque gaussiano
    edged = cv2.Canny(blurred, 20, 60)  # Aplica detecção de bordas de Canny
    cv2.imshow("Camera", edged)  # Exibe o quadro com bordas

    # Se a tecla 'q' for pressionada, saia do loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.moveWindow("Camera", 0, 0)

    # Encontre contornos nas bordas da imagem
    cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    docCnt = None

    # Verifique se existem contornos detectados
    if len(cnts) > 0:
        # Classifique os contornos por área em ordem decrescente
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

        for c in cnts:
            peri = 0.02 * cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, peri, True)

            # Verifique se o contorno tem aproximadamente 4 vértices
            if len(approx) == 4:
                ct = 1
                docCnt = approx
                print(f"Contorno encontrado{docCnt}")
                break
        # Se um contorno de 4 vértices for encontrado
        if ct == 1:
            # Aplique a transformação de perspectiva para retificar a imagem
            paper = four_point_transform(image, docCnt.reshape(4, 2))
            warped = four_point_transform(gray, docCnt.reshape(4, 2))
            altura = paper.shape[0] // 11
            largura = paper.shape[0] // 2.95

            # Recorte a região de interesse (ROI)
            paper = paper[altura:paper.shape[0], largura:paper.shape[1]]
            thresh = cv2.threshold(warped, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            thresh = thresh[altura:thresh.shape[0], largura:thresh.shape[1]]

            # Se a região de interesse (ROI) for válida
            if thresh.shape[0] > 0 and thresh.shape[1] > 0:
                cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                cnts = cnts[0] if imutils.is_cv2() else cnts[1]
                questionCnts = []

                for c in cnts:
                    tamanho = thresh.shape[1] / 5
                    (x, y, w, h) = cv2.boundingRect(c)
                    ar = w / float(h)
                    approx = cv2.approxPolyDP(c, peri, True)

                    # Verifique se o contorno atende a critérios específicos
                    if (w <= tamanho and h < tamanho) and (ar >= 1.6 and ar <= 2.6) and (w > tamanho / 10 and h > tamanho / 10):
                        questionCnts.append(c)

                print(len(questionCnts))

                # Se 50 contornos forem encontrados, saia do loop
                if len(questionCnts) == 50:
                    break

    cont = 0
    x = 0
    y = 0
    res = []
    bubbled = []
    questao = []

    # Verifique se a variável 'questionCnts' está definida
    if 'questionCnts' in locals():
        for (q, i) in enumerate(np.arange(0, len(questionCnts), 5)):
            cont = 0
            cnts = contours.sort_contours(questionCnts[i:i + 5])[0]
            bubbled = []

            for (j, c) in enumerate(cnts):
                x = thresh.shape[0]
                y = thresh.shape[1]
                mask = np.zeros(thresh.shape, dtype="uint8")
                cv2.drawContours(mask, [c], -1, 255, -1)
                mask = cv2.bitwise_and(thresh, thresh, mask=mask)
                total = cv2.countNonZero(mask)

                if total > x // 20 * y // 10:
                    bubbled.append(j)
                    cont += 1
                    
                    # Desenhe um retângulo ao redor do contorno
                    (x, y, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(paper, (x, y), (x + w, y + h), (0, 255, 0), 2)

            if cont == 1:
                res.append(bubbled[0])
            else:
                res.append(-1)

            color = (0, 0, 255)
            k = gb[q]

            if cont == 1:
                if k == bubbled[0]:
                    color = (0, 255, 0)
                    correct += 1

            for s in range(cont):
                cv2.drawContours(paper, [cnts[bubbled[s]]], -1, color, 3)

        # Exiba a imagem processada com os contornos
        cv2.imshow("Cartao Resposta", paper)
    else:
        print("Nenhum contorno foi encontrado.")

    res2 = []

    for i in range(len(res)):
        res2.append(res[len(res) - i - 1])

    print("Gabarito:", gb)
    print("Respostas:", res2)
    print("Nota:", float(correct))

    # Aguarde até que uma tecla seja pressionada (remova este trecho se desejar exibição contínua)
    sair = cv2.waitKey(0)
    if sair == 27:
        break
    cv2.waitKey(0)

# Libere a câmera e feche todas as janelas
cv2.imshow("real", image)
cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()
