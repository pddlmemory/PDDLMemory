import sublime, sublime_plugin
import os

from .ChunkTest import isChunk

# Reusable code
#
#   * Check if all selections are empty

class CreateChunk(sublime_plugin.TextCommand):

    def __init__(self, args):
        self.pm_settings = sublime.load_settings("PDDLMemory.sublime-settings")
        self.domain_folder = self.pm_settings.get("pddlmemory_domain_folder")
        self.display_confirmation = bool(self.pm_settings.get("display_confirmation"))
        sublime_plugin.TextCommand.__init__(self, args)

    def run(self, edit, args):

        chunkid = args['chunkid']

        # check if chunk already exists
        if isChunk(chunkid, self.domain_folder):
            sublime.error_message("Error: A chunk with that name already exists, please try again with a different name.")
            return

        # create the chunk
        try:
            os.makedirs(self.domain_folder + "/" + chunkid)
            os.makedirs(self.domain_folder + "/" + chunkid + "/facts/")
            os.makedirs(self.domain_folder + "/" + chunkid + "/goals/")
            factfile_path = self.domain_folder + "/" + chunkid + "/facts/" + chunkid + ".pdkb"
            factfile = open(factfile_path, 'a').close()
        except FileExistsError:
            sublime.error_message("Error: A folder with that name already exists, but it is not a chunk folder. Please remove this folder before creating the chunk.")
            return

        # check if all selections are empty
        if all([sel.empty() for sel in self.view.sel()]):
            # done, display a confirmation
            if self.display_confirmation:
                sublime.message_dialog("PDDLMemory: Created chunk " + chunkid + ".")
            else:
                sublime.status_message("PDDLMemory: Created chunk " + chunkid + ".")
        else:
            # add selected facts
            self.view.run_command("add_facts", {"args":{'chunkid':chunkid}})