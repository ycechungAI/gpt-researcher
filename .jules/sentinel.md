## 2026-02-07 - SSRF Vulnerability in Scraper
**Vulnerability:** The `Scraper` class in `gpt_researcher/scraper/scraper.py` blindly trusted user-provided URLs and fetched their content. This allowed users to access internal network resources (localhost, private IPs) by submitting malicious URLs as `source_urls` in the research task.
**Learning:** Even in applications designed to "browse the web," it is critical to restrict *what* they can browse. Trust boundaries must be enforced at the edge where external input (URLs) enters the system.
**Prevention:** Always validate URLs against a whitelist of allowed schemes (http, https) and a blocklist of private/reserved IP ranges before making a request. Use DNS resolution to check the actual IP address of the target hostname.
## 2024-05-15 - Path Traversal Vulnerability in File Uploads/Deletions
**Vulnerability:** Arbitrary file write and deletion vulnerabilities in `handle_file_upload` and `handle_file_deletion` via path traversal and unsafe filename handling.
**Learning:** `os.path.basename` does not reliably strip path traversal attacks depending on the input, and user-provided filenames must be strictly validated.
**Prevention:** Always use a `secure_filename` function to sanitize filenames (removing traversals, null bytes, reserved names) and a `validate_file_path` function using `os.path.commonpath` to ensure the final resolved path stays within the intended base directory.
