import threading
from pynput import keyboard
import pyautogui
import time

clicking = False
running = True

def clicker():
    global clicking
    while running:
        if clicking:
            pyautogui.click()
            time.sleep(0.001)  # 200 clicks per second

def toggle_clicking(key):
    global clicking
    if key == keyboard.Key.space:
        clicking = not clicking
    elif key == keyboard.Key.esc:
        return False

    with keyboard.Listener(on_press=toggle_clicking) as listener:
        listener.join()
    threading.Thread(target=clicker, daemon=True).start()
    with keyboard.Listener(on_press=toggle_clicking) as listener:
        listener.join()
    running = False

def main():
    global running
    threading.Thread(target=clicker, daemon=True).start()
    with keyboard.Listener(on_press=toggle_clicking) as listener:
        listener.join()
    running = False

if __name__ == "__main__":
    main()