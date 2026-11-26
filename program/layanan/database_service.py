
import mysql.connector
from mysql.connector import Error


class LayananDatabase:
    def __init__(self):
        self.koneksi = None

    def hubungkan(self):
        try:
            self.koneksi = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="lab_peminjaman",
                port=3306
            )

            if self.koneksi.is_connected():
                print("Berhasil terhubung ke database MySQL!")
                return True

        except Error as error:
            print("Gagal terhubung ke database:", error)
            return False

    def tutup(self):
        if self.koneksi and self.koneksi.is_connected():
            self.koneksi.close()

    def ambil_koneksi(self):
        return self.koneksi
