import sublime, sublime_plugin
import os

from .ChunkTest import isChunk, checkBrackets

class AddFacts(sublime_plugin.TextCommand):

    def __init__(self, args):
        self.pm_settings = sublime.load_settings("PDDLMemory.sublime-settings")
        self.domain_folder =  self.pm_settings.get("pddlmemory_domain_folder")
        self.display_confirmation = bool(self.pm_settings.get("display_confirmation"))
        self.bracket_test = bool(self.pm_settings.get("bracket_test"))
        sublime_plugin.TextCommand.__init__(self, args)

    def run(self, edit, args):

        # check if chunk exists
        chunkid = args['chunkid']
        if not isChunk(chunkid, self.domain_folder):
            sublime.error_message("Error: A chunk with the given name does not exist in the current domain. (add-facts)")
            return

        # populate fact list
        facts = []
        sels = [s for s in self.view.sel() if not s.empty()]
        if len(sels)<1:
            sublime.error_message("Error: Please select some predicates.")
            return
        for sel in sels:
            lines = self.view.split_by_newlines(sel)
            for l in lines:
                predicate = self.view.substr(l).strip()
                facts.append(predicate)

        # perform a bracket test
        if self.bracket_test:
            factstring = ""
            for f in facts:
                factstring += f
            if not (checkBrackets(factstring) == -1):
                sublime.error_message("Error: Number of opening and closing brackets do not match. (add-facts)")
                return

        # write facts to factfile
        factfile_path = self.domain_folder + "/" + chunkid + "/facts/" + chunkid + ".pdkb"
        factfile = open(factfile_path, 'a')
        for f in facts:
            factfile.write(f + "\n")
        factfile.close()

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
                sublime.message_dialog("PDDLMemory: Written facts to chunk " + chunkid + ".")
        else:
                sublime.status_message("PDDLMemory: Written facts to chunk " + chunkid + ".")
