from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static


class NowPlaying(Static):
    def update_track(self, name: str, artist: str, album: str) -> None:
        self.update(f"  {name} - {artist}\n  Album: {album}")


class PlayerControls(Static):
    DEFAULT_CSS = """
    PlayerControls {
        dock: bottom;
        height: 3;
        border: ascii $primary;
        content-align: center middle;
    }
    """

    def render(self) -> str:
        return "[|<]    [||]    [>|]        Vol: [========] 80%"


class HomeScreen(Screen):
    CSS = """
    HomeScreen {
        border: ascii $primary;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield PlayerControls()
        yield Footer()