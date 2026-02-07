## 2026-02-07 - SSRF Vulnerability in Scraper
**Vulnerability:** The `Scraper` class in `gpt_researcher/scraper/scraper.py` blindly trusted user-provided URLs and fetched their content. This allowed users to access internal network resources (localhost, private IPs) by submitting malicious URLs as `source_urls` in the research task.
**Learning:** Even in applications designed to "browse the web," it is critical to restrict *what* they can browse. Trust boundaries must be enforced at the edge where external input (URLs) enters the system.
**Prevention:** Always validate URLs against a whitelist of allowed schemes (http, https) and a blocklist of private/reserved IP ranges before making a request. Use DNS resolution to check the actual IP address of the target hostname.
