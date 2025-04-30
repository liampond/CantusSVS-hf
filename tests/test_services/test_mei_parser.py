import pytest
from pathlib import Path
from unittest.mock import patch

from webapp.services.parsing.mei_parser import parse_mei_for_editor

@patch("webapp.services.parsing.mei_parser._parse_mei_raw")
def test_parse_mei_for_editor_basic(mock_parse_mei_raw):
    # Arrange: mock what _parse_mei_raw would return
    mock_parse_mei_raw.return_value = {
        "notes": ["C4", "D4", "E4"],
        "durations": [1.0, 0.5, 0.75],
        "lyrics": "do re mi"
    }
    
    dummy_path = Path("/fake/path/to/file.mei")
    tempo = 120

    # Act
    result = parse_mei_for_editor(dummy_path, tempo)

    # Assert
    expected = [
        {"id": "note_0", "pitch": "C4", "duration": 1.0, "lyric": "do"},
        {"id": "note_1", "pitch": "D4", "duration": 0.5, "lyric": "re"},
        {"id": "note_2", "pitch": "E4", "duration": 0.75, "lyric": "mi"},
    ]
    assert result == expected

def test_parse_mei_for_editor_empty(monkeypatch):
    # Arrange: _parse_mei_raw returns empty
    def mock_parse_mei_raw(mei_path, tempo):
        return {"notes": [], "durations": [], "lyrics": ""}

    monkeypatch.setattr("webapp.services.parsing.mei_parser._parse_mei_raw", mock_parse_mei_raw)

    dummy_path = Path("/fake/path/to/empty.mei")
    tempo = 120

    # Act
    result = parse_mei_for_editor(dummy_path, tempo)

    # Assert
    assert result == []
