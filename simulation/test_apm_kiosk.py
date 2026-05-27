import threading
import requests
import json
import time

# Target Endpoint
URL = "http://localhost:3000/api/kiosk/register"

# Patients to register concurrently
PATIENTS = [
    {"no_rkm_medis": "000002", "kd_poli": "U0001", "kd_dokter": "D0000004", "kd_pj": "A01"},
    {"no_rkm_medis": "000003", "kd_poli": "U0001", "kd_dokter": "D0000004", "kd_pj": "A01"},
    {"no_rkm_medis": "000005", "kd_poli": "U0001", "kd_dokter": "D0000004", "kd_pj": "A01"},
    {"no_rkm_medis": "000006", "kd_poli": "U0001", "kd_dokter": "D0000004", "kd_pj": "A01"}
]

results = []
barrier = threading.Barrier(len(PATIENTS))

def send_register_request(patient):
    # Wait until all threads are ready, to maximize parallel overlap
    barrier.wait()
    
    start_time = time.time()
    try:
        response = requests.post(
            URL,
            headers={"Content-Type": "application/json"},
            data=json.dumps(patient),
            timeout=5
        )
        latency = time.time() - start_time
        results.append({
            "no_rkm_medis": patient["no_rkm_medis"],
            "status_code": response.status_code,
            "data": response.json() if response.status_code == 201 else None,
            "error": response.text if response.status_code != 201 else None,
            "latency": f"{latency:.3f}s"
        })
    except Exception as e:
        results.append({
            "no_rkm_medis": patient["no_rkm_medis"],
            "status_code": 0,
            "error": str(e),
            "latency": "N/A"
        })

def run_simulation():
    print("=== MEMULAI SIMULASI PENDAFTARAN PARALEL KIOS MANDIRI (APM) ===")
    print(f"Mengirimkan {len(PATIENTS)} request pendaftaran secara bersamaan ke {URL}...")
    
    threads = []
    for p in PATIENTS:
        t = threading.Thread(target=send_register_request, args=(p,))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
        
    print("\n=== HASIL SIMULASI PENDAFTARAN PARALEL ===")
    
    success_count = 0
    failure_count = 0
    created_rawats = []
    created_queues = []
    
    for r in results:
        print(f"\nPasien RM: {r['no_rkm_medis']}")
        print(f"Status Code: {r['status_code']}")
        print(f"Latency: {r['latency']}")
        if r['status_code'] == 201:
            success_count += 1
            reg_info = r['data']
            created_rawats.append(reg_info['no_rawat'])
            created_queues.append(reg_info['no_reg'])
            print(f"  ✓ Sukses Pendaftaran!")
            print(f"  ✓ No. Rawat: {reg_info['no_rawat']}")
            print(f"  ✓ No. Antrean Poli: {reg_info['no_reg']}")
            print(f"  ✓ Sumber Daftar: {reg_info['sumber_daftar']}")
        else:
            failure_count += 1
            print(f"  ❌ Gagal Pendaftaran!")
            print(f"  Detail Error: {r['error']}")
            
    print("\n=== ANALISIS INTEGRITAS TRANSAKSI ===")
    print(f"Total Sukses: {success_count} / {len(PATIENTS)}")
    print(f"Total Gagal : {failure_count} / {len(PATIENTS)}")
    
    # Check for duplicate no_rawat
    if len(created_rawats) == len(set(created_rawats)):
        print("✓ Integritas No Rawat: SEMUA NO RAWAT UNIK (TIDAK ADA DUPLIKASI).")
    else:
        print("❌ Kerusakan Integritas: Ditemukan duplikasi No Rawat!")
        
    # Check for duplicate queue numbers (no_reg)
    if len(created_queues) == len(set(created_queues)):
        print("✓ Integritas Antrean: SEMUA NOMOR ANTREAN UNIK & URUT (TIDAK ADA DUPLIKASI).")
    else:
        print("❌ Kerusakan Integritas: Ditemukan duplikasi nomor antrean poliklinik!")

if __name__ == "__main__":
    run_simulation()
