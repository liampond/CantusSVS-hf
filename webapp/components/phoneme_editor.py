# webapp/components/phoneme_editor.py
from typing import List, Dict
import streamlit as st
from webapp.services.phonemes.phoneme_dict import PHONEMES


def default_phoneme_for_lyric(lyric: str) -> str:
    """
    Simple rule-based default phoneme suggestion for a lyric syllable.

    - Direct match if the lyric exactly matches a phoneme
    - Greedy two-letter prefix match
    - Single-letter fallback
    - Default to 'a'
    """
    l = lyric.lower()
    if l in PHONEMES:
        return l
    if len(l) >= 2 and l[:2] in PHONEMES:
        return l[:2]
    if l and l[0] in PHONEMES:
        return l[0]
    return "a"


def render_phoneme_editor(notes: List[Dict]) -> List[Dict]:
    """
    Display an editable phoneme alignment table in Streamlit, including duration edits.

    Args:
        notes: list of dicts each containing:
            - id: unique identifier
            - pitch: pitch string (e.g. "C4")
            - duration: float, original duration in seconds
            - lyric: string, the syllable/lyric text
            - is_slur: int (0 or 1)
    Returns:
        List of dicts with updated 'duration', 'phoneme', and 'is_slur' fields:
    """
    st.header("2. Phoneme & Duration Alignment")
    st.write("Adjust duration and select phoneme for each note:")

    edited_notes: List[Dict] = []
    for note in notes:
        # Columns: Pitch, Duration input, Lyric, Phoneme select, Slur checkbox
        cols = st.columns([1, 1.2, 1, 2, 1])
        cols[0].markdown(f"**Pitch:** {note['pitch']}")
        # Editable duration
        duration = cols[1].number_input(
            label="Dur (s)",
            min_value=0.0,
            value=note['duration'],
            step=0.01,
            format="%.3f",
            key=f"dur_{note['id']}"
        )
        cols[2].markdown(f"**Lyric:** {note['lyric']}")

        # Default phoneme suggestion
        default = default_phoneme_for_lyric(note['lyric'])
        default_idx = PHONEMES.index(default) if default in PHONEMES else 0
        phoneme = cols[3].selectbox(
            label="Phoneme",
            options=PHONEMES,
            index=default_idx,
            key=f"phoneme_{note['id']}"
        )

        # Slur toggle
        is_slur = cols[4].checkbox(
            label="Slur",
            value=bool(note.get('is_slur', 0)),
            key=f"slur_{note['id']}"
        )

        edited_notes.append({
            **note,
            "duration": duration,
            "phoneme": phoneme,
            "is_slur": int(is_slur)
        })

    return edited_notes
