import os
import cv2
import extrairGabarito

os.system("cls")

opcao1 = [0, 0, 108, 213]
opcao2 = [90, 80, 213, 318]
opcao = [opcao1, opcao2]

img = cv2.VideoCapture(0)

if img.isOpened():  # Verifica se a webcam está funcionando
    while True:
        # Captura o frame da webcam
        check, frame = img.read()

        # Extrai o gabarito da imagem
        gabarito, bbox = extrairGabarito.extrairMaiorCtn(frame)
        if gabarito is not None:
            # Converte a imagem para tons de cinza
            imgCinza = cv2.cvtColor(gabarito, cv2.COLOR_BGR2GRAY)
            # Aplica o filtro de cinza ESCOLHA UMA LINHA OU OUTRA. A PRIMEIRA É MAIS EFICIENTE
            imgTh1 = cv2.adaptiveThreshold(
                imgCinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
            ret, imgTh2 = cv2.threshold(
                imgCinza, 70, 255, cv2.THRESH_BINARY_INV)
            blurred = cv2.GaussianBlur(imgCinza, (3, 3), 0)
            imgTh3 = cv2.Canny(blurred, 20, 150)

            imgTh = imgTh3

            # Desenha o retângulo do gabarito
            cv2.rectangle(
                frame, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (255, 0, 0), 3)

        # for x, y, w, h in opcao:
        #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Video da Webcam", frame)
        cv2.moveWindow("Video da Webcam", 0, 0)
        if gabarito is not None:
            cv2.imshow("Video da Webcam Gabarito", gabarito)
            cv2.imshow("Video da Webcam Cinza", imgTh)

        sair = cv2.waitKey(1)
        if sair == 27:
            break

    # cv2.imwrite("foto.jpg", frame)
    img.release()
    cv2.destroyAllWindows()
