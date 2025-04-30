def validate_ds(ds_dict):
    """
    Ensure that the DS dictionary has all required fields
    and that fields have the correct types and format.
    """
    required_fields = ["ph_seq", "ph_num", "note_seq", "note_dur", "note_slur", "input_type"]

    for field in required_fields:
        if field not in ds_dict:
            raise ValueError(f"Missing required field '{field}' in DS file.")

    if not isinstance(ds_dict["ph_seq"], str):
        raise TypeError("Field 'ph_seq' must be a string (space-separated phonemes).")
    if not isinstance(ds_dict["ph_num"], str):
        raise TypeError("Field 'ph_num' must be a string (space-separated integers).")
    if not isinstance(ds_dict["note_seq"], str):
        raise TypeError("Field 'note_seq' must be a string (space-separated note names).")
    if not isinstance(ds_dict["note_dur"], str):
        raise TypeError("Field 'note_dur' must be a string (space-separated floats).")
    if not isinstance(ds_dict["note_slur"], str):
        raise TypeError("Field 'note_slur' must be a string (space-separated 0/1).")
    if not isinstance(ds_dict["input_type"], str):
        raise TypeError("Field 'input_type' must be a string.")
