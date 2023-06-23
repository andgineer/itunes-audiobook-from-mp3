[![Build Status](https://github.com/andgineer/itunes-audiobook-from-mp3/workflows/ci/badge.svg)](https://github.com/andgineer/itunes-audiobook-from-mp3/actions)
# Audiobooks from mp3 with broken tags

Fix mp3 files tags to convert them into iTunes/iPhone audiobooks..

- Fixes sort order.
- Supports messed encoding like cyrillic Win1251.

Details in [my blog's article](https://sorokin.engineer/posts/en/itunes_audiobook_from_mp3.html).

## Installation

You should have Python installed.

    python -m pip install audiobook-tags

## Usage
    audiobook-tags [-h] [--encoding ENCODING] [--extension EXTENSION] [--set-tag [SET_TAG ...]] [--track-num TRACK_NUM] [--title-prefix TITLE_PREFIX] [--dry] [folder]

    Fixes mp3 tags for iOS audiobooks.

    positional arguments:
      folder                Folder to process. By default current folder.

    options:
      -h, --help            show this help message and exit
      --suffix SUFFIX, -s SUFFIX
                            Files suffix. By default mp3
      --encoding ENCODING, -e ENCODING
                            mp3 tags encoding. "none" if you do not need mp3 tags encoding fix. By default "cp1251".
      --tag [SET_TAG ...], -t [SET_TAG ...]
                            Change mp3 tag to specified string. Format "tag-name/tag-value".
      --num TRACK_NUM, -n TRACK_NUM
                            Sort files and set mp3 tag `track_num`:
                              --num="name" - sort by names;
                              --num="tag-<TAG>" - sort by mp3 tag with name <TAG>.
                                For example to sort by title tag use --num="tag-title".
      --prefix TITLE_PREFIX, -p TITLE_PREFIX
                            Add prefix to title tags. By default `{track:04} - ` if `--num` and no prefix if not.
      --dry, -d             Dry run without changing files.

## Example:

    audiobook-tags --tag="album_artist/Юрий Заборовский (Ардис)" --num="name" --prefix=""

- converts all `mp3` files in current folder and subfolders
- fix encoding supposing that original encoding was `Windows 1251`
- change tag album artist.
- set `track_num` mp3 tag to file number as ordered by file name.
  But do not add the track number to the title (`--prefix="""`).

# Development

### OS Dependencies

#### MacOS

  brew update
  brew install libmagic

### Python dependencies

Note the dot before `./activate.sh`:

  . ./activate.sh

We use [eyeD3](https://eyed3.readthedocs.io/en/latest/) to work with mp3 tags.
