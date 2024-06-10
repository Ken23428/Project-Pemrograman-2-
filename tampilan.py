import sqlite3
from datetime import datetime
import random
import numpy as np
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog, scrolledtext
from ambil_data import *


# Fungsi untuk tambah tanaman
def tambah_tanaman(id_tree, input_window):
    if not id_tree.isdigit():
        messagebox.showerror("Error", "ID Tanaman harus berupa angka.")
        return

    id_tree = int(id_tree)
    latitude = random.uniform(-90, 90)
    longitude = random.uniform(-180, 180)
    added_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO database (id_tree, latitude, longitude, added_timestamp) VALUES (?,?,?,?)',
                       (id_tree, latitude, longitude, added_timestamp))
        conn.commit()
        messagebox.showinfo("Tambah Tanaman", f"Tanaman dengan ID = {id_tree} berhasil ditambahkan")
        input_window.destroy()  # Tutup jendela input ID setelah berhasil menambahkan tanaman
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "ID Tanaman sudah ada.")
    finally:
        conn.close()

# Fungsi untuk menampilkan halaman input ID tanaman
def halaman_tambah_tanaman():
    # Buat window baru
    input_window = tk.Toplevel(root)
    input_window.title("Masukkan ID Tanaman")
    input_window.geometry("400x200")
    
    tk.Label(input_window, text="Masukkan ID Tanaman:", font=("Helvetica", 12)).pack(pady=10)
    
    entry_id_tree = tk.Entry(input_window, font=("Helvetica", 12))
    entry_id_tree.pack(pady=10)
    
    def lanjutkan():
        id_tree = entry_id_tree.get()
        tambah_tanaman(id_tree, input_window)
    
    tk.Button(input_window, text="Tambah", command=lanjutkan, font=("Helvetica", 12), bg="green", fg="white").pack(pady=10)

# Fungsi untuk menghapus tanaman
def hapus_tanaman(id_tree, input_window):
    if not id_tree.isdigit():
        messagebox.showerror("Error", "ID Tanaman harus berupa angka.")
        return

    id_tree = int(id_tree)
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Cek apakah ID tanaman ada dalam database
    cursor.execute('SELECT COUNT(*) FROM database WHERE id_tree = ?', (id_tree,))
    result = cursor.fetchone()
    
    if result[0] == 0:
        messagebox.showerror("Error", "ID Tanaman tidak ditemukan.")
        conn.close()
        return
    
    cursor.execute('DELETE FROM sensor_data WHERE id_tree = ?', (id_tree,))
    cursor.execute('DELETE FROM database WHERE id_tree = ?', (id_tree,))
    conn.commit()
    conn.close()

    messagebox.showinfo("Hapus Tanaman", f"Tanaman dengan ID = {id_tree} dan semua data sensornya berhasil dihapus")
    input_window.destroy()  # Tutup jendela input ID setelah berhasil menghapus tanaman

# Fungsi untuk menampilkan halaman input ID tanaman yang akan dihapus
def halaman_hapus_tanaman():
    # Buat window baru
    input_window = tk.Toplevel(root)
    input_window.title("Hapus Tanaman")
    input_window.geometry("400x200")
    
    tk.Label(input_window, text="Masukkan ID Tanaman yang akan dihapus:", font=("Helvetica", 12)).pack(pady=10)
    
    entry_id_tree = tk.Entry(input_window, font=("Helvetica", 12))
    entry_id_tree.pack(pady=10)
    
    def lanjutkan_hapus():
        id_tree = entry_id_tree.get()
        hapus_tanaman(id_tree, input_window)
    
    tk.Button(input_window, text="Hapus", command=lanjutkan_hapus, font=("Helvetica", 12), bg="red", fg="white").pack(pady=10)
    tk.Button(input_window, text="Kembali", command=input_window.destroy, font=("Helvetica", 12), bg="grey", fg="white").pack(pady=10)

