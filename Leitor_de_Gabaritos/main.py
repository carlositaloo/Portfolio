import os
import cv2
import extrairGabarito

os.system("cls")


usar_webcam = False  # Defina como True para usar a webcam

if usar_webcam:
    # Inicialize a captura de vídeo a partir da webcam (0 é geralmente a câmera padrão)
    captura = cv2.VideoCapture(1)
else:
    # Carregue a imagem estática
    imagem_caminho = 'gabarito2.png'
    img = cv2.imread(imagem_caminho)

if (usar_webcam and captura.isOpened()) or (not usar_webcam and img is not None):
    while True:
        if usar_webcam:
            check, frame = captura.read()   # Captura o frame da webcam
            # Rotaciona o frame
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        else:
            frame = img  # Usar a imagem estática

        # Extrai o gabarito da imagem
        gabarito, bbox = extrairGabarito.extrairMaiorCtn(frame)
        if gabarito is not None:    # Verifica se o gabarito foi encontrado
            contorno, bbox2, gabTh = extrairGabarito.perspectivaCB(gabarito)
            if contorno is not None:    # Mostra o que esta sendo identificado como quadrado
                cv2.drawContours(gabarito, [bbox2], -1, (255, 0, 0), 2)

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

                questaoCnts, gabTh = extrairGabarito.questoes(imgTh)
                if questaoCnts is not None:
                    for c in questaoCnts:
                        x, y, w, h = cv2.boundingRect(c)
                        cv2.drawContours(contorno, [c], -1, (0, 255, 0), 2)

            # Desenha o retângulo do gabarito
            # cv2.rectangle(
            #     frame, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (255, 0, 0), 3)

        cv2.imshow("Video da Webcam", frame)
        cv2.moveWindow("Video da Webcam", 0, 0)
        # if gabarito is not None:
        # cv2.imshow("Video da Webcam Gabaritos", gabarito)
        if contorno is not None:
            cv2.imshow("Video da Webcam Gabarito", contorno)
            cv2.imshow("Video da Webcam Cinza", gabTh)

        sair = cv2.waitKey(1)
        if sair == 27:
            break

    # cv2.imwrite("foto.jpg", frame)  # Salva a imagem
    if usar_webcam:
        captura.release()                   # Desliga a webcam
    cv2.destroyAllWindows()             # Fecha todas as janelas cv2
else:
    print('Não foi possível carregar a imagem.')
