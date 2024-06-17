import os
import cv2
import numpy as np
import imutils
from imutils.perspective import four_point_transform
from imutils.contours import sort_contours

imagem_caminho = 'image/gabarito4.png'
MIN_PIXELS_RATIO = 0.9  # Proporção mínima de pixels para considerar uma bolha preenchida

# Gabarito
GABARITO = {
    1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'A', 6: 'B', 7: 'C', 8: 'D', 9: 'A', 10: 'B', 11: 'C', 12: 'D', 13: 'A', 14: 'B', 15: 'C', 16: 'D', 17: 'A', 18: 'B', 19: 'C', 20: 'D', 21: 'A', 22: 'B', 23: 'C', 24: 'D', 25: 'A', 26: 'B', 27: 'C', 28: 'D', 29: 'A', 30: 'B', 31: 'C', 32: 'D', 33: 'A', 34: 'B', 35: 'C', 36: 'D', 37: 'A', 38: 'B', 39: 'C', 40: 'D', 41: 'A', 43: 'B', 44: 'C', 45: 'D', 46: 'A', 47: 'B', 48: 'C', 49: 'D', 50: 'A', 51: 'B', 52: 'B'
    # Adicione todas as questões aqui
}


# Função para reordenar o gabarito com questões ímpares primeiro
def reordenar_gabarito(gabarito):
    # Separa os valores das chaves ímpares e pares
    valores_impares = [gabarito[k] for k in sorted(gabarito) if k % 2 != 0]
    valores_pares = [gabarito[k] for k in sorted(gabarito) if k % 2 == 0]

    # Junta os valores de volta em ordem original, mas com valores ímpares primeiro, depois pares
    novo_gabarito = {}
    for i, k in enumerate(sorted(gabarito)):
        if i < len(valores_impares):
            novo_gabarito[k] = valores_impares[i]
        else:
            novo_gabarito[k] = valores_pares[i - len(valores_impares)]

    return novo_gabarito

# Função para converter as letras das alternativas em índices numéricos


def converter_gabarito(gabarito):
    mapeamento = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    return {k: mapeamento[v] for k, v in gabarito.items()}


# Converter o gabarito original
GABARITO = reordenar_gabarito(GABARITO)
GABARITO_NUMERICO = converter_gabarito(GABARITO)


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
            respostas_copy = contorno.copy()
            cv2.drawContours(frame_copy, [bbox2], -1, (255, 0, 0), 2)

            imgCinza = cv2.cvtColor(contorno, cv2.COLOR_BGR2GRAY)
            imgTh = cv2.adaptiveThreshold(
                imgCinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
            imgTh_copy = imgTh.copy()

            questaoCnts = questoes(imgTh)

            # Ordenar os contornos de cima para baixo
            questaoCnts = sort_contours(questaoCnts, method="top-to-bottom")[0]

            # Verificar se há questões em blocos
            num_blocos = len(questaoCnts) // 4
            blocos = [questaoCnts[i*4:(i+1)*4] for i in range(num_blocos)]

            # Cores para os blocos de questões
            cores = [(255, 0, 0), (0, 255, 0), (0, 0, 255),
                     (255, 255, 0), (255, 0, 255)]
            cor_index = 0

            for bloco in blocos:
                cnts = sort_contours(bloco, method="left-to-right")[0]
                bubbled = []
                for j, c in enumerate(cnts):
                    mask = np.zeros(imgTh.shape, dtype="uint8")
                    cv2.drawContours(mask, [c], -1, 255, -1)
                    mask = cv2.bitwise_and(imgTh, imgTh, mask=mask)
                    total = cv2.countNonZero(mask)
                    area = cv2.contourArea(c)
                    fill_ratio = total / area
                    if fill_ratio > MIN_PIXELS_RATIO:
                        bubbled.append((total, j))
                    cv2.drawContours(
                        contorno_copy, [c], -1, cores[cor_index % len(cores)], 2)

                if bubbled:
                    for b in bubbled:
                        # Contornos azuis
                        cv2.drawContours(respostas_copy, [
                                         cnts[b[1]]], -1, (255, 0, 0), 2)
                cor_index += 1

            return frame_copy, contorno_copy, respostas_copy, imgTh_copy
    return frame, None, None, None


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

            frame_copy, contorno_copy, respostas_copy, imgTh_copy = processar_frame(
                frame)

            # Redimensionar as imagens antes de exibir
            frame_copy = cv2.resize(frame_copy, (250, 466))  # 300, 400
            cv2.imshow("Video da Webcam", frame_copy)
            cv2.moveWindow("Video da Webcam", 0, 0)

            if contorno_copy is not None:
                contorno_copy = cv2.resize(contorno_copy, (250, 466))
                respostas_copy = cv2.resize(respostas_copy, (250, 466))
                imgTh_copy = cv2.resize(imgTh_copy, (250, 466))
                cv2.imshow("Video da Webcam Gabarito", contorno_copy)
                cv2.imshow("Video da Webcam Respostas", respostas_copy)
                cv2.imshow("Video da Webcam Cinza", imgTh_copy)

            if tecla == 27:
                print(GABARITO)
                # print(GABARITO_NUMERICO)
                print('Saindo...')
                break

        if usar_webcam:
            captura.release()
        cv2.destroyAllWindows()
    else:
        print('Não foi possível carregar a imagem.')


if __name__ == "__main__":
    main()
