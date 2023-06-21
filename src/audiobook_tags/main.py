import sys
from argparse import ArgumentParser, Namespace
from typing import Tuple

from audiobook_tags.tags import (
    OPT_ENCODING_NO_ENCODING,
    OPT_TRACK_NUM_BY_FILE_NAMES,
    OPT_TRACK_NUM_BY_TAG_TITLE,
    process_files,
)

DEFAULT_ENCODING = "cp1251"
FILE_MASK = ".mp3"


def get_opts() -> Tuple[Namespace, ArgumentParser]:
    """Get CLI options."""
    parser = ArgumentParser(description="Fixes mp3 tags for iOS audiobooks.")
    parser.add_argument(
        "folder",
        default=".",
        metavar="folder",
        nargs="?",
        help="Folder to process. By default current folder.",
    )
    parser.add_argument(
        "--mask",
        "-m",
        default=FILE_MASK,
        dest="mask",
        help=f"Files mask. By default {FILE_MASK}",
    )
    parser.add_argument(
        "--encoding",
        "-e",
        default=DEFAULT_ENCODING,
        dest="encoding",
        help=f'mp3 tags encoding. "{OPT_ENCODING_NO_ENCODING}" if you do not need mp3 tags encoding fix. By default "{DEFAULT_ENCODING}".',
    )
    parser.add_argument(
        "--tag",
        "-t",
        default=None,
        dest="set_tag",
        nargs="*",
        help='Change mp3 tag to specified string. Format "tag-name/tag-value".',
    )
    parser.add_argument(
        "--num",
        "-n",
        default=None,
        dest="track_num",
        help=(
            f"""Sort files and set mp3 tag `track_num`:
            TRACK_NUM=`{OPT_TRACK_NUM_BY_FILE_NAMES}` - sort by names;
            TRACK_NUM=`{OPT_TRACK_NUM_BY_TAG_TITLE}<TAG>` - sort by mp3 tag with name <TAG>."""
        ),
    )
    parser.add_argument(
        "--prefix",
        "-p",
        default=None,
        dest="title_prefix",
        help="Add prefix to title tags. By default `{track:04} - ` if `--num` and no prefix if not.",
    )
    parser.add_argument(
        "--dry",
        "-d",
        dest="dry",
        action="store_true",
        default=False,
        help="Dry run without changing files.",
    )
    opts, _ = parser.parse_known_args()
    opts.set_tags = {}
    if opts.set_tag:
        for tag_string in opts.set_tag:
            opts.set_tags[tag_string.split("/")[0]] = tag_string.split("/")[1]
    if opts.title_prefix is None:
        opts.title_prefix = "{track:04} - " if opts.track_num else ""
    return opts, parser


def main() -> None:
    """Do the work."""
    opts, parser = get_opts()
    try:
        process_files(opts)
    except ValueError as e:
        print(f"\nError: {e}\n")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
