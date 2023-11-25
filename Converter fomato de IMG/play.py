import os

# Caminho para o seu script principal
main_script = "main.py"

# Comando para abrir um novo terminal e executar o script principal
command = f"python {main_script}"

# No Windows, você pode usar algo como:
os.system(f"start cmd /k {command}")

# Para macOS, pode ser algo como:
# os.system(f"osascript -e 'tell app \"Terminal\" to do script \"{command}\"'")

# Para Linux, dependendo do terminal, pode ser algo como:
# os.system(f"gnome-terminal -- {command}")
