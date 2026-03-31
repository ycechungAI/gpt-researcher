## 2024-05-15 - Path Traversal Vulnerability in File Uploads/Deletions
**Vulnerability:** Arbitrary file write and deletion vulnerabilities in `handle_file_upload` and `handle_file_deletion` via path traversal and unsafe filename handling.
**Learning:** `os.path.basename` does not reliably strip path traversal attacks depending on the input, and user-provided filenames must be strictly validated.
**Prevention:** Always use a `secure_filename` function to sanitize filenames (removing traversals, null bytes, reserved names) and a `validate_file_path` function using `os.path.commonpath` to ensure the final resolved path stays within the intended base directory.
