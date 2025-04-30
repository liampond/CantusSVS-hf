# inference/ds_generator.py
import json

def build_ds_input(parsed, output_path):
    inp = {
        "text": parsed["lyrics"],
        "note_seq": " ".join(parsed["notes"]),
        "note_dur_seq": " ".join(str(d) for d in parsed["durations"]),
        "is_slur_seq": " ".join(str(s) for s in parsed["is_slur_seq"]),
        "input_type": "word"
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(inp, f, indent=2)
