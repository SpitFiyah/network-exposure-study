import urllib.request
import urllib.error
import time

TARGET = "http://192.168.0.1/"
DELAY = 1.5  # 1.5 seconds between requests

# Focus on configuration backups, logs, and common TP-Link endpoints
PAYLOADS = [
    "config.bin",
    "conf.bin",
    "backup.bin",
    "backup.xml",
    "config.xml",
    "rom-0",
    "syslog.txt",
    "log.txt",
    "debug.txt",
    "userRpm/",
    "cgi/",
    "cgi-bin/",
    "api/",
    "data/",
    ".env",
    "pwd.html",
    "password.html",
    "test.html",
    "test.txt",
    "dev/",
    "tftpboot/",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
}

print(f"[*] Starting stealthy directory fuzzing against {TARGET}")
print(f"[*] Rate limiting: {DELAY}s per request")

for payload in PAYLOADS:
    url = TARGET + payload
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        response = urllib.request.urlopen(req, timeout=5)
        status = response.getcode()
        length = len(response.read())
        print(f"[+] FOUND: {url} - Status: {status} - Length: {length} bytes")
    except urllib.error.HTTPError as e:
        if e.code not in [404, 406]:
            print(f"[*] Interesting: {url} - Status: {e.code}")
    except Exception as e:
        print(f"[-] Error on {url}: {str(e)}")
    
    time.sleep(DELAY)

print("[*] Fuzzing complete.")
