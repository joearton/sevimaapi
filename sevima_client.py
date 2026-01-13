"""
SEVIMA API Platform Python Client

Client untuk mengakses SEVIMA API Platform menggunakan format JSON API.
"""

import os
import requests
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class SEVIMAClient:
    """Client untuk mengakses SEVIMA API Platform"""
    
    BASE_URL = "https://api.sevimaplatform.com"
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        base_url: Optional[str] = None
    ):
        """
        Initialize SEVIMA API Client
        
        Args:
            api_key: API Key (default: dari env SEVIMA_API_KEY)
            secret_key: Secret Key (default: dari env SEVIMA_SECRET_KEY)
            base_url: Base URL API (default: dari env SEVIMA_BASE_URL atau https://api.sevimaplatform.com)
        """
        self.api_key = api_key or os.getenv("SEVIMA_API_KEY")
        self.secret_key = secret_key or os.getenv("SEVIMA_SECRET_KEY")
        self.base_url = base_url or os.getenv("SEVIMA_BASE_URL") or self.BASE_URL
        
        if not self.api_key:
            raise ValueError("API Key is required. Set SEVIMA_API_KEY environment variable or pass api_key parameter.")
        if not self.secret_key:
            raise ValueError("Secret Key is required. Set SEVIMA_SECRET_KEY environment variable or pass secret_key parameter.")
        
        self.session = requests.Session()
        self._setup_headers()
    
    def _setup_headers(self):
        """Setup default headers untuk semua request"""
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-App-Key": self.api_key,
            "X-Secret-Key": self.secret_key
        })
    
    def _request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        json: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Internal method untuk melakukan HTTP request
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint path (contoh: 'siakadcloud/v1/user/login')
            params: Query parameters
            data: Form data
            json: JSON body data
            
        Returns:
            Response JSON sebagai dictionary
            
        Raises:
            requests.HTTPError: Jika request gagal
        """
        url = f"{self.base_url}/{endpoint}"
        
        response = self.session.request(
            method=method,
            url=url,
            params=params,
            data=data,
            json=json
        )
        
        response.raise_for_status()
        return response.json()
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """GET request helper"""
        return self._request("GET", endpoint, params=params)
    
    def post(self, endpoint: str, json: Optional[Dict] = None, data: Optional[Dict] = None) -> Dict[str, Any]:
        """POST request helper"""
        return self._request("POST", endpoint, json=json, data=data)
    
    def put(self, endpoint: str, json: Optional[Dict] = None) -> Dict[str, Any]:
        """PUT request helper"""
        return self._request("PUT", endpoint, json=json)
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """DELETE request helper"""
        return self._request("DELETE", endpoint)
    
    # ==================== AUTENTIKASI ====================
    
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """
        Login dengan kredensial user (SSO)
        
        Args:
            email: Email user
            password: Password user
            
        Returns:
            Response dari API login
        """
        return self.post(
            "siakadcloud/v1/user/login",
            json={"email": email, "password": password}
        )
    
    # ==================== DATA CBT ====================
    
    def get_soal_cbt(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list soal CBT"""
        return self.get("siakadcloud/v1/soal-cbt", params=params)
    
    def get_soal_cbt_by_id(self, soal_id: str) -> Dict[str, Any]:
        """Get detail soal CBT by ID"""
        return self.get(f"siakadcloud/v1/soal-cbt/{soal_id}")
    
    def get_bank_soal_cbt(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list bank soal CBT"""
        return self.get("siakadcloud/v1/bank-soal-cbt", params=params)
    
    def get_bank_soal_cbt_by_id(self, bank_id: str) -> Dict[str, Any]:
        """Get detail bank soal CBT by ID"""
        return self.get(f"siakadcloud/v1/bank-soal-cbt/{bank_id}")
    
    def get_soal_by_bank(self, bank_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get soal dari bank soal tertentu"""
        return self.get(f"siakadcloud/v1/bank-soal-cbt/{bank_id}/soal", params=params)
    
    def get_ujian_cbt(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list ujian CBT"""
        return self.get("siakadcloud/v1/ujian-cbt", params=params)
    
    def get_ujian_cbt_by_id(self, ujian_id: str) -> Dict[str, Any]:
        """Get detail ujian CBT by ID"""
        return self.get(f"siakadcloud/v1/ujian-cbt/{ujian_id}")
    
    def get_jadwal_ujian_cbt(self, ujian_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get jadwal ujian CBT"""
        return self.get(f"siakadcloud/v1/ujian-cbt/{ujian_id}/jadwal", params=params)
    
    def get_peserta_ujian_cbt(self, ujian_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get peserta ujian CBT"""
        return self.get(f"siakadcloud/v1/ujian-cbt/{ujian_id}/peserta", params=params)
    
    def get_jadwal_ujian_cbt_list(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list jadwal ujian CBT"""
        return self.get("siakadcloud/v1/jadwal-ujian-cbt", params=params)
    
    def get_jadwal_ujian_cbt_by_id(self, jadwal_id: str) -> Dict[str, Any]:
        """Get detail jadwal ujian CBT by ID"""
        return self.get(f"siakadcloud/v1/jadwal-ujian-cbt/{jadwal_id}")
    
    def get_soal_ujian_cbt(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list soal ujian CBT"""
        return self.get("siakadcloud/v1/soal-ujian-cbt", params=params)
    
    def get_soal_ujian_cbt_by_id(self, soal_id: str) -> Dict[str, Any]:
        """Get detail soal ujian CBT by ID"""
        return self.get(f"siakadcloud/v1/soal-ujian-cbt/{soal_id}")
    
    def get_peserta_ujian_cbt_list(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list peserta ujian CBT"""
        return self.get("siakadcloud/v1/peserta-ujian-cbt", params=params)
    
    def get_peserta_ujian_cbt_by_id(self, peserta_id: str) -> Dict[str, Any]:
        """Get detail peserta ujian CBT by ID"""
        return self.get(f"siakadcloud/v1/peserta-ujian-cbt/{peserta_id}")
    
    def get_jawaban_peserta_ujian_cbt(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list jawaban peserta ujian CBT"""
        return self.get("siakadcloud/v1/jawaban-peserta-ujian-cbt", params=params)
    
    def get_jawaban_peserta_ujian_cbt_by_id(self, jawaban_id: str) -> Dict[str, Any]:
        """Get detail jawaban peserta ujian CBT by ID"""
        return self.get(f"siakadcloud/v1/jawaban-peserta-ujian-cbt/{jawaban_id}")
    
    # ==================== DATA KEPEGAWAIAN ====================
    
    def get_pegawai(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list pegawai"""
        return self.get("siakadcloud/v1/pegawai", params=params)
    
    def get_pegawai_by_id(self, pegawai_id: str) -> Dict[str, Any]:
        """Get detail pegawai by ID"""
        return self.get(f"siakadcloud/v1/pegawai/{pegawai_id}")
    
    def get_pegawai_cuti(self, pegawai_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get cuti pegawai"""
        return self.get(f"siakadcloud/v1/pegawai/{pegawai_id}/cuti", params=params)
    
    def get_pegawai_izin(self, pegawai_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get izin pegawai"""
        return self.get(f"siakadcloud/v1/pegawai/{pegawai_id}/izin", params=params)
    
    def get_presensi_dosen(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list presensi dosen"""
        return self.get("siakadcloud/v1/presensi-dosen", params=params)
    
    def get_presensi_dosen_by_id(self, presensi_id: str) -> Dict[str, Any]:
        """Get detail presensi dosen by ID"""
        return self.get(f"siakadcloud/v1/presensi-dosen/{presensi_id}")
    
    def get_dosen(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list dosen"""
        return self.get("siakadcloud/v1/dosen", params=params)
    
    def get_dosen_by_id(self, dosen_id: str) -> Dict[str, Any]:
        """Get detail dosen by ID"""
        return self.get(f"siakadcloud/v1/dosen/{dosen_id}")
    
    def get_dosen_penelitian(self, dosen_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get penelitian dosen"""
        return self.get(f"siakadcloud/v1/dosen/{dosen_id}/penelitian", params=params)
    
    def get_dosen_edom(self, dosen_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get evaluasi dosen oleh mahasiswa (EDOM)"""
        return self.get(f"siakadcloud/v1/dosen/{dosen_id}/edom", params=params)
    
    def get_dosen_perwalian(self, dosen_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get perwalian dosen"""
        return self.get(f"siakadcloud/v1/dosen/{dosen_id}/perwalian", params=params)
    
    def get_dosen_kelas(self, dosen_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get kelas dosen"""
        return self.get(f"siakadcloud/v1/dosen/{dosen_id}/kelas", params=params)
    
    def get_dosen_jadwal(self, dosen_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get jadwal dosen"""
        return self.get(f"siakadcloud/v1/dosen/{dosen_id}/jadwal", params=params)
    
    def get_dosen_presensi(self, dosen_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get presensi dosen"""
        return self.get(f"siakadcloud/v1/dosen/{dosen_id}/presensi-dosen", params=params)
    
    def get_dosen_pengabdian(self, dosen_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get pengabdian dosen"""
        return self.get(f"siakadcloud/v1/dosen/{dosen_id}/pengabdian", params=params)
    
    def get_dosen_cuti(self, dosen_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get cuti dosen"""
        return self.get(f"siakadcloud/v1/dosen/{dosen_id}/cuti", params=params)
    
    def get_dosen_izin(self, dosen_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get izin dosen"""
        return self.get(f"siakadcloud/v1/dosen/{dosen_id}/izin", params=params)
    
    def get_dosen_publikasi(self, dosen_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get publikasi dosen"""
        return self.get(f"siakadcloud/v1/dosen/{dosen_id}/publikasi", params=params)
    
    def get_dosen_paten(self, dosen_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get paten dosen"""
        return self.get(f"siakadcloud/v1/dosen/{dosen_id}/paten", params=params)
    
    # ==================== RIWAYAT PENELITIAN ====================
    
    def get_penelitian(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list penelitian"""
        return self.get("siakadcloud/v1/penelitian", params=params)
    
    def get_penelitian_by_id(self, penelitian_id: str) -> Dict[str, Any]:
        """Get detail penelitian by ID"""
        return self.get(f"siakadcloud/v1/penelitian/{penelitian_id}")
    
    def get_dokumen_penelitian(self, penelitian_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get dokumen penelitian"""
        return self.get(f"siakadcloud/v1/penelitian/{penelitian_id}/dokumen-penelitian", params=params)
    
    def get_dosen_penelitian_by_id(self, penelitian_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get dosen yang terlibat dalam penelitian"""
        return self.get(f"siakadcloud/v1/penelitian/{penelitian_id}/dosen", params=params)
    
    def get_paten(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list paten"""
        return self.get("siakadcloud/v1/paten", params=params)
    
    def get_paten_by_id(self, paten_id: str) -> Dict[str, Any]:
        """Get detail paten by ID"""
        return self.get(f"siakadcloud/v1/paten/{paten_id}")
    
    def get_dokumen_paten(self, paten_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get dokumen paten"""
        return self.get(f"siakadcloud/v1/paten/{paten_id}/dokumen-paten", params=params)
    
    def get_dosen_paten_by_id(self, paten_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get dosen yang terlibat dalam paten"""
        return self.get(f"siakadcloud/v1/paten/{paten_id}/dosen", params=params)
    
    def get_dokumen_paten_list(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list dokumen paten"""
        return self.get("siakadcloud/v1/dokumen-paten", params=params)
    
    def get_dokumen_paten_by_id(self, dokumen_id: str) -> Dict[str, Any]:
        """Get detail dokumen paten by ID"""
        return self.get(f"siakadcloud/v1/dokumen-paten/{dokumen_id}")
    
    def get_publikasi(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list publikasi"""
        return self.get("siakadcloud/v1/publikasi", params=params)
    
    def get_publikasi_by_id(self, publikasi_id: str) -> Dict[str, Any]:
        """Get detail publikasi by ID"""
        return self.get(f"siakadcloud/v1/publikasi/{publikasi_id}")
    
    def get_dokumen_publikasi(self, publikasi_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get dokumen publikasi"""
        return self.get(f"siakadcloud/v1/publikasi/{publikasi_id}/dokumen-publikasi", params=params)
    
    def get_dosen_publikasi_by_id(self, publikasi_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get dosen yang terlibat dalam publikasi"""
        return self.get(f"siakadcloud/v1/publikasi/{publikasi_id}/dosen", params=params)
    
    def get_dokumen_publikasi_list(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list dokumen publikasi"""
        return self.get("siakadcloud/v1/dokumen-publikasi", params=params)
    
    def get_dokumen_publikasi_by_id(self, dokumen_id: str) -> Dict[str, Any]:
        """Get detail dokumen publikasi by ID"""
        return self.get(f"siakadcloud/v1/dokumen-publikasi/{dokumen_id}")
    
    # ==================== RIWAYAT PENGABDIAN ====================
    
    def get_pengabdian(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list pengabdian"""
        return self.get("siakadcloud/v1/pengabdian", params=params)
    
    def get_pengabdian_by_id(self, pengabdian_id: str) -> Dict[str, Any]:
        """Get detail pengabdian by ID"""
        return self.get(f"siakadcloud/v1/pengabdian/{pengabdian_id}")
    
    def get_dokumen_pengabdian(self, pengabdian_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get dokumen pengabdian"""
        return self.get(f"siakadcloud/v1/pengabdian/{pengabdian_id}/dokumen-pengabdian", params=params)
    
    def get_dokumen_pengabdian_list(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list dokumen pengabdian"""
        return self.get("siakadcloud/v1/dokumen-pengabdian", params=params)
    
    def get_dokumen_pengabdian_by_id(self, dokumen_id: str) -> Dict[str, Any]:
        """Get detail dokumen pengabdian by ID"""
        return self.get(f"siakadcloud/v1/dokumen-pengabdian/{dokumen_id}")
    
    # ==================== DATA KEUANGAN ====================
    
    def get_invoice(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list invoice"""
        return self.get("siakadcloud/v1/invoice", params=params)
    
    def get_invoice_by_id(self, invoice_id: str) -> Dict[str, Any]:
        """Get detail invoice by ID"""
        return self.get(f"siakadcloud/v1/invoice/{invoice_id}")
    
    def get_pembayaran(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list pembayaran"""
        return self.get("siakadcloud/v1/pembayaran", params=params)
    
    def get_pembayaran_by_id(self, pembayaran_id: str) -> Dict[str, Any]:
        """Get detail pembayaran by ID"""
        return self.get(f"siakadcloud/v1/pembayaran/{pembayaran_id}")
    
    # ==================== DATA LAINNYA ====================
    
    def get_konsentrasi(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list konsentrasi"""
        return self.get("siakadcloud/v1/konsentrasi", params=params)
    
    def get_konsentrasi_by_id(self, konsentrasi_id: str) -> Dict[str, Any]:
        """Get detail konsentrasi by ID"""
        return self.get(f"siakadcloud/v1/konsentrasi/{konsentrasi_id}")
    
    def get_program_studi_by_konsentrasi(self, konsentrasi_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get program studi dari konsentrasi"""
        return self.get(f"siakadcloud/v1/konsentrasi/{konsentrasi_id}/program-studi", params=params)
    
    def get_berkas_syarat_pendaftar(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list berkas syarat pendaftar"""
        return self.get("siakadcloud/v1/berkas-syarat-pendaftar", params=params)
    
    def get_berkas_syarat_pendaftar_by_id(self, berkas_id: str) -> Dict[str, Any]:
        """Get detail berkas syarat pendaftar by ID"""
        return self.get(f"siakadcloud/v1/berkas-syarat-pendaftar/{berkas_id}")
    
    def get_dokumen_penelitian_list(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list dokumen penelitian"""
        return self.get("siakadcloud/v1/dokumen-penelitian", params=params)
    
    def get_dokumen_penelitian_by_id(self, dokumen_id: str) -> Dict[str, Any]:
        """Get detail dokumen penelitian by ID"""
        return self.get(f"siakadcloud/v1/dokumen-penelitian/{dokumen_id}")
    
    # ==================== EDLink ====================
    
    def get_bahan_ajar(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list bahan ajar (EdLink)"""
        return self.get("edlink/v1/bahan-ajar", params=params)
    
    def get_bahan_ajar_by_id(self, bahan_id: str) -> Dict[str, Any]:
        """Get detail bahan ajar by ID"""
        return self.get(f"edlink/v1/bahan-ajar/{bahan_id}")
    
    def get_kelas_edlink(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list kelas (EdLink)"""
        return self.get("edlink/v1/kelas", params=params)
    
    def get_kelas_edlink_by_id(self, kelas_id: str) -> Dict[str, Any]:
        """Get detail kelas by ID"""
        return self.get(f"edlink/v1/kelas/{kelas_id}")
    
    def get_sesi(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list sesi (EdLink)"""
        return self.get("edlink/v1/sesi", params=params)
    
    def get_sesi_by_id(self, sesi_id: str) -> Dict[str, Any]:
        """Get detail sesi by ID"""
        return self.get(f"edlink/v1/sesi/{sesi_id}")
    
    def get_pengajar_kelas(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list pengajar kelas (EdLink)"""
        return self.get("edlink/v1/pengajar-kelas", params=params)
    
    def get_pengajar_kelas_by_id(self, pengajar_id: str) -> Dict[str, Any]:
        """Get detail pengajar kelas by ID"""
        return self.get(f"edlink/v1/pengajar-kelas/{pengajar_id}")
    
    def get_peserta_kelas(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list peserta kelas (EdLink)"""
        return self.get("edlink/v1/peserta-kelas", params=params)
    
    def get_peserta_kelas_by_id(self, peserta_id: str) -> Dict[str, Any]:
        """Get detail peserta kelas by ID"""
        return self.get(f"edlink/v1/peserta-kelas/{peserta_id}")
    
    def get_presensi_kelas(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list presensi kelas (EdLink)"""
        return self.get("edlink/v1/presensi-kelas", params=params)
    
    def get_presensi_kelas_by_id(self, presensi_id: str) -> Dict[str, Any]:
        """Get detail presensi kelas by ID"""
        return self.get(f"edlink/v1/presensi-kelas/{presensi_id}")
    
    def get_tugas(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list tugas (EdLink)"""
        return self.get("edlink/v1/tugas", params=params)
    
    def get_tugas_by_id(self, tugas_id: str) -> Dict[str, Any]:
        """Get detail tugas by ID"""
        return self.get(f"edlink/v1/tugas/{tugas_id}")
    
    def get_soal_edlink(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list soal (EdLink)"""
        return self.get("edlink/v1/soal", params=params)
    
    def get_soal_edlink_by_id(self, soal_id: str) -> Dict[str, Any]:
        """Get detail soal by ID"""
        return self.get(f"edlink/v1/soal/{soal_id}")
    
    def get_peserta_kuis(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list peserta kuis (EdLink)"""
        return self.get("edlink/v1/peserta-kuis", params=params)
    
    def get_peserta_kuis_by_id(self, peserta_id: str) -> Dict[str, Any]:
        """Get detail peserta kuis by ID"""
        return self.get(f"edlink/v1/peserta-kuis/{peserta_id}")
    
    # ==================== DATA MBKM ====================
    
    def get_mitra_mbkm(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list mitra MBKM"""
        return self.get("siakadcloud/v1/mitra-mbkm", params=params)
    
    def get_mitra_mbkm_by_id(self, mitra_id: str) -> Dict[str, Any]:
        """Get detail mitra MBKM by ID"""
        return self.get(f"siakadcloud/v1/mitra-mbkm/{mitra_id}")
    
    def get_posisi_pekerjaan_mbkm(self, mitra_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get posisi pekerjaan dari mitra MBKM"""
        return self.get(f"siakadcloud/v1/mitra-mbkm/{mitra_id}/posisi-pekerjaan", params=params)
    
    def get_program_mbkm(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list program MBKM"""
        return self.get("siakadcloud/v1/program-mbkm", params=params)
    
    def get_program_mbkm_by_id(self, program_id: str) -> Dict[str, Any]:
        """Get detail program MBKM by ID"""
        return self.get(f"siakadcloud/v1/program-mbkm/{program_id}")
    
    def get_peserta_mbkm(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list peserta MBKM"""
        return self.get("siakadcloud/v1/peserta-mbkm", params=params)
    
    def get_peserta_mbkm_by_id(self, peserta_id: str) -> Dict[str, Any]:
        """Get detail peserta MBKM by ID"""
        return self.get(f"siakadcloud/v1/peserta-mbkm/{peserta_id}")
    
    # ==================== DATA MAHASISWA ====================
    
    def get_mahasiswa(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list mahasiswa"""
        return self.get("siakadcloud/v1/mahasiswa", params=params)
    
    def get_mahasiswa_by_id(self, mahasiswa_id: str) -> Dict[str, Any]:
        """Get detail mahasiswa by ID"""
        return self.get(f"siakadcloud/v1/mahasiswa/{mahasiswa_id}")
    
    def get_presensi_mahasiswa(self, mahasiswa_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get presensi mahasiswa"""
        return self.get(f"siakadcloud/v1/mahasiswa/{mahasiswa_id}/presensi", params=params)
    
    def get_nilai_mahasiswa(self, mahasiswa_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get nilai mahasiswa"""
        return self.get(f"siakadcloud/v1/mahasiswa/{mahasiswa_id}/nilai", params=params)
    
    def get_pelanggaran_mahasiswa(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list pelanggaran mahasiswa"""
        return self.get("siakadcloud/v1/pelanggaran-mahasiswa", params=params)
    
    def get_pelanggaran_mahasiswa_by_id(self, pelanggaran_id: str) -> Dict[str, Any]:
        """Get detail pelanggaran mahasiswa by ID"""
        return self.get(f"siakadcloud/v1/pelanggaran-mahasiswa/{pelanggaran_id}")
    
    def get_proporsi_nilai_mahasiswa(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list proporsi nilai mahasiswa"""
        return self.get("siakadcloud/v1/proporsi-nilai-mahasiswa", params=params)
    
    def get_proporsi_nilai_mahasiswa_by_id(self, proporsi_id: str) -> Dict[str, Any]:
        """Get detail proporsi nilai mahasiswa by ID"""
        return self.get(f"siakadcloud/v1/proporsi-nilai-mahasiswa/{proporsi_id}")
    
    def get_pendaftar(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list pendaftar"""
        return self.get("siakadcloud/v1/pendaftar", params=params)
    
    def get_pendaftar_by_id(self, pendaftar_id: str) -> Dict[str, Any]:
        """Get detail pendaftar by ID"""
        return self.get(f"siakadcloud/v1/pendaftar/{pendaftar_id}")
    
    def get_program_studi_pendaftar(self, pendaftar_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get program studi pendaftar"""
        return self.get(f"siakadcloud/v1/pendaftar/{pendaftar_id}/program-studi-pendaftar", params=params)
    
    def get_seleksi_pendaftar(self, pendaftar_id: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get seleksi pendaftar"""
        return self.get(f"siakadcloud/v1/pendaftar/{pendaftar_id}/seleksi", params=params)
    
    # ==================== DATA AKADEMIK ====================
    
    def get_program_studi(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list program studi"""
        return self.get("siakadcloud/v1/program-studi", params=params)
    
    def get_program_studi_by_id(self, program_studi_id: str) -> Dict[str, Any]:
        """Get detail program studi by ID"""
        return self.get(f"siakadcloud/v1/program-studi/{program_studi_id}")
    
    def get_mata_kuliah(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list mata kuliah"""
        return self.get("siakadcloud/v1/mata-kuliah", params=params)
    
    def get_mata_kuliah_by_id(self, mata_kuliah_id: str) -> Dict[str, Any]:
        """Get detail mata kuliah by ID"""
        return self.get(f"siakadcloud/v1/mata-kuliah/{mata_kuliah_id}")
    
    def get_kelas(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list kelas"""
        return self.get("siakadcloud/v1/kelas", params=params)
    
    def get_kelas_by_id(self, kelas_id: str) -> Dict[str, Any]:
        """Get detail kelas by ID"""
        return self.get(f"siakadcloud/v1/kelas/{kelas_id}")
    
    def get_jadwal(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list jadwal"""
        return self.get("siakadcloud/v1/jadwal", params=params)
    
    def get_jadwal_by_id(self, jadwal_id: str) -> Dict[str, Any]:
        """Get detail jadwal by ID"""
        return self.get(f"siakadcloud/v1/jadwal/{jadwal_id}")
    
    def get_cpmk(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Get list CPMK (Capaian Pembelajaran Mata Kuliah)"""
        return self.get("siakadcloud/v1/cpmk", params=params)
    
    def get_cpmk_by_id(self, cpmk_id: str) -> Dict[str, Any]:
        """Get detail CPMK by ID"""
        return self.get(f"siakadcloud/v1/cpmk/{cpmk_id}")


# Example usage
if __name__ == "__main__":
    # Initialize client (akan menggunakan env variables)
    client = SEVIMAClient()
    
    # Contoh penggunaan
    try:
        # Login
        # login_response = client.login("email@example.com", "password")
        # print(login_response)
        
        # Get list dosen
        # dosen_list = client.get_dosen()
        # print(dosen_list)
        
        # Get detail dosen
        # dosen_detail = client.get_dosen_by_id("123")
        # print(dosen_detail)
        
        print("SEVIMA API Client initialized successfully!")
        print("Make sure to set SEVIMA_API_KEY and SEVIMA_SECRET_KEY in your .env file")
    except Exception as e:
        print(f"Error: {e}")