# Fungsi tampilkan data sensor tanaman
def tampilkan_data(id_tree, label_data):
    if not id_tree.isdigit():
        messagebox.showerror("Error", "ID Tanaman harus berupa angka.")
        return

    id_tree = int(id_tree)
    
    label_sensor = {
        0: "Suhu udara (°C)",
        1: "Kelembaban udara (%)",
        2: "Curah hujan (mm)",
        3: "Tingkat sinar UV",
        4: "Suhu tanah (°C)",
        5: "Kelembaban tanah (%)",
        6: "pH tanah",
        7: "Kadar N dalam tanah (mg/kg)",
        8: "Kadar P dalam tanah (mg/kg)",
        9: "Kadar K dalam tanah (mg/kg)"
    }

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT sensor_type, nilai, MAX(timestamp)
    FROM sensor_data 
    WHERE id_tree = ?
    GROUP BY sensor_type
    ''', (id_tree,))

    data = cursor.fetchall()

    cursor.execute('SELECT latitude, longitude, added_timestamp FROM database WHERE id_tree = ?', (id_tree,))
    database_info = cursor.fetchone()
    conn.close()

    if not data:
        messagebox.showerror("Error", f"Tidak ada data sensor untuk tanaman dengan ID = {id_tree}")
        return
    
    latitude, longitude, added_timestamp = database_info if database_info else (None, None, None)

    hasil = f"id: {id_tree} | lat: {latitude} | lon: {longitude}\n"

    if added_timestamp:
        hasil += f"Tanggal ID ditambahkan : {format_timestamp(added_timestamp)}\n\n"
    else:
        hasil += "Tanggal: Tidak Tersedia\n\n"
    
    # menampilkan data 
    for sensor_type, nilai, timestamp in data:
        hasil += f"{label_sensor.get(sensor_type, f'Sensor {sensor_type}')}: {nilai:.2f}   {format_timestamp(timestamp)}\n"

    # Tampilkan hasil dalam widget Label
    label_data.configure(text=hasil)  
    label_data.pack(pady=10)

# Fungsi untuk menampilkan halaman input ID tanaman
def halaman_input_id():
    # Buat window baru
    input_window = tk.Toplevel(root)
    input_window.title("Masukkan ID Tanaman")
    input_window.geometry("400x200")
    
    tk.Label(input_window, text="Masukkan ID Tanaman:", font=("Helvetica", 12)).pack(pady=10)
    
    entry_id_tree = tk.Entry(input_window, font=("Helvetica", 12))
    entry_id_tree.pack(pady=10)
    
    def lanjutkan():
        id_tree = entry_id_tree.get()
        tampilkan_halaman_data(id_tree)
        input_window.destroy()
    
    tk.Button(input_window, text="Lanjutkan", command=lanjutkan, font=("Helvetica", 10), bg="#2ECC71", fg="white").pack(pady=10)

# Fungsi untuk menampilkan halaman data
def tampilkan_halaman_data(id_tree):
    # Buat window baru
    data_window = tk.Toplevel(root)
    data_window.title("Data Tanaman")
    data_window.geometry("600x400")

    label_data = tk.Label(data_window, text="", wraplength=400, justify="center", font=("Helvetica", 10))
    label_data.pack(pady=10)

    # Panggil fungsi untuk menampilkan data
    tampilkan_data(id_tree, label_data)

    tk.Button(data_window, text="Kembali ke Menu", command=data_window.destroy, font=("Helvetica", 10), bg="#A52A2A", fg="white").pack(pady=10)

# Fungsi untuk tampilkan semua data 
def tampilkan_semua_data():
    label_sensor = {
        0: "Suhu udara (°C)",
        1: "Kelembaban udara (%)",
        2: "Curah hujan (mm)",
        3: "Tingkat sinar UV",
        4: "Suhu tanah (°C)",
        5: "Kelembaban tanah (%)",
        6: "pH tanah",
        7: "Kadar N dalam tanah (mg/kg)",
        8: "Kadar P dalam tanah (mg/kg)",
        9: "Kadar K dalam tanah (mg/kg)"
    }

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id_tree, latitude, longitude, added_timestamp FROM database')
    data = cursor.fetchall()
    conn.close()

    if not data:
        messagebox.showinfo("Tidak Ada Tanaman", "Tidak ada tanaman yang ditemukan di database.")
        return

    hasil = ""
    for tanaman in data:
        id_tree, latitude, longitude, added_timestamp = tanaman
        hasil += f"id: {id_tree} | lat: {latitude} | lon: {longitude}\n"
        if added_timestamp:
            hasil += f"Tanggal ID ditambahkan: {added_timestamp}\n\n"
        else:
            hasil += "Tanggal ID ditambahkan: Tidak Tersedia\n"

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
        SELECT sensor_type, nilai, MAX(timestamp)
        FROM sensor_data
        WHERE id_tree = ?
        GROUP BY sensor_type
        ''', (id_tree,))
        sensor_data = cursor.fetchall()
        conn.close()

        for sensor_type, nilai, timestamp in sensor_data:
            hasil += f"{label_sensor.get(sensor_type, f'Sensor {sensor_type}')}: {nilai:.2f}\n"
        hasil += "\n"

    # Membuat window baru untuk menampilkan data tanaman
    tampil_window = tk.Toplevel(root)
    tampil_window.title("Daftar Tanaman")
    tampil_window.geometry("600x400")

    # Menambahkan Text widget dengan scrollbar
    text_area = scrolledtext.ScrolledText(tampil_window, wrap=tk.WORD, padx=10, pady=10, bg="#f0f0f0")
    text_area.pack(expand=True, fill='both')

    # Membuat tag untuk teks center
    text_area.tag_configure("center", justify='center')

    # Menambahkan teks ke dalam Text widget dengan tag 'center'
    text_area.insert(tk.END, hasil, "center")

    # Membuat teks menjadi tidak dapat diedit
    text_area.config(state=tk.DISABLED)


