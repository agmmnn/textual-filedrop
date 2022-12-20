from textual.app import App, ComposeResult
from textual_filedrop import FileDrop


class FileDropApp(App):
    def compose(self) -> ComposeResult:
        yield FileDrop(id="filedrop")

    def on_mount(self):
        self.query_one("#filedrop").focus()

    def on_file_drop_selected(self, message: FileDrop.Selected) -> None:
        path = message.path
        filepaths = message.filepaths
        filenames = message.filenames
        filesobj = message.filesobj
        print(path, filepaths, filenames, filesobj)


if __name__ == "__main__":
    app = FileDropApp()
    app.run()
