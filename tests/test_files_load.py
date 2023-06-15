from unittest.mock import MagicMock, patch

from itunes_audiobook_from_mp3 import (
    OPT_TRACK_NUM_BY_FILE_NAMES,
    OPT_TRACK_NUM_BY_TAG_TITLE,
    fix_mp3_tags,
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
    with patch("itunes_audiobook_from_mp3.pathlib.Path.glob", return_value=["ba.mp3", "ab.mp3"]):
        with patch("eyed3.load") as mock_load:
            mock_load.side_effect = eye3d_load
            audio_files = fix_mp3_tags(opts)
            assert len(audio_files) == 2
            assert audio_files[0].path == "ba.mp3"
            assert audio_files[1].path == "ab.mp3"


def test_fix_mp3_tags_sorted_by_file_names(opts):
    opts.track_num = OPT_TRACK_NUM_BY_FILE_NAMES
    with patch("itunes_audiobook_from_mp3.pathlib.Path.glob", return_value=["ba.mp3", "ab.mp3"]):
        with patch("eyed3.load") as mock_load:
            mock_load.side_effect = eye3d_load
            audio_files = fix_mp3_tags(opts)
            assert len(audio_files) == 2
            assert audio_files[0].path == "ab.mp3"
            assert audio_files[1].path == "ba.mp3"


def test_fix_mp3_tags_sorted_by_tag_title(opts):
    opts.track_num = f"{OPT_TRACK_NUM_BY_TAG_TITLE}title"
    with patch("itunes_audiobook_from_mp3.pathlib.Path.glob", return_value=["ba.mp3", "ab.mp3"]):
        with patch("eyed3.load") as mock_load:
            mock_load.side_effect = eye3d_load
            audio_files = fix_mp3_tags(opts)
            assert len(audio_files) == 2
            assert audio_files[0].path == "ab.mp3"
            assert audio_files[1].path == "ba.mp3"
