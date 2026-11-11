from ..models import Transaksi


class LayananLaporan:
    def riwayat_mahasiswa(self):
        print("\n=== RIWAYAT PEMINJAMAN MAHASISWA ===")
        nim = self._input_tidak_kosong("NIM: ")
        if nim not in self.mahasiswa:
            print("Mahasiswa tidak ditemukan.")
            return
        hasil = [t for t in self.transaksi.values() if t.nim_mahasiswa == nim]
        if not hasil:
            print("Belum memiliki riwayat peminjaman.")
            return
        for t in hasil:
            print(f"\n{t}")
            for item in t.item:
                kondisi = item.kondisi_kembali or "-"
                print(f"  - {item.kode_alat}: "
                      f"{'kembali' if item.dikembalikan else 'dipinjam'}, "
                      f"kondisi akhir: {kondisi}")

    def statistik_peminjaman(self):
        print("\n=== STATISTIK PEMINJAMAN ===")
        selesai = sum(1 for t in self.transaksi.values()
                      if t.status == Transaksi.STATUS_SELESAI)
        aktif = sum(1 for t in self.transaksi.values()
                    if t.status != Transaksi.STATUS_SELESAI)
        print(f"Jumlah transaksi selesai : {selesai}")
        print(f"Jumlah transaksi aktif   : {aktif}")
        if self.peralatan:
            paling_sering = max(self.peralatan.values(),
                                key=lambda a: a.total_dipinjam)
            print(f"Alat paling sering dipinjam: {paling_sering.nama} "
                  f"({paling_sering.total_dipinjam} kali)")
        if self.mahasiswa:
            jumlah = {nim: sum(1 for t in self.transaksi.values()
                               if t.nim_mahasiswa == nim)
                      for nim in self.mahasiswa}
            nim_top = max(jumlah, key=jumlah.get)
            print(f"Mahasiswa paling sering meminjam: "
                  f"{self.mahasiswa[nim_top].nama} ({jumlah[nim_top]} transaksi)")

    def tampilkan_log(self):
        self.log.tampilkan()
