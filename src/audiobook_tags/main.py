import sys
from argparse import ArgumentParser, Namespace
from typing import Tuple

from audiobook_tags.tags import (
    OPT_ENCODING_NO_ENCODING,
    OPT_TRACK_NUM_BY_FILE_NAMES,
    OPT_TRACK_NUM_BY_TAG_TITLE,
    fix_mp3_tags,
)


def get_opts() -> Tuple[Namespace, ArgumentParser]:
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
    parser.add_argument(
        "--extension",
        default=".mp3",
        dest="extension",
        help="File" "s extension including dot, for example `.mp3`.",
    )
    parser.add_argument(
        "--set-tag",
        default=None,
        dest="set_tag",
        nargs="*",
        help='Change mp3 tag to specified string. Format "tag-name/tag-value".',
    )
    parser.add_argument(
        "--track-num",
        default=None,
        dest="track_num",
        help=(
            f"""Sort files and set mp3 tag `track_num`:
            TRACK_NUM=`{OPT_TRACK_NUM_BY_FILE_NAMES}` - sort by names;
            TRACK_NUM=`{OPT_TRACK_NUM_BY_TAG_TITLE}<TAG>` - sort by mp3 tag with name <TAG>."""
        ),
    )
    parser.add_argument(
        "--title-prefix",
        default="{track:04} - ",
        dest="title_prefix",
        help="Prefix each file title with the track number for the file.",
    )
    parser.add_argument(
        "--dry",
        dest="dry",
        action="store_true",
        default=False,
        help="Dry run without changing files.",
    )
    opts, _ = parser.parse_known_args()
    opts.set_tags = {}
    if opts.set_tag:
        for tag_string in opts.set_tag:
            opts.set_tags.update({tag_string.split("/")[0]: tag_string.split("/")[1]})
    return opts, parser


def main() -> None:
    """Do the work."""
    opts, parser = get_opts()
    try:
        fix_mp3_tags(opts)
    except ValueError as e:
        print(f"\nError: {e}\n")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
