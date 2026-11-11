from pathlib import Path
from datetime import date, timedelta
from ..models import Mahasiswa, Peralatan, Transaksi, LogAktivitas
from .file_service import LayananFile


class SistemInti:
    def __init__(self):
        self.mahasiswa = {}
        self.peralatan = {}
        self.transaksi = {}
        self.pemeliharaan = {}
        self.log = LogAktivitas()
        self.nomor_transaksi = 1
        folder_data = Path(__file__).resolve().parents[2] / "data"
        self.file_service = LayananFile(folder_data)
        self.file_service.muat_semua(self)

        # Data contoh hanya dibuat saat seluruh data utama masih kosong.
        if not self.mahasiswa and not self.peralatan and not self.transaksi:
            self.data_awal()
            self.file_service.simpan_semua(self)

    def data_awal(self):
        data_mahasiswa = [
            ("M001", "Andi Pratama", "081234567890"),
            ("M002", "Budi Santoso", "085612345678"),
            ("M003", "Citra Lestari", "081298765432"),
            ("M004", "Dina Putri", "082112223333"),
            ("M005", "Eko Saputra", "081377788899"),
        ]
        for nim, nama, hp in data_mahasiswa:
            self.mahasiswa[nim] = Mahasiswa(nim, nama, hp)

        data_alat = [
            ("A001", "Laptop", "Perangkat Komputasi"),
            ("A002", "Kamera Digital", "Perangkat Multimedia"),
            ("A003", "Tripod", "Perangkat Multimedia"),
            ("A004", "Kabel LAN", "Perangkat Jaringan"),
            ("A005", "Multimeter", "Perangkat Elektronika"),
            ("A006", "Router", "Perangkat Jaringan"),
            ("A007", "Mikrokontroler", "Perangkat Elektronika"),
            ("A008", "Proyektor", "Perangkat Presentasi"),
            ("A009", "Mikrofon", "Perangkat Audio"),
            ("A010", "Oscilloscope", "Perangkat Elektronika"),
        ]
        for kode, nama, kategori in data_alat:
            self.peralatan[kode] = Peralatan(kode, nama, kategori)

        # Tiga transaksi contoh berstatus selesai agar data demo konsisten.
        contoh = [
            ("T001", "M001", ["A001"], date(2026, 8, 10)),
            ("T002", "M002", ["A002", "A003"], date(2026, 8, 11)),
            ("T003", "M003", ["A004"], date(2026, 8, 12)),
        ]
        for id_tr, nim, kode_list, tanggal in contoh:
            t = Transaksi(id_tr, nim, kode_list, tanggal)
            for item in t.item:
                item.dikembalikan = True
                item.tanggal_kembali = tanggal + timedelta(days=1)
                item.kondisi_kembali = "baik"
                self.peralatan[item.kode_alat].total_dipinjam += 1
            t.status = Transaksi.STATUS_SELESAI
            self.transaksi[id_tr] = t
        self.nomor_transaksi = 4

    def _pause(self):
        input("\nTekan ENTER untuk melanjutkan...")

    def _input_tidak_kosong(self, pesan):
        while True:
            nilai = input(pesan).strip()
            if nilai:
                if "|" in nilai or "\n" in nilai:
                    print("Karakter | dan baris baru tidak boleh digunakan.")
                    continue
                return nilai
            print("Input tidak boleh kosong.")

    def _simpan(self):
        return self.file_service.simpan_semua(self)

    def _catat_log(self, pesan):
        self.log.tambah(pesan)
        self.file_service.tambah_log(pesan)

    def _mahasiswa_memiliki_transaksi_aktif(self, nim):
        return any(
            t.nim_mahasiswa == nim and t.status != Transaksi.STATUS_SELESAI
            for t in self.transaksi.values()
        )

    def _jumlah_transaksi_aktif(self, nim):
        return sum(
            1 for t in self.transaksi.values()
            if t.nim_mahasiswa == nim and t.status != Transaksi.STATUS_SELESAI
        )

    def _cari_alat(self, kode):
        return self.peralatan.get(kode)
