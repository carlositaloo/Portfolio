"""
Corretor Ortográfico — LanguageTool (pt-BR)
============================================
Atalho global : Ctrl+'
  → Seleciona todo o texto do app ativo, corrige via LanguageTool e cola de volta.

Bandeja do sistema:
  → Ícone verde  = pronto
  → Ícone amarelo = processando
  → Botão direito > Sair para encerrar

Instalação:
    pip install -r requirements.txt
    python corretor.py   (execute como Administrador no Windows)
"""

import sys
import time
import threading

import keyboard
import pyperclip
import pyautogui
import re
import os
import hashlib
import subprocess

import requests
from spellchecker import SpellChecker
import pystray
from PIL import Image, ImageDraw

# ─── Configurações ────────────────────────────────────────────────────────────

API_URL   = "https://api.languagetoolplus.com/v2/check"
LANGUAGE  = "pt-BR"
TIMEOUT   = 15        # segundos por requisição HTTP
MAX_CHARS = 20_000    # limite gratuito da API por requisição

COR_IDLE        = (34, 197, 94)    # verde  — aguardando
COR_PROCESSANDO = (234, 179, 8)    # amarelo — corrigindo

# ─── Estado global ────────────────────────────────────────────────────────────

_icon: pystray.Icon = None
_lock = threading.Lock()            # evita execuções simultâneas do hotkey
_apostrophe_suppressed = False    # garante que o key-up do atalho também seja suprimido

pyautogui.PAUSE    = 0      # remove pausa padrão entre ações do pyautogui
pyautogui.FAILSAFE = False  # desativa o failsafe de mover mouse p/ canto

# ─── Utilitários ──────────────────────────────────────────────────────────────

def log(msg: str) -> None:
    """Imprime no console; descarta silenciosamente quando rodando como .exe."""
    try:
        print(msg, flush=True)
    except Exception:
        pass


def criar_icone(cor: tuple) -> Image.Image:
    """Gera um ícone circular 64×64 com a cor RGBA indicada."""
    img  = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([4, 4, 60, 60], fill=cor)
    return img


def _set_icon(cor: tuple) -> None:
    """Atualiza o ícone da bandeja de forma thread-safe."""
    global _icon
    if _icon:
        try:
            _icon.icon = criar_icone(cor)
        except Exception:
            pass

# ─── Arquivo de configuração do usuário ──────────────────────────────────────────────

CONFIG_DIR  = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")), "CorretorOrtografico")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.txt")

_CONFIG_TEMPLATE = """\
# =============================================================================
# Corretor Ortográfico — Configurações do usuário
# Linhas começando com # são comentários e serão ignoradas.
# Salve o arquivo e reinicie o corretor para aplicar as mudanças.
# =============================================================================

[palavras_permitidas]
# Palavras que NÃO serão corrigidas (nomes próprios, siglas, termos técnicos).
# Uma palavra por linha:
api
apis
chat
chatgpt
codex
gemini
google
llm
llms
online
python
script
scripts
totvs
fluig

[abreviacoes]
# Abreviações informais e correções de digitação.
# Formato:  abreviação = texto expandido   (uma por linha)
vc = você
vcs = vocês
ce = você
cê = você
tb = também
tbm = também
tmb = também
pq = porque
q = que
qq = qualquer
qlqr = qualquer
n = não
nn = não
naum = não
blz = beleza
vlw = valeu
obg = obrigado
obgd = obrigado
pfv = por favor
pff = por favor
sdds = saudades
msg = mensagem
msgs = mensagens
pse = pois é
psé = pois é
td = tudo
tdo = tudo
hj = hoje
ont = ontem
agr = agora
dps = depois
mt = muito
mto = muito
msm = mesmo
cmg = comigo
ctg = contigo
kd = cadê
cade = cadê
tava = estava
tavam = estavam
tavamos = estávamos
to = estou
tô = estou
hr = hora
hrs = horas
totvs = TOTVS
fluig = Fluig
azer = fazer
tao = tão
euf = eu
"""


