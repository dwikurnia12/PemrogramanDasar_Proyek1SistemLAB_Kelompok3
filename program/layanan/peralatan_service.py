from datetime import date
from ..models import Peralatan, Transaksi


class LayananPeralatan:
    def tambah_peralatan(self):
        print("\n=== TAMBAH PERALATAN ===")
        kode = self._input_tidak_kosong("Kode alat: ")
        if kode in self.peralatan:
            print("Kode alat sudah terdaftar.")
            return
        nama = self._input_tidak_kosong("Nama alat: ")
        kategori = self._input_tidak_kosong("Kategori: ")
        self.peralatan[kode] = Peralatan(kode, nama, kategori)
        self._catat_log(f"Alat {kode} ditambahkan")
        self._simpan()
        print("Alat berhasil ditambahkan.")

    def edit_peralatan(self):
        print("\n=== EDIT PERALATAN ===")
        kode = self._input_tidak_kosong("Kode alat: ")
        alat = self.peralatan.get(kode)
        if not alat:
            print("Alat tidak ditemukan.")
            return
        alat.nama = input(f"Nama [{alat.nama}]: ").strip() or alat.nama
        alat.kategori = input(f"Kategori [{alat.kategori}]: ").strip() or alat.kategori
        self._catat_log(f"Data alat {kode} diubah")
        self._simpan()
        print("Data alat berhasil diubah.")

    def hapus_peralatan(self):
        print("\n=== HAPUS PERALATAN ===")
        kode = self._input_tidak_kosong("Kode alat: ")
        if kode not in self.peralatan:
            print("Alat tidak ditemukan.")
            return
        sedang_dipinjam = any(
            any(item.kode_alat == kode and not item.dikembalikan for item in t.item)
            for t in self.transaksi.values()
            if t.status != Transaksi.STATUS_SELESAI
        )
        if sedang_dipinjam:
            print("Gagal: alat masih tercatat dalam transaksi aktif.")
            return
        del self.peralatan[kode]
        self.pemeliharaan.pop(kode, None)
        self._catat_log(f"Alat {kode} dihapus")
        self._simpan()
        print("Alat berhasil dihapus.")

    def cari_peralatan(self):
        print("\n=== CARI PERALATAN ===")
        kata = self._input_tidak_kosong("Masukkan kode/nama/kategori: ").lower()
        hasil = [a for a in self.peralatan.values()
                 if kata in a.kode.lower() or kata in a.nama.lower()
                 or kata in a.kategori.lower()]
        if not hasil:
            print("Alat tidak ditemukan.")
            return
        for alat in hasil:
            print(alat)

    def tampilkan_alat_tersedia(self):
        print("\n=== ALAT TERSEDIA ===")
        hasil = [a for a in self.peralatan.values() if a.tersedia]
        if not hasil:
            print("Tidak ada alat yang tersedia.")
            return
        for alat in hasil:
            print(alat)

    def tampilkan_alat_dipinjam(self):
        print("\n=== ALAT SEDANG DIPINJAM ===")
        ditemukan = False
        for transaksi in self.transaksi.values():
            for item in transaksi.item:
                if not item.dikembalikan:
                    alat = self.peralatan.get(item.kode_alat)
                    if alat:
                        print(f"{alat.kode} | {alat.nama} | "
                              f"Transaksi: {transaksi.id_transaksi} | "
                              f"NIM: {transaksi.nim_mahasiswa}")
                        ditemukan = True
        if not ditemukan:
            print("Tidak ada alat yang sedang dipinjam.")

    def tampilkan_alat_rusak(self):
        print("\n=== ALAT RUSAK ===")
        hasil = [a for a in self.peralatan.values()
                 if a.kondisi in ("rusak ringan", "rusak berat")]
        if not hasil:
            print("Tidak ada alat rusak.")
            return
        for alat in hasil:
            print(alat)

    def tampilkan_pemeliharaan(self):
        print("\n=== DAFTAR PEMELIHARAAN ===")
        if not self.pemeliharaan:
            print("Tidak ada alat dalam pemeliharaan.")
            return
        for kode, data in self.pemeliharaan.items():
            alat = self.peralatan.get(kode)
            nama = alat.nama if alat else "Nama tidak ditemukan"
            print(f"{kode} | {nama} | {data['tanggal']} | {data['catatan']}")

    def masukkan_pemeliharaan(self):
        print("\n=== MASUKKAN ALAT KE PEMELIHARAAN ===")
        kode = self._input_tidak_kosong("Kode alat: ")
        alat = self.peralatan.get(kode)
        if not alat:
            print("Alat tidak ditemukan.")
            return
        if alat.kondisi != "rusak berat":
            print("Hanya alat rusak berat yang dapat dimasukkan ke pemeliharaan.")
            return
        if any(not item.dikembalikan and item.kode_alat == kode
               for t in self.transaksi.values() for item in t.item):
            print("Alat masih tercatat dipinjam.")
            return
        catatan = input("Catatan kerusakan: ").strip() or "Perlu pemeriksaan"
        self.pemeliharaan[kode] = {
            "tanggal": date.today().isoformat(), "catatan": catatan
        }
        self._catat_log(f"Alat {kode} dimasukkan ke pemeliharaan")
        self._simpan()
        print("Alat berhasil dimasukkan ke daftar pemeliharaan.")

    def selesaikan_pemeliharaan(self):
        print("\n=== SELESAIKAN PEMELIHARAAN ===")
        kode = self._input_tidak_kosong("Kode alat: ")
        if kode not in self.pemeliharaan:
            print("Alat tidak ada dalam daftar pemeliharaan.")
            return
        konfirmasi = input("Alat sudah diperbaiki dan layak pakai? (y/t): ").lower()
        if konfirmasi != "y":
            print("Status alat tidak diubah.")
            return
        alat = self.peralatan[kode]
        alat.kondisi = "baik"
        alat.tersedia = True
        del self.pemeliharaan[kode]
        self._catat_log(f"Pemeliharaan alat {kode} selesai; alat tersedia kembali")
        self._simpan()
        print("Pemeliharaan selesai. Alat sekarang tersedia.")
