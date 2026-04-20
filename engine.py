import pyautogui as pag
from pynput import keyboard as pk
import easyocr as eocr
import numpy as np
import time as t
import pyperclip as ppc
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from art import logo
import ctypes as ct
import tkinter as tk
from plyer import notification as pl
import threading as th

load_dotenv()
clien = OpenAI(api_key=os.getenv("API_KEY"), base_url="https://api.groq.com/openai/v1")
cord = []
reader = eocr.Reader(['hu'], gpu=False)

#functions
def hide_console():
    kernel = ct.windll.kernel32
    user = ct.windll.user32
    hwnd = kernel.GetConsoleWindow()
    if hwnd != 0:
        user.ShowWindow(hwnd, 0)
        #donkos223

def prompting(prompt_text):
    try:
        response = clien.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt_text}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Hiba az API hívás során: {e}"

def note_send(message):
    def show_note(message=message):
        pl.notify(
            title="Megoldás",
            message=message,
            timeout=10,
            app_name="AI Helper")
    th.Thread(target=show_note, daemon=True).start()

def on_press(key):
    global cord
    with open("settings.json", "r") as f:
        data = json.load(f)
    try:
        if key == pk.Key.esc:
            print("Kilépés...")
            return False
        key_char = getattr(key, 'char', None)
        if key_char and key_char.lower() == 'q':
            pos = pag.position()
            cord.append(pos)
            print(f"Pont rögzítve: {pos}")

            if len(cord) == 2:
                print("Terület kijelölve, feldolgozás...")
                
                # Koordináták kiszámítása (hogy ne legyen negatív)
                x1, y1 = cord[0]
                x2, y2 = cord[1]
                left, top = min(x1, x2), min(y1, y2)
                width, height = abs(x2 - x1), abs(y2 - y1)
                
                # Screenshot és OCR
                image = pag.screenshot(region=(left, top, width, height))
                image_np = np.array(image)
                text_list = reader.readtext(image_np, detail=0)
                full_text = " ".join(text_list)
                
                if full_text:
                    result = prompting(f"oldd meg ezt a feladatot magyarul, roviden: {full_text}")

                    if data["note"]:
                        note_send(result[:256])
                    
                    ppc.copy(result)
                    print("Eredmény a vágólapra másolva!")
                    
                    # Várunk egy kicsit, hogy ne ütközzön a billentyűzet figyelővel
                    t.sleep(0.5)
                    if data["auto_paste"]:
                        pag.hotkey('ctrl', 'v')
                    print("Eredmény beillesztve!")
                else:
                    print("Nem találtam szöveget a képen.")
                
                # Koordináták törlése, hogy újra lehessen használni a programot
                cord.clear()

    except Exception as e:
        print(f"Hiba történt: {e}")
        cord = []





def start_engine():
    with pk.Listener(on_press=on_press) as listener:
        listener.join()