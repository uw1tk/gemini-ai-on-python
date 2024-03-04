# -*- coding: utf-8 -*-
import google.generativeai as genai
from colorama import Fore, Style
from datetime import timedelta
import time
import os

genai.configure(api_key="AIzaSyAZqTIzoPeopV1iunJQqCXI3tEB9Kdl1IA")

generation_config = {
  "temperature": 0.8,
  "top_p": 1,
  "top_k": 5,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

oyunlar = {
    "Valorant": os.path.join("C:", "ProgramData", "Microsoft",  "Windows", "Start Menu", "Programs", "Riot Games", "Valorant.lnk"),
    "LOL": os.path.join("C:", "ProgramData", "Microsoft",  "Windows", "Start Menu", "Programs", "Riot Games", "League of Legends.lnk"),
    "Apex": os.path.join("C:", "Program Files", "EA Games", "Apex", "r5apex.exe"),
    "CS": os.path.join("C:", "Users", "Lenova", "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Steam", "Counter-Strike 2.url"),
    "kek": "com.epicgames.launcher://apps/879b0d8776ab46a59a129983ba78f0ce%3A7d690c122fde4c60bed85405f343ad10%3A4,1869934302e4b8cafac2d3c0e7c293d?action=launch&silent=true",
    "TMP": os.path.join("C:", "Users", "Lenova", "AppData", "Local", "TruckersMP", "TruckersMP-Launcher.exe"),
    "ETS2": os.path.join("C:", "Users", "Lenova", "Desktop", "Games", "Euro Truck Simulator 2.url"),
    "WT": os.path.join("C:", "Users", "Lenova", "Desktop", "Games", "War Thunder.url"),
}
                 
convo = model.start_chat(history=[
])
messages = []
print("Alicia: " + Fore.YELLOW + "Merhaba ben Alicia. Sana Nasıl yardımcı olabilirim Ümit?" + Fore.RESET)

def oyun_ac(oyun_adi):
  if oyun_adi in oyunlar:
      try:
        os.startfile(oyunlar[oyun_adi])
        print(f"Alicia: {Fore.YELLOW}{oyun_adi} oyunu açılıyor...{Fore.RESET}")
        return
      except FileNotFoundError:
        print(f"Alicia: {Fore.RED}{oyun_adi} oyunu bulunamadı. Lütfen oyunun dosya yolunu kontrol edin.{Fore.RESET}")
        return
  else:
        print(f"Alicia: {Fore.RED}{oyun_adi} oyunu bulunamadı. Oyunlar listesinde mevcut oyunlardan birini seçin.{Fore.RESET}")
        return
while True:
    message = input("\nYou: ")
    messages.append({
        "role": "user",
        "parts": [message],
    })
    if message == "Oyun aç":
          oyun_adi = input("Alicia: " + Fore.YELLOW + "Hangi oyunu açmamı istersiniz?\n" + Fore.RESET + "You: ")
          oyun_ac(oyun_adi)
          response = None

    elif message == "q":
      print("Alicia: " + Fore.YELLOW + "Program Kapanıyor...")
      duration = timedelta(seconds=3)
      time.sleep(duration.seconds)
      break
      
    else:
      response = model.generate_content(messages)

      messages.append({
              "role": "model",
              "parts": [response.text],
          })

      print("\nAlicia: " + Fore.YELLOW + response.text + Fore.RESET)
