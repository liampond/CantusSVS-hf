import pytest
from webapp.services.parsing.ds_validator import validate_ds

def test_validate_ds_valid():
    # Arrange
    valid_ds = {
        "ph_seq": "k d e",
        "ph_num": "1 1 1",
        "note_seq": "C4 D4 E4",
        "note_dur": "1.0 0.5 0.75",
        "note_slur": "0 0 0",
        "input_type": "phoneme",
    }

    # Act + Assert (no exception means pass)
    validate_ds(valid_ds)

def test_validate_ds_missing_field():
    # Arrange
    invalid_ds = {
        "ph_seq": "k d e",
        # "ph_num" missing
        "note_seq": "C4 D4 E4",
        "note_dur": "1.0 0.5 0.75",
        "note_slur": "0 0 0",
        "input_type": "phoneme",
    }

    # Act + Assert
    with pytest.raises(ValueError, match="Missing required field 'ph_num'"):
        validate_ds(invalid_ds)

def test_validate_ds_wrong_type():
    # Arrange
    invalid_ds = {
        "ph_seq": "k d e",
        "ph_num": 3,  # should be a string!
        "note_seq": "C4 D4 E4",
        "note_dur": "1.0 0.5 0.75",
        "note_slur": "0 0 0",
        "input_type": "phoneme",
    }

    # Act + Assert
    with pytest.raises(TypeError, match="Field 'ph_num' must be a string"):
        validate_ds(invalid_ds)
