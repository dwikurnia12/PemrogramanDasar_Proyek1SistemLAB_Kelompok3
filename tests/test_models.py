import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "program"))

from models import Mahasiswa, Peralatan, ItemPeminjaman, Transaksi, LogAktivitas
from datetime import date, timedelta


def test_mahasiswa_creation():
    m = Mahasiswa("M001", "Test User", "081234567890")
    assert m.nim == "M001"
    assert m.nama == "Test User"
    assert m.no_hp == "081234567890"
    assert m.status_aktif_peminjaman == False


def test_mahasiswa_with_active_status():
    m = Mahasiswa("M002", "Active User", "081234567891", True)
    assert m.status_aktif_peminjaman == True


def test_peralatan_creation():
    p = Peralatan("A001", "Laptop", "Komputer")
    assert p.kode == "A001"
    assert p.nama == "Laptop"
    assert p.kategori == "Komputer"
    assert p.kondisi == "baik"
    assert p.tersedia == True
    assert p.total_dipinjam == 0


def test_peralatan_custom_kondisi():
    p = Peralatan("A002", "Mouse", "Aksesoris", "rusak ringan", False, 5)
    assert p.kondisi == "rusak ringan"
    assert p.tersedia == False
    assert p.total_dipinjam == 5


def test_item_peminjaman_creation():
    item = ItemPeminjaman("A001")
    assert item.kode_alat == "A001"
    assert item.dikembalikan == False
    assert item.tanggal_kembali is None
    assert item.kondisi_kembali is None


def test_item_peminjaman_returned():
    item = ItemPeminjaman("A001", True, date.today(), "baik")
    assert item.dikembalikan == True
    assert item.kondisi_kembali == "baik"


def test_transaksi_creation():
    m = Mahasiswa("M001", "Test", "081234567890")
    t = Transaksi("T001", m, ["A001", "A002"], date.today())
    assert t.id_transaksi == "T001"
    assert t.nim_mahasiswa == "M001"
    assert len(t.item) == 2
    assert t.status == Transaksi.STATUS_DIPINJAM


def test_transaksi_proses_pengembalian():
    m = Mahasiswa("M001", "Test", "081234567890")
    t = Transaksi("T001", m, ["A001", "A002"], date.today())
    
    success, msg = t.proses_pengembalian("A001", "baik")
    assert success == True
    assert t.status == Transaksi.STATUS_SEBAGIAN
    
    success, msg = t.proses_pengembalian("A002", "rusak ringan")
    assert success == True
    assert t.status == Transaksi.STATUS_SELESAI


def test_transaksi_alat_belum_kembali():
    m = Mahasiswa("M001", "Test", "081234567890")
    t = Transaksi("T001", m, ["A001", "A002"], date.today())
    
    t.proses_pengembalian("A001", "baik")
    belum = t.alat_belum_kembali()
    assert len(belum) == 1
    assert belum[0].kode_alat == "A002"


def test_log_aktivitas():
    log = LogAktivitas()
    log.tambah("Test log message")
    assert len(log.logs) == 1
    assert "Test log message" in log.logs[0]


if __name__ == "__main__":  # pragma: no cover
    test_mahasiswa_creation()
    test_mahasiswa_with_active_status()
    test_peralatan_creation()
    test_peralatan_custom_kondisi()
    test_item_peminjaman_creation()
    test_item_peminjaman_returned()
    test_transaksi_creation()
    test_transaksi_proses_pengembalian()
    test_transaksi_alat_belum_kembali()
    test_log_aktivitas()
    print("All tests passed!")
