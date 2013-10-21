import os
import webbrowser
from Tkinter import Tk
from tkFileDialog import askopenfilename


options = {}
options['initialdir'] = 'C:\\Python27\Nick\Playlists'

Tk().withdraw()
#filename = askopenfilename(**options)

music_dir = 'C:\Users\T0135271\Music'
class songData:
    title = ""
    artist = ""
    directory = ""
    tempStr = ""
    def description(self):
        desc_str = "%s is by %s, located at %s" %(self.title,
                                                  self.artist, self.directory)
        return desc_str

deltitnu = songData()
deltitnu.title = "Deltitnu"
deltitnu.artist = "Aydio"
deltitnu.directory = "C:\\My Music"

nwo = songData()
nwo.title = "nwo"
nwo.artist = "Deep Sea Diver"
nwo.directory = "C:\\My Music"


#print(filename)

#b1 = "C:/Python27/sample_playlist.m3u" #make sure notepad is default program
#webbrowser.open(b1)
#print "Done."


#for line in songList:
#    print songList[line]
