from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static
from textual.containers import Container


class NowPlaying(Static):
    def update_track(self, name: str, artist: str) -> None:
        self.update(f"🎵 {name}\n👤 {artist}")


class HomeScreen(Screen):
    CSS = """
    HomeScreen {
        align: center middle;
    }

    Container {
        width: 60;
        height: auto;
        border: round #1DB954;
        padding: 1 2;
        align: center middle;
    }

    NowPlaying {
        text-align: center;
        padding: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with Container():
            yield NowPlaying("No hay nada reproduciéndose", id="now-playing")
        yield Footer()

    def on_mount(self) -> None:
        self.refresh_track()

    def refresh_track(self) -> None:
        sp = self.app.spotify
        state = sp.get_playback_state()

        if state and state.get("item"):
            track = state["item"]
            name = track["name"]
            artist = track["artists"][0]["name"]
            self.query_one("#now-playing", NowPlaying).update_track(name, artist)