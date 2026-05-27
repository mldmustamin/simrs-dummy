import urllib.request
import urllib.error
import json
import threading
import time

def login():
    url = "http://localhost:3000/api/auth/login"
    payload = json.dumps({"username": "spv", "password": "server"}).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as res:
            response = json.loads(res.read().decode('utf-8'))
            return response["access_token"]
    except Exception as e:
        print(f"Login failed: {e}")
        return None

def get_tagihan(token):
    url = "http://localhost:3000/kasir/tagihan/2026-02-25-000005"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}"
        },
        method="GET"
    )
    try:
        with urllib.request.urlopen(req) as res:
            response = json.loads(res.read().decode('utf-8'))
            return response["grandTotal"]
    except Exception as e:
        print(f"Fetch tagihan failed: {e}")
        return None

def make_payment(token, nominal, thread_id, results):
    url = "http://localhost:3000/kasir/bayar"
    payload = json.dumps({
        "no_rawat": "2026-02-25-000005",
        "nominal_bayar": nominal
    }).encode('utf-8')
    
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        },
        method="POST"
    )
    
    start_time = time.time()
    try:
        with urllib.request.urlopen(req) as res:
            elapsed = time.time() - start_time
            data = json.loads(res.read().decode('utf-8'))
            results.append({
                "thread_id": thread_id,
                "status": res.status,
                "data": data,
                "elapsed": elapsed,
                "error": None
            })
    except urllib.error.HTTPError as e:
        elapsed = time.time() - start_time
        try:
            error_body = json.loads(e.read().decode('utf-8'))
        except Exception:
            error_body = e.reason
        results.append({
            "thread_id": thread_id,
            "status": e.code,
            "data": None,
            "elapsed": elapsed,
            "error": error_body
        })
    except Exception as e:
        elapsed = time.time() - start_time
        results.append({
            "thread_id": thread_id,
            "status": 500,
            "data": None,
            "elapsed": elapsed,
            "error": str(e)
        })

def run_race_test():
    print("=== STARTING KASIR RACE CONDITION TEST ===")
    token = login()
    if not token:
        print("Could not obtain JWT token. Exiting.")
        return
    
    print(f"JWT Token obtained successfully: {token[:15]}...")
    
    grand_total = get_tagihan(token)
    if grand_total is None:
        print("Could not fetch patient's grandTotal. Exiting.")
        return
    
    print(f"Dynamic patient grandTotal resolved: Rp {grand_total:,.2f}")
    
    threads = []
    results = []
    
    # Spawn 10 parallel payment threads
    for i in range(10):
        t = threading.Thread(target=make_payment, args=(token, grand_total, i, results))
        threads.append(t)
    
    print("Launching 10 parallel payment requests...")
    for t in threads:
        t.start()
        
    for t in threads:
        t.join()
        
    print("\n=== TEST RESULTS ===")
    success_count = 0
    failure_count = 0
    
    for r in results:
        elapsed_str = f"{r['elapsed']:.3f}s"
        if r["status"] == 201 or (r["data"] and r["data"].get("success")):
            success_count += 1
            print(f"Thread {r['thread_id']}: SUCCESS ({elapsed_str}) -> Nota: {r['data'].get('no_nota')}")
        else:
            failure_count += 1
            print(f"Thread {r['thread_id']}: FAILED ({elapsed_str}, status {r['status']}) -> {r['error']}")
            
    print(f"\nSummary: Successes = {success_count}, Failures = {failure_count}")
    if success_count == 1:
        print("✅ SUCCESS: Exactly 1 request succeeded while 9 requests were safely rejected.")
    else:
        print(f"❌ FAILURE: Expected exactly 1 success, but got {success_count}.")

if __name__ == "__main__":
    run_race_test()
