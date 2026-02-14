## 2024-05-22 - Path Traversal Risks
**Vulnerability:** Identified potential path traversal in `read_report` endpoint where `research_id` is used in `os.path.join`. Also `handle_file_upload` relied on `os.path.basename`.
**Learning:** While FastAPI/Starlette routing effectively blocks `/` in path parameters (mitigating simple traversal), logic should not rely solely on routing constraints. Defense in depth requires sanitizing inputs before filesystem operations.
**Prevention:** Implemented `secure_filename` to strictly validate and sanitize filenames, and `validate_file_path` to ensure paths resolve within intended directories.
