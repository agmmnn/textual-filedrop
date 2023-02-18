from textual.app import App, ComposeResult
from textual.widgets import Static
from textual_filedrop import getfiles
from rich.json import JSON


class FileDropApp(App):
    DEFAULT_CSS = """
    #title {
        margin: 1 3;
        height: auto;
        color: $accent;
    }
    #content {
        border: vkey gray;
        min-height: 18;
        margin: 3;
        background: $panel;
    }
    """

    def compose(self) -> ComposeResult:
        yield Static(id="content", expand=True)

    def on_paste(self, event):
        files = getfiles(event)
        files = str(files).replace("'", '"')
        self.query_one("#content").update(JSON(files))


if __name__ == "__main__":
    app = FileDropApp()
    app.run()
