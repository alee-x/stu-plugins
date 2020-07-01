import sublime, sublime_plugin, itertools

class BulkCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        def transform_string(transform):
            textLen = len(transform)
            neededDash = (80 - textLen) / 2
            return transform + ' ' + " ".join("-"*int(neededDash) + '\n')

        for region in self.view.sel():
            for lin in self.view.lines(region):
                string_to_format = self.view.substr(lin)
                if string_to_format == '':
                    continue
                if string_to_format.strip()[0] == '#' and string_to_format.strip()[len(string_to_format.strip())-1] != '-':
                    transf = transform_string(string_to_format.strip())
                    self.view.replace(edit, lin, transf)
                    #self.view.sel().clear()