# Fungsi membuat grafik sensor
def grafik_sensor(id_tree, sensor_type, nama_sensor, waktu_mulai, waktu_akhir):
    data = ambil_data_sensor_untuk_grafik(id_tree, sensor_type, waktu_mulai, waktu_akhir)
    
    if not data:
        messagebox.showerror("Error", f"Tidak ada data untuk grafik ID tanaman = {id_tree}")
        return
    
    nilai, timestamps = zip(*data)
    timestamps = [datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') for ts in timestamps]

    timestamps, nilai = interpolasi_data_hilang(timestamps, nilai, waktu_mulai, waktu_akhir)

    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'orange', 'purple', 'brown']

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, nilai, marker='o', linestyle='-', label=nama_sensor, color=colors[sensor_type % len(colors)])
    plt.title(f'Grafik {nama_sensor} untuk ID Tanaman {id_tree}')
    plt.xlabel('Waktu')
    plt.ylabel(nama_sensor)

    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))

    plt.gcf().autofmt_xdate()
    plt.grid(True)

    plt.legend()
    plt.show()



def tampilkan_opsi_grafik(id_tree):
    label_sensor = {
        0: "Suhu udara (°C)",
        1: "Kelembaban udara (%)",
        2: "Curah hujan (mm)",
        3: "Tingkat sinar UV",
        4: "Suhu tanah (°C)",
        5: "Kelembaban tanah (%)",
        6: "pH tanah",
        7: "Kadar N dalam tanah (mg/kg)",
        8: "Kadar P dalam tanah (mg/kg)",
        9: "Kadar K dalam tanah (mg/kg)"
    }

    def pilih_sensor(sensor_type):
        waktu_mulai = waktu_mulai_entry.get()
        waktu_akhir = waktu_akhir_entry.get()

        try:
            if waktu_mulai and waktu_akhir:
                waktu_mulai_dt = datetime.strptime(waktu_mulai, '%Y-%m-%d %H:%M:%S')
                waktu_akhir_dt = datetime.strptime(waktu_akhir, '%Y-%m-%d %H:%M:%S')

                waktu_mulai = waktu_mulai_dt.strftime('%Y-%m-%d %H:%M:%S')
                waktu_akhir = waktu_akhir_dt.strftime('%Y-%m-%d %H:%M:%S')

                grafik_sensor(id_tree, sensor_type, label_sensor[sensor_type], waktu_mulai, waktu_akhir)
            else:
                messagebox.showerror("Error", "Waktu mulai dan waktu selesai harus diisi.")
        except ValueError as e:
            messagebox.showerror("Error", f"Format waktu salah: {e}")

    window = tk.Toplevel(root)
    window.title("Pilih Sensor untuk Menampilkan Grafik")
    window.geometry('640x745')

    frame = ttk.Frame(window, padding="10")
    frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(frame, text="Masukkan Rentang Waktu", font=("Helvetica", 14)).pack(pady=10)

    tk.Label(frame, text="Waktu Mulai (YYYY-MM-DD HH:MM:SS)").pack()
    waktu_mulai_entry = tk.Entry(frame, width=30)
    waktu_mulai_entry.pack(pady=5)

    tk.Label(frame, text="Waktu Selesai (YYYY-MM-DD HH:MM:SS)").pack()
    waktu_akhir_entry = tk.Entry(frame, width=30)
    waktu_akhir_entry.pack(pady=5)

    tk.Label(frame, text="Pilih Sensor", font=("Helvetica", 14)).pack(pady=10)

    sensor_frame = ttk.Frame(frame)
    sensor_frame.pack(fill=tk.BOTH, expand=True)
    
    for sensor_type, label in label_sensor.items():
        button = tk.Button(sensor_frame, text=label, command=lambda st=sensor_type: pilih_sensor(st))
        button.pack(pady=5, fill=tk.X)

    def kembali_ke_menu():
        window.destroy()

    tk.Button(frame, text="Kembali ke Menu", command=kembali_ke_menu, font=("Helvetica", 12), bg="red", fg="white").pack(pady=20)

