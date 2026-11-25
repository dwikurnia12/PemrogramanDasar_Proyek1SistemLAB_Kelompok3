import os
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from ..models import Mahasiswa, Peralatan, ItemPeminjaman, Transaksi, LogAktivitas


class MahasiswaRepository(ABC):
    @abstractmethod
    def get_all(self) -> Dict[str, Mahasiswa]:
        pass

    @abstractmethod
    def get_by_nim(self, nim: str) -> Optional[Mahasiswa]:
        pass

    @abstractmethod
    def save(self, mahasiswa: Mahasiswa) -> bool:
        pass

    @abstractmethod
    def delete(self, nim: str) -> bool:
        pass

    @abstractmethod
    def search(self, keyword: str) -> List[Mahasiswa]:
        pass

    @abstractmethod
    def exists(self, nim: str) -> bool:
        pass


class PeralatanRepository(ABC):
    @abstractmethod
    def get_all(self) -> Dict[str, Peralatan]:
        pass

    @abstractmethod
    def get_by_kode(self, kode: str) -> Optional[Peralatan]:
        pass

    @abstractmethod
    def save(self, peralatan: Peralatan) -> bool:
        pass

    @abstractmethod
    def delete(self, kode: str) -> bool:
        pass

    @abstractmethod
    def search(self, keyword: str) -> List[Peralatan]:
        pass

    @abstractmethod
    def get_tersedia(self) -> List[Peralatan]:
        pass

    @abstractmethod
    def get_dipinjam(self) -> List[Peralatan]:
        pass

    @abstractmethod
    def get_rusak(self) -> List[Peralatan]:
        pass

    @abstractmethod
    def exists(self, kode: str) -> bool:
        pass


class TransaksiRepository(ABC):
    @abstractmethod
    def get_all(self) -> Dict[str, Transaksi]:
        pass

    @abstractmethod
    def get_by_id(self, id_transaksi: str) -> Optional[Transaksi]:
        pass

    @abstractmethod
    def get_by_mahasiswa(self, nim: str) -> List[Transaksi]:
        pass

    @abstractmethod
    def save(self, transaksi: Transaksi) -> bool:
        pass

    @abstractmethod
    def update_status(self, id_transaksi: str, status: str) -> bool:
        pass

    @abstractmethod
    def get_next_id(self) -> str:
        pass


class LogRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[str]:
        pass

    @abstractmethod
    def add(self, pesan: str) -> bool:
        pass


class PemeliharaanRepository(ABC):
    @abstractmethod
    def get_all(self) -> Dict[str, Dict[str, str]]:
        pass

    @abstractmethod
    def get_by_kode(self, kode: str) -> Optional[Dict[str, str]]:
        pass

    @abstractmethod
    def save(self, kode: str, tanggal: str, catatan: str) -> bool:
        pass

    @abstractmethod
    def delete(self, kode: str) -> bool:
        pass

    @abstractmethod
    def exists(self, kode: str) -> bool:
        pass
