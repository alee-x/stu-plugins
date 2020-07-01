import sublime, sublime_plugin

# Extends TextCommand so that run() receives a View to modify.
class StuCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for region in self.view.sel():
            if not region.empty():
                # Get the selected text
                s = self.view.substr(region)
                # Transform it
                textLen = len(s)
                neededDash = (78 - textLen) / 2
                transf = '# ' + s + ' ' + " ".join("-"*int(neededDash))
                # Replace the selection with transformed text
                self.view.replace(edit, region, transf)
