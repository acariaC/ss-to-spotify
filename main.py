import json
import os
import re
import cv2
import requests.exceptions
import spotipy
from pytesseract import pytesseract, Output
from spotipy.oauth2 import SpotifyOAuth


def connectToSpotify():
    # print("Get a client ID & client secret from: https://developer.spotify.com/dashboard/applications")
    os.environ['SPOTIPY_REDIRECT_URI'] = 'http://127.0.0.1:8080/'
    # os.environ['SPOTIPY_CLIENT_ID'] = input("Enter your client ID: ")
    # os.environ['SPOTIPY_CLIENT_SECRET'] = input("Enter your client secret: ")


def usernameAuthenticator():
    try:
        print("Note that entering the wrong username will currently crash the application.")
        return "lvrkhn"  # input("Enter your username: ")
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
# playlistName = input("Enter a playlist name: ")

playlistName = "ss-test"
playlistDesc = "Created with ss-to-spotify: https://github.com/acariaC/ss-to-spotify"

# spotifyObject.user_playlist_create(user=username, name=playlistName, public=True, description=playlistDesc)
listOfSongs = []

# Getting the images from a directory
folder_dir = "/Users/oliverkuhn/Documents/iCloud Photos/"  # input("Please choose your photo directory: ")
img = cv2.imread(folder_dir)

for images in os.listdir(folder_dir):
    img = cv2.imread(folder_dir + images)
    if images.endswith('.PNG') or (images.endswith('.jpeg')):
        dimensions = img.shape
        xyRatio = float(format(img.shape[1] / img.shape[0], ".2f"))  # Might be optimized with round() later

        if xyRatio == 0.46:
            cropped_image = img[int(img.shape[0] * 0.35): int(img.shape[0] * 0.75),
                            int(img.shape[1] * 0.23): int(img.shape[1] * 0.90)]

            # cv2.imshow("Cropped Image", cropped_image)
            # cv2.waitKey(0)
            artistAndTitle = (pytesseract.image_to_string(cropped_image))

            result = re.sub(r"[^a-zA-Z0-9]+", ' ', artistAndTitle).strip()
            if result:
                lengthCheck = len(result.split())
                if 3 <= lengthCheck < 30:
                    song = spotifyObject.search(q=result)
                    try:
                        #print(song['tracks']['items'][0]['uri'])
                        print('Track: ' + song['tracks']['items'][0]['name'])
                        print('Artist: ' + song['tracks']['items'][0]['album']['artists'][0]['name'] + '\n')



                        # print(json.dumps(song['tracks']['items'][0], indent=4))
                        listOfSongs.append(song['tracks']['items'][0]['uri'])
                    except IndexError:
                        print("No song found. \n")

# Finding the new playlist
prePlaylist = spotifyObject.user_playlists(user=username)
playlist = prePlaylist['items'][0]['id']

# Adding songs
print(listOfSongs)
spotifyObject.user_playlist_add_tracks(user=username, playlist_id=playlist, tracks=listOfSongs)

print("Finished.")
