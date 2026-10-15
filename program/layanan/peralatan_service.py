from datetime import date
from ..models import Mahasiswa, Peralatan, Transaksi, LogAktivitas

class LayananPeralatan:
        def tambah_peralatan(self):
            print("\n=== TAMBAH PERALATAN ===")
            kode = self._input_tidak_kosong("Kode alat: ")
            if kode in self.peralatan:
                print("Kode alat sudah terdaftar.")
                return
            nama = self._input_tidak_kosong("Nama alat: ")
            kategori = self._input_tidak_kosong("Kategori: ")
            kondisi = input("Kondisi [baik]: ").strip().lower() or "baik"
            if kondisi not in Peralatan.KONDISI_VALID:
                print("Kondisi tidak valid.")
                return
            self.peralatan[kode] = Peralatan(kode, nama, kategori, kondisi)
            self.log.tambah(f"Alat {kode} ditambahkan")
            print("Alat berhasil ditambahkan.")

        def edit_peralatan(self):
            print("\n=== EDIT PERALATAN ===")
            kode = self._input_tidak_kosong("Kode alat: ")
            alat = self.peralatan.get(kode)
            if not alat:
                print("Alat tidak ditemukan.")
                return

            # Alat yang sedang berada dalam transaksi aktif tidak boleh diubah
            # menjadi tersedia secara manual.
            nama = input(f"Nama [{alat.nama}]: ").strip() or alat.nama
            kategori = input(f"Kategori [{alat.kategori}]: ").strip() or alat.kategori

            alat.nama = nama
            alat.kategori = kategori
            self.log.tambah(f"Data alat {kode} diubah")
            print("Data berhasil diubah.")

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
            self.log.tambah(f"Alat {kode} dihapus")
            print("Alat berhasil dihapus.")

        def cari_peralatan(self):
            print("\n=== CARI PERALATAN ===")
            kata = self._input_tidak_kosong(
                "Masukkan kode/nama/kategori: "
            ).lower()

            hasil = [
                alat for alat in self.peralatan.values()
                if kata in alat.kode.lower()
                or kata in alat.nama.lower()
                or kata in alat.kategori.lower()
            ]

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
                            print(
                                f"{alat.kode} | {alat.nama} | "
                                f"Transaksi: {transaksi.id_transaksi} | "
                                f"NIM: {transaksi.nim_mahasiswa}"
                            )
                            ditemukan = True
            if not ditemukan:
                print("Tidak ada alat yang sedang dipinjam.")

        def tampilkan_alat_rusak(self):
            print("\n=== ALAT RUSAK ===")
            hasil = [
                a for a in self.peralatan.values()
                if a.kondisi in ("rusak ringan", "rusak berat")
            ]
            if not hasil:
                print("Tidak ada alat rusak.")
                return
            for alat in hasil:
                print(alat)

