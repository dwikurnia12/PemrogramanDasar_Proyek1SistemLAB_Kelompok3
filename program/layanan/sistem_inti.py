from datetime import date
from ..models import Mahasiswa, Peralatan, Transaksi, LogAktivitas

class SistemInti:
        def __init__(self):
            self.mahasiswa = {}
            self.peralatan = {}
            self.transaksi = {}
            self.log = LogAktivitas()
            self.nomor_transaksi = 1
        def data_awal(self):
            # Contoh data agar program langsung dapat didemonstrasikan.
            data_mahasiswa = [
                ("M001", "Andi", "081234567890"),
                ("M002", "Budi", "082345678901"),
                ("M003", "Citra", "083456789012"),
            ]
            for nim, nama, hp in data_mahasiswa:
                self.mahasiswa[nim] = Mahasiswa(nim, nama, hp)

            data_alat = [
                ("A001", "Laptop", "Perangkat Komputasi"),
                ("A002", "Kamera Digital", "Perangkat Multimedia"),
                ("A003", "Tripod", "Perangkat Multimedia"),
                ("A004", "Kabel LAN", "Perangkat Jaringan"),
                ("A005", "Multimeter", "Perangkat Elektronika"),
            ]
            for kode, nama, kategori in data_alat:
                self.peralatan[kode] = Peralatan(kode, nama, kategori)
        def _pause(self):
            input("\nTekan ENTER untuk melanjutkan...")
        def _input_tidak_kosong(self, pesan):
            while True:
                nilai = input(pesan).strip()
                if nilai:
                    return nilai
                print("Input tidak boleh kosong.")
        def _mahasiswa_memiliki_transaksi_aktif(self, nim):
            return any(
                t.nim_mahasiswa == nim
                and t.status != Transaksi.STATUS_SELESAI
                for t in self.transaksi.values()
            )
        def _jumlah_transaksi_aktif(self, nim):
            return sum(
                1 for t in self.transaksi.values()
                if t.nim_mahasiswa == nim and t.status != Transaksi.STATUS_SELESAI
            )
        def _cari_alat(self, kode):
            return self.peralatan.get(kode)

