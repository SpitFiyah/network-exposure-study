# Router Assessment Archive - 192.168.0.1 (TP-Link Archer C5)

This archive contains all the scripts, payloads, logs, and reports generated during the security assessment of the local router at `192.168.0.1`.

## Directory Structure

*   **`/docs/`**: Contains detailed markdown reports.
    *   `full_report.md`: The comprehensive Red Team operation log detailing reconnaissance, exploitation attempts, and findings.
    *   `command_log.md`: A chronological log of significant terminal commands executed during the assessment.
*   **`/scripts_and_payloads/`**: Contains the custom Python scripts and XML payloads developed during the engagement.
    *   `slow_ssh.py`: Rate-limited SSH credential tester.
    *   `slow_brute.py`: (Initial version, failed due to missing telnetlib). Rate-limited SSH/Telnet tester.
    *   `stealth_fuzz.py`: Rate-limited directory fuzzer for common backup files.
    *   `stealth_cgi_fuzz.py`: Fuzzer for `/cgi/` endpoints (resulted in 406 errors).
    *   `stealth_cgi_post.py`: Advanced fuzzer that bypasses 406 errors by spoofing headers and using POST requests.
    *   `test_overflow.py`: Exploit script to test for CVE-2019-7405 (Password Overflow) against the `/cgi/login` endpoint.
    *   `soap_request.xml`: UPnP SOAP payload to extract the external WAN IP.
    *   `add_port_mapping.xml`: UPnP SOAP payload to test unauthenticated IGD port mapping.

## Key Findings Summary

1.  **CVE-2019-7405 (Authentication Bypass):** Confirmed. Sending an oversized payload to the `/cgi/login` password field successfully bypassed authentication (returned `$.ret=0;`).
2.  **Unauthenticated UPnP Port Mapping:** Confirmed. The router allows unauthenticated local devices to modify WAN-to-LAN port forwarding rules via UPnP IGD.
3.  **Information Leakage:** Extracted precise model and firmware details via UPnP enumeration.

For detailed methodologies and step-by-step progress, refer to `docs/full_report.md`.