import yaml
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth


def auth():
    # read the config file
    with open("config.yml", "r") as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)["spotify"]

    # credentials
    client_id = cfg["client_id"]
    client_secret = cfg["client_secret"]
    redirect_uri = cfg["redirect_uri"]

    # we need to set the scope to read and modify playback state
    scope = "user-read-playback-state user-modify-playback-state"

    # create the oauth object
    sp_oauth = SpotifyOAuth(
        client_id, client_secret, redirect_uri, username=cfg["username"], scope=scope
    )
    credentials = SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret
    )

    # create the spotify object
    sp = spotipy.Spotify(client_credentials_manager=credentials, auth_manager=sp_oauth)

    return sp
