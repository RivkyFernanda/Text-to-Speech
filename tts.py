# Import modul pyttsx3 untuk text-to-speech
import pyttsx3

# Inisialisasi engine pyttsx3 dengan driver SAPI5 (khusus Windows)
engine = pyttsx3.init('sapi5')

# Atur kecepatan bicara (rate), default sekitar 200 kata per menit
engine.setProperty("rate", 125)

# Atur volume suara, dari 0.0 (paling kecil) sampai 1.0 (paling besar)
engine.setProperty("volume", 1.0)

# Ambil daftar suara (biasanya 0 untuk laki-laki, 1 untuk perempuan tergantung sistem)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)  # Gunakan suara perempuan

# Teks yang akan diucapkan (dibacakan)
engine.say("ini hasil sebelum di oprek")
engine.say("This is a test using text to speech in Visual Studio Code.")

# Simpan hasil suara ke dalam file WAV
engine.save_to_file("This is the saved audio output.", "test.wav")

# Jalankan engine untuk memproses dan mengeluarkan suara
engine.runAndWait()

# Hentikan engine setelah selesai
engine.stop()
