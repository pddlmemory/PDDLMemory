# config_utils.py
#
# Useful functions for dynamically adjusting config parameters.
#
# Created: 06/16/2015
# Author: Ivo Chichkov

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