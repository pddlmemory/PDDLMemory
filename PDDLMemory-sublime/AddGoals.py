import sublime, sublime_plugin
import os

from .ChunkTest import isChunk, checkBrackets

class AddGoals(sublime_plugin.TextCommand):

    def __init__(self, args):
        self.pm_settings = sublime.load_settings("PDDLMemory.sublime-settings")
        self.domain_folder =  self.pm_settings.get("pddlmemory_domain_folder")
        self.display_confirmation = bool(self.pm_settings.get("display_confirmation"))
        self.bracket_test = bool(self.pm_settings.get("bracket_test"))
        sublime_plugin.TextCommand.__init__(self, args)

    def run(self, edit, args):

        chunkid = args['chunkid']
        goalid = args['goalid']

        # check if chunk exists
        if not isChunk(chunkid, self.domain_folder):
            sublime.error_message("Error: A chunk with the given name does not exist in the current domain. (add-goals)")
            return

        # populate goal list
        goals = []
        sels = [s for s in self.view.sel() if not s.empty()]
        if len(sels)<1:
            sublime.error_message("Error: Please select some predicates.")
            return
        for sel in sels:
            lines = self.view.split_by_newlines(sel)
            for l in lines:
                predicate = self.view.substr(l).strip()
                goals.append(predicate)

        # perform a bracket test
        if self.bracket_test:
            goalstring = ""
            for g in goals:
                goalstring += g
            if not (checkBrackets(goalstring) == -1):
                sublime.error_message("Error: Number of opening and closing brackets do not match. (add-goals)")
                return

        # write goals to goalfile
        goalfile_path = self.domain_folder + "/" + chunkid + "/goals/" + goalid + ".pdkb"
        goalfile = open(goalfile_path, 'a')
        for g in goals:
            goalfile.write(g + "\n")
        goalfile.close()

        # erase selected facts
        for sel in reversed(sels):
            self.view.erase(edit, sel)

        # remove empty lines
        for sel in self.view.sel():
            lines = self.view.split_by_newlines(sel)
            for l in lines:
                full_line = self.view.substr(self.view.full_line(l))
                if full_line.isspace():
                    self.view.erase(edit, self.view.full_line(l))

        # clear selection
        self.view.sel().clear()

        # show confirmation message
        if self.display_confirmation:
            sublime.message_dialog("PDDLMemory: Written goal " + goalid + " to chunk " + chunkid + ".")
        else:
            sublime.status_message("PDDLMemory: Written goal " + goalid + " to chunk " + chunkid + ".")