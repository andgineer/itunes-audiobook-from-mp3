import eyed3
import os


def fix_encoding(s):
    return s.encode('latin_1').decode('cp1251')


for subdir, dirs, files in os.walk('.'):
    for file_name in files:
        file_path = subdir + os.sep + file_name
        if file_path.endswith('.mp3'):
            print(file_name)
            audio_file = eyed3.load(file_path)
            for tag_name in ['artist', 'title', 'album', 'album_artist']:
                audio_file.tag.__setattr__(tag_name, audio_file.tag.__getattribute__(tag_name))
            audio_file.tag.genre = 'audiobook'

            print(fix_encoding(audio_file.tag.artist))
# audiofile.tag.album = u"Humanity Is The Devil"
# audiofile.tag. = u"Integrity"
# audiofile.tag. = u"Hollow"
# audiofile.tag.track_num = 2
