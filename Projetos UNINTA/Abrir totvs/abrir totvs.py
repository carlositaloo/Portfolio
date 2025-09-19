import pyautogui
import time
import keyboard
import sys
import os

# Configurações iniciais
TIMING = 0.1
script_dir = os.path.dirname(os.path.abspath(__file__))


# =========================
# Funções utilitárias
# =========================
def verificar_cancelamento():
    """Sai do script se o usuário pressionar ESC duas vezes."""
    try:
        if keyboard.is_pressed("esc"):
            print("Script cancelado pelo usuário.")
            time.sleep(0.1)  # evita múltiplas detecções
            if keyboard.is_pressed("esc"):  # confirma cancelamento
                sys.exit()
    except Exception:
        pass


def sleep_cancelamento(duration: float):
    """Sleep que verifica ESC a cada 0.1s."""
    elapsed = 0.0
    while elapsed < duration:
        verificar_cancelamento()
        sleep_time = min(0.1, duration - elapsed)
        time.sleep(sleep_time)
        elapsed += sleep_time


def aguardar_imagem(
    imagem_path: str, numero: int = 1, timeout: float = 30.0, intervalo: float = 0.1, confidence: float = 0.8
):
    """Aguarda uma imagem aparecer na tela e retorna a região (box) da n-ésima ocorrência."""
    caminho_completo = os.path.join(script_dir, imagem_path)
    inicio = time.time()
    while time.time() - inicio < timeout:
        verificar_cancelamento()
        try:
            todas = list(pyautogui.locateAllOnScreen(caminho_completo, confidence=confidence))
            if len(todas) >= numero:
                return todas[numero - 1]
        except Exception:
            # ignora erros temporários do locate
            pass
        sleep_cancelamento(intervalo)

    raise TimeoutError(f"Imagem {imagem_path} (ocorrência {numero}) não encontrada em {timeout}s")


def clicar(pos, img=None, click_img=False, wait_first=False, delay=0.15):
    """
    Clica em coordenadas fixas (pos) e lida com a imagem (img) associada ao passo.
    - Se wait_first=True: aguarda a imagem antes de clicar na posição.
      (útil quando a imagem já deveria estar visível antes do clique)
    - Se click_img=True: após aguardar a imagem, clica no centro da imagem.
      (por padrão apenas aguardamos a imagem)
    """
    # Se for para esperar a imagem antes do clique na posição:
    if wait_first and img:
        region = aguardar_imagem(img)
        # se pediu pra clicar na própria imagem:
        if click_img:
            cx, cy = pyautogui.center(region)
            pyautogui.click(cx, cy, duration=delay)
            sleep_cancelamento(TIMING)
        # depois clica na posição
        x, y = pos
        pyautogui.click(x, y, duration=delay)
        sleep_cancelamento(TIMING)
        return

    # comportamento padrão: clica na posição primeiro
    x, y = pos
    pyautogui.click(x, y, duration=delay)
    sleep_cancelamento(TIMING)

    # se houver imagem associada, aguarda-a (e opcionalmente clica nela)
    if img:
        region = aguardar_imagem(img)
        if click_img:
            cx, cy = pyautogui.center(region)
            pyautogui.click(cx, cy, duration=delay)
            sleep_cancelamento(TIMING)


# =========================
# Sequência de passos
# =========================
# Observações:
# - Por padrão cada passo faz: click(pos) -> aguarda img (se houver).
# - Se você quiser que a espera aconteça ANTES do clique na posição, use "wait_first": True.
# - Se você quiser que, além de aguardar, o script clique na própria imagem, use "click_img": True.
passos = [
    {"pos": (17, 43), "img": "img\\menu0.png"},                        # MENU (click -> wait)
    {"pos": (107, 283), "img": "img\\erro.png", "click_img": True},    # SERVIÇOS GLOBAIS (click -> wait -> click imagem)
    {"pos": (179, 44), "img": "img\\cortina0.png", "wait_first": True},# SUB MENU (espera cortina antes de clicar na posição)
    {"pos": (176, 94), "img": "img\\usuario.png"},                     # USUARIOS
    {"pos": (17, 43), "img": "img\\img0.png"},                         # MENU
    {"pos": (129, 110), "img": "img\\menu0.png"},                      # EDUCACIONAL
    {"pos": (341, 125), "img": "img\\educacional.png"},                # EDUCACIONAL
    {"pos": (27, 82), "img": "img\\img1.png"},                         # ALUNO
    {"pos": (79, 84), "img": "img\\img2.png"},                         # PROFESSOR
    {"pos": (17, 43), "img": "img\\menu0.png"},                        # MENU
    {"pos": (165, 86), "img": "img\\menu0.png"},                       # RH
    {"pos": (386, 157), "img": "img\\cortina1.png"},                   # GESTÃO DE PESSOAS
    {"pos": (207, 42), "img": "img\\acompanhamento.png"},              # SUB MENU
    {"pos": (42, 72), "img": "img\\img3.png"},                         # FUNCIONARIO
    {"pos": (94, 85), "img": "img\\img4.png"},                         # PESSOAS
    {"pos": (17, 43), "img": "img\\menu0.png"},                        # MENU
    {"pos": (129, 110), "img": "img\\menu0.png"},                      # EDUCACIONAL
    {"pos": (341, 125), "img": "img\\educacional.png"},                # EDUCACIONAL
    {"pos": (768, 93), "img": "img\\disciplina.png"},                  # DISCIPLINA
]


# =========================
# Execução automática
# =========================
if __name__ == "__main__":
    try:
        for passo in passos:
            pos = passo["pos"]
            img = passo.get("img")
            click_img = passo.get("click_img", False)
            wait_first = passo.get("wait_first", False)
            clicar(pos, img=img, click_img=click_img, wait_first=wait_first)
    except KeyboardInterrupt:
        print("Interrompido pelo usuário.")
    except Exception as e:
        print("Erro durante execução:", e)
        raise
