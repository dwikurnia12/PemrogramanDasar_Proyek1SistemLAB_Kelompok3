# Sistem Pengelolaan Peminjaman Peralatan Laboratorium

Aplikasi berbasis Python untuk mengelola data mahasiswa, data peralatan laboratorium, transaksi peminjaman, serta pengembalian peralatan. Aplikasi ini dikembangkan menggunakan pendekatan **Object-Oriented Programming (OOP)** dengan memanfaatkan struktur data bawaan Python berupa `List` dan `Dictionary` untuk menyimpan serta mengelola data selama program berjalan.

Proyek ini dibuat untuk memenuhi tugas **Proyek I Praktikum Pemrograman Dasar**.

## 📌 Deskripsi Proyek

Proses pencatatan peminjaman peralatan laboratorium secara manual dapat menyebabkan berbagai permasalahan, seperti kesulitan memantau ketersediaan alat, melacak riwayat peminjaman, mencatat pengembalian, dan mengetahui kondisi peralatan setelah digunakan.

Oleh karena itu, dikembangkan aplikasi Sistem Pengelolaan Peminjaman Peralatan Laboratorium yang membantu mengelola proses tersebut secara terstruktur melalui program Python.

Aplikasi ini dirancang untuk mempermudah pengelolaan data mahasiswa, peralatan, transaksi peminjaman, pengembalian alat, dan riwayat aktivitas dalam satu sistem.

## 🎯 Tujuan

- Menerapkan konsep Object-Oriented Programming (OOP) menggunakan Python.
- Mengimplementasikan hubungan antarclass sesuai rancangan UML Class Diagram.
- Menggunakan List dan Dictionary untuk pengelolaan data dinamis.
- Menerapkan operasi CRUD (*Create, Read, Update, Delete*) pada data yang dikelola.
- Mengelola transaksi peminjaman dan pengembalian peralatan laboratorium.
- Mengembangkan program secara terstruktur dan kolaboratif menggunakan GitHub.

## ✨ Fitur Aplikasi

Aplikasi Sistem Pengelolaan Peminjaman Peralatan Laboratorium menyediakan menu interaktif berbasis terminal yang terdiri dari 12 fitur utama dan satu opsi untuk keluar dari program.

1. Kelola Data Mahasiswa — menambahkan, mengedit, menghapus, dan mencari data mahasiswa.
2. Kelola Data Alat — mengelola data peralatan laboratorium.
3. Buat Transaksi Peminjaman — mencatat transaksi peminjaman peralatan oleh mahasiswa.
4. Tampilkan Transaksi — menampilkan data transaksi peminjaman.
5. Proses Pengembalian Alat — memproses pengembalian peralatan beserta kondisi alat.
6. Cari Transaksi Berdasarkan Mahasiswa — mencari transaksi berdasarkan mahasiswa yang melakukan peminjaman.
7. Tampilkan Alat yang Tersedia — menampilkan peralatan yang dapat dipinjam.
8. Tampilkan Alat yang Sedang Dipinjam — menampilkan peralatan yang masih berada dalam transaksi peminjaman aktif.
9. Tampilkan Alat yang Rusak — menampilkan peralatan yang mengalami kerusakan.
10. Tampilkan Riwayat Peminjaman Mahasiswa — melihat riwayat peminjaman berdasarkan mahasiswa.
11. Statistik Peminjaman — menampilkan informasi statistik terkait aktivitas peminjaman.
12. Tampilkan Log Aktivitas — menampilkan catatan aktivitas yang dilakukan dalam sistem.
0. Keluar — mengakhiri penggunaan aplikasi.

## 🛠️ Teknologi yang Digunakan

- **Bahasa pemrograman:** Python
- **Paradigma pemrograman:** Object-Oriented Programming (OOP)
- **Struktur data:** List dan Dictionary
- **Editor kode:** Visual Studio Code
- **Version control:** Git dan GitHub

## 📂 Struktur Folder

```text
proyek_lab/
├── program/
│   ├── layanan/
│   │   ├── laporan_service.py
│   │   ├── mahasiswa_service.py
│   │   ├── menu_service.py
│   │   ├── peralatan_service.py
│   │   ├── sistem_inti.py
│   │   └── transaksi_service.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── item_peminjaman.py
│   │   ├── log_aktivitas.py
│   │   ├── mahasiswa.py
│   │   ├── peralatan.py
│   │   └── transaksi.py
│   │
│   ├── __init__.py
│   └── sistem.py
│
├── main.py
└── README.md
```

## 🧩 Penjelasan Struktur Program

### 1. Folder `models`

Folder ini berisi class yang merepresentasikan objek dan data utama dalam sistem.