def tampilkan_grafik():
    def submit_id():
        id_tree = id_entry.get()
        if id_tree:
            try:
                id_tree = int(id_tree)
                tampilkan_opsi_grafik(id_tree)
                input_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "ID Tanaman harus berupa angka.")
        else:
            messagebox.showerror("Error", "ID Tanaman harus diisi.")

    input_window = tk.Toplevel(root)
    input_window.title("Masukkan ID Tanaman")
    input_window.geometry('300x150')

    tk.Label(input_window, text="Masukkan ID Tanaman:", font=("Helvetica", 12)).pack(pady=10)
    id_entry = tk.Entry(input_window, width=20)
    id_entry.pack(pady=5)

    tk.Button(input_window, text="Submit", command=submit_id, font=("Helvetica", 12), bg="green", fg="white").pack(pady=10)

# Fungsi untuk menampilkan rata-rata data sensor
def tampilkan_rata_rata_sensor():
    def submit_rata_rata():
        waktu_mulai = waktu_mulai_entry.get()
        waktu_akhir = waktu_akhir_entry.get()

        try:
            if waktu_mulai and waktu_akhir:
                waktu_mulai_dt = datetime.strptime(waktu_mulai, '%Y-%m-%d %H:%M:%S')
                waktu_akhir_dt = datetime.strptime(waktu_akhir, '%Y-%m-%d %H:%M:%S')

                waktu_mulai = waktu_mulai_dt.strftime('%Y-%m-%d %H:%M:%S')
                waktu_akhir = waktu_akhir_dt.strftime('%Y-%m-%d %H:%M:%S')

                rata_rata = ambil_rata_rata_sensor(waktu_mulai, waktu_akhir)
                if rata_rata:
                    grafik_rata_rata_sensor(rata_rata, waktu_mulai, waktu_akhir)
                else:
                    messagebox.showinfo("Tidak Ada Data", "Tidak ada data rata-rata sensor yang ditemukan.")
            else:
                messagebox.showerror("Error", "Waktu mulai dan waktu selesai harus diisi.")
        except ValueError as e:
            messagebox.showerror("Error", f"Format waktu salah: {e}")

    input_window = tk.Toplevel(root)
    input_window.title("Masukkan Rentang Waktu")
    input_window.geometry('400x200')


    tk.Label(input_window, text="Masukkan Rentang Waktu", font=("Helvetica", 14)).pack(pady=10)

    tk.Label(input_window, text="Waktu Mulai (YYYY-MM-DD HH:MM:SS)").pack()
    waktu_mulai_entry = tk.Entry(input_window, width=30)
    waktu_mulai_entry.pack(pady=5)

    tk.Label(input_window, text="Waktu Selesai (YYYY-MM-DD HH:MM:SS)").pack()
    waktu_akhir_entry = tk.Entry(input_window, width=30)
    waktu_akhir_entry.pack(pady=5)

    tk.Button(input_window, text="Submit", command=submit_rata_rata, font=("Helvetica", 12), bg="green", fg="white").pack(pady=10)


