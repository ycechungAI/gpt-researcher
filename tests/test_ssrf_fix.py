import pytest
import socket
from unittest.mock import MagicMock, patch
from gpt_researcher.scraper.scraper import Scraper
from gpt_researcher.utils.workers import WorkerPool

class TestSSRFProtection:
    @pytest.fixture
    def scraper(self):
        worker_pool = MagicMock(spec=WorkerPool)
        return Scraper(urls=[], user_agent="test", scraper="bs", worker_pool=worker_pool)

    @patch('socket.gethostbyname')
    def test_validate_url_valid(self, mock_gethostbyname, scraper):
        # Mock Google IP to a public IP
        mock_gethostbyname.return_value = "142.250.190.46"
        assert scraper.validate_url("https://google.com") == True
        assert scraper.validate_url("http://example.com") == True

    def test_validate_url_invalid_scheme(self, scraper):
        assert scraper.validate_url("ftp://example.com") == False
        assert scraper.validate_url("file:///etc/passwd") == False
        assert scraper.validate_url("javascript:alert(1)") == False

    @patch('socket.gethostbyname')
    def test_validate_url_private_ip(self, mock_gethostbyname, scraper):
        # Mock various resolutions to private IPs
        mock_gethostbyname.side_effect = lambda host: {
            "localhost": "127.0.0.1",
            "internal.server": "192.168.1.1",
            "cloud.metadata": "169.254.169.254",
            "zeros": "0.0.0.0"
        }.get(host, "1.1.1.1")

        assert scraper.validate_url("http://localhost") == False
        assert scraper.validate_url("http://internal.server") == False
        assert scraper.validate_url("http://cloud.metadata") == False
        assert scraper.validate_url("http://zeros") == False

    def test_validate_url_direct_ip_private(self, scraper):
        # socket.gethostbyname handles IP strings too
        with patch('socket.gethostbyname', side_effect=lambda x: x):
            assert scraper.validate_url("http://127.0.0.1") == False
            assert scraper.validate_url("http://192.168.1.1") == False
            assert scraper.validate_url("http://10.0.0.1") == False
            assert scraper.validate_url("http://0.0.0.0") == False

    def test_validate_url_direct_ip_public(self, scraper):
        with patch('socket.gethostbyname', side_effect=lambda x: x):
            assert scraper.validate_url("http://8.8.8.8") == True
