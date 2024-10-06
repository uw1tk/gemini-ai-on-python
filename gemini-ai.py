import os
import tkinter as tk
from tkinter import PhotoImage, messagebox, scrolledtext, simpledialog
from tkinter import simpledialog
import google.generativeai as genai
import customtkinter as ctk


# API key'i ayarlama
genai.configure(api_key="API_KEYINIZ")

# Yapay zekanızın output ayarları
generation_config = {
  "temperature": 0.8,
  "top_p": 1,
  "top_k": 5,
  "max_output_tokens": 2048,
}

# Güvenlik seçenekleri
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

model = genai.GenerativeModel(model_name="gemini-1.5-pro-002",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Oyunların yolları
oyunlar = {
    # Örnek
    "Oyun1": os.path.join("C:", "ProgramData", "Microsoft",  "Windows", "Start Menu", "Programs", "abc games", "Oyun1.exe"),

}
# Oyun açma fonksiyonu
def oyun_ac(oyun_adi):
    if oyun_adi in oyunlar:
        try:
            os.startfile(oyunlar[oyun_adi])
            append_text(f"Alicia: {oyun_adi} oyunu açılıyor...")
            display_default_icon()
            return
        except FileNotFoundError:
            append_text(f"Alicia: {oyun_adi} oyunu bulunamadı. Lütfen oyunun dosya yolunu kontrol edin.\n")
            return
    else:
        append_text(f"\nAlicia: {oyun_adi} oyunu bulunamadı. Oyunlar listesinde mevcut oyunlardan birini seçin.\n")
        return


def oyun_ac_callback(event):
    oyun_adi = input_entry.get()
    input_entry.delete(0, tk.END)
    append_text(f"You: {oyun_adi}")
    oyun_ac(oyun_adi)
    input_entry.unbind("<Return>")


def append_text(text):
    output_text.configure(state=tk.NORMAL)
    output_text.insert(tk.END, text + "\n")
    output_text.configure(state=tk.DISABLED)
    output_text.see(tk.END)

def handle_command():
    message = input_entry.get()
    input_entry.delete(0, tk.END)
    append_text(f"You: {message}")
    
    if message == "Oyun aç":
        oyun_adi = custom_askstring("Oyun Seçimi", "Hangi oyunu açmamı istersin?\n")
        if oyun_adi:
            oyun_ac(oyun_adi)
    elif message == "q":
        append_text("\nAlicia: Program Kapanıyor...\n")
        root.after(3000, root.quit)
    else:
        response = model.generate_content(message)
        response_text = response.text  # Yanıt metnini al

        root.after(0, append_text, "\nAlicia: " + response_text + "\n")



# Arayüz  oluşturma
root = ctk.CTk()
root.title(" ") #AI'nıza vereceğiniz isim


root.geometry("950x650") # Pencere boyutunu ayarlayın
# İkon dosyasının yolunu ve formatını kontrol edin
icon_path = " "  #  .ico dosyasının yolunu belirtin
if os.path.exists(icon_path):
    root.iconbitmap(default=icon_path)
else:
    print(f"Icon file not found at {icon_path}")
ctk.set_default_color_theme("dark-blue") 
ctk.set_appearance_mode("dark")



# Oyun açmak için açılan soru kutucuğu
def custom_askstring(title, prompt):
    dialog = ctk.CTkToplevel(root)
    dialog.title(title)
    dialog.geometry("300x150")
    root.iconbitmap(default=" ") # .ico dosyasının yolunu belirtin
    label = ctk.CTkLabel(dialog, text=prompt, font=("Helvetica", 14))
    label.pack(pady=10)

    entry = ctk.CTkEntry(dialog, width=250)
    entry.pack(pady=5)

    result = []

    def on_submit():
        result.append(entry.get())
        dialog.destroy()

    button = ctk.CTkButton(dialog, text="Tamam", command=on_submit)
    button.pack(pady=10)

    dialog.grab_set()
    root.wait_window(dialog)

    return result[0] if result else None
#Çıktı ekranı
output_text = ctk.CTkTextbox(root, state=tk.DISABLED, width=60, height=20, font=("Helvetica", 16), text_color="white")
output_text.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

# Giriş satırı
input_entry = ctk.CTkEntry(root, placeholder_text="Mesajınızı buraya yazın.", width=400, font=("Helvetica", 16))
input_entry.pack(pady=5)

# Gönder düğmesi
button = ctk.CTkButton(root, text="Gönder", command=handle_command, text_color="white", font=("Helvetica", 12))
button.pack(pady=20)
# Enter tuşuna basıldığında Gönder butonu tetiklenir
input_entry.bind("<Return>", lambda event: handle_command())

root.mainloop()
