# inference/mei_parser.py
from lxml import etree

def parse_mei(mei_path, tempo=120):
    tree = etree.parse(str(mei_path))
    ns = {"mei": "http://www.music-encoding.org/ns/mei"}

    staff_defs = tree.xpath("//mei:staffDef", namespaces=ns)
    if len(staff_defs) != 1:
        raise ValueError(f"Expected exactly one staffDef (monophonic input), found {len(staff_defs)}.")

    notes = []
    syllables = []
    durations = []
    is_slur_seq = []

    quarter_duration = 60 / tempo

    for note in tree.xpath("//mei:staff//mei:note", namespaces=ns):
        pname = note.get("pname")
        octv = note.get("oct")
        dur = note.get("dur")
        syl_elem = note.find(".//mei:syl", namespaces=ns)

        if not pname or not octv or not dur:
            continue

        # Note name
        pitch = pname.upper() + octv
        notes.append(pitch)

        # Duration in seconds
        dur_val = int(dur)
        sec = 4 / dur_val * quarter_duration
        durations.append(round(sec, 6))

        # Syllable text
        if syl_elem is not None and syl_elem.text:
            syllables.append(syl_elem.text.strip())
            is_slur_seq.append(1 if syl_elem.get("con") == "d" else 0)
        else:
            syllables.append("a")
            is_slur_seq.append(0)

    return {
        "notes": notes,
        "durations": durations,
        "lyrics": " ".join(syllables),
        "is_slur_seq": is_slur_seq
    }
