from unittest.mock import Mock, patch

from audiobook_tags.main import get_opts, main

import pytest


@patch("audiobook_tags.main.process_files")
@patch("audiobook_tags.main.get_opts")
def test_main(mock_get_opts, mock_fix_mp3_tags):
    mock_get_opts.return_value = (Mock(), Mock())
    main()
    assert mock_get_opts.called
    assert mock_fix_mp3_tags.called


def test_get_opts():
    with patch(
        "argparse.ArgumentParser.parse_known_args",
        return_value=(
            Mock(
                folder="test_folder",
                encoding="cp1251",
                suffix="mp3",
                set_tag=["tag1/value1", "tag2/value2"],
                track_num="name",
                title_prefix="test_prefix - ",
                dry=True,
            ),
            [],
        ),
    ):
        opts, _ = get_opts()
        assert opts.set_tags == {"tag1": "value1", "tag2": "value2"}


@patch("audiobook_tags.main.process_files")
@patch("audiobook_tags.main.get_opts")
def test_main_success(mock_get_opts, mock_process_files):
    mock_get_opts.return_value = (Mock(), Mock())
    main()
    assert mock_get_opts.called
    assert mock_process_files.called


@patch("audiobook_tags.main.process_files")
@patch("audiobook_tags.main.get_opts")
def test_main_value_error(mock_get_opts, mock_process_files):
    mock_get_opts.return_value = (Mock(), Mock())
    mock_process_files.side_effect = ValueError("Test error")
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 1


def test_get_opts_default_values():
    with patch("sys.argv", ["script.py"]):
        opts, _ = get_opts()
        assert opts.folder == "."
        assert opts.suffix == "mp3"
        assert opts.encoding == "cp1251"
        assert opts.set_tag is None
        assert opts.track_num is None
        assert opts.title_prefix == ""
        assert not opts.dry
        assert opts.set_tags == {}


def test_get_opts_invalid_tag_format():
    with patch("sys.argv", ["script.py", "--tag", "invalid_format"]):
        with pytest.raises(IndexError):
            get_opts()


@pytest.mark.parametrize(
    "track_num,expected_prefix",
    [
        (None, ""),
        ("name", "{track:04} - "),
    ],
)
def test_get_opts_title_prefix(track_num, expected_prefix):
    with patch("sys.argv", ["script.py"] + (["--num", track_num] if track_num else [])):
        opts, _ = get_opts()
        assert opts.title_prefix == expected_prefix
