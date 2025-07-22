import pyautogui
import keyboard
import pyperclip
import time
import sys

# === CONFIGURAÇÕES ===
# IDs de atendimento
IDS = [
    "1-1-919291", "1-1-802553", "1-1-810649", "1-1-744091", "1-1-669096", "1-1-236843",
    "1-1-207808", "1-1-173618", "1-1-283389", "1-1-233753", "1-1-231388", "1-1-223547",
    "1-1-230096", "1-1-223555", "1-1-270944", "1-1-223519", "1-1-291813", "1-1-237742",
    "1-1-237783", "1-1-276908", "1-1-277039", "1-1-416808", "1-1-187741", "1-1-327347",
    "1-1-304466", "1-1-880126", "1-1-1292099", "1-1-1275130", "1-1-560652", "1-1-697919",
    "1-1-566819", "1-1-709611", "1-1-701361", "1-1-697523", "1-1-682022", "1-1-612705",
    "1-1-562056", "1-1-678881", "1-1-697527", "1-1-564017", "1-1-561332", "1-1-573110",
    "1-1-657813", "1-1-575390", "1-1-555129", "1-1-572179", "1-1-658110", "1-1-580859",
    "1-1-574419", "1-1-586851", "1-1-554721", "1-1-671760", "1-1-569537", "1-1-685434",
    "1-1-568142", "1-1-557793", "1-1-666664", "1-1-693839", "1-1-693878", "1-1-602455",
    "1-1-675684", "1-1-972320", "1-1-982487", "1-1-984868", "1-1-985103", "1-1-986195",
    "1-1-982819", "1-1-982874", "1-1-982766", "1-1-984844", "1-1-988199", "1-1-990792",
    "1-1-972361", "1-1-980422", "1-1-1004647", "1-1-988762", "1-1-973551", "1-1-974945",
    "1-1-1003796", "1-1-977133", "1-1-987979", "1-1-24203", "1-1-6525", "1-1-744780",
    "1-1-1213266"
]


def on_esc():
    print("\n< ESC pressionado — script encerrado >")
    sys.exit(0)

def main():
    pyautogui.hotkey('alt', 'tab') #Alterar janela
    time.sleep(1)  # dê um tempinho pra janela focar

    keyboard.add_hotkey('esc', on_esc)

    for atendimento_id in IDS:
        pyperclip.copy(atendimento_id)
        keyboard.add_hotkey('esc', on_esc)
        pyautogui.doubleClick(1762, 174, duration=0.25)  # Clica no campo de pesquisa
        pyautogui.hotkey('ctrl', 'v')  # cola o ID do atendimento
        time.sleep(1.5)
        keyboard.add_hotkey('esc', on_esc)
        pyautogui.click(114, 325, duration=0.25)  # Seleciona o primeiro resultado
        keyboard.add_hotkey('esc', on_esc)

    print("\n< Processo concluído >")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n!! Erro inesperado: {e}")
        sys.exit(1)
