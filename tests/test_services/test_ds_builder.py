import json
from pathlib import Path
import tempfile

from webapp.services.parsing.ds_builder import build_ds_from_notes

def test_build_ds_from_notes_basic():
    # Arrange
    notes = [
        {"pitch": "C4", "duration": 1.0, "phoneme": "k"},
        {"pitch": "D4", "duration": 0.5, "phoneme": "d"},
        {"pitch": "E4", "duration": 0.75, "phoneme": "e"},
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test.ds"

        # Act
        build_ds_from_notes(notes, output_path)

        # Assert
        with open(output_path, "r", encoding="utf-8") as f:
            ds = json.load(f)

        assert ds["ph_seq"] == "k d e"
        assert ds["ph_num"] == "1 1 1"
        assert ds["note_seq"] == "C4 D4 E4"
        assert ds["note_dur"] == "1.0 0.5 0.75"
        assert ds["note_slur"] == "0 0 0"
        assert ds["input_type"] == "phoneme"
