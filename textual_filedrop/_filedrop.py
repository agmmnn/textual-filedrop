import os
import re
import shlex

from typing import List, Dict, Any

from textual.widget import Widget
from textual.reactive import reactive
from textual.message import Message
from textual import events

from rich.console import RenderableType

from ._icons import get_icon


def _extract_filepaths(text: str) -> List[str]:
    split_filepaths = []
    if os.name == "nt":
        pattern = r'(?:[^\s"]|"(?:\\"|[^"])*")+'
        split_filepaths = re.findall(pattern, text)
    else:
        split_filepaths = shlex.split(text)

    split_filepaths = shlex.split(text)
    print(split_filepaths)
    filepaths = []
    for i in split_filepaths:
        item = i.replace("\x00", "").replace('"', "")
        if os.path.isfile(item):
            filepaths.append(i)
        elif os.path.isdir(item):
            for root, _, files in os.walk(item):
                for file in files:
                    filepaths.append(os.path.join(root, file))
    return filepaths


def _build_filesobj(filepaths: List[str]) -> List[Dict[str, Any]]:
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
    return filesobj


class FileDrop(Widget, can_focus=True, can_focus_children=False):
    DEFAULT_CSS = """
    FileDrop {
        border: round gray;
        height: 100%;
        background: $panel;
        content-align: center middle;
        padding: 0 3;
    }
    """

    txt = reactive("Please Drag and Drop the files here...")

    def __init__(
        self,
        display: bool = True,
        name: str = None,
        id: str = None,
        classes: str = None,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes)
        self.styles.display = "none" if not display else None

    def render(self) -> RenderableType:
        return self.txt

    class Dropped(Message):
        def __init__(
            self,
            path: str,
            filepaths: list,
            filenames: list,
            filesobj: list,
            oneline: str,
        ) -> None:
            super().__init__()
            self.path = path
            self.filepaths = filepaths
            self.filenames = filenames
            self.filesobj = filesobj
            self.oneline = oneline

    async def on_event(self, event: events.Event) -> None:
        if isinstance(event, events.Focus):
            self.styles.border = ("round", "dodgerblue")
        elif isinstance(event, events.Blur):
            self.styles.border = ("round", "gray")

        if isinstance(event, events.Paste):
            filepaths = _extract_filepaths(event.text)
            if filepaths:
                filesobj = _build_filesobj(filepaths)
                filenames = [os.path.basename(i) for i in filepaths]
                oneline = " ".join(
                    [
                        f'[on dodger_blue3] {i["icon"]} [/][on gray27]{i["name"]}[/]'
                        for i in filesobj
                    ]
                )
                self.post_message(
                    self.Dropped(
                        os.path.split(filepaths[0])[0],
                        filepaths,
                        filenames,
                        filesobj,
                        oneline,
                    )
                )
                self.txt = oneline
