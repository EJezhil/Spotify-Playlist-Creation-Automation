#  STEP1 : Check Spotify API for USER_ID, CLIENT_SECRET                                               bb

from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = "http://example.com"
CURRENT_USER = ""

# input for year
time_period = input("Enter which year you want to travel in YYYY-MM-DD: ")
year = time_period.split("-")[0]

response = requests.get(f"https://www.billboard.com/charts/hot-100/{time_period}/")
webhtml = response.text
# print(webhtml)

soup = BeautifulSoup(webhtml, "html.parser")
songs_lists = soup.select("li ul li h3")
print(songs_lists)

song_names = [i.text for i in songs_lists]
print(song_names)

# finding list of 100 songs from Billboard
song_list = [i.strip() for i in song_names]
print(song_list)


# getting access token
param_token = {
    "grant_type": "client_credentials",
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,

}
token = requests.post(url="https://accounts.spotify.com/api/token", data=param_token)
# print(token.raise_for_status())
access_token = token.json()["access_token"]
# print(access_token)



# auth = SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI,access_token)
# print(auth.get_auth_response())


# create authorization with spotify
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
# getting current user id
current_user = sp.current_user()["id"]
print(current_user)


# {year}
# getting song track uri for all the 100 songs from list
all_songs = []
for i in song_list:
    try:
        results = sp.search(q=f"track:{i}", type="track")
        song_uri = results["tracks"]["items"][0]["uri"]
        song_name = results["tracks"]["items"][0]["name"]
        print(song_uri)
    except:
        print("Song not found")
        continue
    else:
        # all_songs.append(f"uri: {song_uri}  song: {song_name}")
        all_songs.append(song_uri)
print(all_songs)


# creating playlist
playlist = sp.user_playlist_create(user=CURRENT_USER, name=f"{time_period} Billboard 100", public=False)
# print(playlist)
playlist_id = playlist["id"]
print(playlist_id)


# adding songs into playlist
add_track = sp.playlist_add_items(playlist_id,all_songs, position=0)















