"""Fix audiobook tags in mp3 files."""

import pathlib
from argparse import Namespace
from typing import Optional

import eyed3
from eyed3 import AudioFile

OPT_ENCODING_NO_ENCODING: str = "none"
OPT_TRACK_NUM_BY_TAG_TITLE: str = "tag-"
OPT_TRACK_NUM_BY_FILE_NAMES: str = "name"


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
            audio_file.tag.save(version=eyed3.id3.ID3_DEFAULT_VERSION, encoding="utf-8")

    return successful_files


def fix_file_tags(file_path: pathlib.Path, opts: Namespace, track: int) -> AudioFile:
    """Fix tags for one file."""
    audio_file: AudioFile = eyed3.load(file_path)
    if opts.verbose:
        print(f"Processing: {file_path}")
        print(f"  Original title: {audio_file.tag.title}")
    else:
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
            name=audio_file.tag.title,
            track=track,
        )
        track += 1

    if opts.verbose:
        print(f"  Updated title: {audio_file.tag.title}")
        print(f"  Artist: {audio_file.tag.artist}")
        print(f"  Album: {audio_file.tag.album} by {audio_file.tag.album_artist}")
        print(f"  Genre: {audio_file.tag.genre}")
        if opts.track_num:
            print(f"  Track: {audio_file.tag.track_num}, Part: {audio_file.tag.part}")
        print()
    else:
        print(f"--> {audio_file.tag.title} ", end="")
        if opts.track_num:
            print(
                f"by {audio_file.tag.artist}, "
                f"album {audio_file.tag.album} by {audio_file.tag.album_artist}, "
                f"genre {audio_file.tag.genre}, part {audio_file.tag.part}",
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
            paths = sorted(
                paths,
                key=lambda path: getattr(eyed3.load(path).tag, tag_name),
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
