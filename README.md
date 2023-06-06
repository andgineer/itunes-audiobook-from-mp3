[![Build Status](https://github.com/andgineer/itunes-audiobook-from-mp3/workflows/ci/badge.svg)](https://github.com/andgineer/itunes-audiobook-from-mp3/actions)
# iTunes audiobooks from mp3

Converts mp3 files tags to use in iTunes/iPhone audiobooks. 

Fixes sort order. 

Supports cyrillic.

Details in [my blog's article](https://sorokin.engineer/posts/en/itunes_audiobook_from_mp3.html).


## MacOS

  brew update
  brew install libmagic
  
# Python dependencies  

Note the dot before `./activate.sh`:

  . ./activate.sh
  
# Usage
    python src/itunes_audiobook_from_mp3.py 
         [folder]
         [-h] 
         [--encoding ENCODING]
         [--extension EXTENSION]
         [--set-tag [SET_TAG [SET_TAG ...]]]
         [--track-num TRACK_NUM] [--fix FIX]
         [--dry DRY]

#### positional arguments:

*  folder                Folder to process

#### optional arguments:

*  -h, --help            show this help message and exit
* --encoding ENCODING   mp3 tags encoding. "none" if you do not need mp3 tags
                        encoding fix.
*  --extension EXTENSION
                        Files extension.
*  --set-tag [SET_TAG [SET_TAG ...]]
                        Change mp3 tag to specified string. Format "tag-
                        name/tag-value".
*  --track-num TRACK_NUM
                        Set mp3 tag `track_num` as specified. - - file number
                        for files sorted by names. Use none if you do not want
                        to set this tag.
*  --fix               Process and fix files.
*  --dry DRY             Just dry run without files fix.

#### For example:

  python src/itunes_audiobook_from_mp3 --fix --set-tag="album_artist/Юрий Заборовский (Ардис)"
  
- Convers all `.mp3` files in current folder and subfolders, fix encoding supposing
- that original encoding was `Windows 1251`, and change tag album artist.
- Also it will set `track_num` mp3 tag to file number as ordered by file name.
 
  