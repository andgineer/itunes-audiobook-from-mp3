[![Build Status](https://github.com/andgineer/itunes-audiobook-from-mp3/workflows/ci/badge.svg)](https://github.com/andgineer/itunes-audiobook-from-mp3/actions)
# Audiobooks from mp3 with broken tags

Fix mp3 files tags to convert them into iTunes/iPhone audiobooks..

- Fixes sort order.
- Supports messed encoding like cyrillic Win1251.

Details in [my blog's article](https://sorokin.engineer/posts/en/itunes_audiobook_from_mp3.html).

## Installation

You should have Python 3.6+ installed.

    pip install audiobook-tags

## Usage
    audiobook-tags [-h] [--encoding ENCODING] [--extension EXTENSION] [--set-tag [SET_TAG ...]] [--track-num TRACK_NUM] [--title-prefix TITLE_PREFIX] [--dry] [folder]

    Fixes mp3 tags for iOS audiobooks.

    positional arguments:
      folder                Folder to process, do not add file name.

    options:
      -h, --help            show this help message and exit
      --encoding ENCODING   mp3 tags encoding. "none" if you do not need mp3 tags encoding fix.
      --extension EXTENSION
                            Files extension including dot, for example `.mp3`.
      --set-tag [SET_TAG ...]
                            Change mp3 tag to specified string. Format "tag-name/tag-value".
      --track-num TRACK_NUM
                            Sort files and set mp3 tag `track_num`: TRACK_NUM=`name` - sort by names; TRACK_NUM=`tag-<TAG>` - sort by mp3 tag with name <TAG>.
      --title-prefix TITLE_PREFIX
                            Prefix each file title with the track number for the file.
      --dry                 Dry run without changing files.

## Example:

    audiobook-tags --set-tag="album_artist/Юрий Заборовский (Ардис)" --track-num="name"

- Convers all `.mp3` files in current folder and subfolders
- fix encoding supposing that original encoding was `Windows 1251`
- change tag album artist.
- set `track_num` mp3 tag to file number as ordered by file name

# Development

### OS Dependencies

#### MacOS

  brew update
  brew install libmagic

### Python dependencies

Note the dot before `./activate.sh`:

  . ./activate.sh
