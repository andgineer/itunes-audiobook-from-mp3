import os
from argparse import ArgumentParser, Namespace
from typing import List

import eyed3
import eyed3.id3
from eyed3 import AudioFile

OPT_ENCODING_NO_ENCODING = "none"
OPT_TRACK_NUM_NO_TRACK_NUM = "none"
OPT_TRACK_NUM_BY_FILE_NAMES = ""


def fix_encoding(text: str, fix_encoding: str) -> str:
    """Decode from specifyed in CLI encoding."""
    if fix_encoding.lower() != OPT_ENCODING_NO_ENCODING.lower():
        try:
            text = text.encode("latin_1").decode(fix_encoding)
        except UnicodeEncodeError as e:
            print(text)
            print(e)
    return text


def get_opts() -> Namespace:
    """Get CLI options."""
    parser = ArgumentParser(description="Fixes mp3 tags for iOS audiobooks.")
    parser.add_argument(
        "folder",
        default=".",
        metavar="folder",
        nargs="?",
        help="Folder to process, do not add file name.",
    )
    parser.add_argument(
        "--encoding",
        default="cp1251",
        dest="encoding",
        help=f'mp3 tags encoding. "{OPT_ENCODING_NO_ENCODING}" if you do not need mp3 tags encoding fix.',
    )
    parser.add_argument("--extension", default="mp3", dest="extension", help="File" "s extension.")
    parser.add_argument(
        "--set-tag",
        default=None,
        dest="set_tag",
        nargs="*",
        help='Change mp3 tag to specified string. Format "tag-name/tag-value".',
    )
    parser.add_argument(
        "--track-num",
        default="sort-file-names",
        dest="track_num",
        help=(
            f"""Set mp3 tag `track_num` as specified.
            - {OPT_TRACK_NUM_BY_FILE_NAMES} - file number for files sorted by names.
            Use {OPT_TRACK_NUM_NO_TRACK_NUM} if you do not want to set this tag."""
        ),
    )
    parser.add_argument(
        "--title-prefix",
        default="{track:04} - ",
        dest="title_prefix",
        help="Prefix each file title with the track number for the file.",
    )
    parser.add_argument("--dry", dest="dry", help="Just dry run without files fix.")
    opts, _ = parser.parse_known_args()
    opts.set_tags = {}
    if opts.set_tag:
        for tag_string in opts.set_tag:
            opts.set_tags.update({tag_string.split("/")[0]: tag_string.split("/")[1]})
    return opts


def fix_mp3_tags(opts: Namespace) -> List[AudioFile]:
    """Fix mp3 tags."""
    paths = []
    for subdir, dirs, files in os.walk(opts.folder):
        for file_name in files:
            file_path = subdir + os.sep + file_name
            paths.append(file_path)

    if opts.track_num and opts.track_num == OPT_TRACK_NUM_BY_FILE_NAMES:
        paths = sorted(paths)  # Paths would be sorted in order as track number should increment

    result = []
    track = 1
    for file_path in paths:
        if file_path.endswith("." + opts.extension):
            try:
                audio_file = eyed3.load(file_path)
                print(file_path, audio_file.tag.title)
                for tag_name in opts.set_tags:
                    setattr(audio_file.tag, tag_name, opts.set_tags[tag_name])
                for tag_name in ["artist", "title", "album", "album_artist"]:
                    if tag_name not in opts.set_tags and getattr(audio_file.tag, tag_name):
                        setattr(
                            audio_file.tag,
                            tag_name,
                            fix_encoding(getattr(audio_file.tag, tag_name), opts.encoding),
                        )
                audio_file.tag.genre = "Audiobook"
                audio_file.tag.mediatype = "Audiobook"
                # audio_file.tag.compilation = '1'
                # audiofile.tag.images.set(3, open('cover.jpg','rb').read(), 'image/jpeg')
                if opts.track_num:
                    audio_file.tag.track_num = track
                    audio_file.tag.part = f"{track:04d}"
                    audio_file.tag.chapter = track
                    audio_file.tag.title = (opts.title_prefix + "{name}").format(
                        name=audio_file.tag.title, track=track
                    )
                    track += 1
                print(
                    f"--> {audio_file.tag.title} by {audio_file.tag.artist}, "
                    f"album {audio_file.tag.album} by {audio_file.tag.album_artist}, "
                    f"genre {audio_file.tag.genre}, part {audio_file.tag.part}"
                )
                if not opts.dry:
                    audio_file.tag.save(version=eyed3.id3.ID3_DEFAULT_VERSION, encoding="utf-8")
                result.append(audio_file)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                raise
    return result


def main() -> None:
    """Do the work."""
    opts = get_opts()
    fix_mp3_tags(opts)


if __name__ == "__main__":
    main()