# Fungsi untuk menampilkan grafik rata-rata sensor
def grafik_rata_rata_sensor(rata_rata, waktu_mulai, waktu_akhir):
    label_sensor = {
        0: "Suhu udara (°C)",
        1: "Kelembaban udara (%)",
        2: "Curah hujan (mm)",
        3: "Tingkat sinar UV",
        4: "Suhu tanah (°C)",
        5: "Kelembaban tanah (%)",
        6: "pH tanah",
        7: "Kadar N dalam tanah (mg/kg)",
        8: "Kadar P dalam tanah (mg/kg)",
        9: "Kadar K dalam tanah (mg/kg)"
    }

    jumlah_sensor = len(label_sensor)
    fig, ax = plt.subplots(figsize=(12, 8))

    # Menyiapkan array untuk posisi bar
    bar_positions = np.arange(jumlah_sensor)

    # Menyiapkan array untuk lebar bar
    bar_width = 0.35

    # Menyiapkan array untuk label bar
    bar_labels = [label_sensor[i] for i in range(jumlah_sensor)]

    # Menyiapkan warna untuk setiap bar
    colors = ['skyblue', 'salmon', 'lightgreen', 'gold', 'lightcoral', 
              'lightskyblue', 'orange', 'mediumseagreen', 'lightpink', 'lightgrey']

    # Plot garis untuk rata-rata pembacaan sensor, satu garis untuk setiap sensor
    jitter = np.linspace(-0.2, 0.2, jumlah_sensor)  # Menambahkan jitter untuk nilai x
    for i in range(jumlah_sensor):
        x_values = bar_positions + jitter[i]  # Menambahkan jitter pada posisi x
        y_values = [rata_rata[j] for j in range(jumlah_sensor)]
        ax.plot(x_values, y_values, marker='o', linestyle='-', color=colors[i], linewidth=2, label=label_sensor[i])

    # Tambahkan label pada sumbu-x
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(bar_labels, rotation=45, ha='right')

    # Tambahkan label pada sumbu-y
    ax.set_ylabel('Rata-rata Nilai Sensor')

    # Tambahkan judul dengan keterangan rentang waktu
    ax.set_title(f'Rata-rata Sensor untuk Setiap Tipe Sensor Semua Tanaman\nRentang Waktu: {waktu_mulai} - {waktu_akhir}')

    # Tambahkan grid
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Tambahkan legend
    ax.legend()

    plt.tight_layout()
    plt.show()

    # Plot bar untuk rata-rata pembacaan sensor dengan warna yang berbeda
    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.bar(bar_positions, [rata_rata[i] if rata_rata[i] is not None else 0 for i in range(jumlah_sensor)], 
                  bar_width, color=colors, label='Rata-rata Nilai Sensor')

    # Tambahkan label pada sumbu-x
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(bar_labels, rotation=45, ha='right')

    # Tambahkan label pada sumbu-y
    ax.set_ylabel('Rata-rata Nilai Sensor')

    # Tambahkan judul dengan keterangan rentang waktu
    ax.set_title(f'Rata-rata Sensor untuk Setiap Tipe Sensor Semua Tanaman\nRentang Waktu: {waktu_mulai} - {waktu_akhir}')

    # Tambahkan grid
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Tambahkan legend
    ax.legend()

    # Tambahkan nilai rata-rata di atas bar
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval, round(yval, 2), va='bottom', ha='center')

    plt.tight_layout()
    plt.show()

