import tkinter as tk
from tkinter import messagebox
import subprocess
import sqlite3

def connect_db():
    return sqlite3.connect("users.db")

# Validate the login credentials
def validate_login():
    email = entry_login_email.get()
    password = entry_login_password.get()

    # Cek admin hardcode
    if email == "fadhil@gmail.com" and password == "admin123":
        messagebox.showinfo("Login Success", "Login sebagai Admin berhasil!")
        login_window.destroy()
        subprocess.Popen(["python", "utama.py", "admin"])
        return

    # Cek ke database users (selain admin)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        messagebox.showinfo("Login Success", f"Login sebagai User ({user[1]}) berhasil!")
        login_window.destroy()
        subprocess.Popen(["python", "utama.py", "user"])
    else:
        messagebox.showerror("Login Failed", "Email atau Password salah!")
        
def back_to_pembuka():
    login_window.destroy()
    subprocess.Popen(['python', 'pembuka.py'])

# Login window for users
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("800x600")
login_window.configure(bg='#87CEFA')

login_frame = tk.Frame(login_window, bg='#87CEFA')
login_frame.pack(pady=40)

label_login_email = tk.Label(login_frame, text="Email", font=("Arial", 12), bg='#87CEFA')
label_login_email.grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_login_email = tk.Entry(login_frame, font=("Arial", 14), width=30)
entry_login_email.grid(row=0, column=1, padx=10, pady=10)

label_login_password = tk.Label(login_frame, text="Password", font=("Arial", 12), bg='#87CEFA')
label_login_password.grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_login_password = tk.Entry(login_frame, font=("Arial", 14), show="*", width=30)
entry_login_password.grid(row=1, column=1, padx=10, pady=10)

btn_login = tk.Button(login_window, text="Login", command=validate_login, font=("Arial", 14), width=15, bg='#4CAF50', fg='white')
btn_login.pack(pady=20)

btn_back = tk.Button(login_window, text="Back", command=back_to_pembuka, font=("Arial", 14), width=15, bg='red', fg='white')
btn_back.pack(pady=5)

login_window.mainloop()
