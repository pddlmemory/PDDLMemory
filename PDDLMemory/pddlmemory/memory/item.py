# item.py
#
# The item class represents an item.
# Items are the basic storage units that can be stored in memory.
#
# Created: 07/11/2014
# Author: Ivo Chichkov


class Item:

    def __init__(self, obj):
        # The object that is contained in this item
        self.obj = obj

        # The activation of the item in memory, values >0 mean 'activated'
        self.activation = -1

        # Stores wether the item is protected from beeing forgotten
        self.keep_active = False

    def __str__(self):
        """ Return a string representation """
        return self.obj.__str__()

    def getObject(self):
        return self.obj
