# Import semua modul yang diperlukan
import pyttsx3  # TTS offline
from gtts import gTTS  # TTS online (Google)
from pydub import AudioSegment  # Untuk konversi WAV ke MP3
import tkinter as tk  # GUI
from tkinter import filedialog, messagebox  # Dialog dan pesan
from tkinter.ttk import Combobox  # Combo box untuk pilihan suara
import os  # Operasi file
import tempfile  # Untuk menyimpan file sementara
import playsound  # Untuk memutar file suara

# Inisialisasi engine TTS dan speech recognizer
engine = pyttsx3.init()  # pyttsx3 untuk TTS offline

# Fungsi untuk memutar suara dari file path
def play_audio(path):
    try:
        playsound.playsound(path)  # Memutar file audio
    except Exception as e:
        messagebox.showerror("Error", f"Gagal memutar audio: {str(e)}")

# Fungsi untuk mengatur suara laki-laki atau perempuan (pyttsx3)
def set_voice(gender):
    voices = engine.getProperty('voices')
    if gender == 'Laki-laki':
        engine.setProperty('voice', voices[0].id)
    else:
        engine.setProperty('voice', voices[1].id)

# Fungsi TTS menggunakan pyttsx3 (offline)
def tts_pyttsx3():
    text = text_input.get("1.0", tk.END).strip()  # Ambil teks dari GUI
    if not text:
        messagebox.showwarning("Peringatan", "Teks kosong!")
        return

    engine.setProperty('rate', int(rate_var.get()))  # Set kecepatan bicara
    engine.setProperty('volume', float(volume_var.get()))  # Set volume
    set_voice(voice_var.get())  # Set suara berdasarkan pilihan

    temp_path = tempfile.mktemp(suffix=".wav")  # File sementara untuk audio
    engine.save_to_file(text, temp_path)
    engine.runAndWait()
    play_audio(temp_path)  # Putar audio
    os.remove(temp_path)  # Hapus file ementara

# Fungsi TTS menggunakan gTTS (online)
def tts_gtts():
    text = text_input.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Peringatan", "Teks kosong!")
        return

    try:
        tts = gTTS(text=text, lang='id')  # Gunakan Bahasa Indonesia
        temp_path = tempfile.mktemp(suffix=".mp3")
        tts.save(temp_path)
        play_audio(temp_path)  # Putar audio
        os.remove(temp_path)  # Hapus file
    except Exception as e:
        messagebox.showerror("Error", f"Gagal memproses gTTS: {str(e)}")

# Fungsi untuk menyimpan hasil audio ke file MP3
def save_audio(method):
    text = text_input.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Peringatan", "Teks kosong!")
        return

    output_file = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
    if not output_file:
        return

    try:
        if method == 'pyttsx3':
            engine.setProperty('rate', int(rate_var.get()))
            engine.setProperty('volume', float(volume_var.get()))
            set_voice(voice_var.get())

            temp_path = tempfile.mktemp(suffix=".wav")
            engine.save_to_file(text, temp_path)
            engine.runAndWait()
            sound = AudioSegment.from_wav(temp_path)
            sound.export(output_file, format="mp3")  # Simpan sebagai MP3
            os.remove(temp_path)

        elif method == 'gTTS':
            tts = gTTS(text=text, lang='id')
            tts.save(output_file)  # Simpan file langsung dari gTTS

        messagebox.showinfo("Sukses", f"Audio berhasil disimpan di: {output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menyimpan audio: {str(e)}")

# Setup GUI
root = tk.Tk()
root.title("TTS: pyttsx3 & gTTS")
root.geometry("600x500")

# Area input teks
tk.Label(root, text="Masukkan Teks:").pack()
text_input = tk.Text(root, height=10)
text_input.pack(fill="both", padx=10, pady=5)

# Dropdown pilihan suara
tk.Label(root, text="Pilih Suara (khusus pyttsx3):").pack()
voice_var = tk.StringVar(value="Perempuan")
voice_dropdown = Combobox(root, textvariable=voice_var, values=["Laki-laki", "Perempuan"])
voice_dropdown.pack(pady=5)

# Input kecepatan bicara dan volume
tk.Label(root, text="Kecepatan Bicara (contoh: 125):").pack()
rate_var = tk.StringVar(value="125")
tk.Entry(root, textvariable=rate_var).pack(pady=5)

tk.Label(root, text="Volume (0.0 - 1.0):").pack()
volume_var = tk.StringVar(value="1.0")
tk.Entry(root, textvariable=volume_var).pack(pady=5)

# Tombol untuk berbagai aksi
tk.Label(root, text="Metode TTS:").pack(pady=5)
tk.Button(root, text="🔊 Putar Suara (pyttsx3)", command=tts_pyttsx3).pack(pady=3)
tk.Button(root, text="🔊 Putar Suara (gTTS)", command=tts_gtts).pack(pady=3)
tk.Button(root, text="💾 Simpan MP3 (pyttsx3)", command=lambda: save_audio('pyttsx3')).pack(pady=3)
tk.Button(root, text="💾 Simpan MP3 (gTTS)", command=lambda: save_audio('gTTS')).pack(pady=3)

# Jalankan GUI
tk.mainloop()
