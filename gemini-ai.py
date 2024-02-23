# -*- coding: utf-8 -*-
import google.generativeai as genai
from colorama import Fore, Style
from datetime import timedelta
import time
import os

genai.configure(api_key="Api")
#AIstudio üzerinden aldığınız API key'ini buraya yapıştırın.


generation_config = {
  "temperature": 0.8,
  "top_p": 1,
  "top_k": 5,
  "max_output_tokens": 2048,
}
#temperature: Bu değer metnin yaratıcılığını kontrol eder. 0 değeri en az yaratıcı, 1 değeri ise en yaratıcı metni üretir.
#top_p: Bu değer modelin en olası kelimeleri seçme eğilimini belirler. 0 değeri en rastgele, 1 değeri ise en olası kelimeleri seçer.
#top_k: Bu değer modelin her adımda dikkate aldığı olası kelimelerin sayısını belirler. Düşük değerler daha özgün ve beklenmedik metinler, yüksek değerler ise daha tutarlı ve akıcı metinler üretme eğilimindedir. 
#max_output_tokens: Bu değer modelin üretebileceği maksimum kelime sayısını belirler.

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
#Güvenlik ayarları  

     
convo = model.start_chat(history=[
])
messages = []
print("Gemini: " + Fore.YELLOW + "Merhaba ben Gemini. Sana Nasıl yardımcı olabilirim kullanıcı?" + Fore.RESET)
#AI kullanıcıyı selamlar.

def oyun_ac(oyun_adi):
  oyunlar = {
    "Valorant": os.path.join("C:", "ProgramData", "Microsoft",  "Windows", "Start Menu", "Programs", "Riot Games", "Valorant.lnk"),
    #Bunu yol örneğini burada örnek olarak bıraktım. unicode escape hatası almamak için dosya yollarınızı bu şekilde yazın.
}
  if oyun_adi in oyunlar:
        os.startfile(oyunlar[oyun_adi])
        print(f"Gemini: {Fore.YELLOW}{oyun_adi} oyunu açılıyor...{Fore.RESET}")
        return
  else:
        print(f"Gemini: {Fore.RED}{oyun_adi} oyunu bulunamadı.{Fore.RESET}")
        return
while True:
    message = input("\nYou: ")
    messages.append({
        "role": "user",
        "parts": [message],
    })
#Kullanıcıdan girdi alır ve 'message' olarak tanımlar
    if message == "Oyun aç":
          oyun_adi = input("Gemini: " + Fore.YELLOW + "Hangi oyunu açmamı istersiniz?\n" + Fore.RESET + "You: ")
          oyun_ac(oyun_adi)
#Eğer girdi 'Oyun aç' ise oyun_ac fonksiyonu dönmeye başlar.
    elif message == "q":
      print("Gemini: " + Fore.YELLOW + "Program Kapanıyor...")
      duration = timedelta(seconds=3)
      time.sleep(duration.seconds)
      break
#Eğer girdi 'q' ise Program uyarı verip 3 saniye sonrasında kendini kapatır.
    response = model.generate_content(messages)

    messages.append({
        "role": "model",
        "parts": [response.text],
    })
    print("\nGemini: " + Fore.YELLOW + response.text + Fore.RESET)
#Girdi bunlardan hiç biri değilse Gemini AI bir cevap üretir ve ekrana yazdırır.