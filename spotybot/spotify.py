import yaml
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth


def auth():
    with open("config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)["spotify"]
    client_id = cfg["client_id"]
    client_secret = cfg["client_secret"]
    redirect_uri = cfg["redirect_uri"]
    scope = "user-read-playback-state user-modify-playback-state"
    sp_oauth = SpotifyOAuth(
        client_id, client_secret, redirect_uri, username=cfg["username"], scope=scope
    )
    credentials = SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret
    )
    sp = spotipy.Spotify(client_credentials_manager=credentials, auth_manager=sp_oauth)
    return sp
