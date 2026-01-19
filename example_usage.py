"""
Contoh penggunaan SEVIMA API Client
"""

from sevima_client import SEVIMAClient

def main():
    # Initialize client (menggunakan environment variables dari .env)
    client = SEVIMAClient()
    
    print("=== SEVIMA API Client Example ===\n")
    
    try:
        # Contoh 1: Get list dosen
        print("1. Mengambil list dosen...")
        dosen_list = client.get_dosen()
        print(f"   Response keys: {list(dosen_list.keys()) if isinstance(dosen_list, dict) else 'N/A'}\n")
        
        # Contoh 2: Get list mahasiswa
        print("2. Mengambil list mahasiswa...")
        mahasiswa_list = client.get_mahasiswa()
        print(f"   Response keys: {list(mahasiswa_list.keys()) if isinstance(mahasiswa_list, dict) else 'N/A'}\n")
        
        # Contoh 3: Get list program studi
        print("3. Mengambil list program studi...")
        program_studi = client.get_program_studi()
        print(f"   Response keys: {list(program_studi.keys()) if isinstance(program_studi, dict) else 'N/A'}\n")

        # Contoh tambahan: build query params dengan filtering & ordering
        print("4. Contoh build params (filtering & ordering)")
        filters = {
            'nilai_angka': ('3', 'gt'),
            'program_studi': 'Ilmu Hukum'
        }
        order = {'nim': 'asc'}
        built = client._merge_query_params(params=None, page=1, per_page=20, filters=filters, order=order)
        print(f"   Built query params: {built}\n")

        # Contoh fetch all pages (hanya contoh; akan melakukan request jika API key disetel)
        # all_pages_result = client.get_all_pages('siakadcloud/v1/mahasiswa', per_page=50)
        # print(f"   All pages data count: {len(all_pages_result.get('data', []))}")
        
        # Contoh 4: Get detail dosen (jika ada ID)
        # dosen_id = "123"  # Ganti dengan ID yang valid
        # dosen_detail = client.get_dosen_by_id(dosen_id)
        # print(f"Dosen detail: {dosen_detail}\n")
        
        # Contoh 5: Get penelitian dosen
        # dosen_id = "123"  # Ganti dengan ID yang valid
        # penelitian = client.get_dosen_penelitian(dosen_id)
        # print(f"Penelitian dosen: {penelitian}\n")
        
        # Contoh 6: Login (jika diperlukan)
        # login_response = client.login("email@example.com", "password")
        # print(f"Login response: {login_response}\n")
        
        print("✅ Semua request berhasil!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
