# SEVIMA API Platform Python Client

Python client untuk mengakses SEVIMA API Platform menggunakan format JSON API.

## Instalasi

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Setup environment variables:
```bash
cp .env.example .env
```

3. Edit file `.env` dan isi dengan credentials Anda:
```
SEVIMA_API_KEY=your_api_key_here
SEVIMA_SECRET_KEY=your_secret_key_here
```

## Penggunaan

### Basic Usage

```python
from sevima_client import SEVIMAClient

# Initialize client (menggunakan env variables)
client = SEVIMAClient()

# Atau langsung pass credentials
client = SEVIMAClient(
    api_key="your_api_key",
    secret_key="your_secret_key"
)
```

### Contoh Penggunaan

#### 1. Autentikasi
```python
# Login dengan email dan password
login_response = client.login("email@example.com", "password")
print(login_response)
```

#### 2. Data Dosen
```python
# Get list dosen
dosen_list = client.get_dosen()

# Get detail dosen by ID
dosen_detail = client.get_dosen_by_id("123")

# Get penelitian dosen
penelitian = client.get_dosen_penelitian("123")

# Get jadwal dosen
jadwal = client.get_dosen_jadwal("123")
```

#### 3. Data Mahasiswa
```python
# Get list mahasiswa
mahasiswa_list = client.get_mahasiswa()

# Get detail mahasiswa
mahasiswa_detail = client.get_mahasiswa_by_id("123")

# Get presensi mahasiswa
presensi = client.get_presensi_mahasiswa("123")

# Get nilai mahasiswa
nilai = client.get_nilai_mahasiswa("123")
```

#### 4. Data CBT
```python
# Get list soal CBT
soal_list = client.get_soal_cbt()

# Get detail soal
soal_detail = client.get_soal_cbt_by_id("123")

# Get list ujian CBT
ujian_list = client.get_ujian_cbt()

# Get peserta ujian
peserta = client.get_peserta_ujian_cbt("ujian_id")
```

#### 5. Data Akademik
```python
# Get program studi
program_studi = client.get_program_studi()

# Get mata kuliah
mata_kuliah = client.get_mata_kuliah()

# Get kelas
kelas = client.get_kelas()

# Get jadwal
jadwal = client.get_jadwal()
```

#### 6. Data MBKM
```python
# Get mitra MBKM
mitra = client.get_mitra_mbkm()

# Get program MBKM
program = client.get_program_mbkm()

# Get peserta MBKM
peserta = client.get_peserta_mbkm()
```

#### 7. EdLink
```python
# Get bahan ajar
bahan_ajar = client.get_bahan_ajar()

# Get kelas EdLink
kelas = client.get_kelas_edlink()

# Get tugas
tugas = client.get_tugas()
```

### Advanced Usage

#### Custom Request dengan Query Parameters
```python
# Beberapa endpoint mendukung query parameters
dosen_list = client.get_dosen(params={
    "page": 1,
    "per_page": 10,
    "filter": "aktif"
})
```

#### Direct API Call
Jika endpoint belum tersedia di method helper, Anda bisa menggunakan method langsung:

```python
# GET request
response = client.get("siakadcloud/v1/custom-endpoint", params={"key": "value"})

# POST request
response = client.post("siakadcloud/v1/custom-endpoint", json={"data": "value"})

# PUT request
response = client.put("siakadcloud/v1/custom-endpoint", json={"data": "value"})

# DELETE request
response = client.delete("siakadcloud/v1/custom-endpoint")
```

## Error Handling

```python
from sevima_client import SEVIMAClient
import requests

client = SEVIMAClient()

try:
    response = client.get_dosen()
except requests.HTTPError as e:
    print(f"HTTP Error: {e}")
    print(f"Response: {e.response.text}")
except Exception as e:
    print(f"Error: {e}")
```

## Available Methods

Client ini menyediakan method untuk semua endpoint yang ada di SEVIMA API Platform:

### Autentikasi
- `login(email, password)`

### Data CBT
- `get_soal_cbt()`, `get_soal_cbt_by_id(id)`
- `get_bank_soal_cbt()`, `get_bank_soal_cbt_by_id(id)`
- `get_ujian_cbt()`, `get_ujian_cbt_by_id(id)`
- `get_jadwal_ujian_cbt()`, `get_peserta_ujian_cbt()`
- Dan lainnya...

### Data Kepegawaian
- `get_pegawai()`, `get_pegawai_by_id(id)`
- `get_dosen()`, `get_dosen_by_id(id)`
- `get_dosen_penelitian(id)`, `get_dosen_pengabdian(id)`
- Dan lainnya...

### Data Mahasiswa
- `get_mahasiswa()`, `get_mahasiswa_by_id(id)`
- `get_presensi_mahasiswa(id)`, `get_nilai_mahasiswa(id)`
- `get_pendaftar()`, `get_pendaftar_by_id(id)`
- Dan lainnya...

### Data Akademik
- `get_program_studi()`, `get_mata_kuliah()`
- `get_kelas()`, `get_jadwal()`
- `get_cpmk()`
- Dan lainnya...

### Data MBKM
- `get_mitra_mbkm()`, `get_program_mbkm()`
- `get_peserta_mbkm()`
- Dan lainnya...

### EdLink
- `get_bahan_ajar()`, `get_kelas_edlink()`
- `get_tugas()`, `get_soal_edlink()`
- Dan lainnya...

### Data Keuangan
- `get_invoice()`, `get_pembayaran()`

Lihat file `sevima_client.py` untuk daftar lengkap semua method yang tersedia.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SEVIMA_API_KEY` | Yes | API Key untuk autentikasi |
| `SEVIMA_SECRET_KEY` | Yes | Secret Key untuk autentikasi |
| `SEVIMA_BASE_URL` | No | Base URL API (default: https://api.sevimaplatform.com) |

## License

MIT
