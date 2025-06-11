import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import sqlite3
import os
from PIL import Image, ImageTk
import sys
import subprocess  # Tambahan untuk memanggil file transaksi.py

def connect_db():
    return sqlite3.connect("produk.db")

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produk (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_produk TEXT,
            harga_produk REAL,
            foto_produk TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_data():
    nama = entry_nama.get()
    try:
        harga = float(entry_harga.get())
    except ValueError:
        messagebox.showwarning("Input Error", "Harga harus angka!")
        return
    foto = entry_foto.get()
    if not os.path.exists(foto):
        messagebox.showwarning("Input Error", "File gambar tidak ditemukan!")
        return

    if nama and foto:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO produk (nama_produk, harga_produk, foto_produk) VALUES (?, ?, ?)",
                       (nama, harga, foto))
        conn.commit()
        conn.close()
        load_data()
        clear_inputs()
        messagebox.showinfo("Success", "Data berhasil ditambahkan!")
    else:
        messagebox.showwarning("Input Error", "Semua field harus diisi!")

def update_data():
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Pilih data yang ingin diubah.")
        return
    item_id = treeview.item(selected_item[0], 'values')[0]
    new_nama = entry_nama.get()
    try:
        new_harga = float(entry_harga.get())
    except ValueError:
        messagebox.showwarning("Input Error", "Harga harus angka.")
        return
    new_foto = entry_foto.get()

    if new_nama and new_foto:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE produk 
            SET nama_produk = ?, harga_produk = ?, foto_produk = ?
            WHERE id = ?
        """, (new_nama, new_harga, new_foto, item_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Data berhasil diubah!")
        load_data()
        clear_inputs()
        toggle_buttons("reset")
    else:
        messagebox.showwarning("Input Error", "Semua field harus diisi!")

def delete_data():
    selected_item = treeview.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Pilih data yang ingin dihapus.")
        return
    item_id = treeview.item(selected_item[0], 'values')[0]
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produk WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Data berhasil dihapus!")
    load_data()
    clear_inputs()
    toggle_buttons("reset")

def search_data():
    global photo_refs
    query = entry_search.get()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produk WHERE nama_produk LIKE ?", ('%' + query + '%',))
    rows = cursor.fetchall()
    conn.close()

    for row in treeview.get_children():
        treeview.delete(row)
    photo_refs = {}
    for idx, row in enumerate(rows):
        foto_path = row[3]
        tag = 'even' if idx % 2 == 0 else 'odd'
        if foto_path and os.path.exists(foto_path):
            try:
                img = Image.open(foto_path)
                img = img.resize((120, 120), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                photo_refs[idx] = photo
                treeview.insert('', 'end', text='', image=photo, values=(row[0], row[1], row[2], row[3]), tags=(tag,))
            except:
                treeview.insert('', 'end', text='[Gambar Error]', values=(row[0], row[1], row[2], row[3]), tags=(tag,))
        else:
            treeview.insert('', 'end', text='[Tidak Ada Gambar]', values=(row[0], row[1], row[2], row[3]), tags=(tag,))

def load_data():
    global photo_refs
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produk")
    rows = cursor.fetchall()
    conn.close()

    for row in treeview.get_children():
        treeview.delete(row)
    photo_refs = {}
    for idx, row in enumerate(rows):
        foto_path = row[3]
        tag = 'even' if idx % 2 == 0 else 'odd'
        if foto_path and os.path.exists(foto_path):
            try:
                img = Image.open(foto_path)
                img = img.resize((120, 120), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                photo_refs[idx] = photo
                treeview.insert('', 'end', text='', image=photo, values=(row[0], row[1], row[2], row[3]), tags=(tag,))
            except:
                treeview.insert('', 'end', text='[Gambar Error]', values=(row[0], row[1], row[2], row[3]), tags=(tag,))
        else:
            treeview.insert('', 'end', text='[Tidak Ada Gambar]', values=(row[0], row[1], row[2], row[3]), tags=(tag,))

def clear_inputs():
    entry_nama.delete(0, tk.END)
    entry_harga.delete(0, tk.END)
    entry_foto.delete(0, tk.END)

def toggle_buttons(state):
    if state == "reset":
        btn_add.config(state=tk.NORMAL)
        btn_update.config(state=tk.DISABLED)
        btn_delete.config(state=tk.DISABLED)
    elif state == "update":
        btn_add.config(state=tk.DISABLED)
        btn_update.config(state=tk.NORMAL)
        btn_delete.config(state=tk.NORMAL)

def on_select(event):
    selected_item = treeview.selection()
    if selected_item:
        selected_data = treeview.item(selected_item[0])['values']
        entry_nama.delete(0, tk.END)
        entry_nama.insert(0, selected_data[1])
        entry_harga.delete(0, tk.END)
        entry_harga.insert(0, selected_data[2])
        entry_foto.delete(0, tk.END)
        entry_foto.insert(0, selected_data[3])
        toggle_buttons("update")

# Fungsi baru untuk membuka file transaksi.py
def buka_transaksi(produk_id):
    """Membuka file transaksi.py dengan mengirim ID produk sebagai argumen"""
    try:
        # Menjalankan transaksi.py dengan argumen produk_id
        subprocess.Popen([sys.executable, "transaksi.py", str(produk_id)])
    except FileNotFoundError:
        messagebox.showerror("Error", "File transaksi.py tidak ditemukan!")
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

# Fungsi baru untuk menangani klik user non-admin
def on_user_click(event):
    """Handler untuk klik user non-admin - menampilkan popup konfirmasi pembelian dengan tampilan lebih bagus"""
    selected_item = treeview.selection()
    if selected_item:
        selected_data = treeview.item(selected_item[0])['values']
        produk_id = selected_data[0]
        nama_produk = selected_data[1]
        harga_produk = selected_data[2]

        # Format harga dengan benar
        try:
            harga_num = float(harga_produk)
            harga_tampil = f"{harga_num:,.0f}"
        except ValueError:
            harga_tampil = str(harga_produk)

        # Buat window konfirmasi custom
        popup = tk.Toplevel()
        popup.title("Konfirmasi Pembelian")
        popup.geometry("400x260")
        popup.configure(bg="#e3f2fd")
        popup.resizable(False, False)

        # Judul
        tk.Label(popup, text="Konfirmasi Pembelian", font=("Arial", 14, "bold"), bg="#e3f2fd", fg="#1976d2").pack(pady=(20, 10))

        # Info produk
        frame_info = tk.Frame(popup, bg="#e3f2fd")
        frame_info.pack(pady=5)
        tk.Label(frame_info, text="Produk:", font=("Arial", 12), bg="#e3f2fd").grid(row=0, column=0, sticky="w")
        tk.Label(frame_info, text=nama_produk, font=("Arial", 12, "bold"), bg="#e3f2fd", fg="#388e3c").grid(row=0, column=1, sticky="w", padx=5)
        tk.Label(frame_info, text="Harga:", font=("Arial", 12), bg="#e3f2fd").grid(row=1, column=0, sticky="w")
        tk.Label(frame_info, text=f"Rp {harga_tampil}", font=("Arial", 12, "bold"), bg="#e3f2fd", fg="#d84315").grid(row=1, column=1, sticky="w", padx=5)

        # Garis pemisah
        tk.Frame(popup, height=2, bd=0, bg="#90caf9").pack(fill="x", padx=20, pady=10)

        # Teks instruksi
        tk.Label(popup, text="Klik 'Ya' untuk melanjutkan pembelian.", font=("Arial", 11), bg="#e3f2fd").pack(pady=(0, 10))

        # Tombol aksi
        def lanjutkan():
            popup.destroy()
            # Langsung buka transaksi.py dengan produk_id
            buka_transaksi(produk_id)

        def batal():
            popup.destroy()

        btn_frame = tk.Frame(popup, bg="#e3f2fd")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Ya", command=lanjutkan, font=("Arial", 11, "bold"), bg="#43a047", fg="white", width=10).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Batal", command=batal, font=("Arial", 11), bg="#e53935", fg="white", width=10).pack(side="left", padx=10)

        # Fokus ke popup
        popup.transient(treeview)
        popup.grab_set()
        popup.wait_window()

def browse_file():
    file_path = filedialog.askopenfilename(title="Pilih Foto Produk",
                                           filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")])
    if file_path:
        entry_foto.delete(0, tk.END)
        entry_foto.insert(0, file_path)

def open_data_window(is_admin=True):
    global entry_nama, entry_harga, entry_foto, treeview, entry_search, btn_add, btn_update, btn_delete, photo_refs

    root = tk.Tk()
    root.title("Pengelolaan Produk")
    root.geometry("1400x800")
    root.configure(bg='#87CEFA')

    if is_admin:
        input_frame = tk.Frame(root, bg='#87CEFA')
        input_frame.pack(pady=20)

        labels = ["Nama Produk", "Harga Produk", "Foto Produk"]
        entries = []
        for i, label in enumerate(labels):
            tk.Label(input_frame, text=label, font=("Arial", 12), bg='#87CEFA').grid(row=i, column=0, padx=10, pady=10, sticky="w")
            entry = tk.Entry(input_frame, font=("Arial", 14), width=40)
            entry.grid(row=i, column=1, padx=10, pady=10)
            entries.append(entry)

        entry_nama, entry_harga, entry_foto = entries

        btn_browse = tk.Button(input_frame, text="Pilih File", command=browse_file, font=("Arial", 10))
        btn_browse.grid(row=2, column=2, padx=5)

        button_frame = tk.Frame(root, bg='#87CEFA')
        button_frame.pack(pady=10)

        btn_add = tk.Button(button_frame, text="Tambah Data", command=add_data, font=("Arial", 14), width=15, bg='#4CAF50', fg='white')
        btn_update = tk.Button(button_frame, text="Ubah Data", command=update_data, font=("Arial", 14), width=15, bg='#2196F3', fg='white', state=tk.DISABLED)
        btn_delete = tk.Button(button_frame, text="Hapus Data", command=delete_data, font=("Arial", 14), width=15, bg='#F44336', fg='white', state=tk.DISABLED)

        btn_add.pack(side=tk.LEFT, padx=5)
        btn_update.pack(side=tk.LEFT, padx=5)
        btn_delete.pack(side=tk.LEFT, padx=5)
    else:
        # Menambahkan label instruksi untuk user non-admin
        instruksi_frame = tk.Frame(root, bg='#87CEFA')
        instruksi_frame.pack(pady=10)
        tk.Label(instruksi_frame, text="Klik pada baris produk untuk membeli", 
                font=("Arial", 14, "italic"), bg='#87CEFA', fg='#0066CC').pack()
        
        entry_nama = entry_harga = entry_foto = btn_add = btn_update = btn_delete = btn_browse = None

    search_frame = tk.Frame(root, bg='#e0f7fa')
    search_frame.pack(pady=10)

    tk.Label(search_frame, text="Cari Produk", font=("Arial", 12), bg='#e0f7fa').grid(row=0, column=0, padx=10, pady=10)
    entry_search = tk.Entry(search_frame, font=("Arial", 14), width=20)
    entry_search.grid(row=0, column=1, padx=10, pady=10)
    tk.Button(search_frame, text="Cari", command=search_data, font=("Arial", 14), width=10, bg='#FFC107').grid(row=0, column=2, padx=10, pady=10)

    columns = ('ID', 'Nama Produk', 'Harga Produk', 'Foto')
    treeview = ttk.Treeview(root, columns=columns, show='tree headings')
    treeview.pack(fill='both', expand=True, padx=20, pady=10)

    treeview.heading('#0', text='Foto')
    treeview.column('#0', width=130, anchor='center', stretch=False)
    treeview.heading('Nama Produk', text='Nama Produk')
    treeview.column('Nama Produk', width=420, anchor='center')
    treeview.heading('Harga Produk', text='Harga Produk')
    treeview.column('Harga Produk', width=420, anchor='center')
    treeview.heading('ID', text='ID')
    treeview.column('ID', width=0, stretch=False)
    treeview.heading('Foto', text='Foto (path)')
    treeview.column('Foto', width=0, stretch=False)

    style = ttk.Style()
    style.configure("Treeview", rowheight=120)
    style.map('even.Treeview', background=[('selected', '#b3e0ff')])
    style.map('odd.Treeview', background=[('selected', '#99ccff')])
    treeview.tag_configure('even', background='#b3e0ff')
    treeview.tag_configure('odd', background='#3399ff')

    create_table()
    load_data()

    # Binding event yang berbeda untuk admin dan user
    if is_admin:
        treeview.bind("<<TreeviewSelect>>", on_select)
    else:
        # Binding untuk user non-admin - klik sekali untuk popup beli
        treeview.bind("<ButtonRelease-1>", on_user_click)

    root.mainloop()

def show_login_window():
    login_root = tk.Tk()
    login_root.title("Login")
    login_root.geometry("300x200")
    login_root.configure(bg='#e0f7fa')

    tk.Label(login_root, text="Masukkan Email", font=("Arial", 12), bg='#e0f7fa').pack(pady=20)
    email_entry = tk.Entry(login_root, font=("Arial", 12), width=30)
    email_entry.pack(pady=5)

    def login():
        email = email_entry.get().strip().lower()
        login_root.destroy()
        if email == "fadhil@gmail.com":
            open_data_window(is_admin=True)
        else:
            open_data_window(is_admin=False)

    tk.Button(login_root, text="Login", command=login, font=("Arial", 12), bg='#4CAF50', fg='white').pack(pady=20)
    login_root.mainloop()

if __name__ == "__main__":
    create_table()
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "admin":
        open_data_window(is_admin=True)
    else:
        open_data_window(is_admin=False)