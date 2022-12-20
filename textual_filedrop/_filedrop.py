from textual.app import App, ComposeResult
from textual.widget import Widget
from textual.reactive import reactive
from textual.message import Message
from textual._types import MessageTarget
from textual import events

from rich.console import RenderableType

import os
import re

from ._icons import get_icon


class FileDrop(Widget, can_focus=True, can_focus_children=False):
    DEFAULT_CSS = """
    FileDrop {
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
            self,
            sender: MessageTarget,
            path: str,
            filepaths: list,
            filenames: list,
            filesobj: list,
        ) -> None:
            self.path = path
            self.filepaths = filepaths
            self.filenames = filenames
            self.filesobj = filesobj
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
                filesobj = []
                for i in filepaths:
                    file_name = os.path.basename(i)
                    _, file_ext = os.path.splitext(file_name)
                    file_ext = file_ext.replace(".", "")
                    file_path = i
                    filesobj.append(
                        {
                            "path": file_path,
                            "name": file_name,
                            "ext": file_ext,
                            "icon": get_icon(file_name, file_ext),
                        }
                    )
                await self.emit(
                    self.Selected(
                        self,
                        os.path.split(filepaths[0])[0],
                        filepaths,
                        filenames,
                        filesobj,
                    )
                )
                self.txt = ", ".join(
                    [f'[on dark_green] {i["icon"]} [/]{i["name"]}' for i in filesobj]
                )
                self.styles.border = ("round", "#2E8B57")
