# Command Execution Log

This document chronicles the key shell commands executed during the security research and validation testing of `192.168.0.1`.

## 1. Network Reconnaissance
*   `ip addr` - Gathered local interface and subnet information.
*   `nmap -sn 192.168.0.0/24` - Ping sweep to identify active hosts, locating the target router at 192.168.0.1.
*   `nmap 192.168.0.1` - Initial fast port scan.
*   `nmap -sV -sC -O -p 22,23,53,80,1900 192.168.0.1` - Detailed service fingerprinting, script scanning, and OS detection.

## 2. Web Interface Analysis
*   `curl -s -v http://192.168.0.1 | head -n 50` - Fetched initial HTTP headers and HTML, revealing client-side encryption logic.
*   `curl -s -H "Accept: text/javascript..." -H "Referer: http://192.168.0.1/" ... http://192.168.0.1/js/tpEncrypt.js | head -n 50` - Bypassed 406 Not Acceptable to read client-side encryption logic.

## 3. Vulnerability Research
*   `searchsploit "Portable SDK for UPnP"`
*   `searchsploit TP-Link | grep -i bypass`
*   `searchsploit Archer C5`
*   `searchsploit dnsmasq 2.8`
*   `searchsploit dropbear 2020`

## 4. UPnP Protocol Analysis
*   `nmap -sU -p 1900 --script=upnp-info 192.168.0.1` - Extracted device make, model, and version via UPnP.
*   `curl -s http://192.168.0.1:1900/pdttgy/gatedesc.xml | grep -i controlURL -B 2 -A 2` - Located UPnP SOAP control URLs.
*   `curl -s -H "Content-Type: text/xml; charset=\"utf-8\"" -H "SOAPAction: ..." -d @/home/ZeroDay/soap_request.xml http://192.168.0.1:1900/upnp/control/pdttgy/WANIPConn1` - Extracted WAN IP.
*   `curl -s -v -H "Content-Type: text/xml; charset=\"utf-8\"" -H "SOAPAction: ..." -d @/home/ZeroDay/add_port_mapping.xml http://192.168.0.1:1900/upnp/control/pdttgy/WANIPConn1` - Analyzed UPnP IGD port mapping policy.

## 5. Custom Validation Scripts
*   `python3 /home/ZeroDay/slow_ssh.py` - Executed rate-limited SSH baseline credential validation.
*   `python3 /home/ZeroDay/stealth_fuzz.py` - Executed rate-limited endpoint enumeration.
*   `python3 /home/ZeroDay/stealth_cgi_fuzz.py` - Executed CGI endpoint enumeration (received 406 errors).
*   `python3 /home/ZeroDay/stealth_cgi_post.py` - Executed POST-based CGI enumeration testing header enforcement.
*   `python3 /home/ZeroDay/test_overflow.py` - Executed validation script testing input boundaries for anomalous authentication behavior.