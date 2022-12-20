from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal, Container
from textual.widgets import Static, Button, Input, Tree, TreeNode
from rich.text import Text

import tldextract

from textual_filedrop import FileDrop


class CombinerApp(App):
    CSS = """
        Screen {
            align: center middle;
        }
        Tree {
            border: round $panel-lighten-2;
        }
    """

    def compose(self) -> ComposeResult:
        yield Vertical(FileDrop(id="drag"), Horizontal(classes="root"))

    def on_mount(self):
        self.root = self.query_one(".root")
        self.drag = self.query_one("#drag")
        self.drag.focus()

    def on_file_drop_selected(self, message: FileDrop.Selected) -> None:
        try:
            self.query_one(".tree").remove()
        except:
            pass
        self.drag.styles.height = 7
        self.drag.styles.dock = "top"

        filepaths = message.filepaths
        subs = []
        for i in filepaths:
            try:
                with open(i, "r") as f:
                    contents = f.read()
                subs.extend(filter(lambda x: x != "", contents.split("\n")))
            except:
                print("Something went wrong when opening the file")

        result = {}
        extract = tldextract.TLDExtract()
        for i in subs:
            item = extract(i)
            domain = item.domain + "." + item.suffix  # aa.com.tr
            sub = item.subdomain.split(".")
            subroot = sub[-1]
            sublevel = ".".join(sub[:-1])
            if domain not in result and domain:
                result[domain] = {}
            if sub != [""] and subroot:
                if subroot not in result[domain] and subroot:
                    result[domain][subroot] = []
                elif sublevel not in result[domain][subroot] and sublevel:
                    result[domain][subroot].append(sublevel)

        result = dict(sorted(result.items()))
        print(result)

        tree: Tree[dict] = Tree("domain-tree", classes="tree")
        for i in result:
            domain = tree.root.add(i, expand=True)
            self.add_json(domain, result[i], i)
        tree.root.expand()
        tree.show_root = False
        tree.show_guides = True
        self.root.mount(tree)

    def on_tree_node_selected(self, message: Tree.NodeSelected) -> None:
        print(message.name)

    @classmethod
    def add_json(cls, node: TreeNode, json_data: object, root_name: str) -> None:
        """Adds JSON data to a node.

        Args:
            node (TreeNode): A Tree node.
            json_data (object): An object decoded from JSON.
        """

        from rich.highlighter import ReprHighlighter

        highlighter = ReprHighlighter()

        def add_node(name: str, node: TreeNode, data: object) -> None:
            """Adds a node to the tree.

            Args:
                name (str): Name of the node.
                node (TreeNode): Parent node.
                data (object): Data associated with the node.
            """
            if isinstance(data, dict):
                node._label = Text(f"🌐{name}")
                for key, value in data.items():
                    new_node = node.add("", expand=True)
                    add_node(key, new_node, value)
            elif isinstance(data, list):
                node._label = Text(f"{name}")
                for index, value in enumerate(data):
                    new_node = node.add("", expand=True)
                    add_node(str(index), new_node, value)
            else:
                node._allow_expand = False
                label = Text.assemble(data)
                node._label = label

        add_node(root_name, node, json_data)


if __name__ == "__main__":
    app = CombinerApp()
    app.run()
