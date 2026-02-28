from auth import get_spotify_client
from services.spotify import SpotifyService
from ui.app import TermifyApp

def main():
    sp = get_spotify_client()
    service = SpotifyService(sp)
    app = TermifyApp(spotify=service)
    app.run()

if __name__ == "__main__":
    main()