from pathlib import Path
from datetime import date
from ..models import Mahasiswa, Peralatan, ItemPeminjaman, Transaksi, LogAktivitas

class LayananFile:
    """Satu tempat untuk seluruh proses baca/tulis text file."""

    NAMA_FILE = (
        "mahasiswa.txt", "alat.txt", "transaksi.txt",
        "detail_transaksi.txt", "pemeliharaan.txt", "log.txt"
    )

    def __init__(self, folder_data):
        self.folder_data = Path(folder_data)
        self.folder_data.mkdir(parents=True, exist_ok=True)
        for nama in self.NAMA_FILE:
            path = self.folder_data / nama
            if not path.exists():
                try:
                    with open(path, "w", encoding="utf-8") as file:
                        pass
                except OSError as error:
                    print(f"Peringatan: gagal membuat {nama}: {error}")

    def _baca_baris(self, nama_file, jumlah_kolom):
        path = self.folder_data / nama_file
        hasil = []
        try:
            with open(path, "r", encoding="utf-8") as file:
                for nomor, baris in enumerate(file, start=1):
                    baris = baris.rstrip("\n")
                    if not baris:
                        continue
                    kolom = baris.split("|")
                    if len(kolom) != jumlah_kolom:
                        print(f"Peringatan: {nama_file} baris {nomor} dilewati (format salah).")
                        continue
                    hasil.append(kolom)
        except FileNotFoundError:
            try:
                with open(path, "w", encoding="utf-8") as file:
                    pass
            except OSError as error:
                print(f"Peringatan: gagal membuat {nama_file}: {error}")
        except OSError as error:
            print(f"Peringatan: gagal membaca {nama_file}: {error}")
        return hasil

    def _tulis_baris(self, nama_file, baris_data):
        path = self.folder_data / nama_file
        try:
            with open(path, "w", encoding="utf-8") as file:
                for kolom in baris_data:
                    file.write("|".join(str(nilai) for nilai in kolom) + "\n")
            return True
        except OSError as error:
            print(f"Gagal menyimpan {nama_file}: {error}")
            return False

    def tambah_log(self, pesan):
        from datetime import datetime
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M")
        path = self.folder_data / "log.txt"
        try:
            with open(path, "a", encoding="utf-8") as file:
                file.write(f"[{waktu}] {pesan}\n")
            return True
        except OSError as error:
            print(f"Gagal menulis log: {error}")
            return False

    def muat_semua(self, sistem):
        sistem.mahasiswa.clear()
        sistem.peralatan.clear()
        sistem.transaksi.clear()
        sistem.pemeliharaan.clear()
        sistem.log.logs = []

        for nim, nama, hp, aktif in self._baca_baris("mahasiswa.txt", 4):
            if nim in sistem.mahasiswa:
                print(f"Peringatan: NIM duplikat {nim}, baris dilewati.")
                continue
            sistem.mahasiswa[nim] = Mahasiswa(nim, nama, hp, aktif == "aktif")

        for kode, nama, kategori, kondisi, status, total in self._baca_baris("alat.txt", 6):
            if kode in sistem.peralatan:
                print(f"Peringatan: kode alat duplikat {kode}, baris dilewati.")
                continue
            try:
                tersedia = status == "tersedia"
                sistem.peralatan[kode] = Peralatan(
                    kode, nama, kategori, kondisi, tersedia, int(total)
                )
            except ValueError:
                print(f"Peringatan: data alat {kode} tidak valid, baris dilewati.")

        data_transaksi = self._baca_baris("transaksi.txt", 5)
        detail = {}
        for id_transaksi, kode, status_item, kondisi, tgl_kembali in self._baca_baris(
            "detail_transaksi.txt", 5
        ):
            detail.setdefault(id_transaksi, []).append(
                (kode, status_item, kondisi, tgl_kembali)
            )

        for id_tr, nim, tgl_pinjam, batas, status in data_transaksi:
            if id_tr in sistem.transaksi or nim not in sistem.mahasiswa:
                print(f"Peringatan: transaksi {id_tr} duplikat atau NIM tidak ditemukan.")
                continue
            try:
                tanggal = date.fromisoformat(tgl_pinjam)
                batas_tanggal = date.fromisoformat(batas)
                daftar_item = []
                valid = True
                for kode, status_item, kondisi, tgl_kembali in detail.get(id_tr, []):
                    if kode not in sistem.peralatan:
                        valid = False
                        break
                    kembali = status_item == "dikembalikan"
                    tgl = date.fromisoformat(tgl_kembali) if tgl_kembali != "-" else None
                    daftar_item.append(ItemPeminjaman(
                        kode, kembali, tgl, None if kondisi == "-" else kondisi
                    ))
                if not valid or not daftar_item:
                    print(f"Peringatan: detail transaksi {id_tr} tidak valid.")
                    continue
                sistem.transaksi[id_tr] = Transaksi(
                    id_tr, nim, [], tanggal, batas_tanggal, status, daftar_item
                )
            except ValueError:
                print(f"Peringatan: tanggal transaksi {id_tr} tidak valid.")

        for kode, tanggal, catatan in self._baca_baris("pemeliharaan.txt", 3):
            if kode in sistem.peralatan:
                sistem.pemeliharaan[kode] = {
                    "tanggal": tanggal, "catatan": catatan
                }

        path_log = self.folder_data / "log.txt"
        try:
            with open(path_log, "r", encoding="utf-8") as file:
                sistem.log.logs = [baris.rstrip("\n") for baris in file if baris.strip()]
        except OSError as error:
            print(f"Peringatan: gagal membaca log: {error}")

        # Hitung ulang status aktif mahasiswa berdasarkan transaksi yang dimuat.
        for mhs in sistem.mahasiswa.values():
            mhs.status_aktif_peminjaman = any(
                t.nim_mahasiswa == mhs.nim
                and t.status != Transaksi.STATUS_SELESAI
                for t in sistem.transaksi.values()
            )

        # Nomor transaksi berikutnya ditentukan dari ID terbesar agar tidak duplikat.
        angka = []
        for id_tr in sistem.transaksi:
            try:
                angka.append(int(id_tr[1:]))
            except ValueError:
                continue
        sistem.nomor_transaksi = max(angka, default=0) + 1

    def simpan_semua(self, sistem):
        mahasiswa = [
            [m.nim, m.nama, m.no_hp,
             "aktif" if m.status_aktif_peminjaman else "tidak aktif"]
            for m in sistem.mahasiswa.values()
        ]
        alat = [
            [a.kode, a.nama, a.kategori, a.kondisi,
             "tersedia" if a.tersedia else "tidak tersedia",
             a.total_dipinjam]
            for a in sistem.peralatan.values()
        ]
        transaksi = [
            [t.id_transaksi, t.nim_mahasiswa, t.tanggal_peminjaman.isoformat(),
             t.batas_pengembalian.isoformat(), t.status]
            for t in sistem.transaksi.values()
        ]
        detail = []
        for t in sistem.transaksi.values():
            for item in t.item:
                detail.append([
                    t.id_transaksi, item.kode_alat,
                    "dikembalikan" if item.dikembalikan else "dipinjam",
                    item.kondisi_kembali or "-",
                    item.tanggal_kembali.isoformat() if item.tanggal_kembali else "-"
                ])
        pemeliharaan = [
            [kode, data["tanggal"], data["catatan"]]
            for kode, data in sistem.pemeliharaan.items()
        ]

        berhasil = True
        berhasil = self._tulis_baris("mahasiswa.txt", mahasiswa) and berhasil
        berhasil = self._tulis_baris("alat.txt", alat) and berhasil
        berhasil = self._tulis_baris("transaksi.txt", transaksi) and berhasil
        berhasil = self._tulis_baris("detail_transaksi.txt", detail) and berhasil
        berhasil = self._tulis_baris("pemeliharaan.txt", pemeliharaan) and berhasil
        return berhasil
