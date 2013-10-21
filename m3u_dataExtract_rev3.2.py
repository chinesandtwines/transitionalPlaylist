import os, webbrowser, wave, errno, shelve, shutil, random
from Tkinter import Tk
from tkFileDialog import askopenfilename
import numpy as np
import matplotlib.pyplot as plt

## -------------------------------------------------------------------------------------------

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
    """
    Holds a variety of song data

    Returns:
        title: Title of song
        artist: Artist of song
        album: Album the song belongs to
        ext: File type of the song
        ampS[]: Amplitude data for the first x seconds of the song
        ampF[]: amplitude data for the last x seconds of the song
    """
    def __init__(self, title="", artist="", album="", directory="", ext = "",
                 ampS=[], ampF=[], ampSavg="", ampFavg=""):
        self.title, self.artist, self.album, self.directory = title, artist, album, directory
        self.ampS, self.ampF, self.ampSavg, self.ampFavg = ampS, ampF, ampSavg, ampFavg
        self.ext = ext
    def __str__(self):
        data_filled = 'No'
        if len(self.ampS) > 0 and len(self.ampF) > 0:
            data = 'Yes'
        desc_str = "Title: %s \nArtist: %s \nAlbum: %s \nDirectory: %s \nData: %s \n" %(
            self.title, self.artist, self.album, self.directory, data_filled)
        return desc_str

## -------------------------------------------------------------------------------------------

def make_sure_path_exists(directory):
    """
    Checks if a directory exists. If it doesn't, it is created

    Args:
        directory: Folder to be checked
    """
    try:
        os.makedirs(directory)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
        
## -------------------------------------------------------------------------------------------

def dumpWAV(name, i):
    """
    Converts an .mp3 to a .wav file

    Args:
        name: full location of .mp3 file
        i: index of loop that function is placed inside
    Returns:
        .wav version of the original .mp3 file in temp_folder
    """
    import pymedia.audio.acodec as acodec
    import pymedia.muxer as muxer
    import time, wave, string, os
    ext_len = len(extNames[i])
    name1= name[:-4]
    
    # Open demuxer first
    dm = muxer.Demuxer(extNames[i].lower())
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
                        snd= wave.open( destination, 'wb' )
                        snd.setparams( (1, 2, r.sample_rate, 0, 'NONE','') )
                                            
                    snd.writeframes( r.data )

## -------------------------------------------------------------------------------------------
## Extract song title, artist, album, directory, extension
## -------------------------------------------------------------------------------------------                    
                    
songNames, artistNames, albumNames, dirNames, extNames = [], [], [], [], []

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
            songNames.append(new_split[-1][0])
            extNames.append(new_split[-1][1])
            dirStr = music_dir+'\\'+new_split[0]+'\\'+new_split[1][0]+'.'+new_split[1][1]
            dirNames.append(dirStr)
        elif len(new_split) == 3:       # ['artist', 'album', ['song', 'ext']]
            artistNames.append(new_split[0])
            albumNames.append(new_split[1])
            songNames.append(new_split[-1][0])
            extNames.append(new_split[-1][1])
            dirStr = (music_dir+'\\'+new_split[0]+'\\'+new_split[1]+'\\'
                      +new_split[2][0]+'.'+new_split[2][1])
            dirNames.append(dirStr)            

songdata = [SongData(*params) for params in zip(songNames, artistNames,
                                                albumNames, dirNames, extNames)]

library = 'C:\\Python27\Nick\library.db'
d = shelve.open(library)

## -------------------------------------------------------------------------------------------
## Extract song amplitude data
## -------------------------------------------------------------------------------------------

make_sure_path_exists(wav_path)

for i, file in enumerate(dirNames):
    print file

    if songNames[i] in d.keys():
        print 'Passing, data already present.\n'
        pass
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
        weights = range(len(songNames))
        songdata[i].ampSavg = np.average(da)

        song_length = wr.getnframes()
        wr.setpos(song_length - sz)
        da = np.fromstring(wr.readframes(sz), dtype=np.int16)
        songdata[i].ampF = da
        songdata[i].ampFavg = np.average(da)

        d[songNames[i]] = songdata[i]
                
        wr.close()
        os.remove(destination)

shutil.rmtree(wav_path) #delete temp folder

print '-'*77, '\n' #divider to make print out clearer

## -------------------------------------------------------------------------------------------
## Determine transitional order of songs, starting from a random song
## -------------------------------------------------------------------------------------------

rand = random.randint(0, len(songNames)-1)
#rand = 2
next_song = rand
excl_list = [] # exclusion list **(also becomes new song order list)**
excl_list.append(songNames[rand])
print 'Initial excl_list: ', excl_list, '\n'

for j in range(len(songNames)-1):
    new_diff = 100000
    for i, song in enumerate(songNames):
        if songNames[i] not in excl_list:
            diff = d[songNames[next_song]].ampFavg - d[songNames[i]].ampSavg
            print 'Trying: ',songNames[next_song],'-',songNames[i],'=',diff
            if diff < new_diff:
                new_diff = diff
                next_song_temp = i
                
    next_song = next_song_temp        
    excl_list.append(songNames[next_song])
    print 'Next song: ', songNames[next_song], '\n'
    print 'Updated excl_list: ', excl_list, '\n'
 
d.close() #close library
print '-'*77, '\n' #divider to make print out clearer

## -------------------------------------------------------------------------------------------
## Create new playlist in transitional order
## -------------------------------------------------------------------------------------------

new_playlist =  filename[:-4]+'_trans.m3u'
a = open(new_playlist, 'w')
a.write('#EXTM3U\n')

for s, song in enumerate(excl_list):
    str1 = '#EXTINF:0,'+songNames[s]+'.'+extNames[s]+'\n'
    str2 = dirNames[s]+'\n\n'
    a.write(str1)
    a.write(str2)

a.close()

## -------------------------------------------------------------------------------------------    

#>>> d[songNames[0]].ampSavg  # Kalimba
#-12.355414965986395
#>>> d[songNames[0]].ampFavg
#-6.5762993197278909
#>>> d[songNames[1]].ampSavg  # Sleep Away 
#-12.101183333333333
#>>> d[songNames[1]].ampFavg
#-4.9915041666666671
#>>> d[songNames[2]].ampSavg  # Maid with the Flaxen Hair
#-8.1146077097505671
#>>> d[songNames[2]].ampFavg
#-0.22770521541950114

## -------------------------------------------------------------------------------------------    

## Given name = 'C:\Python27\Nick\Kalimba.mp3'
## dumpWav(name) returns the following for name1, name2
## >>> name1
## ['C:\\Python27\\Nick\\Kalimba', 'mp3']
## >>> name2
## 'C:\\Python27\\Nick\\Kalimba'

## -------------------------------------------------------------------------------------------
## for song in songdata:
##    print song
## -------------------------------------------------------------------------------------------

## To print SongData for a single song:
## print songdata[i]
## Use songNames, artistNames, albumNames, dirNames to find correct index

## To apply attribute to a class instance
## songdata[1].amp =

## To access the docstring of a function:
## print dumpWAV.__doc__

## -------------------------------------------------------------------------------------------

