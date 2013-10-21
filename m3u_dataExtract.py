import os
import webbrowser
from Tkinter import Tk
from tkFileDialog import askopenfilename


options = {}
options['initialdir'] = 'C:\\Python27\Nick\Playlists'

Tk().withdraw()
#filename = askopenfilename(**options)
filename = 'C:\\Python27\Nick\Playlists\Chills 5.2.m3u'

music_dir = 'C:\Users\T0135271\Music'

class SongData(object):
    def __init__(self, title="", artist="", album="", directory=""):
        self.title, self.artist, self.album, self.directory = title, artist, album, directory
    def __str__(self):
        desc_str = "Title: %s \nArtist: %s \nAlbum: %s \nDirectory: %s \n" %(
            self.title, self.artist, self.album, self.directory)
        return desc_str

songList = []
artistList = []
tempList = []
#print(filename)

#b1 = "C:/Python27/sample_playlist.m3u" #make sure notepad is default program
#webbrowser.open(b1)
#print "Done."

with open(filename) as f:
    content = f.readlines()

content[:] = [x for x in content if x != '\n'] #removes new lines
del content[0] #remove '#EXTM3U'

for line in content:
    #row = 0
    if (line[0:2] != '\n' and line[0] != '#'):
        tempLine = line.strip('\n')
        tempLine = tempLine.lstrip("..\\")
        print tempLine
        tempList.append(tempLine)
        part = tempList.partition("/") #NEED TO SPLIT UP tempList BY BACKSLASHES
                                       #TO DETERMINE ARTIST, ALBUM, SONGNAME
        print part
        #songList.append('\n')
        #row += 1
        #print tempLine
        #part = line.partition("\\")
        #print part

    if (line.startswith('#EXT')):
        tempLine = line
        tempLine = tempLine.strip('\n') #works

        suffix = tempLine.lower()
        if suffix.endswith('mp3'):
            tempLine = tempLine[:-4]

        comma_index = line.find(',') #works
        tempLine = tempLine[comma_index+1:]
        songList.append(tempLine)
        

       

for name in songList:
    #print name
    songs = {name: SongData(title = name)}
    #print songs[name]
