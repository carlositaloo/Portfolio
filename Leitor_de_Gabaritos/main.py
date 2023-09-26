import os
import cv2
import pickle
import numpy as np
from imutils import contours
import extrairGabarito

os.system("cls")


usar_webcam = False  # Defina como True para usar a webcam
tipoGabarito = True   # True para gabarito de bolhas, False para gabarito de quadrados
questoes = []

if usar_webcam:
    # Inicialize a captura de vídeo a partir da webcam (0 é geralmente a câmera padrão)
    captura = cv2.VideoCapture(1)
else:
    # Carregue a imagem estática
    imagem_caminho = 'gabarito2.png'
    img = cv2.imread(imagem_caminho)

if (usar_webcam and captura.isOpened()) or (not usar_webcam and img is not None):
    while True:
        tecla = cv2.waitKey(1)
        if usar_webcam:
            check, frame = captura.read()   # Captura o frame da webcam
            # Rotaciona o frame
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        else:
            frame = img  # Usar a imagem estática

        # Extrai o gabarito da imagem
        zoomGabarito, bbox = extrairGabarito.extrairMaiorCtn(frame)
        if zoomGabarito is not None:    # Verifica se o gabarito foi encontrado
            contorno, bbox2 = extrairGabarito.perspectivaCB(zoomGabarito)
            if contorno is not None:    # Mostra o que esta sendo identificado como quadrado
                frame_copy = frame.copy()
                contorno_copy = contorno.copy()
                cv2.drawContours(frame_copy, [bbox2], -1, (255, 0, 0), 2)

                # Converte a imagem para tons de cinza
                imgCinza = cv2.cvtColor(contorno, cv2.COLOR_BGR2GRAY)
                # Aplica o filtro de cinza ESCOLHA UMA IMGTH. A PRIMEIRA É MAIS EFICIENTE
                imgTh1 = cv2.adaptiveThreshold(
                    imgCinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
                ret, imgTh2 = cv2.threshold(
                    imgCinza, 70, 255, cv2.THRESH_BINARY_INV)
                blurred = cv2.GaussianBlur(imgCinza, (3, 3), 0)
                imgTh3 = cv2.Canny(blurred, 20, 150)

                imgTh = imgTh1
                imgTh_copy = imgTh.copy()

                questaoCnts = extrairGabarito.questoes(imgTh, tipoGabarito)
                # print(questaoCnts)
                
                questaoCnts = contours.sort_contours(questaoCnts,method="top-to-bottom")[0]
                correto = 0
                for (q, i) in enumerate(np.arange(0, len(questaoCnts), 5)):
                    cnts = contours.sort_contours(questaoCnts[i:i + 5])[0]
                    bubbled = None
                    
                if questaoCnts is not None:
                    for c in questaoCnts:
                        cv2.drawContours(contorno_copy, [c], -1, (0, 255, 0), 2)

                # with open('questoes.pkl', 'rb') as arquivo:
                #     questoes = pickle.load(arquivo)

                # if tecla == 13:
                #     print(questoes)
                # for c in questoes:
                #     cv2.drawContours(contorno_copy, [c], -1, (0, 0, 255), 2)

            # Desenha o retângulo do gabarito
            # cv2.rectangle(
                # frame, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (255, 0, 0), 3)

        cv2.imshow("Video da Webcam", frame_copy)
        cv2.moveWindow("Video da Webcam", 0, 0)

        if contorno is not None:
            cv2.imshow("Video da Webcam Gabarito", contorno_copy)
            cv2.imshow("Video da Webcam Cinza", imgTh_copy)
            # cv2.imshow("Video da zoomGabarito", zoomGabarito)

        if tecla == 27:
            print('Saindo...')
            # with open('questoes.pkl', 'wb') as arquivo:
            # pickle.dump(questoes, arquivo)
            break

    # cv2.imwrite("foto.jpg", frame)  # Salva a imagem
    if usar_webcam:
        captura.release()                   # Desliga a webcam
    cv2.destroyAllWindows()             # Fecha todas as janelas cv2
else:
    print('Não foi possível carregar a imagem.')
