from datetime import date
from ..models import Mahasiswa, Peralatan, Transaksi, LogAktivitas

class LayananMahasiswa:
        def tambah_mahasiswa(self):
            print("\n=== TAMBAH MAHASISWA ===")
            nim = self._input_tidak_kosong("NIM: ")
            if nim in self.mahasiswa:
                print("NIM sudah terdaftar.")
                return
            nama = self._input_tidak_kosong("Nama: ")
            hp = self._input_tidak_kosong("Nomor HP: ")
            self.mahasiswa[nim] = Mahasiswa(nim, nama, hp)
            self.log.tambah(f"Mahasiswa {nim} ditambahkan")
            print("Mahasiswa berhasil ditambahkan.")

        def edit_mahasiswa(self):
            print("\n=== EDIT MAHASISWA ===")
            nim = self._input_tidak_kosong("NIM yang akan diedit: ")
            mhs = self.mahasiswa.get(nim)
            if not mhs:
                print("Mahasiswa tidak ditemukan.")
                return
            nama = input(f"Nama [{mhs.nama}]: ").strip() or mhs.nama
            hp = input(f"Nomor HP [{mhs.no_hp}]: ").strip() or mhs.no_hp
            mhs.nama = nama
            mhs.no_hp = hp
            self.log.tambah(f"Data mahasiswa {nim} diubah")
            print("Data berhasil diubah.")

        def hapus_mahasiswa(self):
            print("\n=== HAPUS MAHASISWA ===")
            nim = self._input_tidak_kosong("NIM: ")
            if nim not in self.mahasiswa:
                print("Mahasiswa tidak ditemukan.")
                return
            if self._mahasiswa_memiliki_transaksi_aktif(nim):
                print("Gagal: mahasiswa masih memiliki transaksi aktif.")
                return
            del self.mahasiswa[nim]
            self.log.tambah(f"Mahasiswa {nim} dihapus")
            print("Mahasiswa berhasil dihapus.")

        def cari_mahasiswa(self):
            print("\n=== CARI MAHASISWA ===")
            kata = self._input_tidak_kosong("Masukkan NIM/nama: ").lower()
            hasil = [
                m for m in self.mahasiswa.values()
                if kata in m.nim.lower() or kata in m.nama.lower()
            ]
            if not hasil:
                print("Data tidak ditemukan.")
                return
            for m in hasil:
                print(m)

        def tampilkan_mahasiswa(self):
            print("\n=== DATA MAHASISWA ===")
            if not self.mahasiswa:
                print("Belum ada data.")
                return
            for m in self.mahasiswa.values():
                print(m)