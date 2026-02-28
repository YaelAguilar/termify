from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label

class TermifyApp(App):
    TITLE = "Termify"
    CSS = """
    Screen {
        align: center middle;
    }

    Label {
        padding: 1 2;
    } 
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Welcome to Termify!")
        yield Footer()

if __name__ == "__main__":
    app = TermifyApp()
    app.run()