from blessed import Terminal
from services.spotify import SpotifyService

t = Terminal()


class TermifyApp:
    def __init__(self, spotify: SpotifyService):
        self.spotify = spotify

    def run(self):
        with t.fullscreen():
            with t.hidden_cursor():
                self.draw()
                self.handle_input()

    def handle_input(self):
        with t.cbreak():
            while True:
                key = t.inkey()
                height = t.height

                if key == 'q' or key == 'Q':
                    break
                elif key.name == 'KEY_RIGHT' or key == 'n':
                    try:
                        self.spotify.next_track()
                    except Exception:
                        pass
                    self.draw()
                elif key.name == 'KEY_LEFT' or key == 'p':
                    try:
                        self.spotify.previous_track()
                    except Exception:
                        pass
                    self.draw()
                elif key == ' ':
                    try:
                        state = self.spotify.get_playback_state()
                        if state and state.get("is_playing"):
                            self.spotify.pause()
                        else:
                            self.spotify.play()
                    except Exception as e:
                        print(t.move(height - 1, 0) + str(e))
                        t.inkey(timeout=3)
                    self.draw()

    def draw(self):
        print(t.clear())
        width = t.width
        height = t.height
        left_width = 22

        # Titulo
        title = "TERMIFY"
        print(t.move(0, width // 2 - len(title) // 2) + t.bold(title))

        # Borde superior
        print(t.move(1, 0) + "+" + "-" * (width - 2) + "+")

        # Separador vertical panel izquierdo
        for i in range(2, height - 4):
            print(t.move(i, left_width) + "|")

        # Contenido panel izquierdo
        print(t.move(2, 2) + t.bold("> Your Library"))
        print(t.move(4, 2) + "Playlists")

        # Playlists del usuario
        playlists = self.spotify.get_user_playlists()
        max_name_width = left_width - 5
        row = 5
        for playlist in playlists[:height - 10]:
            name = playlist['name'].encode('ascii', 'ignore').decode().strip()
            if not name:
                continue
            if len(name) > max_name_width:
                name = name[:max_name_width - 2] + ".."
            print(t.move(row, 2) + f"  {name}")
            row += 1

        # Panel central - cancion actual
        state = self.spotify.get_playback_state()
        center_x = left_width + 3
        center_width = width - left_width - 5

        print(t.move(2, center_x) + t.bold("Now Playing"))
        print(t.move(3, center_x) + "-" * center_width)

        if state and state.get("item"):
            track = state["item"]
            name = track["name"][:center_width]
            artist = track["artists"][0]["name"][:center_width]
            album = track["album"]["name"][:center_width]

            print(t.move(4, center_x) + f"{name} - {artist}")
            print(t.move(5, center_x) + f"Album: {album}")
        else:
            print(t.move(4, center_x) + "No hay nada reproduciendose")

        # Borde inferior
        print(t.move(height - 4, 0) + "+" + "-" * (width - 2) + "+")

        # Controles
        is_playing = state and state.get("is_playing")
        play_pause = "[||]" if is_playing else "[|>]"

        supports_volume = state and state.get("device") and state["device"].get("supports_volume")
        if supports_volume:
            volume = state["device"]["volume_percent"]
            filled = int(volume / 10)
            vol_bar = "=" * filled + "-" * (10 - filled)
            controls = f"[|<]    {play_pause}    [>|]        Vol: [{vol_bar}] {volume}%"
        else:
            controls = f"[|<]    {play_pause}    [>|]"

        print(t.move(height - 3, width // 2 - len(controls) // 2) + controls)

        # Atajos
        hints = "[ SPACE: play/pause | <- prev | -> next | Q: salir ]"
        print(t.move(height - 2, width // 2 - len(hints) // 2) + hints)