class ItemPeminjaman:
    def __init__(self, kode_alat):
        self.kode_alat = kode_alat
        self.dikembalikan = False
        self.tanggal_kembali = None
        self.kondisi_kembali = None

    def __str__(self):
        status = "Sudah kembali" if self.dikembalikan else "Masih dipinjam"
        return f"{self.kode_alat} - {status}"

