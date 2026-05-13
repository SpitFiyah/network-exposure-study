# Router Security Research & Validation - 192.168.0.1 (TP-Link Archer C5)

This archive contains the scripts, payloads, logs, and reports generated during disciplined security research into the network exposure and attack surface of a local router at `192.168.0.1`.

## Directory Structure

*   **`/docs/`**: Contains detailed markdown reports.
    *   `full_report.md`: Detailed assessment log documenting reconnaissance, protocol analysis, validation testing, and findings.
    *   `command_log.md`: A chronological log of significant terminal commands executed during the assessment.
*   **`/scripts_and_payloads/`**: Contains the custom Python validation scripts and XML payloads developed during the research.
    *   `slow_ssh.py`: Rate-limited SSH credential validation script.
    *   `slow_brute.py`: Rate-limited SSH/Telnet validation script.
    *   `stealth_fuzz.py`: Rate-limited endpoint enumeration script.
    *   `stealth_cgi_fuzz.py`: Enumeration script for `/cgi/` endpoints.
    *   `stealth_cgi_post.py`: Advanced enumeration script testing header handling and POST requests.
    *   `test_overflow.py`: Validation script to test for anomalous authentication behavior related to CVE-2019-7405.
    *   `soap_request.xml`: UPnP SOAP payload for protocol analysis.
    *   `add_port_mapping.xml`: UPnP SOAP payload to analyze IGD port mapping policies.

## Key Findings Summary

1.  **CVE-2019-7405 (Authentication Anomaly):** Observed behavior potentially consistent with CVE-2019-7405 conditions during controlled testing. Sending an oversized payload to the `/cgi/login` password field triggered anomalous authentication behavior (returned `$.ret=0;`). Further vendor validation required.
2.  **UPnP Port Mapping Policy:** Confirmed that the router's default UPnP Internet Gateway Device (IGD) configuration allows unauthenticated local devices to modify WAN-to-LAN port forwarding rules.
3.  **Information Disclosure:** Extracted precise model and firmware details via standard UPnP protocol queries.

For detailed methodologies and step-by-step progress, refer to `docs/full_report.md`.