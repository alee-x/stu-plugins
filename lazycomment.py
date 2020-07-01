import sublime, sublime_plugin

# Extends TextCommand so that run() receives a View to modify.
class StuCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        def on_done(input_string):
            #self.view.run_command("move_to", {"to": "bof"})
            transf = transform_string(input_string)
            self.view.run_command("insert", {"characters": transf})

        def on_change(input_string):
            print("Input changed: %s" % input_string)

        def on_cancel():
            print("User cancelled the input")

        def transform_string(transform):
            textLen = len(transform)
            neededDash = (78 - textLen) / 2
            return '# ' + transform + ' ' + " ".join("-"*int(neededDash) + '\n')

        for region in self.view.sel():
            if not region.empty():
                # Get the selected text
                s = self.view.substr(region)
                transf = transform_string(s)
                # Replace the selection with transformed text
                self.view.replace(edit, region, transf)
                self.view.sel().clear()
            if region.empty():
                window = self.view.window()
                window.show_input_panel("Text to Insert:", "", on_done, on_change, on_cancel)