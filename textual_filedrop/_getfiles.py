from typing import List, Dict, Any
from textual import events
from ._filedrop import _build_filesobj, _extract_filepaths


def getfiles(event: events.Paste) -> List[Dict[str, Any]]:
    filepaths = _extract_filepaths(event.text)
    filesobj = []
    if filepaths:
        filesobj = _build_filesobj(filepaths)
    return filesobj
