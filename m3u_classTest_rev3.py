class SongData(object):
    def __init__(self, title="", artist="", directory=""):
        self.title, self.artist, self.directory = title, artist, directory
    def __str__(self):
        desc_str = "Title: %s \nArtist: %s \nDirectory: %s \n" %(self.title,
                                                self.artist, self.directory)
        return desc_str

songNames = ['song1', 'song2', 'song3']
songs = {name: SongData(title=name) for name in songNames}

name = raw_input('What song do you want info on?')
print(songs[name])
