![screenshot](https://user-images.githubusercontent.com/16024979/208250956-6a3c37ad-25b3-4698-8863-7c116e76b652.gif)

# textual-filedrop

Add filedrop support to your [Textual](https://github.com/textualize/textual/) apps, easily drag and drop files into your terminal apps. _Tested in Windows Terminal only. Other terminals/operating systems may not be using the [Paste](https://textual.textualize.io/events/paste/) event._

## Install

```
pip install textual-filedrop
```

## Usage

You can find more examples [here](./examples).

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
    print(path, filepaths, filenames)
# output: path, [filepaths], [filenames]
```
