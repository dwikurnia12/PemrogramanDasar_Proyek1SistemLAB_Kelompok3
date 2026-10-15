class Peralatan:
    KONDISI_VALID = ("baik", "rusak ringan", "rusak berat")

    def __init__(self, kode, nama, kategori, kondisi="baik"):
        self.kode = kode
        self.nama = nama
        self.kategori = kategori
        self.kondisi = kondisi.lower()
        self.tersedia = self.kondisi == "baik"
        self.total_dipinjam = 0

    def __str__(self):
        status = "Tersedia" if self.tersedia else "Tidak tersedia"
        return (
            f"{self.kode} | {self.nama} | {self.kategori} | "
            f"Kondisi: {self.kondisi} | {status}"
        )

