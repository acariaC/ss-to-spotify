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

# spotifyObject.user_playlist_create(user=username, name=playlistName, public=True, description=playlistDesc)
listOfSongs = []

# Getting the images from a directory
folder_dir = "/Users/oliverkuhn/Documents/iCloud Photos/Sample/"  # input("Please choose your photo directory: ")
img = cv2.imread(folder_dir)

# newCropped_image = img[1670: 1800, 250: 1000]

for images in os.listdir(folder_dir):
    img = cv2.imread(folder_dir + images)
    if images.endswith('.PNG') or (images.endswith('.jpeg')):
        dimensions = img.shape
        xyRatio = float(format(img.shape[1] / img.shape[0], ".2f")) # Might be optimized with round() later
        print(xyRatio)
        if xyRatio == 0.46:
            # Cropping the image down to the relevant parts
            cv2.rectangle(img, (0, 520), (0, 1659), (255, 0, 255), -1)
            cropped_image = img[int(img.shape[0]*0.35): int(img.shape[0]*0.70), int(img.shape[1]*0.23): int(img.shape[1]*0.90)]


            d = pytesseract.image_to_data(img, output_type=Output.DICT)
            n_boxes = len(d['level'])
            for i in range(n_boxes):
                (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)


            cv2.imshow("Cropped Image", cropped_image)
            cv2.waitKey(0)

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

                        #cv2.imshow("Cropped Image", cropped_image)
                        #cv2.waitKey(0)

# Finding the new playlist
prePlaylist = spotifyObject.user_playlists(user=username)
playlist = prePlaylist['items'][0]['id']

# Adding songs
print(listOfSongs)
spotifyObject.user_playlist_add_tracks(user=username, playlist_id=playlist, tracks=listOfSongs)

# cv2.imshow("Boxed", cropped_image)
print("Finished.")
