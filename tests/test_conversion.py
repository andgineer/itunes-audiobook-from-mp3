from unittest.mock import Mock

import pytest

from audiobook_tags.tags import fix_encoding, process_files


def test_fix_encoding():
    assert fix_encoding("abc", fix_encoding="cp1251") == "abc"

    assert fix_encoding("abc", fix_encoding="none") == "abc"

    with pytest.raises(LookupError):
        fix_encoding("abc", fix_encoding="invalid_encoding")


def test_fix_mp3_tags_real_mp3(opts):
    audio_files = process_files(
        Mock(
            folder="tests/resources/",
            encoding="cp1251",
            mask=".mp3",
            set_tag="tag1/value1",
            set_tags={"tag1": "value1"},
            track_num="name",
            title_prefix="test_prefix - ",
            dry=True,
        )
    )
    assert len(audio_files) == 1
    assert audio_files[0].tag.artist == "Ф. М. Достоевский"
    assert (
        audio_files[0].tag.title
        == "test_prefix - БРАТЬЯ КАРАМАЗОВЫ. Часть 2. Книга 04. Глава 02. Фрагмент 01"
    )
    assert audio_files[0].tag.album == "Mp3-КНИГА"
    assert audio_files[0].tag.tag1 == "value1"
