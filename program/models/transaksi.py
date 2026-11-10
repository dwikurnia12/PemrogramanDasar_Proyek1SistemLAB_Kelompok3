from datetime import date, timedelta
from .item_peminjaman import ItemPeminjaman


class Transaksi:
    STATUS_DIPINJAM = "dipinjam"
    STATUS_SEBAGIAN = "sebagian dikembalikan"
    STATUS_SELESAI = "selesai"

    def __init__(self, id_transaksi, mahasiswa, kode_alat, tanggal_pinjam=None,
                 batas_pengembalian=None, status=None, items=None):
        self.id_transaksi = id_transaksi
        self.nim_mahasiswa = mahasiswa.nim if hasattr(mahasiswa, "nim") else mahasiswa
        self.item = items if items is not None else [
            ItemPeminjaman(kode) for kode in kode_alat
        ]
        self.tanggal_peminjaman = tanggal_pinjam or date.today()
        self.batas_pengembalian = (
            batas_pengembalian or self.tanggal_peminjaman + timedelta(days=7)
        )
        self.status = status or self.STATUS_DIPINJAM

    def alat_belum_kembali(self):
        return [item for item in self.item if not item.dikembalikan]

    def proses_pengembalian(self, kode_alat, kondisi):
        for item in self.item:
            if item.kode_alat == kode_alat:
                if item.dikembalikan:
                    return False, "Alat tersebut sudah dikembalikan."
                item.dikembalikan = True
                item.tanggal_kembali = date.today()
                item.kondisi_kembali = kondisi.lower()
                self.status = (
                    self.STATUS_SELESAI if not self.alat_belum_kembali()
                    else self.STATUS_SEBAGIAN
                )
                return True, "Pengembalian berhasil."
        return False, "Alat tidak ditemukan dalam transaksi."

    def __str__(self):
        alat = ", ".join(item.kode_alat for item in self.item)
        return (f"{self.id_transaksi} | NIM: {self.nim_mahasiswa} | "
                f"Alat: {alat} | Pinjam: {self.tanggal_peminjaman} | "
                f"Batas: {self.batas_pengembalian} | Status: {self.status}")
