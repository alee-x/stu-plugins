import re
import sublime
import sublime_plugin


class commentSectionCommand(sublime_plugin.TextCommand):
    def on_done(self, input_string):
        # self.view.run_command("move_to", {"to": "bof"})
        transf = self.transform_string(input_string.strip())
        self.view.run_command("insert", {"characters": transf})

    def on_change(self, input_string):
        print("Input changed: %s" % input_string)

    def on_cancel():
        print("User cancelled the input")

    def transform_string(self, txt):
        txt = re.sub(r"^[# ]+", "", txt)
        txt = re.sub(r"[ \-=]+$", "", txt)
        txtLen = len(txt)
        neededDash = 77 - txtLen
        txt = "# " + txt + " " + "-" * int(neededDash) + "\n"
        return txt

    def run(self, edit):
        region = self.view.sel()[0]
        line = self.view.line(region)
        if not region.empty():
            # get text of region as a string
            s = self.view.substr(region)
            transf = self.transform_string(s)
            self.view.replace(edit, region, transf)
            # job done, jog on
            self.view.sel().clear()
            (row, col) = self.view.rowcol(region.end())
            self.view.run_command("goto_line", {"line": row + 2})
        elif not line.empty():  # expand selection to line
            # get text of line as a string
            s = self.view.substr(line)
            # transform text and replace
            transf = self.transform_string(s)
            self.view.replace(edit, line, transf)
            # job done, jog on
            (row, col) = self.view.rowcol(region.end())
            self.view.run_command("goto_line", {"line": row + 2})
        else:
            window = self.view.window()
            window.show_input_panel(
                "Text to Insert:", "", self.on_done, self.on_change, self.on_cancel
            )


class commentSubsectionCommand(commentSectionCommand):
    def transform_string(self, txt):
        txt = re.sub(r"^[# ]+", "", txt)
        txt = re.sub(r"[ \-=]+$", "", txt)
        txtLen = len(txt)
        neededDash = (78 - txtLen) / 2
        if len(txt) % 2 == 1:
            txt = "# " + txt + " " + " -" * int(neededDash) + "\n"
        else:
            txt = "# " + txt + " " + "- " * int(neededDash) + "\n"
        txt = txt[:80]
        return txt