def _carregar_config() -> None:
    """Lê o arquivo de configuração do usuário e mescla com os dados embutidos."""
    os.makedirs(CONFIG_DIR, exist_ok=True)

    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            f.write(_CONFIG_TEMPLATE)
        log(f"[Corretor] Arquivo de configuração criado em: {CONFIG_FILE}")

    try:
        novas_palavras = []
        novas_abrevs   = {}
        section        = None

        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            for linha in f:
                linha = linha.strip()
                if not linha or linha.startswith("#"):
                    continue
                if linha.startswith("[") and linha.endswith("]"):
                    section = linha[1:-1].strip().lower()
                    continue
                if section == "palavras_permitidas":
                    novas_palavras.append(linha.lower())
                elif section == "abreviacoes" and "=" in linha:
                    chave, _, valor = linha.partition("=")
                    novas_abrevs[chave.strip().lower()] = valor.strip()

        PALAVRAS_PROTEGIDAS.update(novas_palavras)
        ABREVIACOES.update(novas_abrevs)

        if novas_palavras:
            _spell.word_frequency.load_words(novas_palavras)
        if novas_abrevs:
            _spell.word_frequency.load_words(
                palavra for expansao in novas_abrevs.values() for palavra in expansao.split()
            )

        total = len(novas_palavras) + len(novas_abrevs)
        if total:
            log(f"[Corretor] Config: {len(novas_palavras)} palavra(s) e {len(novas_abrevs)} abreviação(ões) do usuário carregada(s).")
    except Exception as exc:
        log(f"[Corretor] Erro ao ler configuração: {exc}")


# ─── Dados para correção local ─────────────────────────────────────────────────────────

ABREVIACOES: dict = {}
PALAVRAS_PROTEGIDAS: set = set()

_TOKEN_RE = re.compile(r"https?://\S+|[\wÀ-ÿ]+|[^\wÀ-ÿ\s]+|\s+", re.UNICODE)

# SpellChecker inicializado uma vez (custo único de ~300 ms).
# Palavras geradas pelas expansões e as protegidas são registradas para que
# o corretor não tente "consertar" o que já está certo.
_spell = SpellChecker(language="pt", distance=1)

_carregar_config()


def _aplicar_maiusculas(original: str, corrigida: str) -> str:
    """Preserva o padrão de capitalização da palavra original."""
    if original.isupper():
        return corrigida.upper()
    if original[:1].isupper():
        return corrigida.capitalize()
    return corrigida


def _deve_ignorar_token(token: str) -> bool:
    """True se o token não deve ser submetido ao SpellChecker."""
    if not token.strip() or token.startswith(("http://", "https://")):
        return True
    if any(c.isdigit() for c in token) or "@" in token or "_" in token:
        return True
    if len(token) <= 2 or (token.isupper() and len(token) <= 5):
        return True
    return False


def _capitalizar_frases(texto: str) -> str:
    """Capitaliza a primeira letra após pontuação final (. ! ?)."""
    return re.sub(
        r"(^|[.!?]\s+)([\"'([{]*)([a-zá-ÿ])",
        lambda m: f"{m.group(1)}{m.group(2)}{m.group(3).upper()}",
        texto,
    )


def _pre_processar(texto: str) -> tuple[str, int]:
    """
    Estágio 1: expande abreviações informais e aplica correções diretas locais.
    Retorna (texto_expandido, quantidade_de_substituições).
    """
    tokens = _TOKEN_RE.findall(texto)
    partes = []
    count = 0
    for token in tokens:
        if re.fullmatch(r"[\wÀ-ÿ]+", token, flags=re.UNICODE):
            chave = token.lower()
            if chave in ABREVIACOES:
                partes.append(_aplicar_maiusculas(token, ABREVIACOES[chave]))
                count += 1
                continue
        partes.append(token)
    return "".join(partes), count


def _afinar_spelling(texto: str) -> tuple[str, int]:
    """
    Estágio 3: SpellChecker como ajuste fino — corrige palavras que a API
    não detectou, respeitando PALAVRAS_PROTEGIDAS.
    Retorna (texto_corrigido, quantidade_de_ajustes).
    """
    tokens = _TOKEN_RE.findall(texto)
    partes = []
    count = 0
    for token in tokens:
        if not re.fullmatch(r"[\wÀ-ÿ]+", token, flags=re.UNICODE):
            partes.append(token)
            continue
        chave = token.lower()
        if chave in PALAVRAS_PROTEGIDAS or _deve_ignorar_token(token):
            partes.append(token)
            continue
        sugestao = _spell.correction(chave)
        if sugestao and sugestao != chave:
            partes.append(_aplicar_maiusculas(token, sugestao))
            count += 1
        else:
            partes.append(token)
    return "".join(partes), count


