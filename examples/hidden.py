from textual.app import App, ComposeResult, RenderableType
from textual.widgets import Static
from textual_filedrop import FileDrop
from textual.reactive import reactive


class FileDropApp(App):
    DEFAULT_CSS = """
    #title {
        margin: 1 3;
        height: auto;
        color: $accent;
    }
    #content {
        border: vkey gray;
        height: 18;
        padding: 1 1;
        margin: 0 3;
        background: $panel;
    }
    """

    def compose(self) -> ComposeResult:
        yield FileDrop(id="filedrop", display=False)
        yield Static("filename", id="title")
        yield Static(id="content")

    def on_mount(self):
        self.query_one("#filedrop").focus()

    def on_file_drop_dropped(self, event: FileDrop.Dropped) -> None:
        path = event.path
        filepaths = event.filepaths
        filenames = event.filenames
        filesobj = event.filesobj

        with open(filepaths[0], "r") as f:
            self.query_one("#title").update(filenames[0])
            self.query_one("#content").update(f.read())

        print(path, filepaths, filenames, filesobj)


if __name__ == "__main__":
    app = FileDropApp()
    app.run()
