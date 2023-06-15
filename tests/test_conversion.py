from unittest.mock import Mock, patch

import pytest

from itunes_audiobook_from_mp3 import fix_encoding, fix_mp3_tags


def test_fix_encoding():
    assert fix_encoding("abc", fix_encoding="cp1251") == "abc"

    assert fix_encoding("abc", fix_encoding="none") == "abc"

    with pytest.raises(LookupError):
        fix_encoding("abc", fix_encoding="invalid_encoding")


@patch("itunes_audiobook_from_mp3.eyed3.load")
@patch("os.walk")
def test_fix_mp3_tags_mock(mock_os_walk, mock_eyed3_load, opts):
    mock_os_walk.return_value = [("dir", [], ["file1.mp3"])]
    mock_audio_file = Mock()
    tag = Mock(artist="Artist", title="Title", album="Album", album_artist="Album Artist")
    mock_audio_file.tag = tag
    mock_eyed3_load.return_value = mock_audio_file
    fix_mp3_tags(opts)
    assert mock_audio_file.tag.artist


def test_fix_mp3_tags_real_mp3(opts):
    audio_files = fix_mp3_tags(
        Mock(
            folder="tests/resources",
            encoding="cp1251",
            extension=".mp3",
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
