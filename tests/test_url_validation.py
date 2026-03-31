import pytest
import sys
import os
import socket
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gpt_researcher.utils.validators import validate_url

class TestUrlValidation:

    def test_valid_urls(self):
        # We mock gethostbyname to return a public IP for these domains
        with patch("socket.gethostbyname") as mock_gethost:
            mock_gethost.return_value = "93.184.216.34" # example.com
            assert validate_url("https://google.com") == True
            assert validate_url("http://example.com/path") == True

    def test_invalid_schemes(self):
        assert validate_url("ftp://example.com") == False
        assert validate_url("file:///etc/passwd") == False
        assert validate_url("gopher://example.com") == False
        assert validate_url("javascript:alert(1)") == False

    def test_private_ips(self):
        # We need to mock socket.gethostbyname to reliably test IP blocking
        # without depending on actual DNS or local network config
        with patch("socket.gethostbyname") as mock_gethost:
            # Test localhost
            mock_gethost.return_value = "127.0.0.1"
            assert validate_url("http://localhost") == False

            # Test private range 10.x.x.x
            mock_gethost.return_value = "10.0.0.1"
            assert validate_url("http://internal-service") == False

            # Test private range 192.168.x.x
            mock_gethost.return_value = "192.168.1.1"
            assert validate_url("http://router") == False

            # Test private range 172.16.x.x
            mock_gethost.return_value = "172.16.0.1"
            assert validate_url("http://docker-container") == False

            # Test valid public IP
            mock_gethost.return_value = "8.8.8.8"
            assert validate_url("http://public-service") == True

    def test_direct_ip_usage(self):
        # socket.gethostbyname("1.2.3.4") returns "1.2.3.4"
        # We can just rely on the real behavior or mock it.
        # Mocking is safer to avoid network calls.
        with patch("socket.gethostbyname") as mock_gethost:
            def side_effect(host):
                return host
            mock_gethost.side_effect = side_effect

            assert validate_url("http://127.0.0.1") == False
            assert validate_url("http://169.254.169.254") == False # Link-local (AWS metadata)
            assert validate_url("http://0.0.0.0") == False
            assert validate_url("http://8.8.8.8") == True

    def test_unresolvable_host(self):
        with patch("socket.gethostbyname") as mock_gethost:
            mock_gethost.side_effect = socket.gaierror("DNS Error")
            assert validate_url("http://nonexistent-domain.test") == False