# Fungsi untuk memanggil database
database()


def masuk_ke_aplikasi():
    # Membersihkan tampilan utama
    for widget in root.winfo_children():
        widget.destroy()

    # Membuat Canvas untuk latar belakang gambar
    canvas = tk.Canvas(root, width=640, height=480)
    canvas.pack(fill="both", expand=True)

    # Memuat gambar
    try:
        bg_photo = tk.PhotoImage(file="plant.png")
    except tk.TclError:
        print("Error: Gambar 'pohon.png' tidak ditemukan atau format tidak didukung.")
        return

    # Menambahkan gambar ke canvas
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    # Menyimpan referensi gambar agar tidak dikumpulkan oleh garbage collector
    root.bg_photo = bg_photo

    # Membuat tombol-tombol dan menempatkannya di Canvas
    btn_tambah_tanaman = tk.Button(root, text="Tambah Tanaman", command=halaman_tambah_tanaman, bg="#006400", fg="white", font=("Helvetica", 12, "bold"))
    canvas.create_window(90, 140, window=btn_tambah_tanaman)  # Koordinat (100, 50)

    btn_hapus_tanaman = tk.Button(root, text="Hapus Tanaman", command=halaman_hapus_tanaman, bg="#A52A2A", fg="white", font=("Helvetica", 12, "bold"))
    canvas.create_window(540, 140, window=btn_hapus_tanaman)  # Koordinat (500, 50)

    btn_tampilkan_data = tk.Button(root, text="Data Tanaman", command=halaman_input_id, bg="#FF7F50", fg="white", font=("Helvetica", 12, "bold"))
    canvas.create_window(310, 150, window=btn_tampilkan_data)  # Koordinat (300, 100)

    btn_tampilkan_semua_tanaman = tk.Button(root, text="Daftar Tanaman", command=tampilkan_semua_data, bg="#00cc00", fg="white", font=("Helvetica", 12, "bold"))
    canvas.create_window(310, 320, window=btn_tampilkan_semua_tanaman)  # Koordinat (320, 200)

    btn_tampilkan_grafik = tk.Button(root, text="Grafik Sensor Tanaman", command=tampilkan_grafik, bg="#008b8b", fg="white", font=("Helvetica", 12, "bold"))
    canvas.create_window(115, 360, window=btn_tampilkan_grafik)  # Koordinat (100, 300)

    btn_tampilkan_rata_rata = tk.Button(root, text="Tampilkan Rata-rata Sensor", command=tampilkan_rata_rata_sensor, bg="#8a2be2", fg="white", font=("Helvetica", 12, "bold"))
    canvas.create_window(515, 360, window=btn_tampilkan_rata_rata)  # Koordinat (500, 300)



# Menampilkan GUI
root = tk.Tk()
root.title("Aplikasi Tanaman")
root.geometry("640x745")

# Menambahkan gambar latar belakang
background_image = tk.PhotoImage(file="animasi.png")
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Frame utama untuk layar selamat datang
welcome_frame = tk.Frame(root, bg="#FFFFFF", bd=10)
welcome_frame.pack(pady=20, padx=20)

# Menambahkan teks selamat datang
welcome_label = tk.Label(welcome_frame, text="SELAMAT DATANG DI APLIKASI TANAMAN", font=("Helvetica", 18), fg="#FFFFFF", bg="#2ECC71")
welcome_label.pack(pady=10) 

name_label = tk.Label(welcome_frame, text="M. Syahru Ramadhan\n2304111010086", font=("Arial", 16), fg="#000", bg="#FFFFFF")
name_label.pack(pady=10)

# Tombol untuk masuk ke tampilan berikutnya
btn_masuk = tk.Button(text="Mulai", command=masuk_ke_aplikasi, bg="#2ECC71", fg="#FFFFFF", font=("Helvetica", 14, "bold"))
btn_masuk.place(x=268, y=330, width=120, height=40)

# Fungsi untuk mengambil data sensor
mulai_ambil_data_sensor()

# Fungi untuk jalankan aplikasi
root.mainloop()


