# Tugas 4 - Otomasi Pengujian OrangeHRM dengan Selenium WebDriver

Proyek ini berisi tes otomatis untuk aplikasi demo [OrangeHRM](https://opensource-demo.orangehrmlive.com) menggunakan Python, Selenium WebDriver, dan pytest. Proyek mencakup skalabilitas kode, eksekusi paralel dengan Selenium Grid, integrasi CI/CD dengan GitHub Actions, dan laporan HTML.

- **Mata kuliah:** Software Testing and Quality Assurance (STQA)
- **Nama:** <Shabrina Zahrah Ramadhani>
- **NIM:** <H071241045>

## Ringkasan

| Aspek | Penerapan |
|---|---|
| Skalabilitas | Konfigurasi terpusat di `config.py`, fixture bersama di `conftest.py`, tes `parametrize` untuk banyak menu |
| Eksekusi paralel | `pytest-xdist` (`-n`) dan Selenium Grid |
| CI/CD | GitHub Actions (`.github/workflows/tests.yml`) |
| Pelaporan | `pytest-html` dengan screenshot pada setiap tes |

## Struktur Proyek

```
Tugas4_Selenium/
├── .github/workflows/tests.yml   # pipeline CI
├── config.py                     # BASE_URL, USERNAME, PASSWORD
├── conftest.py                   # fixture driver, wait, logged_in, dan hook laporan
├── test_login.py                 # login valid, login invalid, logout
├── test_admin.py                 # cari user, tambah job title
├── test_modules.py               # buka halaman berbagai menu (parametrize)
├── requirements.txt
└── .gitignore
```

Total ada 20 tes: 3 di `test_login.py`, 2 di `test_admin.py`, dan 15 di `test_modules.py`.

## Prasyarat

- Python 3.11
- Mozilla Firefox
- Java (hanya untuk menjalankan Selenium Grid)
- Git

## Instalasi

```bash
git clone https://github.com/<Shabrinazahrahramadhani>/tugas4-selenium.git
cd tugas4-selenium
python -m venv venv
venv\Scripts\activate          
pip install -r requirements.txt
```

## Menjalankan Tes

### 1. Lokal (satu per satu)

```bash
pytest -v
```

Firefox akan terbuka dan menjalankan tiap tes secara berurutan.

### 2. Paralel dengan pytest-xdist

```bash
pytest -v -n 4
```

Angka setelah `-n` adalah jumlah worker.

### 3. Mode headless

Tanpa jendela browser, cocok untuk server atau CI.

```bash
set HEADLESS=1                 
pytest -v
```

### 4. Paralel dengan Selenium Grid

Unduh `selenium-server-<versi>.jar` dari [halaman rilis Selenium](https://github.com/SeleniumHQ/selenium/releases) dengan versi yang sama dengan paket Python `selenium`. Cek versinya dengan `pip show selenium`. File jar tidak disertakan di repo.

**Terminal 1:** jalankan Grid.

```bash
java -jar selenium-server-4.51.0.jar standalone
```

Antarmuka Grid dapat dibuka di `http://localhost:4444/ui/`.

**Terminal 2:** jalankan tes lewat Grid.

```bash
set GRID_URL=http://localhost:4444
pytest -v -n 4 --html=report.html --self-contained-html
```

Untuk kembali ke mode lokal, kosongkan variabelnya dengan `set GRID_URL=`.

### Variabel lingkungan

| Variabel | Fungsi |
|---|---|
| `HEADLESS=1` | Jalankan Firefox tanpa tampilan |
| `GRID_URL` | Alamat Selenium Grid. Jika diisi, tes memakai `webdriver.Remote` |

## Laporan HTML

```bash
pytest -v --html=report.html --self-contained-html
```

Buka `report.html` di browser. Laporan memuat hasil tiap tes beserta screenshot yang diambil otomatis oleh hook di `conftest.py`.

## CI/CD (GitHub Actions)

Workflow `.github/workflows/tests.yml` berjalan setiap kali ada push ke branch `main`, atau secara manual lewat tombol **Run workflow**. Langkahnya:

1. Checkout kode
2. Menyiapkan Python 3.11
3. Memasang dependensi dari `requirements.txt`
4. Menjalankan `pytest -v -n 2` dalam mode headless
5. Mengunggah `report.html` sebagai artifact bernama `laporan-pengujian`

Hasil run dapat dilihat di tab **Actions** pada repo, dan laporan diunduh dari bagian **Artifacts** di halaman run.

## Hasil Eksekusi

| Skenario | Hasil | Waktu |
|---|---|---|
| Lokal, berurutan (`pytest -v`) | 20 lulus | 8 menit 24 detik |
| Selenium Grid, 4 worker (`-n 4`) | 20 lulus | 2 menit 9 detik |
| GitHub Actions, headless, 2 worker | 20 lulus | 2 menit 43 detik |

Eksekusi paralel dengan Grid mempercepat waktu total sekitar 3,9 kali dibanding eksekusi berurutan.

## Catatan

- Aplikasi demo OrangeHRM bersifat publik dan dipakai banyak orang. Datanya bisa direset dan kecepatannya bisa berubah, sehingga tes sesekali dapat gagal tanpa ada masalah di kode. Jalankan ulang untuk memastikan.
- Tes yang menulis data (misalnya menambah job title) memakai nama yang dibuat unik pada setiap run.
- Kredensial yang dipakai adalah akun demo publik bawaan OrangeHRM, bukan data pribadi.