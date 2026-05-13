import urllib.request
import urllib.error
import time

TARGET = "http://192.168.0.1/cgi/"
DELAY = 1.0

PAYLOADS = [
    "info",
    "getDeviceInfo",
    "login",
    "getBindStatus",
    "setPwd",
    "auth",
    "status",
    "wan",
    "wifi",
    "dhcp",
    "log",
    "syslog",
    "backup",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "*/*",
    "Connection": "keep-alive",
}

print(f"[*] Fuzzing CGI endpoints at {TARGET}")

for payload in PAYLOADS:
    url = TARGET + payload
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        response = urllib.request.urlopen(req, timeout=5)
        status = response.getcode()
        length = len(response.read())
        print(f"[+] {payload} - Status: {status} - Length: {length}")
    except urllib.error.HTTPError as e:
        print(f"[*] {payload} - Status: {e.code}")
    except Exception as e:
        print(f"[-] {payload} - Error: {str(e)}")
    
    time.sleep(DELAY)

print("[*] CGI Fuzzing complete.")