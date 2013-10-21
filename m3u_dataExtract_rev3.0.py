import os, webbrowser, wave, errno, shelve, shutil
from Tkinter import Tk
from tkFileDialog import askopenfilename
import numpy as np
import matplotlib.pyplot as plt

options = {}
options['initialdir'] = 'C:\\Python27\Nick\Playlists'

Tk().withdraw()
#filename = askopenfilename(**options)
#filename = 'C:\\Python27\Nick\Playlists\Chills 5.2 rev2.m3u'
filename = 'C:\\Python27\Nick\Playlists\Chills 5.2.m3u'
#filename = 'C:\\Python27\Nick\Playlists\Chills 1.m3u'
#filename = 'C:\\Python27\Nick\Playlists\sample_playlist.m3u'

#music_dir = 'C:\Users\T0135271\Music'
music_dir = 'C:\\Users\Nick\Music'
wav_path = 'C:\\Python27\Nick\\temp_wav\\'

## -------------------------------------------------------------------------------------------

class SongData(object):
    def __init__(self, title="", artist="", album="", directory="", ampS=[], ampF=[]):
        self.title, self.artist, self.album, self.directory = title, artist, album, directory
        self.ampS, self.ampF = ampS, ampF
    def __str__(self):
        data_filled = 'No'
        if len(self.ampS) > 0 and len(self.ampF) > 0:
            data = 'Yes'
        desc_str = "Title: %s \nArtist: %s \nAlbum: %s \nDirectory: %s \nData: %s \n" %(
            self.title, self.artist, self.album, self.directory, data_filled)
        return desc_str

## -------------------------------------------------------------------------------------------

def make_sure_path_exists(directory):
    #if not os.path.exists(directory):
    #    os.makedirs(directory)
    try:
        os.makedirs(directory)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
        
## -------------------------------------------------------------------------------------------

def dumpWAV(name, i):
    import pymedia.audio.acodec as acodec
    import pymedia.muxer as muxer
    import time, wave, string, os
    name1= str.split( name, '.' )
    name2= string.join( name1[ : len( name1 )- 1 ] )
    # Open demuxer first

    dm= muxer.Demuxer( name1[ -1 ].lower() )
    dec= None
    f= open( name, 'rb' )
    snd= None
    s= " "
    while len( s ):
        s= f.read( 20000 )
        if len( s ):
            frames= dm.parse( s )
            for fr in frames:
                if dec== None:
                    # Open decoder

                    dec= acodec.Decoder( dm.streams[ 0 ] )
                r= dec.decode( fr[ 1 ] )
                if r and r.data:
                    if snd== None:
                        destination = wav_path+songNames[i]+ '.wav'
                        #print destination, '\n'
                        snd= wave.open( destination, 'wb' )
                        snd.setparams( (1, 2, r.sample_rate, 0, 'NONE','') )
                                            
                    snd.writeframes( r.data )

## -------------------------------------------------------------------------------------------

songNames, artistNames, albumNames, dirNames = [], [], [], []

with open(filename) as f:
    content = f.readlines()

for line in content:
    if (line[0:2] != '\n' and line[0] != '#'):
        line = line.strip('\n')
        split = line.split('\\')
        new_split = [elem for elem in split if elem != '..' and elem != 'Music']
        sub_split = new_split[-1].split('.')
        new_split[-1] = sub_split

        if len(new_split) == 2:     # ['artist', ['song', 'ext']]
            artistNames.append(new_split[0])
            albumNames.append(r'n\a')
            songNames.append(new_split[1][0])
            dirStr = music_dir+'\\'+new_split[0]+'\\'+new_split[1][0]+'.'+new_split[1][1]
            dirNames.append(dirStr)
        elif len(new_split) == 3:       # ['artist', 'album', ['song', 'ext']]
            artistNames.append(new_split[0])
            albumNames.append(new_split[1])
            songNames.append(new_split[2][0])
            dirStr = music_dir+'\\'+new_split[0]+'\\'+new_split[1]+'\\'+new_split[2][0]+'.'+new_split[2][1]
            dirNames.append(dirStr)            

songdata = [SongData(*params) for params in zip(songNames, artistNames,
                                                albumNames, dirNames)]

library = 'C:\\Python27\Nick\library.db'
d = shelve.open(library)

## -------------------------------------------------------------------------------------------
## dumpWAV gets confused if there is a period in the artist name
## it tries to split the file into ['song', 'ext'] at the artist name
## instead of at the song name

## maybe fix this by taking the length of the extension found in songNames
## and then chopping off the amount of chars that equal len(ext)
#for file in dirNames:
## -------------------------------------------------------------------------------------------

for i, file in enumerate(dirNames[0:7]):
    print file

    if songNames[i] in d.keys():
        print 'Passing, data already present.\n'
    else:
        print 'Analyzing data.\n'
        dumpWAV(file, i)

        destination = wav_path+songNames[i]+ '.wav'
        wr = wave.open(destination, 'r')

        sample_length = 10 #seconds
        sample_rate = wr.getframerate()
        sz = sample_length * sample_rate
        da = np.fromstring(wr.readframes(sz), dtype=np.int16)

        songdata[i].ampS = da
        d[songNames[i]] = songdata[i]
        wr.close()
        os.remove(destination)

d.close()
shutil.rmtree(wav_path)
## -------------------------------------------------------------------------------------------    

## Given name = 'C:\Python27\Nick\Kalimba.mp3'
## dumpWav(name) returns the following for name1, name2
## >>> name1
## ['C:\\Python27\\Nick\\Kalimba', 'mp3']
## >>> name2
## 'C:\\Python27\\Nick\\Kalimba'

## -------------------------------------------------------------------------------------------
#for song in songdata:
#    print song
## -------------------------------------------------------------------------------------------

## To print SongData for a single song:
# print songdata[i]
## Use songNames, artistNames, albumNames, dirNames to find correct index

## To apply attribute to a class instance
#songdata[1].amp = 



