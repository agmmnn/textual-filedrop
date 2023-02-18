![textual-filedrop](https://user-images.githubusercontent.com/16024979/208708722-e550d8ca-22a7-47f0-adf9-16cad570cdfd.png)

# textual-filedrop

Add filedrop support to your [Textual](https://github.com/textualize/textual/) apps, easily drag and drop files into your terminal apps.

> _Tested on `Windows` and [`macOS`](https://github.com/Textualize/textual/discussions/1414#discussioncomment-4467029)._

> _[Nerd Font](https://www.nerdfonts.com/font-downloads) is required to display file icons._

## Install

```
pip install textual-filedrop
```

or

```
git clone https://github.com/agmmnn/textual-filedrop.git
cd textual-filedrop
poetry install
```

## Note

Since version [0.10.0](https://github.com/Textualize/textual/releases/tag/v0.10.0) Textual supports [bubble](https://textual.textualize.io/guide/events/#bubbling) for the [paste event](https://textual.textualize.io/events/paste/) ([Textualize/textual#1434](https://github.com/Textualize/textual/issues/1434)). So if the terminal where your app is running treats the file drag and drop as a paste event, you can catch it yourself with the `on_paste` function without widget.

## Usage

### `getfiles`

The `getfiles` function will return an object containing the the _path, file name, extension, icon_ of the files.

```py
from textual_filedrop import getfiles

class MyApp(App):
...
    def on_paste(self, event) -> None:
        files = getfiles(event)
        print(files)
```

![](https://i.imgur.com/1xdpivC.png)

### `FileDrop` Widget

As long as the `FileDrop` widget is in focus, it will give the information of the dragged files and render the file names with their icons on the screen.

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
# when the files are dropped
def on_file_drop_dropped(self, message: FileDrop.Dropped) -> None:
    path = message.path
    filepaths = message.filepaths
    filenames = message.filenames
    filesobj = message.filesobj
    print(path, filepaths, filenames, filesobj)


# output: path, [filepaths], [filenames], [filesobj]
```

You can find more examples [here](./examples).

## Examples

### [subdomain_lister.py](./examples/subdomain_lister.py)

Drag and drop the subdomain list files and see the results as a tree list.

![subdomain_lister](https://user-images.githubusercontent.com/16024979/208706132-0a33bb21-51b8-441a-aeb9-668dbfcb382c.gif)

### [fullscreen.py](./examples/fullscreen.py)

Fullscreen example, will show the results in the textual console.

### [hidden.py](./examples/hidden.py)

As long as focus is on, the `FileDrop` widget will be active even if it is not visible on the screen.

### [without_widget.py](./examples/without_widget.py)

An example that renders the object with the information of the dragged files returned from the `getfiles` function to the screen with `rich.json`.

## Dev

```
poetry install

textual console
poetry run textual run --dev examples/subdomain_lister.py
```