| File | Tanggung Jawab |
|---|---|
| `mahasiswa.py` | Merepresentasikan data mahasiswa, seperti NIM, nama, nomor HP, dan status peminjaman. |
| `peralatan.py` | Merepresentasikan data peralatan, termasuk kode, nama, kategori, kondisi, dan ketersediaan. |
| `transaksi.py` | Merepresentasikan transaksi peminjaman, mahasiswa peminjam, daftar alat, tanggal, dan status transaksi. |
| `item_peminjaman.py` | Menyimpan detail setiap alat dalam transaksi, termasuk informasi pengembalian. |
| `log_aktivitas.py` | Mengelola pencatatan dan penampilan log aktivitas sistem. |
| `__init__.py` | Menandai folder sebagai package Python dan dapat mengatur impor modul. |

### 2. Folder `layanan`

Folder ini berisi modul yang menangani proses bisnis dan layanan aplikasi.

| File | Tanggung Jawab |
|---|---|
| `mahasiswa_service.py` | Menangani proses pengelolaan data mahasiswa. |
| `peralatan_service.py` | Menangani proses pengelolaan data peralatan. |
| `transaksi_service.py` | Menangani proses transaksi peminjaman dan pengembalian. |
| `laporan_service.py` | Menangani penyusunan atau penampilan laporan dan statistik. |
| `menu_service.py` | Menangani menu interaktif yang digunakan pengguna. |
| `sistem_inti.py` | Mendukung koordinasi proses inti sistem sesuai implementasi program. |

### 3. File Utama

- `sistem.py` — mengelola sistem utama dan menghubungkan komponen yang dibutuhkan.
- `main.py` — menjadi titik masuk untuk menjalankan aplikasi.
- `README.md` — berisi dokumentasi proyek, struktur folder, dan petunjuk penggunaan.

## 📋 Aturan Bisnis

Sistem dirancang dengan memperhatikan aturan bisnis berikut:

1. Mahasiswa hanya dapat meminjam peralatan yang tersedia.
2. Seorang mahasiswa maksimal memiliki dua transaksi peminjaman aktif.
3. Satu transaksi dapat memuat beberapa jenis peralatan.
4. Pengembalian alat dapat dilakukan secara bertahap atau sebagian.
5. Transaksi tetap aktif sampai seluruh alat dalam transaksi dikembalikan.
6. Peralatan yang rusak tidak langsung dihitung sebagai stok yang tersedia.
7. Data mahasiswa tidak dapat dihapus selama masih memiliki transaksi peminjaman aktif.
8. Data peralatan tidak dapat dihapus selama masih tercatat dalam transaksi peminjaman aktif.

## 🏗️ Perancangan Sistem

Sistem dirancang menggunakan UML Class Diagram untuk menggambarkan class, atribut, method, dan hubungan antarclass.
Class utama yang digunakan meliputi:
- `Mahasiswa`
- `Peralatan`
- `Transaksi`
- `ItemPeminjaman`
- `LogAktivitas`
- `SistemLaboratorium`

Rancangan tersebut menjadi dasar pembagian tanggung jawab setiap class dan implementasi program menggunakan Python.

## 👥 Anggota Kelompok dan Kontribusi
Proyek Sistem Pengelolaan Peminjaman Peralatan Laboratorium dikembangkan secara kolaboratif oleh empat anggota kelompok. Setiap anggota bertanggung jawab pada modul tertentu sesuai pembagian tugas yang telah disepakati.

| No. | Nama Anggota | Kontribusi |
|---|---|---|
| 1. | Farradila Sari | transaksi.py, transaksi_service.py, sistem.py, pengujian program, dan dokumentasi. |
| 2. | Arindya Aulia W | mahasiswa.py dan mahasiswa_service.py untuk pengelolaan data mahasiswa. |
| 3. | Dwi Kurniawati H| peralatan.py dan peralatan_service.py untuk pengelolaan data peralatan laboratorium. |
| 4. | Niceforus Helas N | log_aktivitas.py dan laporan_service.py untuk pencatatan aktivitas dan penyusunan laporan. |

## 🧪 Pengujian Program

Pengujian dilakukan untuk memastikan fitur utama sistem berjalan sesuai kebutuhan, antara lain:

1. Menambahkan data mahasiswa dan peralatan.
2. Membuat transaksi peminjaman beberapa alat sekaligus.
3. Memastikan sistem menolak peminjaman alat yang tidak tersedia.
4. Memproses pengembalian sebagian alat.
5. Memeriksa perubahan status dan kondisi peralatan setelah pengembalian.
6. Memastikan mahasiswa dengan transaksi aktif tidak dapat dihapus.




