# Security Research & Validation Log: Router Assessment (192.168.0.1)

**Target:** 192.168.0.1 (TP-Link Archer C5 AC1200 MU-MIMO Wi-Fi Router, Firmware v6.8)
**WAN IP:** 10.251.252.155 (Observed via UPnP)
**Research Node IP:** 192.168.0.54
**Date:** 2026-05-13
**Primary Objective:** Network Exposure and Attack Surface Analysis
**Operational Constraint:** Controlled testing, rate-limited enumeration, and strict adherence to non-disruptive validation techniques.

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

## 2. Vulnerability Assessment & Validation Testing

### 2.1 Web Interface (Port 80) Analysis
**Goal:** Understand the authentication mechanism and surface architecture.
**Action:** Fetched HTTP headers and initial HTML.
**Result:** Discovered client-side encryption scripts (`encrypt.js`, `tpEncrypt.js`, `cryptoJS.min.js`). The router uses RSA and AES to encrypt credentials before sending them via POST, enforcing structured API interactions over basic plaintext authentication.

### 2.2 Rate-Limited Credential Validation (SSH/Telnet)
**Goal:** Test for default system configurations or legacy accounts non-disruptively.
**Action:** Developed and executed custom, rate-limited Python validation scripts (`slow_ssh.py`, `slow_brute.py`) to test common default credentials.
**Result:** No default credentials were valid. Services appear properly secured against baseline access attempts.

### 2.3 Rate-Limited Endpoint Enumeration
**Goal:** Identify exposed configuration files or undocumented API endpoints.
**Action:** 
1.  Created `stealth_fuzz.py` for common file enumeration. Found no exposed files.
2.  Created `stealth_cgi_fuzz.py` to analyze `/cgi/` endpoints. Received `406 Not Acceptable` responses.
3.  Developed `stealth_cgi_post.py` to test header enforcement (`Referer`, `Content-Type`, `X-Requested-With`) and POST request handling.
**Result:** Confirmed the API requires specific HTTP headers. Reached endpoints like `/cgi/login` and `/cgi/getBindStatus`, which returned standard error codes (e.g., `$.ret=71234;`) without exposing sensitive data. The API structural integrity is enforced.

### 2.4 UPnP Protocol Analysis (Port 1900)
**Goal:** Analyze UPnP for information exposure or misconfigurations.
**Command:** `nmap -sU -p 1900 --script=upnp-info 192.168.0.1`
**Result (Information Exposure):** Extracted exact device model (Archer-C5 v6.8) via standard protocol queries.

**Command:** Extracted `gatedesc.xml` and identified control URLs. Crafted a custom SOAP request (`soap_request.xml`) to `WANIPConn1`.
**Result (Information Exposure):** Successfully queried the router's WAN IP (`10.251.252.155`).

**Command:** Crafted a SOAP request (`add_port_mapping.xml`) to test UPnP IGD port mapping policies.
**Result (Policy Finding):** The router returned `200 OK` and accepted the mapping. 
**Finding:** The router's default UPnP Internet Gateway Device (IGD) implementation allows unauthenticated local network clients to modify WAN-to-LAN port forwarding rules, potentially altering the external network perimeter.

### 2.5 Vulnerability Research
**Goal:** Review public vulnerability databases for the identified firmware/model.
**Action:** Consulted public CVE databases and security advisories for the TP-Link Archer series.
**Result:** Identified relevant historical context:
*   **CVE-2018-19537:** Authenticated configuration parsing flaw.
*   **CVE-2019-7405:** Authentication anomaly (Password Overflow) affecting older Archer C5 variants, caused by inadequate bounds checking on HTTP requests.
*   **CVE-2025-15517:** Missing authentication checks in CGI endpoints on related hardware families.

### 2.6 Validation of CVE-2019-7405 Conditions
**Goal:** Test for anomalous authentication behavior consistent with historical CVEs.
**Action:** Developed a Python script (`test_overflow.py`) to send progressively larger payloads to the `/cgi/login` endpoint to test input validation boundaries.
**Result:** **ANOMALOUS BEHAVIOR OBSERVED.** Payload sizes of 256 and 512 bytes triggered anomalous authentication responses (`$.ret=0;` instead of standard errors). 
**Finding:** Observed behavior is potentially consistent with CVE-2019-7405 conditions during controlled testing. The device appears to lack strict input bounds checking on the authentication endpoint. Further vendor validation required.

---

## 3. Conclusions & Recommendations

**Summary:** 
The disciplined security research into the TP-Link Archer C5 (192.168.0.1) revealed structural security mechanisms (client-side API encryption) but identified two significant areas of concern regarding local network exposure: unauthenticated UPnP IGD port mapping and anomalous authentication boundary handling.

**Next Steps (Research & Mitigation):**
1.  **Document and Report:** Consolidate findings for internal security review and potential vendor disclosure regarding the anomalous authentication behavior.
2.  **Mitigation Analysis:** Research methods to disable or secure the UPnP service on this specific model to prevent unauthorized perimeter modifications.
3.  **Network Segmentation:** Evaluate the necessity of isolating this device on a dedicated management VLAN to mitigate the risks associated with the observed local attack surface.

*(End of Report)*