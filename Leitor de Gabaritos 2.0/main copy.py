import os
import cv2
import numpy as np
import imutils
from imutils.perspective import four_point_transform
from imutils.contours import sort_contours

# Configurações e constantes
IMAGEM_CAMINHO = 'image/gabarito4.png'
MIN_PIXELS_RATIO = 0.9  # Proporção mínima de pixels para considerar uma bolha preenchida
USAR_WEBCAM = False

# Configuração da grade
num_perguntas = 52  # Número total de perguntas
num_colunas = 2  # Número de colunas de bolhas
perguntas_por_coluna = num_perguntas // num_colunas

# Gabarito
GABARITO = {
    1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'A', 6: 'B', 7: 'C', 8: 'D', 9: 'A', 10: 'B', 11: 'C', 12: 'D',
    13: 'A', 14: 'B', 15: 'C', 16: 'D', 17: 'A', 18: 'B', 19: 'C', 20: 'D', 21: 'A', 22: 'B', 23: 'C', 24: 'D',
    25: 'A', 26: 'B', 27: 'C', 28: 'D', 29: 'A', 30: 'B', 31: 'C', 32: 'D', 33: 'A', 34: 'B', 35: 'C', 36: 'D',
    37: 'A', 38: 'B', 39: 'C', 40: 'D', 41: 'A', 42: 'B', 43: 'C', 44: 'D', 45: 'A', 46: 'B', 47: 'C', 48: 'D',
    49: 'A', 50: 'B', 51: 'C', 52: 'D'
}


def reordenar_gabarito(gabarito, inverter=False):
    chaves_ordenadas = sorted(gabarito.keys())
    meio = (len(chaves_ordenadas) + 1) // 2
    primeira_metade = chaves_ordenadas[:meio]
    segunda_metade = chaves_ordenadas[meio:]

    novo_gabarito = {}
    for i in range(len(segunda_metade)):
        if inverter:
            novo_gabarito[primeira_metade[i]] = gabarito[2*i + 1]
            novo_gabarito[segunda_metade[i]] = gabarito[2*i + 2]
        else:
            novo_gabarito[2*i + 1] = gabarito[primeira_metade[i]]
            novo_gabarito[2*i + 2] = gabarito[segunda_metade[i]]

    if len(primeira_metade) > len(segunda_metade):
        if inverter:
            novo_gabarito[primeira_metade[-1]
                          ] = gabarito[len(novo_gabarito) + 1]
        else:
            novo_gabarito[len(novo_gabarito) +
                          1] = gabarito[primeira_metade[-1]]

    return novo_gabarito


def converter_gabarito(gabarito):
    mapeamento = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    novo_gabarito = {k-1: mapeamento[v] for k, v in gabarito.items()}
    return novo_gabarito


