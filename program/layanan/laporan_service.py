from datetime import date
from ..models import Mahasiswa, Peralatan, Transaksi, LogAktivitas

class LayananLaporan:
        def riwayat_mahasiswa(self):
            print("\n=== RIWAYAT PEMINJAMAN MAHASISWA ===")
            nim = self._input_tidak_kosong("NIM: ")
            if nim not in self.mahasiswa:
                print("Mahasiswa tidak ditemukan.")
                return

            hasil = [
                t for t in self.transaksi.values()
                if t.nim_mahasiswa == nim
            ]
            if not hasil:
                print("Belum memiliki riwayat peminjaman.")
                return

            for t in hasil:
                print(f"\n{t}")
                for item in t.item:
                    kondisi = item.kondisi_kembali or "-"
                    print(
                        f"  - {item.kode_alat}: "
                        f"{'kembali' if item.dikembalikan else 'dipinjam'}, "
                        f"kondisi akhir: {kondisi}"
                    )

        def statistik_peminjaman(self):
            print("\n=== STATISTIK PEMINJAMAN ===")

            print("\nJumlah transaksi:")
            selesai = sum(
                1 for t in self.transaksi.values()
                if t.status == Transaksi.STATUS_SELESAI
            )
            aktif = sum(
                1 for t in self.transaksi.values()
                if t.status != Transaksi.STATUS_SELESAI
            )
            print(f"- Selesai : {selesai}")
            print(f"- Aktif   : {aktif}")

            if self.peralatan:
                alat_tersering = max(
                    self.peralatan.values(),
                    key=lambda a: a.total_dipinjam
                )
                print(
                    f"\nAlat paling sering dipinjam: "
                    f"{alat_tersering.nama} ({alat_tersering.total_dipinjam} kali)"
                )

            if self.mahasiswa:
                hitung = {
                    nim: sum(1 for t in self.transaksi.values()
                             if t.nim_mahasiswa == nim)
                    for nim in self.mahasiswa
                }
                if hitung:
                    nim_terbanyak = max(hitung, key=hitung.get)
                    print(
                        f"Mahasiswa paling sering meminjam: "
                        f"{self.mahasiswa[nim_terbanyak].nama} "
                        f"({hitung[nim_terbanyak]} transaksi)"
                    )

        def tampilkan_log(self):
            self.log.tampilkan()

