from datetime import date
from ..models import Transaksi, Peralatan


class LayananTransaksi:
    def buat_transaksi(self):
        print("\n=== BUAT TRANSAKSI PEMINJAMAN ===")
        nim = self._input_tidak_kosong("NIM mahasiswa: ")
        mhs = self.mahasiswa.get(nim)
        if not mhs:
            print("Mahasiswa tidak ditemukan.")
            return
        if self._jumlah_transaksi_aktif(nim) >= 2:
            print("Gagal: mahasiswa sudah memiliki maksimal 2 transaksi aktif.")
            return

        kode_input = self._input_tidak_kosong("Kode alat (pisahkan dengan koma): ")
        kode_list = list(dict.fromkeys(
            kode.strip() for kode in kode_input.split(",") if kode.strip()
        ))
        if not kode_list:
            print("Daftar alat kosong.")
            return

        # Semua alat divalidasi lebih dahulu agar transaksi gagal tidak mengubah data.
        for kode in kode_list:
            alat = self._cari_alat(kode)
            if not alat:
                print(f"Gagal: alat {kode} tidak ditemukan.")
                return
            if not alat.tersedia or alat.kondisi != "baik":
                print(f"Gagal: alat {kode} sedang tidak tersedia.")
                return

        id_transaksi = f"T{self.nomor_transaksi:03d}"
        transaksi = Transaksi(id_transaksi, mhs, kode_list, date.today())
        self.transaksi[id_transaksi] = transaksi
        self.nomor_transaksi += 1

        for kode in kode_list:
            self.peralatan[kode].tersedia = False
            self.peralatan[kode].total_dipinjam += 1
        mhs.status_aktif_peminjaman = True
        self._catat_log(f"Transaksi {id_transaksi} dibuat oleh mahasiswa {nim}")
        self._simpan()
        print("Transaksi berhasil dibuat.")
        print(transaksi)

    def tampilkan_transaksi(self):
        print("\n=== DAFTAR TRANSAKSI ===")
        if not self.transaksi:
            print("Belum ada transaksi.")
            return
        for transaksi in self.transaksi.values():
            print(transaksi)
            for item in transaksi.item:
                print(f"  - {item}")

    def cari_transaksi_mahasiswa(self):
        print("\n=== CARI TRANSAKSI BERDASARKAN MAHASISWA ===")
        nim = self._input_tidak_kosong("NIM: ")
        hasil = [t for t in self.transaksi.values() if t.nim_mahasiswa == nim]
        if not hasil:
            print("Transaksi tidak ditemukan.")
            return
        for t in hasil:
            print(t)

    def proses_pengembalian(self):
        print("\n=== PENGEMBALIAN ALAT ===")
        id_transaksi = self._input_tidak_kosong("ID transaksi: ")
        transaksi = self.transaksi.get(id_transaksi)
        if not transaksi:
            print("Transaksi tidak ditemukan.")
            return
        if transaksi.status == Transaksi.STATUS_SELESAI:
            print("Transaksi sudah selesai.")
            return

        print("Alat dalam transaksi:")
        for item in transaksi.item:
            print(item)

        kode = self._input_tidak_kosong("Kode alat yang dikembalikan: ").strip()
        kondisi = self._input_tidak_kosong(
            "Kondisi [baik/rusak ringan/rusak berat]: "
        ).lower()
        if kondisi not in Peralatan.KONDISI_VALID:
            print("Kondisi tidak valid.")
            return

        berhasil, pesan = transaksi.proses_pengembalian(kode, kondisi)
        if not berhasil:
            print(pesan)
            return

        alat = self.peralatan.get(kode)
        if alat:
            alat.kondisi = kondisi
            alat.tersedia = kondisi == "baik"
            if kondisi == "rusak berat":
                print("Catatan: alat rusak berat belum tersedia. Masukkan ke menu pemeliharaan.")
        mhs = self.mahasiswa.get(transaksi.nim_mahasiswa)
        if transaksi.status == Transaksi.STATUS_SELESAI and mhs:
            mhs.status_aktif_peminjaman = self._jumlah_transaksi_aktif(mhs.nim) > 0

        self._catat_log(
            f"Alat {kode} dikembalikan dari transaksi {id_transaksi} dengan kondisi {kondisi}"
        )
        self._simpan()
        print(pesan)
        print(f"Status transaksi: {transaksi.status}")
        print("Ketersediaan alat: " +
              ("tersedia" if alat and alat.tersedia else "tidak tersedia"))
