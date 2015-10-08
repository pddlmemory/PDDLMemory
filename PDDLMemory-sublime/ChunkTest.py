# ChunkTest.py
#
# The ChunkTest module contains useful PDDLMemory functions for the SublimeText plugin.
#
# Created: 10/06/2015
# Author: Ivo Chichkov

import sublime, sublime_plugin
import os

def isChunk(chunk_id, domain_folder):
    ''' Return True if the chunk with the specified id exists in the current domain. '''

    # init variables
    chunk_hasDir = False
    chunk_hasFactsDir = False
    chunk_hasGoalsDir = False

    # 1) check if folder exists
    chunk_hasDir = os.path.isdir(domain_folder + "/" + chunk_id + "/")

    # 2) check if subfolders (facts, goals) exist
    if chunk_hasDir:
        chunk_hasFactsDir = os.path.isdir(domain_folder + "/" + chunk_id + "/facts/")
        chunk_hasGoalsDir = os.path.isdir(domain_folder + "/" + chunk_id + "/goals/")

    # 3) Return result
    return (chunk_hasDir and chunk_hasFactsDir and chunk_hasGoalsDir)


def getChunkList(domain_folder):
    ''' Return a list of the chunks defined for the current domain. '''

    chunklist = []

    for f in os.listdir(domain_folder):
        if os.path.isdir( domain_folder + "/" + f + "/") and isChunk(f, domain_folder):
            chunklist.append(f)

    chunklist.sort()

    return chunklist


def checkBrackets(characters):
        '''Check the balance of brackets of a PDDL code snippet.

           Return -1 if all delimiters are balanced or
           the char number of the first delimiter mismatch.

        '''
        openers = {
            '(': ')',
            }
        closers = set(openers.values())
        stack = []
        for i, c in enumerate(characters, start=1):
            if c in openers:
                stack.append(openers[c])
            elif c in closers:
                if not stack or c != stack.pop():
                    return i
        if stack:
            return i
        return -1