def extrair_maior_contorno(frame):
    img_cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img_th = cv2.adaptiveThreshold(
        img_cinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 12)
    kernel = np.ones((2, 2), np.uint8)
    img_dil = cv2.dilate(img_th, kernel)
    contours, _ = cv2.findContours(
        img_dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if contours:
        maior_contorno = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(maior_contorno)
        margin = 10
        x, y, w, h = x - margin, y - margin, w + 2 * margin, h + 2 * margin
        x, y, w, h = max(x, 0), max(y, 0), max(w, 0), max(h, 0)
        bbox = [x, y, w, h]
        recorte = frame[y:y+h, x:x+w]
        return recorte, bbox
    return None, None


def perspectiva_cb(img):
    cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(cinza, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)
    cnts = cv2.findContours(
        edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    if cnts:
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


def encontrar_questoes(gab_th):
    cnts = cv2.findContours(gab_th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    questao_cnts = [c for c in cnts if validar_questao(c)]
    return questao_cnts


def validar_questao(c):
    x, y, w, h = cv2.boundingRect(c)
    ar = w / float(h)
    return w >= 13 and h >= 13 and 0.1 <= ar <= 3.3


def processar_frame(frame, gabarito_numerico):
    zoom_gabarito, bbox = extrair_maior_contorno(frame)
    if zoom_gabarito is not None:
        contorno, bbox2 = perspectiva_cb(zoom_gabarito)
        if contorno is not None:
            return analisar_contorno(frame, contorno, bbox, bbox2, gabarito_numerico)
    return frame, None, None, None


def analisar_contorno(frame, contorno, bbox, bbox2, gabarito_numerico):
    frame_copy = frame.copy()
    contorno_copy = contorno.copy()
    respostas_copy = contorno.copy()

    # Ajustar bbox2 com a posição do maior contorno (bbox)
    bbox2 += bbox[:2]
    cv2.drawContours(frame_copy, [bbox2], -1, (255, 50, 255), 2)

    img_cinza = cv2.cvtColor(contorno, cv2.COLOR_BGR2GRAY)
    img_th = cv2.adaptiveThreshold(
        img_cinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    questao_cnts = encontrar_questoes(img_th)
    questao_cnts = sort_contours(questao_cnts, method="top-to-bottom")[0]

    # Dividir as questões em duas colunas
    colunas = [[], []]
    for (i, c) in enumerate(questao_cnts):
        colunas[i % num_colunas].append(c)

    # Ordenar cada coluna de cima para baixo
    for coluna in colunas:
        coluna.sort(key=lambda x: cv2.boundingRect(x)[1])

    # Misturar as colunas para obter a ordem correta
    questao_cnts = [c for col in colunas for c in col]

    blocos = [questao_cnts[i:i + 4] for i in range(0, len(questao_cnts), 4)]
    cores = [(255, 0, 0), (0, 255, 0), (0, 0, 255),
             (255, 255, 0), (255, 0, 255)]
    cor_index = 0
    respostas_aluno = {}
    for bloco in blocos:
        bubbled = []
        for j, c in enumerate(bloco):
            if is_bubbled(c, img_th):
                bubbled.append((cv2.countNonZero(cv2.bitwise_and(img_th, img_th, mask=cv2.drawContours(
                    np.zeros(img_th.shape, dtype="uint8"), [c], -1, 255, -1))), j))
            cv2.drawContours(
                contorno_copy, [c], -1, cores[cor_index % len(cores)], 2)
        if bubbled:
            bubbled.sort(reverse=True)
            if len(bubbled) == 1:
                # Converter índice para letra
                respostas_aluno[len(respostas_aluno) +
                                1] = chr(bubbled[0][1] + 65)
            else:
                respostas_aluno[len(respostas_aluno) + 1] = '-'
            for b in bubbled:
                cv2.drawContours(respostas_copy, [
                                 bloco[b[1]]], -1, (0, 255, 255), 2)  # Amarelo
        else:
            respostas_aluno[len(respostas_aluno) + 1] = '-'
        cor_index += 1

    # Verificar respostas do aluno em comparação com o gabarito
    for num_questao, resposta_aluno in respostas_aluno.items():
        resposta_certa = chr(gabarito_numerico[num_questao - 1] + 65)
        if resposta_aluno == '-':
            # Vermelho para questões não respondidas
            cv2.drawContours(respostas_copy, [
                             questao_cnts[num_questao - 1]], -1, (0, 0, 255), 2)
        elif resposta_aluno == resposta_certa:
            # Verde para respostas corretas
            cv2.drawContours(respostas_copy, [
                             questao_cnts[num_questao - 1]], -1, (0, 255, 0), 2)
        else:
            # Vermelho para respostas incorretas
            cv2.drawContours(respostas_copy, [
                             questao_cnts[num_questao - 1]], -1, (0, 0, 255), 2)

    # Reordenar as respostas do aluno de volta à ordem original
    respostas_aluno_reordenadas = reordenar_gabarito(
        respostas_aluno, inverter=True)

    return frame_copy, contorno_copy, respostas_copy, img_th, respostas_aluno_reordenadas


def is_bubbled(c, img_th):
    mask = np.zeros(img_th.shape, dtype="uint8")
    cv2.drawContours(mask, [c], -1, 255, -1)
    mask = cv2.bitwise_and(img_th, img_th, mask=mask)
    total = cv2.countNonZero(mask)
    area = cv2.contourArea(c)
    fill_ratio = total / area
    return fill_ratio > MIN_PIXELS_RATIO


def main():
    os.system("cls")
    gabarito_reordenado = reordenar_gabarito(GABARITO)
    gabarito_numerico = converter_gabarito(gabarito_reordenado)
    if USAR_WEBCAM:
        captura = cv2.VideoCapture(1)
    else:
        img = cv2.imread(IMAGEM_CAMINHO)
    if (USAR_WEBCAM and captura.isOpened()) or (not USAR_WEBCAM and img is not None):
        while True:
            tecla = cv2.waitKey(1)
            if USAR_WEBCAM:
                _, frame = captura.read()
                frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            else:
                frame = img
            frame_copy, contorno_copy, respostas_copy, img_th_copy, respostas_aluno = processar_frame(
                frame, gabarito_numerico)
            exibir_frames(frame_copy, contorno_copy,
                          respostas_copy, img_th_copy)
            if tecla == 27:
                respostas_aluno = dict(sorted(respostas_aluno.items()))
                print('\nRespostas do aluno:\n')
                print(respostas_aluno)
                print('\nSaindo...')
                break
        if USAR_WEBCAM:
            captura.release()
        cv2.destroyAllWindows()
    else:
        print('Não foi possível carregar a imagem.')


def exibir_frames(frame_copy, contorno_copy, respostas_copy, img_th_copy):
    frame_copy = cv2.resize(frame_copy, (250, 466))
    cv2.imshow("Video da Webcam", frame_copy)
    cv2.moveWindow("Video da Webcam", 0, 0)
    if contorno_copy is not None:
        contorno_copy = cv2.resize(contorno_copy, (250, 466))
        respostas_copy = cv2.resize(respostas_copy, (250, 466))
        img_th_copy = cv2.resize(img_th_copy, (250, 466))
        cv2.imshow("Video da Webcam Gabarito", contorno_copy)
        cv2.imshow("Video da Webcam Respostas", respostas_copy)
        cv2.imshow("Video da Webcam Cinza", img_th_copy)


if __name__ == "__main__":
    main()
