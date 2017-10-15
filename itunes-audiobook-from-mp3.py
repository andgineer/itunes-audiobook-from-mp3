import eyed3
import eyed3.id3
import os
from argparse import ArgumentParser


OPT_ENCODING_NO_ENCODING = 'none'
OPT_TRACK_NUM_NO_TRACK_NUM = 'none'
OPT_TRACK_NUM_BY_FILE_NAMES = ''



def fix_encoding(s):
    if opts.encoding.lower() == OPT_ENCODING_NO_ENCODING.lower():
        return s
    else:
        try:
            s = s.encode('latin_1').decode(opts.encoding)
        except UnicodeEncodeError as e:
            print(s)
            print(e)
        return s


def get_opts():
    parser = ArgumentParser(description='Fixes mp3 tags for iOS audiobooks.')
    parser.add_argument('folder', default='.', metavar='folder', nargs='?',
                        help='Folder to process')
    parser.add_argument('--encoding', default='cp1251', dest='encoding',
        help=('mp3 tags encoding. "{}" if you do not need mp3 tags encoding fix.'.format(
                OPT_ENCODING_NO_ENCODING
                )
              )
        )
    parser.add_argument('--extension', default='mp3', dest='extension',
                        help=('File''s extension.'))
    parser.add_argument('--set-tag', default=None, dest='set_tag', nargs='*',
                        help=('Change mp3 tag to specified string. Format "tag-name/tag-value".'))
    parser.add_argument('--track-num', default='sort-file-names', dest='track_num',
                        help=('''Set mp3 tag `track_num` as specified.
                                - {} - file number for files sorted by names.
                            Use {} if you do not want to set this tag.'''.format(
                                OPT_TRACK_NUM_BY_FILE_NAMES,
                                OPT_TRACK_NUM_NO_TRACK_NUM)))
    parser.add_argument('--fix', action='store_true', dest='fix',
                        help=('Process and fix files.'))
    parser.add_argument('--dry', dest='dry',
                        help=('Just dry run without files fix.'))
    opts, _ = parser.parse_known_args()
    if not opts.fix:
        parser.print_help()
    opts.set_tags = {}
    if opts.set_tag:
        for tag_string in opts.set_tag:
            opts.set_tags.update({tag_string.split('/')[0]: tag_string.split('/')[1]})
    return opts


def fix_mp3_tages():
    paths = []
    for subdir, dirs, files in os.walk(opts.folder):
        for file_name in files:
            file_path = subdir + os.sep + file_name
            paths.append(file_path)

    if opts.track_num:
        # Paths would be sorted in order as track number should increment
        if opts.track_num == OPT_TRACK_NUM_BY_FILE_NAMES:
            paths = sorted(paths)

    track = 1
    for file_path in paths:
        if file_path.endswith('.' + opts.extension):
            print(file_path)
            audio_file = eyed3.load(file_path)
            for tag_name in ['artist', 'title', 'album', 'album_artist']:
                if tag_name in opts.set_tags:
                    audio_file.tag.__setattr__(tag_name, opts.set_tags[tag_name])
                else:
                    audio_file.tag.__setattr__(tag_name, fix_encoding(audio_file.tag.__getattribute__(tag_name)))
            audio_file.tag.genre = 'Audiobook'
            if opts.track_num:
                audio_file.tag.track_num = track
                track += 1
            print('{} by {}, album {} by {}, genre {}, num {}, '.format(
                audio_file.tag.title, audio_file.tag.artist, audio_file.tag.album, audio_file.tag.album_artist,
                audio_file.tag.genre, audio_file.tag.track_num))
            if opts.fix:
                audio_file.tag.save(version=eyed3.id3.ID3_DEFAULT_VERSION,encoding='utf-8')

def main():
    global opts

    opts = get_opts()
    fix_mp3_tages()


main()