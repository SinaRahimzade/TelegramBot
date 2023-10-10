from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from telegram_bot import yaml_parser
import spotipy


def spotify_auth() -> spotipy.Spotify:

    """
    Authenticate with Spotify API

    ------------------------------------------------------------------------------------

    Returns:
        Spotify object
    """

    cfg = yaml_parser()

    client_id = cfg["client_id"]
    client_secret = cfg["client_secret"]

    sp_oauth = SpotifyOAuth(
        client_id, 
        client_secret, 
        cfg["redirect_uri"], 
        username=cfg["username"], 
        scope="user-read-playback-state user-modify-playback-state"
    )
    credentials = SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret
    )

    return spotipy.Spotify(
        client_credentials_manager=credentials, auth_manager=sp_oauth
    )


__all__ = ['spotify_auth']