# ─── API LanguageTool ─────────────────────────────────────────────────────────

_cache_api: dict = {}
_CACHE_MAX = 50


def chamar_api(texto: str):
    """
    Envia o texto para a API do LanguageTool.
    Usa cache em memória para evitar chamadas repetidas ao mesmo texto.
    Retorna (matches: list, erro: str | None).
    """
    chave = hashlib.md5(texto.encode()).hexdigest()
    if chave in _cache_api:
        log("[Corretor] Cache: reutilizando resultado da API.")
        return _cache_api[chave], None

    try:
        resp = requests.post(
            API_URL,
            data={"text": texto, "language": LANGUAGE},
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        matches = resp.json().get("matches", [])
        if len(_cache_api) >= _CACHE_MAX:
            for k in list(_cache_api)[:_CACHE_MAX // 2]:
                del _cache_api[k]
        _cache_api[chave] = matches
        return matches, None

    except requests.exceptions.Timeout:
        return None, f"Timeout: a API não respondeu em {TIMEOUT}s."
    except requests.exceptions.ConnectionError:
        return None, "Sem conexão: verifique sua internet ou a disponibilidade da API."
    except requests.exceptions.HTTPError as exc:
        code = exc.response.status_code
        if code == 429:
            return None, "Limite atingido (20 req/min). Aguarde um momento e tente novamente."
        return None, f"Erro HTTP {code} retornado pela API."
    except Exception as exc:
        return None, f"Erro inesperado: {exc}"


def aplicar_correcoes(texto: str, matches: list):
    """
    Aplica a primeira sugestão de cada match, percorrendo de trás para frente
    para não deslocar os offsets dos erros anteriores.
    Palavras em PALAVRAS_PROTEGIDAS são ignoradas mesmo que a API as sinalize.
    Retorna (texto_corrigido, quantidade_de_correcoes).
    """
    matches_desc = sorted(matches, key=lambda m: m["offset"], reverse=True)
    count = 0
    for match in matches_desc:
        replacements = match.get("replacements", [])
        if not replacements:
            continue
        offset  = match["offset"]
        length  = match["length"]
        # Não modifica palavras da lista de proteção (ex.: Fluig, TOTVS, Python…)
        if texto[offset:offset + length].lower() in PALAVRAS_PROTEGIDAS:
            continue
        novo    = replacements[0]["value"]
        texto   = texto[:offset] + novo + texto[offset + length:]
        count  += 1
    return texto, count

# ─── Hook de teclado ─────────────────────────────────────────────────────────

def _keyboard_hook(event: keyboard.KeyboardEvent) -> bool:
    """
    Hook global de baixo nível.
    Suprime AMBOS os eventos (key-down e key-up) do "'" quando Ctrl estiver
    pressionado, impedindo que o caractere apareça no app ativo.
    Retorna False para suprimir o evento, True para deixar passar.
    """
    global _apostrophe_suppressed

    # Deixa todos os outros eventos passarem sem interferência
    if event.name not in ("'", "apostrophe"):
        return True

    # Ctrl+' pressionado: dispara correção e suprime o key-down do "'"
    if event.event_type == keyboard.KEY_DOWN and keyboard.is_pressed("ctrl"):
        _apostrophe_suppressed = True
        threading.Thread(target=on_hotkey, daemon=True).start()
        return False   # suprime key-down

    # Suprime o key-up correspondente ao atalho já interceptado
    if event.event_type == keyboard.KEY_UP and _apostrophe_suppressed:
        _apostrophe_suppressed = False
        return False   # suprime key-up

    return True   # "'" sem Ctrl: passa normalmente


# ─── Callback do atalho ───────────────────────────────────────────────────────

def on_hotkey() -> None:
    """Executado a cada Ctrl+'. Lançado em thread pelo _keyboard_hook."""
    if not _lock.acquire(blocking=False):
        log("[Corretor] Já está processando uma correção, aguarde...")
        return

    texto_para_colar = None   # None = não colar; str = colar no finally

    try:
        _set_icon(COR_PROCESSANDO)

        # Selecionar todo o texto e copiar para o clipboard
        pyautogui.hotkey("ctrl", "a")
        time.sleep(0.05)
        pyautogui.hotkey("ctrl", "c")
        time.sleep(0.10)

        texto = pyperclip.paste()

        if not texto or not texto.strip():
            log("[Corretor] Nenhum texto encontrado para corrigir.")
            return   # nada selecionado — não há o que colar de volta

        if len(texto) > MAX_CHARS:
            log(
                f"[Corretor] Texto muito longo ({len(texto):,} chars). "
                f"Limite gratuito da API: {MAX_CHARS:,} chars."
            )
            texto_para_colar = texto   # devolve o original intacto
            return

        log(f"[Corretor] Verificando {len(texto):,} caractere(s)...")

        # Estágio 1 — expansão local de abreviações e correções diretas
        texto_proc, n_preproc = _pre_processar(texto)

        # Estágio 2 — LanguageTool (gramática e contexto)
        n_lt = 0
        matches, erro = chamar_api(texto_proc)
        if erro:
            log(f"[Corretor] API indisponível — {erro}")
            log("[Corretor] Continuando com correções locais...")
        elif matches:
            texto_proc, n_lt = aplicar_correcoes(texto_proc, matches)

        # Estágio 3 — SpellChecker (ajuste fino de ortografia)
        texto_proc, n_spell = _afinar_spelling(texto_proc)

        # Estágio 4 — capitalização de frases
        texto_final = _capitalizar_frases(texto_proc)

        total = n_preproc + n_lt + n_spell
        if total == 0 and texto_final == texto:
            log("[Corretor] Nenhuma correção necessária.")
        else:
            partes_log = []
            if n_preproc: partes_log.append(f"abreviações: {n_preproc}")
            if n_lt:      partes_log.append(f"LanguageTool: {n_lt}")
            if n_spell:   partes_log.append(f"SpellChecker: {n_spell}")
            resumo = f" — {', '.join(partes_log)}" if partes_log else ""
            log(f"[Corretor] ✓ {total} correção(ões){resumo}")

        texto_para_colar = texto_final

    finally:
        # Sempre cola de volta (original ou corrigido) quando havia texto selecionado
        if texto_para_colar is not None:
            pyperclip.copy(texto_para_colar)
            time.sleep(0.05)
            pyautogui.hotkey("ctrl", "v")
        _lock.release()
        _set_icon(COR_IDLE)

# ─── Bandeja do sistema ───────────────────────────────────────────────────────

def _abrir_config(icon_ref: pystray.Icon, item) -> None:
    """Abre o arquivo de configuração no editor padrão (ou a pasta, se falhar)."""
    try:
        os.startfile(CONFIG_FILE)
    except Exception:
        try:
            subprocess.Popen(["explorer", "/select," + CONFIG_FILE])
        except Exception:
            subprocess.Popen(["explorer", CONFIG_DIR])


def ao_sair(icon_ref: pystray.Icon, item) -> None:
    """Encerra o programa a partir do menu da bandeja."""
    log("[Corretor] Encerrando...")
    keyboard.unhook_all()
    icon_ref.stop()
    sys.exit(0)


def iniciar_tray() -> None:
    """Cria e inicia o ícone na bandeja do sistema (bloqueia a main thread)."""
    global _icon

    menu = pystray.Menu(
        pystray.MenuItem("Corretor Ortográfico", None, enabled=False),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Abrir configurações", _abrir_config),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Sair", ao_sair),
    )

    _icon = pystray.Icon(
        name  = "corretor_ortografico",
        icon  = criar_icone(COR_IDLE),
        title = "Corretor Ortográfico  |  Ctrl+'",
        menu  = menu,
    )

    _icon.run()   # necessário rodar na main thread no Windows

# ─── Ponto de entrada ─────────────────────────────────────────────────────────

def main() -> None:
    # Hook de baixo nível: intercepta apostrophe a nível global, suprimindo
    # tanto o key-down quanto o key-up quando Ctrl estiver pressionado.
    keyboard.hook(_keyboard_hook, suppress=True)
    log("[Corretor] Iniciado. Pressione Ctrl+' para corrigir o texto.")
    log("[Corretor] Clique com botão direito no ícone da bandeja para sair.")
    iniciar_tray()


if __name__ == "__main__":
    main()
