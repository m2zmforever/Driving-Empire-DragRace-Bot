import cv2
import numpy as np
import pyautogui
import keyboard
import time
import pydirectinput
import win32api
import win32con
import subprocess
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from rich.align import Align
from datetime import datetime

console = Console()

# Ekranda bir görseli arayan fonksiyon
def find_image_on_screen(template_path, threshold=0.8):
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    template = cv2.imread(template_path)
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return max_val >= threshold

def print_menu(status, race_count, last_action, first_place_count, second_place_count):
    table = Table(title="Driving Empire AI Bot", show_header=True, header_style="bold magenta")
    table.add_column("Status", style="cyan", width=12)
    table.add_column("Race Count", style="green", width=12)
    table.add_column("1.lik", style="bold yellow", width=8)
    table.add_column("2.lik", style="bold blue", width=8)
    table.add_column("Last Action", style="yellow", width=30)
    table.add_row(status, str(race_count), str(first_place_count), str(second_place_count), last_action)
    console.clear()
    console.print(Panel(table, title="[bold blue]Bot Status", border_style="bright_blue"))

log_lines = []
def log_event(event):
    now = datetime.now().strftime('%H:%M:%S')
    log_line = f"[{now}] {event}"
    log_lines.append(log_line)
    if len(log_lines) > 20:
        log_lines.pop(0)
    for idx, line in enumerate(log_lines):
        console.print(line, style="bold white" if idx == len(log_lines)-1 else "white")

if __name__ == "__main__":
    print("AI başlatıldı. race_start.png bekleniyor...")
    race_count = 0
    first_place_count = 0
    second_place_count = 0
    last_action = "Bot başlatıldı"
    log_event("Bot başlatıldı")
    while True:
        w_pressed = False
        shift_pressed = False
        status = "Bekliyor"
        print_menu(status, race_count, last_action, first_place_count, second_place_count)
        log_event("Yarış bekleniyor...")
        # Yarış başlatma döngüsü
        while True:
            if not w_pressed and find_image_on_screen("race_start.png"):
                status = "Yarış Başladı"
                last_action = f"{datetime.now().strftime('%H:%M:%S')} - W basıldı"
                print_menu(status, race_count, last_action, first_place_count, second_place_count)
                log_event("race_start.png bulundu! W tuşuna basıldı.")
                keyboard.press('w')
                w_pressed = True
                time.sleep(6)
                last_action = f"{datetime.now().strftime('%H:%M:%S')} - Shift basıldı"
                print_menu(status, race_count, last_action, first_place_count, second_place_count)
                log_event("Shift tuşuna basıldı.")
                keyboard.press('shift')
                shift_pressed = True
            if find_image_on_screen("play_again.png"):
                status = "Yarış Bitti"
                last_action = f"{datetime.now().strftime('%H:%M:%S')} - play_again tıklandı"
                print_menu(status, race_count, last_action, first_place_count, second_place_count)
                log_event("play_again.png bulundu! Tuşlar bırakıldı ve tıklama denendi.")
                if w_pressed:
                    keyboard.release('w')
                    w_pressed = False
                    log_event("W tuşu bırakıldı.")
                if shift_pressed:
                    keyboard.release('shift')
                    shift_pressed = False
                    log_event("Shift tuşu bırakıldı.")
                # Birinci ve ikinci olma kontrolünü daha güvenli yap
                first_found = find_image_on_screen("first_place.png")
                second_found = False
                if not first_found:
                    second_found = find_image_on_screen("second_place.png")
                if first_found:
                    first_place_count += 1
                    log_event(f"Birinci olundu! Toplam: {first_place_count}")
                elif second_found:
                    second_place_count += 1
                    log_event(f"İkinci olundu! Toplam: {second_place_count}")
                screenshot = pyautogui.screenshot()
                screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                template = cv2.imread("play_again.png")
                result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                if max_val >= 0.8:
                    h, w = template.shape[:2]
                    center_x = max_loc[0] + w // 2
                    center_y = max_loc[1] + h // 2
                    # Sadece pyautogui ile tıklama, mouse'u tam ortada ve kısa bekleme
                    pyautogui.moveTo(center_x, center_y, duration=0.3)
                    time.sleep(0.3)
                    pyautogui.click(center_x, center_y)
                    time.sleep(0.2)
                    pydirectinput.click(center_x, center_y)
                    time.sleep(0.2)
                    win32api.SetCursorPos((center_x, center_y))
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, center_x, center_y, 0, 0)
                    time.sleep(0.05)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, center_x, center_y, 0, 0)
                    time.sleep(0.2)
                    subprocess.run([
                        r'C:\Program Files\AutoHotkey\v2\AutoHotkey64.exe',
                        r'c:\Users\Administrator\Desktop\Driving Empire DragRace AI\play_click.ahk',
                        str(center_x), str(center_y)
                    ])
                    log_event("play_again butonuna tüm yöntemlerle tıklama denendi!")
                # Birinci ve ikinci olma kontrolünü tekrar yap
                first_found = find_image_on_screen("first_place.png")
                second_found = False
                if not first_found:
                    second_found = find_image_on_screen("second_place.png")
                if first_found:
                    first_place_count += 1
                    log_event(f"Birinci olundu! Toplam: {first_place_count}")
                elif second_found:
                    second_place_count += 1
                    log_event(f"İkinci olundu! Toplam: {second_place_count}")
                break
            time.sleep(1)
        race_count += 1
        status = f"Yeni Yarış Bekleniyor"
        last_action = f"{datetime.now().strftime('%H:%M:%S')} - Döngü tamamlandı"
        print_menu(status, race_count, last_action, first_place_count, second_place_count)
        log_event("Yeni yarış için bekleniyor...")
        time.sleep(2)
