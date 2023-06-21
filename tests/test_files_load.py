from unittest.mock import MagicMock, patch

import pytest

from audiobook_tags.tags import (
    OPT_TRACK_NUM_BY_FILE_NAMES,
    OPT_TRACK_NUM_BY_TAG_TITLE,
    process_files,
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
