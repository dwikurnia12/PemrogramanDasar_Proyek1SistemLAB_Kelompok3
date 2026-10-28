class Mahasiswa:
    def __init__(self, nim, nama, no_hp):
        self.nim = nim
        self.nama = nama
        self.no_hp = no_hp
        self.status_aktif_peminjaman = False

    def __str__(self):
        status = "Aktif" if self.status_aktif_peminjaman else "Tidak ada"
        return f"{self.nim} | {self.nama} | {self.no_hp} | Peminjaman: {status}"