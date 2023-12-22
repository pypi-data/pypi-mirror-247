from tkinter import messagebox

def deskripsi():
    """
    Fungsi untuk mencetak deskripsi kode program ke konsol
    dan menampilkan informasi nama kelompok menggunakan messagebox.
    """
    description = "Kode tersebut merupakan implementasi aplikasi absensi menggunakan OpenCV dan Tkinter. \n\nAplikasi ini memungkinkan pengguna untuk menambahkan data wajah mahasiswa, melakukan absensi melalui kamera, dan menyimpan hasil absensi ke dalam file Excel. \n\nDengan antarmuka pengguna yang bersih dan tombol tambahan tampilkan deskripsi yang memberikan notifikasi, aplikasi ini menyediakan pengalaman pengguna yang intuitif."
    print(description)

    messagebox.showinfo("Milik Kelompok 2:", description)
