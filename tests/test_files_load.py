from unittest.mock import MagicMock, patch, Mock

import pytest

from audiobook_tags.tags import (
    OPT_TRACK_NUM_BY_FILE_NAMES,
    OPT_TRACK_NUM_BY_TAG_TITLE,
    process_files,
    fix_file_tags,
    get_files_list,
)


def eye3d_load(file_path):
    mock_audio_file = MagicMock()
    mock_audio_file.path = file_path
    mock_audio_file.tag.title = file_path
    mock_audio_file.tag.artist = "an artist"
    mock_audio_file.tag.album = "an album"
    mock_audio_file.tag.album_artist = "an album artist"
    mock_audio_file.tag.genre = None
    mock_audio_file.tag.mediatype = None
    mock_audio_file.tag.track_num = None
    mock_audio_file.tag.part = None
    mock_audio_file.tag.chapter = None
    return mock_audio_file


def test_fix_mp3_tags_no_sorting(opts):
    with patch("audiobook_tags.tags.pathlib.Path.glob", return_value=["ba.mp3", "ab.mp3"]):
        with patch("eyed3.load") as mock_load:
            mock_load.side_effect = eye3d_load
            audio_files = process_files(opts)
            assert len(audio_files) == 2
            assert audio_files[0].path == "ba.mp3"
            assert audio_files[1].path == "ab.mp3"


@pytest.mark.parametrize(
    "track_num_option, expected_paths",
    [
        (OPT_TRACK_NUM_BY_FILE_NAMES, ["ab.mp3", "ba.mp3"]),
        (f"{OPT_TRACK_NUM_BY_TAG_TITLE}title", ["ab.mp3", "ba.mp3"]),
    ],
)
def test_fix_mp3_tags(opts, track_num_option, expected_paths):
    opts.track_num = track_num_option
    with patch("audiobook_tags.tags.pathlib.Path.glob", return_value=expected_paths):
        with patch("eyed3.load") as mock_load:
            mock_load.side_effect = eye3d_load
            audio_files = process_files(opts)
            assert len(audio_files) == len(expected_paths)
            assert all(
                audio_file.path == expected_path
                for audio_file, expected_path in zip(audio_files, expected_paths)
            )


def test_process_files_no_files(opts):
    with patch("audiobook_tags.tags.pathlib.Path.glob", return_value=[]):
        result = process_files(opts)
        assert result == []


def test_process_files_file_error(opts):
    with patch("audiobook_tags.tags.pathlib.Path.glob", return_value=["test.mp3"]):
        with patch("eyed3.load", side_effect=Exception("Test error")):
            result = process_files(opts)
            assert len(result) == 0


def test_fix_file_tags_with_errors():
    mock_audio_file = Mock()
    mock_audio_file.tag.title = "test"
    mock_audio_file.tag.artist = "test"
    mock_audio_file.tag.album = "test"
    mock_audio_file.tag.album_artist = "test"
    mock_audio_file.tag.genre = None

    with patch("eyed3.load", return_value=mock_audio_file):
        opts = Mock(
            set_tags={},
            encoding="cp1251",  # Using valid encoding
            track_num=None,
            title_prefix="",
        )
        result = fix_file_tags("test.mp3", opts, 1)
        assert result == mock_audio_file
        assert result.tag.genre == "Audiobook"


def test_fix_file_tags_invalid_encoding():
    mock_audio_file = Mock()
    mock_audio_file.tag.title = "test"
    mock_audio_file.tag.artist = "test"
    mock_audio_file.tag.album = None
    mock_audio_file.tag.album_artist = None

    with patch("eyed3.load", return_value=mock_audio_file):
        opts = Mock(set_tags={}, encoding="invalid_encoding", track_num=None, title_prefix="")
        with pytest.raises(LookupError):
            fix_file_tags("test.mp3", opts, 1)


def test_get_files_list_invalid_track_num():
    with pytest.raises(ValueError, match="Unknown track_num option: invalid"):
        get_files_list(".", "mp3", "invalid")
