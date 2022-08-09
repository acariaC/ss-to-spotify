import os
import re
import cv2
import spotipy
from pytesseract import pytesseract
from spotipy.oauth2 import SpotifyOAuth

# Setting up the Spotify API

scope = "playlist-modify-public"
username = "lvrkhn"

token = SpotifyOAuth(scope=scope, username=username)
spotifyObject = spotipy.Spotify(auth_manager=token)

# Creating the playlist

playlistName = input("Enter a playlist name: ")
playlistDesc = "Created with ss-to-spotify"

spotifyObject.user_playlist_create(user=username, name=playlistName, public=True, description=playlistDesc)
listOfSongs = []

# Getting the images from a directory
folder_dir = "/Users/oliverkuhn/Desktop/iCloud Photos/"
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

cv2.imshow("Boxed", cropped_image)

scope = "playlist-modify-public"
username = "lvrkhn"

token = SpotifyOAuth(scope=scope, username=username)
spotifyObject = spotipy.Spotify(auth_manager=token)