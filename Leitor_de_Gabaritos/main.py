import os
import cv2
import extrairGabarito

os.system("cls")

img = cv2.VideoCapture(1)

if img.isOpened():  # Verifica se a webcam está funcionando
    while True:
        check, frame = img.read()   # Captura o frame da webcam
        # Gira o quadro em 90graus
        frame90 = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        # Extrai o gabarito da imagem
        gabarito, bbox = extrairGabarito.extrairMaiorCtn(frame90)
        if gabarito is not None:    # Verifica se o gabarito foi encontrado
            contorno, bbox2, imgTh4 = extrairGabarito.perspectivaCB(gabarito)
            if contorno is not None:    # Mostra o que esta sendo identificado como quadrado
                cv2.drawContours(gabarito, [bbox2], -1, (0, 255, 0), 2)

                # Converte a imagem para tons de cinza
                imgCinza = cv2.cvtColor(contorno, cv2.COLOR_BGR2GRAY)
                # Aplica o filtro de cinza ESCOLHA UMA LINHA OU OUTRA. A PRIMEIRA É MAIS EFICIENTE
                imgTh1 = cv2.adaptiveThreshold(
                    imgCinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
                ret, imgTh2 = cv2.threshold(
                    imgCinza, 70, 255, cv2.THRESH_BINARY_INV)
                blurred = cv2.GaussianBlur(imgCinza, (3, 3), 0)
                imgTh3 = cv2.Canny(blurred, 20, 150)
                imgTh4 = cv2.threshold(
                    imgTh4, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

                imgTh = imgTh1
                
                respostas = extrairGabarito.respostas(imgTh4)
                if respostas is not None:
                    cv2.drawContours(gabarito, [respostas], -1, (0, 255, 0), 2)

            # Desenha o retângulo do gabarito
            # cv2.rectangle(
            #     frame90, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (255, 0, 0), 3)

        cv2.imshow("Video da Webcam", frame90)
        cv2.moveWindow("Video da Webcam", 0, 0)
        # if gabarito is not None:
        #     cv2.imshow("Video da Webcam Gabaritos", gabarito)
        if contorno is not None:
            cv2.imshow("Video da Webcam Gabarito", contorno)
            cv2.imshow("Video da Webcam Cinza", imgTh)

        sair = cv2.waitKey(1)
        if sair == 27:
            break

    # cv2.imwrite("foto.jpg", frame90)  # Salva a imagem
    img.release()                       # Desliga a webcam
    cv2.destroyAllWindows()             # Fecha todas as janelas cv2
