from textual.app import App, ComposeResult
from textual_filedrop import FileDrop


class FileDropApp(App):
    def compose(self) -> ComposeResult:
        yield FileDrop(id="filedrop")

    def on_mount(self):
        self.query_one("#filedrop").focus()

    def on_file_drop_dropped(self, event: FileDrop.Dropped) -> None:
        path = event.path
        filepaths = event.filepaths
        filenames = event.filenames
        filesobj = event.filesobj
        print(path, filepaths, filenames, filesobj)


if __name__ == "__main__":
    app = FileDropApp()
    app.run()
