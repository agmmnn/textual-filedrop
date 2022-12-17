from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.reactive import reactive
from textual.message import Message
from textual._types import MessageTarget
from textual import events

from rich.console import RenderableType

import os
import re


class Filedrop(Widget, can_focus=True, can_focus_children=False):
    DEFAULT_CSS = """
    Filedrop {
        height: 100%;
        border: round $panel-lighten-2;
        background: $panel;
        content-align: center middle;
        padding: 0 3;
    }
    """
    txt = reactive("Please Drag and Drop the files here...")

    def __init__(
        self,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes)

    def render(self) -> RenderableType:
        return self.txt

    class Selected(Message):
        """File paths selected message."""

        def __init__(
            self, sender: MessageTarget, path: str, filepaths: list, filenames: list
        ) -> None:
            self.path = path
            self.filepaths = filepaths
            self.filenames = filenames
            super().__init__(sender)

    async def on_event(self, event: events.Event) -> None:
        if isinstance(event, events.Paste):
            pattern = r'(?:[^\s"]|"(?:\\"|[^"])*")+'
            split_filepaths = re.findall(pattern, event.text)
            filepaths = [
                i.replace("\x00", "").replace('"', "")
                for i in split_filepaths
                if os.path.isfile(i.replace("\x00", "").replace('"', ""))
            ]
            if filepaths:
                filenames = [os.path.basename(i) for i in filepaths]
                await self.emit(
                    self.Selected(
                        self, os.path.split(filepaths[0])[0], filepaths, filenames
                    )
                )
                self.txt = ", ".join(["📄" + filename for filename in filenames])
                self.styles.border = ("round", "#2E8B57")


class FiledropApp(App):
    def compose(self) -> ComposeResult:
        yield Filedrop(id="filedrop")

    def on_mount(self):
        self.query_one("#filedrop").focus()

    def on_filedrop_selected(self, message: Filedrop.Selected) -> None:
        path = message.path
        filepaths = message.filepaths
        filenames = message.filenames
        print(path, filepaths, filenames)


if __name__ == "__main__":
    app = FiledropApp()
    app.run()
