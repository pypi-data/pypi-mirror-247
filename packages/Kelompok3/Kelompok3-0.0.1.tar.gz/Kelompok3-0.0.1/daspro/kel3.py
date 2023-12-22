# File: program_ui.py
import tkinter as tk
from tkinter import messagebox

class ProgramUI:
    def __init__(self, master):
        self.master = master
        master.title("Deskripsi Program dan Profil Anggota Kelompok")

        # Membuat tombol untuk menampilkan deskripsi
        self.description_button = tk.Button(master, text="Deskripsi Program", command=self.show_description)
        self.description_button.pack(pady=10)

        # Membuat tombol untuk menampilkan profil anggota kelompok
        self.profile_button = tk.Button(master, text="Profil Anggota Kelompok", command=self.show_team_profile)
        self.profile_button.pack(pady=10)

    def show_description(self):
        description_text = (
            "Program Input Data Gaji menggunakan Python adalah alat yang sederhana dan efektif "
            "untuk memudahkan penginputan informasi gaji karyawan. Dengan fitur input data karyawan, "
            "program ini membantu menyederhanakan proses administrasi kepegawaian. Didesain dengan "
            "antarmuka pengguna yang intuitif, program ini memastikan keakuratan perhitungan gaji, "
            "mencegah kesalahan input, dan memberikan kemudahan dalam mengelola data gaji karyawan."
        )
        messagebox.showinfo("Informasi Program", description_text)

    def show_team_profile(self):
        team_profile_text = "Anggota Kelompok:\n1. Faranaya\n2. Rizal\n3. Adit\n4. Sabil\n5. Windy"
        messagebox.showinfo("Profil Anggota Kelompok", team_profile_text)
