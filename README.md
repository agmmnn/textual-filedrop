![textual-filedrop](https://user-images.githubusercontent.com/16024979/208708722-e550d8ca-22a7-47f0-adf9-16cad570cdfd.png)

# textual-filedrop

Add filedrop support to your [Textual](https://github.com/textualize/textual/) apps, easily drag and drop files into your terminal apps.

> _Tested in `Windows Terminal` only. Other terminals/operating systems may not be using the [Paste](https://textual.textualize.io/events/paste/) event._

## Install

```
pip install textual-filedrop
```

## Usage

You can find more examples [here](./examples).

```py
from textual_filedrop import FileDrop
```

```py
# add FileDrop widget to your app
yield FileDrop(id="filedrop")
```

```py
# focus the widget
self.query_one("#filedrop").focus()
```

```py
# when the files are selected/dropped
def on_file_drop_selected(self, message: FileDrop.Selected) -> None:
    path = message.path
    filepaths = message.filepaths
    filenames = message.filenames
    filesobj = message.filesobj
    print(path, filepaths, filenames, filesobj)


# output: path, [filepaths], [filenames], [filesobj]
```

## Examples

### [subdomain_lister](./examples/subdomain_lister.py)

Drag and drop the subdomain list files and see the results as a tree list.

![subdomain_lister](https://user-images.githubusercontent.com/16024979/208706132-0a33bb21-51b8-441a-aeb9-668dbfcb382c.gif)

### [fullscreen](./examples/fullscreen.py)

Fullscreen example, will show the results in the textual console.

### [hidden](./examples/hidden.py)

As long as focus is on, the FileDrop widget will be active even if it is not visible on the screen.

## Dev

```
poetry install

textual console
poetry run textual run --dev examples/subdomain_lister.py
```
