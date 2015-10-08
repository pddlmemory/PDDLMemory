import sublime, sublime_plugin

class InsertMarkers(sublime_plugin.TextCommand):

    def run(self, edit, args):
        marker = args['marker']

        # erase current selection
        for sel in reversed(self.view.sel()):
            self.view.erase(edit, sel)

        # remove empty lines
        for sel in self.view.sel():
            lines = self.view.split_by_newlines(sel)
            for l in lines:
                full_line = self.view.substr(self.view.full_line(l))
                if full_line.isspace():
                    self.view.erase(edit, self.view.full_line(l))

        # insert marker
        sel = self.view.sel()[0]
        self.view.insert(edit, sel.begin(), marker)
