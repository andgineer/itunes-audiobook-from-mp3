"""Fix audiobook tags in mp3 files."""

import pathlib
from argparse import Namespace
from typing import TYPE_CHECKING, Optional, cast

import eyed3
import eyed3.id3
from eyed3 import AudioFile

if TYPE_CHECKING:
    from eyed3.id3 import Tag

OPT_ENCODING_NO_ENCODING: str = "none"
OPT_TRACK_NUM_BY_TAG_TITLE: str = "tag-"
OPT_TRACK_NUM_BY_FILE_NAMES: str = "name"

GENRE_AUDIOBOOK: int = 183  # ID3 genre ID for Audiobook


def _print_file_list(paths: list[pathlib.Path], verbose: bool) -> None:
    """Print list of files to process in verbose mode."""
    if verbose:
        print(f"Found {len(paths)} files to process:")
        for i, path in enumerate(paths, 1):
            print(f"  {i:3d}. {path}")
        print()


def _print_summary(
    paths: list[pathlib.Path],
    successful_files: list[AudioFile],
    failed_files: list[tuple[pathlib.Path, str]],
    opts: Namespace,
) -> None:
    """Print processing summary."""
    total_files = len(paths)
    if total_files == 0:
        print(f"(!) No files were found in folder `{opts.folder}` with suffix {opts.suffix}.")
    elif failed_files:
        print(f"(!) {len(failed_files)} of {total_files} files failed to process.")
        if opts.verbose:
            print("Failed files:")
            for file_path, error in failed_files:
                print(f"  - {file_path}: {error}")
        if not opts.dry:
            print("Successfully processed files were saved.")
    elif opts.dry:
        print(f"(!) Dry run. {len(successful_files)} files would be modified.")
    else:
        print(f"Successfully processed {len(successful_files)} files.")
        if opts.verbose and successful_files:
            print("Successfully processed files:")
            for audio_file in successful_files:
                print(f"  ✓ {audio_file.path}")


def process_files(opts: Namespace) -> list[AudioFile]:
    """Scan files and fix mp3 tags."""
    paths = get_files_list(opts.folder, opts.suffix, opts.track_num, opts.verbose)
    successful_files: list[AudioFile] = []
    failed_files: list[tuple[pathlib.Path, str]] = []
    track: int = 1

    _print_file_list(paths, opts.verbose)

    for file_path in paths:
        try:
            audio_file = fix_file_tags(file_path, opts, track)
            successful_files.append(audio_file)
            track += 1  # Only increment on success
        except Exception as e:  # noqa: BLE001
            print(f"Error processing {file_path}: {e}")
            failed_files.append((file_path, str(e)))

    _print_summary(paths, successful_files, failed_files, opts)

    # Only save successful files
    if not opts.dry and successful_files:
        for audio_file in successful_files:
            if audio_file.tag is not None:
                tag = cast("Tag", audio_file.tag)
                tag.save(version=eyed3.id3.ID3_DEFAULT_VERSION, encoding="utf-8")

    return successful_files


def fix_file_tags(file_path: pathlib.Path, opts: Namespace, track: int) -> AudioFile:
    """Fix tags for one file."""
    audio_file = eyed3.load(file_path)
    if audio_file is None or audio_file.tag is None:
        raise ValueError(f"Failed to load audio file or tag: {file_path}")

    # Cast to id3.Tag to give type checker access to id3-specific attributes
    tag = cast("Tag", audio_file.tag)

    if opts.verbose:
        print(f"Processing: {file_path}")
        print(f"  Original title: {tag.title}")
    else:
        print(file_path, tag.title)

    tag.genre = GENRE_AUDIOBOOK
    # tag.compilation = '1'
    # tag.images.set(3, open('cover.jpg','rb').read(), 'image/jpeg')

    for tag_name in opts.set_tags:
        setattr(tag, tag_name, opts.set_tags[tag_name])
    for tag_name in ["artist", "title", "album", "album_artist"]:
        if tag_name not in opts.set_tags and getattr(tag, tag_name):
            setattr(
                tag,
                tag_name,
                fix_encoding(getattr(tag, tag_name), opts.encoding),
            )

    if opts.track_num:
        # Assign as int; eyeD3 converts to CountAndTotalTuple automatically
        tag.track_num = track  # type: ignore[assignment]
        tag.title = (opts.title_prefix + "{name}").format(
            name=tag.title,
            track=track,
        )
        track += 1

    if opts.verbose:
        print(f"  Updated title: {tag.title}")
        print(f"  Artist: {tag.artist}")
        print(f"  Album: {tag.album} by {tag.album_artist}")
        print(f"  Genre: {tag.genre}")
        if opts.track_num:
            print(f"  Track: {tag.track_num}")
        print()
    else:
        print(f"--> {tag.title} ", end="")
        if opts.track_num:
            print(
                f"by {tag.artist}, album {tag.album} by {tag.album_artist}, genre {tag.genre}",
            )
        print()
    return audio_file


def get_files_list(
    folder: str,
    suffix: str,
    track_num: Optional[str],
    verbose: bool = False,
) -> list[pathlib.Path]:
    """Load audio files filtered by extension.

    Sort files according `track_num` option.
    """
    paths: list[pathlib.Path] = list(pathlib.Path(folder).glob(f"**/*.{suffix}"))

    if verbose:
        print(f"Scanning folder: {folder}")
        print(f"Looking for files with suffix: {suffix}")

    if track_num:
        if track_num == OPT_TRACK_NUM_BY_FILE_NAMES:
            if verbose:
                print("Sorting files by name...")
            paths = sorted(paths)
        elif track_num.startswith(OPT_TRACK_NUM_BY_TAG_TITLE):
            tag_name: str = track_num[len(OPT_TRACK_NUM_BY_TAG_TITLE) :]
            if verbose:
                print(f"Sorting files by tag: {tag_name}...")

            def get_tag_value(path: pathlib.Path) -> str:
                audio = eyed3.load(path)
                if audio is None or audio.tag is None:
                    return ""
                return str(getattr(audio.tag, tag_name, ""))

            paths = sorted(paths, key=get_tag_value)
        else:
            raise ValueError(f"Unknown track_num option: {track_num}")
    return paths


def fix_encoding(text: str, fix_encoding: str) -> str:
    """Decode from specified in CLI encoding."""
    if fix_encoding.lower() != OPT_ENCODING_NO_ENCODING.lower():
        try:
            text = text.encode("latin_1").decode(fix_encoding)
        except UnicodeEncodeError as e:
            print(text)
            print(e)
    return text
