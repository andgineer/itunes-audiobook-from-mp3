"""Fix audiobook tags in mp3 files."""

import pathlib
from argparse import Namespace
from typing import List, Optional

import eyed3
from eyed3 import AudioFile

OPT_ENCODING_NO_ENCODING = "none"
OPT_TRACK_NUM_BY_TAG_TITLE = "tag-"
OPT_TRACK_NUM_BY_FILE_NAMES = "name"


def process_files(opts: Namespace) -> List[AudioFile]:
    """Scan files and fix mp3 tags."""
    paths = get_files_list(opts.folder, opts.suffix, opts.track_num)
    result = []
    track = 1
    for file_path in paths:
        try:
            audio_file = fix_file_tags(file_path, opts, track)
            result.append(audio_file)
        except Exception as e:  # pylint: disable=broad-except
            print(f"Error processing {file_path}: {e}")
    if not result:
        print(
            f"(!) No files were found in folder `{opts.folder}` with suffix {opts.suffix}."
        )
    elif any(isinstance(file, Exception) for file in result):
        print("(!) Errors occurred. No files were changed.")
    elif opts.dry:
        print("(!) Dry run. No files were changed.")
    else:
        for audio_file in result:
            audio_file.tag.save(version=eyed3.id3.ID3_DEFAULT_VERSION, encoding="utf-8")
    return result


def fix_file_tags(file_path: pathlib.Path, opts: Namespace, track: int) -> AudioFile:
    """Fix tags for one file."""
    audio_file = eyed3.load(file_path)
    print(file_path, audio_file.tag.title)

    audio_file.tag.genre = "Audiobook"
    audio_file.tag.mediatype = "Audiobook"
    # audio_file.tag.compilation = '1'
    # audiofile.tag.images.set(3, open('cover.jpg','rb').read(), 'image/jpeg')

    for tag_name in opts.set_tags:
        setattr(audio_file.tag, tag_name, opts.set_tags[tag_name])
    for tag_name in ["artist", "title", "album", "album_artist"]:
        if tag_name not in opts.set_tags and getattr(audio_file.tag, tag_name):
            setattr(
                audio_file.tag,
                tag_name,
                fix_encoding(getattr(audio_file.tag, tag_name), opts.encoding),
            )

    if opts.track_num:
        audio_file.tag.track_num = track
        audio_file.tag.part = f"{track:04d}"
        audio_file.tag.chapter = track
        audio_file.tag.title = (opts.title_prefix + "{name}").format(
            name=audio_file.tag.title, track=track
        )
        track += 1
    print(f"--> {audio_file.tag.title} ", end="")
    if opts.track_num:
        print(
            f"by {audio_file.tag.artist}, "
            f"album {audio_file.tag.album} by {audio_file.tag.album_artist}, "
            f"genre {audio_file.tag.genre}, part {audio_file.tag.part}"
        )
    print()
    return audio_file


def get_files_list(
    folder: str, suffix: str, track_num: Optional[str]
) -> List[pathlib.Path]:
    """Load audio files filtered by extension.

    Sort files according `track_num` option.
    """
    paths = list(pathlib.Path(folder).glob(f"**/*.{suffix}"))
    if track_num:
        if track_num == OPT_TRACK_NUM_BY_FILE_NAMES:
            paths = sorted(paths)
        elif track_num.startswith(OPT_TRACK_NUM_BY_TAG_TITLE):
            tag_name = track_num[len(OPT_TRACK_NUM_BY_TAG_TITLE) :]
            paths = sorted(
                paths, key=lambda path: getattr(eyed3.load(path).tag, tag_name)
            )
        else:
            raise ValueError(f"Unknown track_num option: {track_num}")
    return paths


def fix_encoding(text: str, fix_encoding: str) -> str:  # pylint: disable=redefined-outer-name
    """Decode from specified in CLI encoding."""
    if fix_encoding.lower() != OPT_ENCODING_NO_ENCODING.lower():
        try:
            text = text.encode("latin_1").decode(fix_encoding)
        except UnicodeEncodeError as e:
            print(text)
            print(e)
    return text
