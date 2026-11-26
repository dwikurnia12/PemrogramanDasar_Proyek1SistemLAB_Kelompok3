class LayananMenu:
    def jalankan(self):
        while True:
            print("\n" + "=" * 60)
            print(" SISTEM PENGELOLAAN PEMINJAMAN PERALATAN LABORATORIUM")
            print("=" * 60)
            print("1. Kelola data mahasiswa")
            print("2. Kelola data alat")
            print("3. Buat transaksi peminjaman")
            print("4. Tampilkan transaksi")
            print("5. Proses pengembalian alat")
            print("6. Cari transaksi berdasarkan mahasiswa")
            print("7. Tampilkan alat yang tersedia")
            print("8. Tampilkan alat yang sedang dipinjam")
            print("9. Tampilkan alat yang rusak")
            print("10. Tampilkan riwayat peminjaman mahasiswa")
            print("11. Statistik peminjaman")
            print("12. Tampilkan log aktivitas")
            print("13. Menu pemeliharaan alat")
            print("0. Keluar")
            pilihan = input("Pilih menu: ").strip()

            if pilihan == "1":
                self.menu_mahasiswa()
            elif pilihan == "2":
                self.menu_peralatan()
            elif pilihan == "3":
                self.buat_transaksi()
                self._pause()
            elif pilihan == "4":
                self.tampilkan_transaksi()
                self._pause()
            elif pilihan == "5":
                self.proses_pengembalian()
                self._pause()
            elif pilihan == "6":
                self.cari_transaksi_mahasiswa()
                self._pause()
            elif pilihan == "7":
                self.tampilkan_alat_tersedia()
                self._pause()
            elif pilihan == "8":
                self.tampilkan_alat_dipinjam()
                self._pause()
            elif pilihan == "9":
                self.tampilkan_alat_rusak()
                self._pause()
            elif pilihan == "10":
                self.riwayat_mahasiswa()
                self._pause()
            elif pilihan == "11":
                self.statistik_peminjaman()
                self._pause()
            elif pilihan == "12":
                self.tampilkan_log()
                self._pause()
            elif pilihan == "13":
                self.menu_pemeliharaan()
            elif pilihan == "0":
                self._simpan()
                print("Seluruh data disimpan. Terima kasih.")
                break
            else:
                print("Pilihan tidak valid.")

    def menu_mahasiswa(self):
        while True:
            print("\n--- KELOLA MAHASISWA ---")
            print("1. Tampilkan semua")
            print("2. Tambah")
            print("3. Edit")
            print("4. Hapus")
            print("5. Cari")
            print("0. Kembali")
            p = input("Pilih: ").strip()
            if p == "1": self.tampilkan_mahasiswa()
            elif p == "2": self.tambah_mahasiswa()
            elif p == "3": self.edit_mahasiswa()
            elif p == "4": self.hapus_mahasiswa()
            elif p == "5": self.cari_mahasiswa()
            elif p == "0": break
            else: print("Pilihan tidak valid.")
            self._pause()

    def menu_peralatan(self):
        while True:
            print("\n--- KELOLA ALAT ---")
            print("1. Tampilkan semua")
            print("2. Tambah")
            print("3. Edit nama/kategori")
            print("4. Hapus")
            print("5. Cari kode/nama/kategori")
            print("0. Kembali")
            p = input("Pilih: ").strip()
            if p == "1":
                for alat in self.peralatan.values(): print(alat)
            elif p == "2": self.tambah_peralatan()
            elif p == "3": self.edit_peralatan()
            elif p == "4": self.hapus_peralatan()
            elif p == "5": self.cari_peralatan()
            elif p == "0": break
            else: print("Pilihan tidak valid.")
            self._pause()

    def menu_pemeliharaan(self):
        while True:
            print("\n--- PEMELIHARAAN ALAT ---")
            print("1. Lihat daftar pemeliharaan")
            print("2. Masukkan alat rusak berat")
            print("3. Tandai selesai diperbaiki")
            print("0. Kembali")
            p = input("Pilih: ").strip()
            if p == "1": self.tampilkan_pemeliharaan()
            elif p == "2": self.masukkan_pemeliharaan()
            elif p == "3": self.selesaikan_pemeliharaan()
            elif p == "0": break
            else: print("Pilihan tidak valid.")
            self._pause()
