import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import json
from datetime import datetime

#pip install spotipy, datetime

#Creating Environment
os.environ["SPOTIPY_CLIENT_ID"] = "ed5cbf589898495db2525f4a918ecdd5"
os.environ["SPOTIPY_CLIENT_SECRET"] = "cf8d56c29a9c45b983e7933ebbee009b"
os.environ["SPOTIPY_REDIRECT_URI"] = "http://127.0.0.1:8080"

#Client Login 
client_credentials_manager = SpotifyClientCredentials(client_id='ed5cbf589898495db2525f4a918ecdd5', client_secret='cf8d56c29a9c45b983e7933ebbee009b')
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

#Authenticate With Account and specify permissions
scope = 'playlist-modify-public playlist-modify-private'

#Change to yours if you want to do testing on your computer
username = '9upv4ku9el0ve5vp4m56rvbm8'

#Object and Token Creation

token = SpotifyOAuth(scope=scope, username=username)
spotifyObject = spotipy.Spotify(auth_manager = token)

class newPlayList:

    def __init__(self, playList, playListID):
        self.playList = playList
        self.playListID = playListID

    def createPlaylist(self, listName, description):
        playlist_name = input(listName)
        playlist_description = input(description)

        newPlaylist = spotifyObject.user_playlist_create(username, playlist_name, public=True, collaborative=False, description=playlist_description)
        playlist_id = newPlaylist["id"]
        self.playListID = playlist_id
        print(playlist_id)
        return

    def addToPlaylist(self, songs):
        playlist_id = self.playListID
        print(playlist_id)
        spotifyObject.playlist_add_items(playlist_id, songs, position=0)

    def copyFromPlaylist(self, playlist_id):
        playList = spotifyObject.playlist(playlist_id, fields=None, market=None, additional_types=('track', ))
        songs = []
        for track in sp.playlist_tracks('4F3glBXOBMm0lYtlelYtgm')["items"]:
            songs.append(track["track"]["uri"])
        self.addToPlaylist(songs)

    def organizeByYear(self): 
        dupleList = []
        playlist = []
        for track in sp.playlist_tracks(self.playListID)["items"]:
            track_uri = track["track"]["uri"]
            track_info = sp.track(track_uri)
            release_date = track_info["album"]["release_date"]
            yearTuple = (track_uri, release_date)
            print(yearTuple)
            dupleList.append(yearTuple)
        
        dupleList = sorted(dupleList, key=lambda x: x[1])
        print(dupleList)
        for item in dupleList:
            playlist.append(item[0])
        print(playlist)
        spotifyObject.user_playlist_replace_tracks(username, self.playListID, playlist)

    # def organizeSadToHappy():
    #     for track in sp.playlist_tracks(self.playListID)["items"]:

playlist = newPlayList('playlistName', 'playlistID')
playlist.createPlaylist('enter name: ', 'description: ')
playlist.copyFromPlaylist('0YCQ3PEOC3qUeuoZz2yt8k')
playlist.organizeByYear() 
