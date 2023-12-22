# import awal
from librarykelompok2.mylibrary import deskripsi


# tambahan pada kode program
class AttendanceApp:
    def _init_(self, root):
        self.btn_tampilkan_deskripsi = tk.Button(root, text='Tampilkan Deskripsi', command=self.tampilkan_deskripsi, font=("Arial", 15))
        self.btn_tampilkan_deskripsi.place(x=1100, y=590)
        self.btn_tampilkan_deskripsi.configure(width=20, height=3)
        
    def tampilkan_deskripsi(self):
        # Memanggil fungsi untuk menampilkan deskripsi dari mylibrary
        deskripsi()