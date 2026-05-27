import urllib.request
import urllib.error
import json
import concurrent.futures
import time

URL = "http://localhost:3000/api/kiosk/register"

def send_request(thread_id):
    start_time = time.time()
    # We use dynamic RM to ensure we have enough patients to register 
    # but for concurrency test, registering the same patient multiple times 
    # simultaneously will trigger unique constraints and race conditions.
    # Let's register RM '000007' simultaneously 50 times!
    payload = {
        "no_rkm_medis": "000002",
        "kd_poli": "U0009",
        "kd_dokter": "D0000002",
        "kd_pj": "A01"
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(URL, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        response = urllib.request.urlopen(req)
        res_data = response.read().decode('utf-8')
        end_time = time.time()
        return thread_id, "SUCCESS", res_data, end_time - start_time
    except urllib.error.HTTPError as e:
        end_time = time.time()
        return thread_id, f"FAILED ({e.code})", e.read().decode('utf-8'), end_time - start_time
    except Exception as e:
        end_time = time.time()
        return thread_id, "ERROR", str(e), end_time - start_time

def main():
    print("=== STARTING KIOSK STRESS TEST (POST) ===")
    print("Simulating 50 simultaneous POST requests for the same patient to trigger heavy race conditions...")
    
    # We want exactly 1 success or maybe 0 if the patient is already registered today
    num_requests = 50
    results = []
    
    start_global = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [executor.submit(send_request, i) for i in range(num_requests)]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    end_global = time.time()
    
    print("\n=== STRESS TEST RESULTS ===")
    successes = 0
    failures = 0
    
    for tid, status, res_data, latency in results:
        if status == "SUCCESS":
            successes += 1
            print(f"Thread {tid}: {status} ({latency:.3f}s) -> {res_data}")
        else:
            failures += 1
            # only print a few failures to avoid spam
            if failures <= 5:
                print(f"Thread {tid}: {status} ({latency:.3f}s) -> {res_data}")
                
    if failures > 5:
        print(f"... and {failures - 5} more failures.")

    print(f"\nSummary: {successes} Successes, {failures} Failures")
    print(f"Total time taken for 50 concurrent requests: {end_global - start_global:.3f}s")

if __name__ == "__main__":
    main()
