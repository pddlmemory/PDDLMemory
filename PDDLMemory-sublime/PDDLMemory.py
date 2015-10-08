import sublime, sublime_plugin
import threading, os

from .ChunkTest import getChunkList

# A list of PDDLMemory markers
markerlist = ["[[KNOWLEDGE BASE]]\n",
              "[[GOAL BASE]]\n"]

class PddlMemoryCommand(sublime_plugin.TextCommand):

    def __init__(self, args):

        # Dictionary used to collect user input
        self.userdict = {}

        # Load settings
        self.pm_settings = sublime.load_settings("PDDLMemory.sublime-settings")
        self.domain_folder =  self.pm_settings.get("pddlmemory_domain_folder")

        sublime_plugin.TextCommand.__init__(self, args)

    def run(self, edit, **args):
        """
            Compile a list of selected facts and start
            the thread for further processing.
        """
        self.args = args

        # Command: Create a new chunk
        if self.args['text'][0] == "chunk":
            self.view.window().show_input_panel("Enter name for new chunk:", '', self.on_done_chunk, None, None)

        # Command: Add facts to chunk
        if self.args['text'][0] == "add-facts":
            # display a dropdown with chunk names
            chunklist = getChunkList(self.domain_folder)
            if len(chunklist)>0:
                self.view.window().show_quick_panel(chunklist, self.on_done_addfacts)
            else:
                sublime.error_message("Error: There are no chunks in the current domain. Please create a chunk using the chunk command.")

        # Command: Add goals to chunk
        if self.args['text'][0] == "add-goals":
            # display a dropdown with chunk names (A) and ask for a goal name (B)
            chunklist = getChunkList(self.domain_folder)
            if len(chunklist)>0:
                self.view.window().show_quick_panel(chunklist, self.on_done_addgoals_A)
            else:
                sublime.error_message("Error: There are no chunks in the current domain. Please create a chunk using the chunk command.")
        # Command: Insert PDDLMemory markers into current file
        if self.args['text'][0] == "insert-markers":
            self.view.window().show_quick_panel(markerlist, self.on_done_markers)


    def on_done_chunk(self, user_input):
        self.view.run_command("create_chunk", {"args":{'chunkid':user_input}})

    def on_done_addfacts(self, user_input):
        if user_input > -1:
            selected_chunk = getChunkList(self.domain_folder)[user_input]
            self.view.run_command("add_facts", {"args":{'chunkid':selected_chunk}})

    def on_done_addgoals_A(self, user_input):
        if user_input > -1:
            selected_chunk = getChunkList(self.domain_folder)[user_input]
            self.userdict["chunkid"] = selected_chunk
            self.view.window().show_input_panel("Adding goal to chunk "+selected_chunk+", goal id:", '', self.on_done_addgoals_B, None, None)

    def on_done_addgoals_B(self, user_input):
        if user_input != "":
            self.userdict["goalid"] = user_input
            self.view.run_command("add_goals", {"args":self.userdict})
            self.userdict = {}
        else:
            sublime.error_message("Error: Goal id should not be empty.")

    def on_done_markers(self, user_input):
        if user_input > -1:
            selected_marker = markerlist[user_input]
            self.view.run_command("insert_markers", {"args":{'marker':selected_marker}})




