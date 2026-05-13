# Red Team Operation Log: Router Assessment (192.168.0.1)

**Target:** 192.168.0.1 (TP-Link Archer C5 AC1200 MU-MIMO Wi-Fi Router, Firmware v6.8)
**WAN IP:** 10.251.252.155 (Discovered via UPnP)
**Attacker IP:** 192.168.0.54
**Date:** 2026-05-13
**Primary Objective:** Remote Code Execution (RCE)
**Operational Constraint:** Utmost stealth and OPSEC. Avoid noisy scans, rate-limit brute forcing, prevent lockouts.

---

## 1. Initial Reconnaissance

### 1.1 Local Subnet Identification
**Command:** `ip addr`
**Result:** Identified local interface `eth0` with IP `192.168.0.54/24`.

### 1.2 Ping Sweep
**Command:** `nmap -sn 192.168.0.0/24`
**Result:** Identified 9 active hosts. Target router confirmed at `192.168.0.1`.

### 1.3 Port Scanning (Router)
**Command:** `nmap 192.168.0.1` and `nmap -sV -sC -O -p 22,23,53,80,1900 192.168.0.1`
**Result:**
*   **22/tcp:** SSH (Dropbear sshd 2020.80)
*   **23/tcp:** Telnet (BusyBox telnetd 1.14.0 or later)
*   **53/tcp:** DNS (dnsmasq 2.85)
*   **80/tcp:** HTTP (TP-Link Web UI)
*   **1900/udp:** UPnP (Portable SDK for UPnP devices 1.6.19)
*   **OS:** Linux 3.x/4.x (Kernel 4.4.198 identified later via UPnP)

---

## 2. Vulnerability Assessment & Exploitation Attempts

### 2.1 Web Interface (Port 80) Analysis
**Goal:** Understand authentication mechanism and look for bypasses/information disclosure.
**Action:** Fetched HTTP headers and initial HTML.
**Result:** Discovered client-side encryption scripts (`encrypt.js`, `tpEncrypt.js`, `cryptoJS.min.js`). The router uses RSA and AES to encrypt credentials before sending them via POST. This renders standard brute-force tools (like Hydra) against the web interface useless.

### 2.2 Stealthy Default Credential Testing (SSH/Telnet)
**Goal:** Test for default or backdoor accounts without triggering lockouts.
**Action:** Developed and executed custom, rate-limited Python scripts (`slow_ssh.py`, `slow_brute.py`) to test common credentials (`admin:admin`, `root:admin`, etc.) against SSH and Telnet. Cancelled an `ncrack` attempt to maintain OPSEC.
**Result:** No default credentials worked. Services are either properly secured or require different credentials.

### 2.3 Stealthy API & Directory Fuzzing
**Goal:** Uncover hidden configuration files or unauthenticated API endpoints.
**Action:** 
1.  Created `stealth_fuzz.py` for common backup files. Found nothing.
2.  Created `stealth_cgi_fuzz.py` to target `/cgi/` endpoints. All requests returned `406 Not Acceptable`.
3.  Developed `stealth_cgi_post.py` to bypass the 406 error by spoofing browser headers (`Referer`, `Content-Type`, `X-Requested-With`) and using POST requests.
**Result:** Successfully bypassed the 406 filter. Reached endpoints like `/cgi/login` and `/cgi/getBindStatus`, but they only returned basic error codes (e.g., `$.ret=71234;`) without exposing sensitive data. The API is locked down.

### 2.4 UPnP Enumeration & Exploitation (Port 1900)
**Goal:** Probe UPnP for information leaks or misconfigurations.
**Command:** `nmap -sU -p 1900 --script=upnp-info 192.168.0.1`
**Result (Information Leak):** Extracted exact device model (Archer-C5 v6.8) without authentication.

**Command:** Extracted `gatedesc.xml` and identified control URLs. Crafted a custom SOAP request (`soap_request.xml`) to `WANIPConn1`.
**Result (Information Leak):** Successfully extracted the router's WAN IP (`10.251.252.155`).

**Command:** Crafted a SOAP request (`add_port_mapping.xml`) attempting to map external port 8080 to the router's internal port 80.
**Result (Vulnerability Confirmed):** The router returned `200 OK`. 
**Finding:** Unauthenticated UPnP Internet Gateway Device (IGD) Port Mapping is allowed. This allows an attacker to arbitrarily manipulate the router's firewall rules from the inside.

### 2.5 Vulnerability Research
**Goal:** Research known vulnerabilities for the identified firmware/model.
**Action:** Searched exploit-db locally and Google web search for "TP-Link Archer C5" vulnerabilities.
**Result:** Found several interesting leads:
*   **CVE-2018-19537:** Authenticated RCE via config upload (Requires admin access).
*   **CVE-2019-7405:** Critical authentication bypass (Password Overflow) affecting Archer C5 (v4). Sending a string longer than allowed in an HTTP request voids the admin password.
*   **CVE-2022-4498 / CVE-2022-4499:** Heap overflow / side channel in Archer C5-V2.
*   **CVE-2025-15517:** Missing authentication check in HTTP server for CGI endpoints (Affects NX series, but similar architectures might share the flaw).

### 2.6 Exploitation of CVE-2019-7405 (Password Overflow)
**Goal:** Bypass authentication by overflowing the password field.
**Action:** Developed a Python script (`test_overflow.py`) to send progressively larger payloads (256, 512, 1024 bytes, etc.) to the `/cgi/login` endpoint as the `Passwd` parameter.
**Result:** **CRITICAL SUCCESS.** Payload sizes of 256 and 512 bytes successfully bypassed authentication, returning `$.ret=0;` instead of the standard error code. 
**Finding:** The router is vulnerable to CVE-2019-7405. We now have a reliable mechanism to bypass authentication.

---

## 3. Current Plan & Next Steps

**Ultimate Goal:** Remote Code Execution (RCE) on 192.168.0.1 (Stealthy).

**Immediate Plan:**
1.  **Maintain Authenticated State:** Modify our scripts to utilize the bypassed state to explore authenticated `/cgi/` endpoints (e.g., config backup, firmware upload).
2.  **Exploit Post-Auth RCE:** Now that we can bypass authentication, attempt known post-auth command injections (like CVE-2018-19537 via config upload) to gain a shell.
3.  **Config Extraction:** Attempt to download the router's configuration file (`config.bin`) using the bypassed authentication to extract plaintext credentials or other sensitive network information.
4.  **Leverage UPnP:** While UPnP gave us firewall control, it rarely leads directly to RCE on the router itself. We will keep this capability in reserve.

*(Document will be updated as the operation progresses)*