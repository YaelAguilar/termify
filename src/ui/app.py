from textual.app import App, ComposeResult
from ui.screens.home import HomeScreen
from services.spotify import SpotifyService


class TermifyApp(App):
    TITLE = "Termify"

    def __init__(self, spotify: SpotifyService):
        super().__init__()
        self.spotify = spotify

    def on_mount(self) -> None:
        self.push_screen(HomeScreen())