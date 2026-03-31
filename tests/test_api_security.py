import pytest
from unittest.mock import Mock, MagicMock
import sys
import os

# Mock dependencies to import app
# We need to reuse the mocking logic from reproduce_path_traversal.py or similar
# because app.py imports a lot of things.

import types
def mock_module(name):
    if name not in sys.modules:
        m = types.ModuleType(name)
        sys.modules[name] = m
    return sys.modules[name]

# Mock everything under gpt_researcher
gr = mock_module("gpt_researcher")
gr.GPTResearcher = MagicMock()

gru = mock_module("gpt_researcher.utils")
grue = mock_module("gpt_researcher.utils.enum")
grue.Tone = MagicMock()
grue.ReportType = MagicMock()

gra = mock_module("gpt_researcher.actions")
gra.stream_output = MagicMock()

grd = mock_module("gpt_researcher.document")
grdd = mock_module("gpt_researcher.document.document")
grdd.DocumentLoader = MagicMock()

# Mock chat
mock_module("chat")
cc = mock_module("chat.chat")
cc.ChatAgentWithMemory = MagicMock()

# Mock report_type
rt = mock_module("report_type")
rt.BasicReport = MagicMock()
rt.DetailedReport = MagicMock()

# Mock utils
u = mock_module("utils")
u.write_md_to_word = MagicMock()
u.write_md_to_pdf = MagicMock()
u.write_text_to_md = MagicMock()

# Import app
sys.path.insert(0, os.path.abspath("backend"))
from backend.server.app import read_report
from fastapi import HTTPException

@pytest.mark.asyncio
async def test_read_report_traversal():
    request = Mock()

    # Test with malicious ID that starts with ..
    with pytest.raises(HTTPException) as exc:
        await read_report(request, "../secret")

    assert exc.value.status_code == 400
    assert "Invalid research ID" in exc.value.detail

@pytest.mark.asyncio
async def test_read_report_valid():
    request = Mock()

    # Test with valid ID
    # We expect {"message": "Report not found."} because file doesn't exist
    res = await read_report(request, "valid_id")
    assert res == {"message": "Report not found."}
