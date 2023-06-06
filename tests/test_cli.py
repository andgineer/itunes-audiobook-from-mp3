from unittest.mock import Mock, patch
from itunes_audiobook_from_mp3 import fix_encoding, get_opts, fix_mp3_tags, main

@patch('itunes_audiobook_from_mp3.fix_mp3_tags')
@patch('itunes_audiobook_from_mp3.get_opts')
def test_main(mock_get_opts, mock_fix_mp3_tags):
    mock_get_opts.return_value = Mock()
    main()
    assert mock_get_opts.called
    assert mock_fix_mp3_tags.called


def test_get_opts():
    with patch('argparse.ArgumentParser.parse_known_args', return_value=(Mock(
            folder="test_folder",
            encoding="cp1251",
            extension="mp3",
            set_tag=["tag1/value1", "tag2/value2"],
            track_num="sort-file-names",
            title_prefix="test_prefix - ",
            dry=True
        ), [])):
        opts = get_opts()
        assert opts.set_tags == {"tag1": "value1", "tag2": "value2"}