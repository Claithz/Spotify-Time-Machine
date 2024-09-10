from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_CLIENT_ID = ""#add your CLIENT-ID
SPOTIFY_CLIENT_SECRET = ""#add your CLIENT-SECRET
REDIRECT_URI = "http://example.com"

client_credential_manager = spotipy.oauth2.SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                                        client_secret=SPOTIFY_CLIENT_SECRET,
                                                        redirect_uri=REDIRECT_URI,
                                                        show_dialog=True,
                                                        cache_path="CACHE PATH",
                                                        scope="playlist-modify-private",
                                                        username="USERNAME")
sp = spotipy.Spotify(client_credentials_manager=client_credential_manager)
token = client_credential_manager.get_access_token()
user_id = sp.current_user()["id"]

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")


response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
web_data = response.text

soup = BeautifulSoup(web_data, "html.parser")

song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]


uris = []

for song in song_names:
    result = sp.search(q=song, type='track', limit=1)
    if result['tracks']['items']:
        uri = result['tracks']['items'][0]['uri']
        uris.append(uri)

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False, collaborative=True)

sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist["id"], tracks=uris)
