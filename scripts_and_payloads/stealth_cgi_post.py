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
    "status",
    "wan",
    "wifi",
    "log",
    "syslog",
    "backup",
    "conf",
    "getSyslog",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
    "Referer": "http://192.168.0.1/",
    "Content-Type": "application/x-www-form-urlencoded",
    "X-Requested-With": "XMLHttpRequest"
}

print(f"[*] Fuzzing CGI endpoints at {TARGET} with POST and spoofed headers")

for payload in PAYLOADS:
    url = TARGET + payload
    # Creating a POST request with empty data
    data = b"" 
    req = urllib.request.Request(url, data=data, headers=HEADERS, method='POST')
    try:
        response = urllib.request.urlopen(req, timeout=5)
        status = response.getcode()
        body = response.read()
        length = len(body)
        print(f"[+] {payload} - Status: {status} - Length: {length}")
        if length > 0 and length < 200:
            print(f"    Preview: {body[:100]}")
    except urllib.error.HTTPError as e:
        print(f"[*] {payload} - Status: {e.code}")
    except Exception as e:
        print(f"[-] {payload} - Error: {str(e)}")
    
    time.sleep(DELAY)

print("[*] CGI Fuzzing complete.")