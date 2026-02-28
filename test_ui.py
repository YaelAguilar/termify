from blessed import Terminal

t = Terminal()

def draw_ui():
    print(t.clear())
    width = t.width
    height = t.height

    # Titulo
    title = "TERMIFY"
    print(t.move(0, width // 2 - len(title) // 2) + t.bold(title))

    # Borde superior
    print(t.move(1, 0) + "+" + "-" * (width - 2) + "+")

    # Panel izquierdo
    left_width = 22
    print(t.move(2, 2) + "> Your Library")
    print(t.move(4, 2) + "Playlists")
    print(t.move(5, 2) + "> playlist 1")
    print(t.move(6, 2) + "  playlist 2")
    print(t.move(7, 2) + "  playlist 3")
    print(t.move(8, 2) + "  playlist 4")

    # Separador vertical
    for i in range(2, height - 4):
        print(t.move(i, left_width) + "|")

    # Panel central
    print(t.move(2, left_width + 3) + t.bold("Now Playing"))
    print(t.move(3, left_width + 3) + "-" * (width - left_width - 5))
    print(t.move(4, left_width + 3) + "white tee - Lil Peep")
    print(t.move(5, left_width + 3) + "Album: Come Over When You're Sober")

    # Borde inferior
    print(t.move(height - 4, 0) + "+" + "-" * (width - 2) + "+")

    # Controles
    controls = "[|<]    [||]    [>|]        Vol: [========] 80%"
    print(t.move(height - 3, width // 2 - len(controls) // 2) + controls)

    input()

with t.fullscreen():
    with t.hidden_cursor():
        draw_ui()