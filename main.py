import os
import re
import cv2
import requests.exceptions
import spotipy
from pytesseract import pytesseract
from spotipy.oauth2 import SpotifyOAuth

def connectToSpotify():
    print("Get a client ID & client secret from: https://developer.spotify.com/dashboard/applications")
    os.environ['SPOTIPY_REDIRECT_URI'] = 'http://127.0.0.1:8080/'
    os.environ['SPOTIPY_CLIENT_ID'] = input("Enter your client ID: ")
    os.environ['SPOTIPY_CLIENT_SECRET'] = input("Enter your client secret: ")


def usernameAuthenticator():
    try:
        print("Note that entering the wrong username will currently crash the application.")
        return input("Enter your username: ")
    except requests.exceptions.HTTPError or spotipy.SpotifyException:  # Does not work
        print("You can not create a playlist for another user.")
        usernameAuthenticator()


# Setting up the Spotify API
scope = "playlist-modify-public"
username = usernameAuthenticator()
connectToSpotify()

token = SpotifyOAuth(scope=scope, username=username)
spotifyObject = spotipy.Spotify(auth_manager=token)

# Creating the playlist

playlistName = input("Enter a playlist name: ")
playlistDesc = "Created with ss-to-spotify: https://github.com/acariaC/ss-to-spotify"

spotifyObject.user_playlist_create(user=username, name=playlistName, public=True, description=playlistDesc)
listOfSongs = []

# Getting the images from a directory
folder_dir = input("Please choose your photo directory: ")
img = cv2.imread(folder_dir)

for images in os.listdir(folder_dir):
    img = cv2.imread(folder_dir + images)
    if images.endswith('.PNG') or (images.endswith('.JPEG')):
        dimensions = img.shape

        if dimensions == (2532, 1170, 3):
            # Cropping the image down to the relevant parts
            cropped_image = img[870: 1030, 380: 1000]

            # Getting the text in the cropped image
            options = r'-c textord_min_xheight=55 -c ' \
                      r'preserve_interword_spaces=0'

            artistAndTitle = pytesseract.image_to_string(cropped_image, config=options)
            result = re.sub(r"[^a-zA-Z0-9]+", ' ', artistAndTitle).strip()
            if result:
                # print(result)
                lengthCheck = len(result.split())
                if lengthCheck >= 3:
                    print(result)
                    song = spotifyObject.search(q=result)
                    try:
                        print(song['tracks']['items'][0]['uri'])
                        listOfSongs.append(song['tracks']['items'][0]['uri'])
                    except IndexError:
                        print("No song found.")

                        # cv2.imshow("Cropped Image", cropped_image)
                        # cv2.waitKey(0)

# Finding the new playlist
prePlaylist = spotifyObject.user_playlists(user=username)
playlist = prePlaylist['items'][0]['id']

# Adding songs
spotifyObject.user_playlist_add_tracks(user=username, playlist_id=playlist, tracks=listOfSongs)

# cv2.imshow("Boxed", cropped_image)
print("Finished.")
