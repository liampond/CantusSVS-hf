import json
from pathlib import Path

def build_ds_from_notes(notes_with_phoneme, output_path: Path):
    """
    Build a DiffSinger-compatible .ds JSON file from note-level data with user-specified phonemes.

    Args:
        notes_with_phoneme: List of dicts, each containing:
            - "pitch": str (e.g. "C4")
            - "duration": float
            - "phoneme": str
            - optional "is_slur": int
        output_path: Path where the .ds file will be written
    """
    # Extract sequences
    note_seq = [note['pitch'] for note in notes_with_phoneme]
    note_dur = [note['duration'] for note in notes_with_phoneme]
    ph_seq = [note['phoneme'] for note in notes_with_phoneme]
    # Default slur sequence to 0 if not provided
    note_slur = [note.get('is_slur', 0) for note in notes_with_phoneme]

    ds_input = {
        "ph_seq": " ".join(ph_seq),
        "ph_num": " ".join(["1"] * len(ph_seq)),  # ← 🔥 ph_num must be a string of 1s
        "note_seq": " ".join(note_seq),
        "note_dur": " ".join(str(d) for d in note_dur),  # ← 🔥 note_dur, not note_dur_seq
        "note_slur": " ".join(str(s) for s in note_slur),  # ← 🔥 note_slur, not is_slur_seq
        "input_type": "phoneme"
    }

    # Write JSON file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(ds_input, f, indent=2)
