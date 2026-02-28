from auth import get_spotify_client
from ui.app import TermifyApp

def main():
    sp = get_spotify_client()
    app = TermifyApp()
    app.run()

if __name__ == "__main__":
    main()