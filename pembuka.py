import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Tambahkan ini untuk memuat gambar
import subprocess  # Untuk menjalankan file lain (login.py)

# Fungsi untuk membuka file login.py
def open_login():
    try:
        root.destroy()
        subprocess.run(["python", "login.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

# Fungsi untuk membuka file register.py
def open_register():
    try:
        root.destroy()
        subprocess.run(["python", "register.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

# Membuat jendela utama
root = tk.Tk()
root.title("Aplikasi Pembuka")
root.geometry("800x600")
root.configure(bg='#87CEFA')

# Membuat frame untuk logo
logo_frame = tk.Frame(root, bg='#87CEFA')
logo_frame.pack(expand=True)

# Memuat dan menampilkan logo.jpg
try:
    img = Image.open("logo.jpg")
    img = img.resize((500, 350), Image.Resampling.LANCZOS)  # Resize jika perlu
    logo = ImageTk.PhotoImage(img)
    logo_label = tk.Label(logo_frame, image=logo, bg='#87CEFA')
    logo_label.image = logo  # Simpan referensi agar tidak terhapus oleh garbage collector
    logo_label.pack()
except Exception as e:
    logo_label = tk.Label(logo_frame, text="Logo tidak ditemukan", font=("Arial", 16), bg='#87CEFA', fg='red')
    logo_label.pack()

# Frame tombol kanan atas
button_frame = tk.Frame(root, bg='#87CEFA')
button_frame.pack(side=tk.TOP, anchor='ne', padx=10, pady=10)

# Tombol Login dan Register
btn_login = tk.Button(button_frame, text="Login", command=open_login, font=("Arial", 12), bg='#4CAF50', fg='white')
btn_login.pack(side=tk.LEFT, padx=5)

btn_register = tk.Button(button_frame, text="Register", command=open_register, font=("Arial", 12), bg='#2196F3', fg='white')
btn_register.pack(side=tk.LEFT, padx=5)

# Menjalankan aplikasi
root.mainloop()
