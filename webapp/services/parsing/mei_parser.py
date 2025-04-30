from pathlib import Path
from inference.mei_parser import parse_mei as _parse_mei_raw


def parse_mei_for_editor(mei_path: Path, tempo: int = 120):
    """
    Parse the MEI file and return a list of note dicts for phoneme editing:

    [
        {
            "id": str,       # a unique note identifier
            "pitch": str,    # e.g., "C4"
            "duration": float,# duration in seconds
            "lyric": str     # the syllable text for this note
        },
        ...
    ]
    """
    # Use the existing parse_mei to get raw sequences
    raw = _parse_mei_raw(mei_path, tempo)
    notes = raw.get("notes", [])
    durations = raw.get("durations", [])
    # parse_mei returns lyrics as a space-separated string
    syllables = raw.get("lyrics", "").split()

    notes_for_editor = []
    for idx, (pitch, dur, lyric) in enumerate(zip(notes, durations, syllables)):
        note_id = f"note_{idx}"
        notes_for_editor.append({
            "id": note_id,
            "pitch": pitch,
            "duration": dur,
            "lyric": lyric,
        })

    return notes_for_editor
