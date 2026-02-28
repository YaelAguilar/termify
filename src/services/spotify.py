import spotipy

class SpotifyService:
    def __init__(self, client: spotipy.Spotify):
        self.client = client

    def get_current_user(self) -> dict:
        return self.client.current_user()
    
    def get_playback_state(self) -> dict | None:
        return self.client.current_playback()
    
    def get_user_playlists(self) -> list:
        result = self.client.current_user_playlists()
        return result['items'] if result else []
    
    def play(self) -> None:
        self.client.start_playback()

    def next_track(self) -> None:
        self.client.next_track()

    def previous_track(self) -> None:
        self.client.previous_track()

    def set_volume(self, volume: int) -> None:
        self.client.volume(volume)