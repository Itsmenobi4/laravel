import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import sys
from PIL import Image, ImageTk
import os

def connect_db():
    return sqlite3.connect("produk.db")

def get_product_details(product_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT nama_produk, harga_produk, foto_produk FROM produk WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    conn.close()
    return product

def create_transaction_window(product_id):
    product = get_product_details(product_id)
    if not product:
        messagebox.showerror("Error", "Produk tidak ditemukan!")
        return

    nama_produk, harga_produk, foto_produk = product
    
    # Format harga
    try:
        harga_num = float(harga_produk)
        harga_tampil = f"Rp {harga_num:,.0f}"
    except ValueError:
        harga_tampil = f"Rp {harga_produk}"

    # Buat window transaksi (jadikan root window, bukan Toplevel)
    transaksi_window = tk.Tk()
    transaksi_window.title(f"Transaksi - {nama_produk}")
    transaksi_window.geometry("500x600")
    transaksi_window.configure(bg='#e3f2fd')
    transaksi_window.resizable(False, False)

    # Header
    tk.Label(transaksi_window, text="Detail Pembelian", font=("Arial", 16, "bold"), 
             bg='#e3f2fd', fg='#1976d2').pack(pady=20)

    # Frame untuk produk
    product_frame = tk.Frame(transaksi_window, bg='#e3f2fd')
    product_frame.pack(pady=10)

    # Tampilkan gambar produk jika ada
    if foto_produk and os.path.exists(foto_produk):
        try:
            img = Image.open(foto_produk)
            img = img.resize((200, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(product_frame, image=photo, bg='#e3f2fd')
            img_label.image = photo
            img_label.pack()
        except:
            tk.Label(product_frame, text="[Gambar Tidak Tersedia]", bg='#e3f2fd').pack()
    else:
        tk.Label(product_frame, text="[Gambar Tidak Tersedia]", bg='#e3f2fd').pack()

    # Detail produk
    detail_frame = tk.Frame(transaksi_window, bg='#e3f2fd')
    detail_frame.pack(pady=10)

    tk.Label(detail_frame, text="Nama Produk:", font=("Arial", 12), bg='#e3f2fd').grid(row=0, column=0, sticky="w", padx=5, pady=5)
    tk.Label(detail_frame, text=nama_produk, font=("Arial", 12, "bold"), bg='#e3f2fd').grid(row=0, column=1, sticky="w", padx=5, pady=5)

    tk.Label(detail_frame, text="Harga:", font=("Arial", 12), bg='#e3f2fd').grid(row=1, column=0, sticky="w", padx=5, pady=5)
    tk.Label(detail_frame, text=harga_tampil, font=("Arial", 12, "bold"), bg='#e3f2fd').grid(row=1, column=1, sticky="w", padx=5, pady=5)

    # Form pembeli
    form_frame = tk.Frame(transaksi_window, bg='#e3f2fd')
    form_frame.pack(pady=20)

    tk.Label(form_frame, text="Data Pembeli", font=("Arial", 14, "bold"), bg='#e3f2fd').grid(row=0, columnspan=2, pady=10)

    fields = [
        ("Nama Pembeli", "entry_nama"),
        ("Email", "entry_email"),
        ("Alamat Pengiriman", "entry_alamat"),
        ("Jumlah Beli", "entry_jumlah")
    ]

    entries = {}
    for i, (label, key) in enumerate(fields):
        tk.Label(form_frame, text=label, font=("Arial", 11), bg='#e3f2fd').grid(row=i+1, column=0, sticky="w", padx=10, pady=5)
        entry = tk.Entry(form_frame, font=("Arial", 11), width=30)
        entry.grid(row=i+1, column=1, padx=10, pady=5)
        entries[key] = entry

    # Tombol proses transaksi
    def process_transaction():
        jumlah = entries['entry_jumlah'].get()
        try:
            jumlah = int(jumlah)
            if jumlah <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Jumlah beli harus angka positif!")
            return

        if not all(entries[key].get() for key in entries):
            messagebox.showerror("Error", "Semua field harus diisi!")
            return

        total = harga_num * jumlah

        # Tampilkan konfirmasi
        messagebox.showinfo("Sukses", 
            f"Pembelian berhasil!\n\n"
            f"Total: Rp {total:,.0f}\n"
            f"Produk akan dikirim ke alamat:\n{entries['entry_alamat'].get()}")
        
        transaksi_window.destroy()

    btn_frame = tk.Frame(transaksi_window, bg='#e3f2fd')
    btn_frame.pack(pady=20)

    tk.Button(btn_frame, text="Proses Pembelian", command=process_transaction, 
              font=("Arial", 12, "bold"), bg='#43a047', fg='white').pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Batal", command=transaksi_window.destroy, 
              font=("Arial", 12), bg='#e53935', fg='white').pack(side=tk.LEFT, padx=10)

    transaksi_window.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        product_id = sys.argv[1]
        create_transaction_window(product_id)
    else:
        # Buat root window agar messagebox bisa tampil
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", "ID produk tidak ditemukan!")
        root.destroy()