import pytest
from unittest.mock import Mock, patch
from itunes_audiobook_from_mp3 import fix_encoding, get_opts, fix_mp3_tags

def test_fix_encoding():
    with patch('itunes_audiobook_from_mp3.opts', Mock(encoding="cp1251")):
        assert fix_encoding("abc") == "abc"

    with patch('itunes_audiobook_from_mp3.opts', Mock(encoding="none")):
        assert fix_encoding("abc") == "abc"

    with pytest.raises(LookupError):
        with patch('itunes_audiobook_from_mp3.opts', Mock(encoding="invalid_encoding")):
            fix_encoding("abc")

@patch('itunes_audiobook_from_mp3.eyed3.load')
@patch('os.walk')
def test_fix_mp3_tags(mock_os_walk, mock_eyed3_load):
    with patch('itunes_audiobook_from_mp3.opts', Mock(
            folder="test_folder",
            encoding="cp1251",
            extension="mp3",
            set_tags={"tag1": "value1"},
            track_num="sort-file-names",
            title_prefix="test_prefix - ",
            dry=True
        )):
        mock_os_walk.return_value = [("dir", [], ["file1.mp3"])]
        mock_audio_file = Mock()
        tag = Mock(artist='Artist', title='Title', album='Album', album_artist='Album Artist')
        mock_audio_file.tag = tag
        mock_eyed3_load.return_value = mock_audio_file
        fix_mp3_tags()
        assert mock_audio_file.tag.artist



