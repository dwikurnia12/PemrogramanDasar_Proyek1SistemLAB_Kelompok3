class ItemPeminjaman:
    def __init__(self, kode_alat, dikembalikan=False, tanggal_kembali=None,
                 kondisi_kembali=None):
        self.kode_alat = kode_alat
        self.dikembalikan = dikembalikan
        self.tanggal_kembali = tanggal_kembali
        self.kondisi_kembali = kondisi_kembali

    def __str__(self):
        status = "Sudah kembali" if self.dikembalikan else "Masih dipinjam"
        return f"{self.kode_alat} - {status}"
