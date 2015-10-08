# main.py
#
# The memory stores goals and facts about the world. (items)
# Items can be in an active or inactive state. The module provides
# functions for activating, deactivating of items.
# Adding and deleting of PlaceNodes is also supported.
#
# Created: 07/11/2014
# Author: Ivo Chichkov

# modules
from fact import Fact
from goal import Goal
from item import Item

# config
from ..config import DEBUG
from ..config import activation_limit

###
# NOTES
#
# reusable code:
#   * import python module from path (absolute)
#   * earlier: use weakref, weak references that get deleted by garbage collection
#
# to do:
#   * done
#
###


class Memory(object):

    def __init__(self):
        self.items = {}
        self.activation_limit = activation_limit

        # store the active item ids in the order of activation
        self.active_item_ids = []

    def activateItem(self, item_id):
        """ Activates an item """
        try:
            # if the activation limit has been reached,
            if self.activationLimitReached():
                # try to deactivate the item that was active longest
                for d in reversed(self.active_item_ids):
                    if not self.isProtected(d):
                        self.deactivateItem(d)
                        break
                # if deactivation was not succesful, return
                if len(self.active_item_ids) >= self.activation_limit:
                    return

            # activate the item
            self.items[item_id].activation = 1
            self.active_item_ids.insert(0, item_id)

        except KeyError:
            if DEBUG:
                print "Warning: Item to be activated," + \
                    " not found in memory."

    def deactivateItem(self, item_id):
        """ Deactivates an item """

        # remove item from active items list
        if self.isActive(item_id):
            if not self.isProtected(item_id):
                self.active_item_ids.remove(item_id)
        else:
            if DEBUG:
                print "Warning: Item to be deactivated " + \
                      "is not active."
            return

        # deactivate item
        try:
            if not self.isProtected(item_id):
                self.items[item_id].activation = -1
        except KeyError:
            if DEBUG:
                print "Warning: Item to be deactivated " + \
                    "not found in memory."

    def isActive(self, item_id):
        """ Returns True if item is active """
        try:
            self.active_item_ids.index(item_id)
            return True
        except ValueError:
            return False

    def isProtected(self, item_id):
        """ Returns True if item isProtected, i.e. cannot be deactivated  """
        try:
            return self.items[item_id].keep_active
        except KeyError:
            return False

    def retreiveItems(self, filter=None):
        """
        Retreive all items currently present in memory.

        @param filter       specifies the type of the items
                            to be returned (e.g. PlaceNode)
        """
        for item_id in self.items:
            obj = self.items[item_id].getObject()
            # filter items
            if filter:
                if isinstance(obj, filter):
                    yield self.items[item_id]
            else:
                yield self.items[item_id]

    def retreiveActiveItems(self, filter=None):
        """
        Retreive the currently active items in memory.

        @param filter       specifies the type of the items
                            to be returned (e.g. PlaceNode)
        """
        # todo: filter items
        for item_id in self.items:
            if self.items[item_id].activation > 0:
                yield self.items[item_id]

    def activationLimitReached(self):
        """
        Returns True if the activation limit has been reached.
        """
        if len(self.active_item_ids) >= self.activation_limit:
            return True
        else:
            return False

    def countActiveItems(self):
        return len(self.active_item_ids)

    # The shape method is not realised in the current release.
    # It can be used for modelling association processes.
    def shape(self, key, activationStrength=1):
        """
        The shape method models the process of storing and retreiving
        information from memory. When a new item (key) reaches memory,
        storage and retreival processes are activated at the same time.
        Key can be stored in memory as a new item. (storage)
        Inactive items already present in memory can become activated
        when key is observed. (retreival)

        @param key                  Key represents the "new" information
                                    that reaches memory.

        @param activationStrength   This parameter regulates the intensity of
                                    activation and controls the way associated
                                    items are retreived from memory.
        """

        # Assure that key has the right type
        errormsg = "Key should be an instance of Fact or Goal."
        assert isinstance(key, Fact) or isinstance(key, Goal), errormsg

        # todo: check wether node should be updated (lcation change)

        # if isinstance(key, Fact):
        #
        #     item = Item(key)
        #     label = item.dumpPDDL()
        #     # todo: check if fact already inside
        #     self.facts[label] = item

        # elif isinstance(key, Goal):
        #     item = Item(key)
        #     label = key.getName()
        #     # todo: check if goal already inside
        #     self.goals[label] = item

    def tick(self):
        """
        A memory tick affects activation levels of items.
        """
        pass

    # PlaceNode methods
    def addNode(self, placenode):
        """ Add a PlaceNode to the PlacesGraph """
        errormsg = "PlaceNode is already contained in memory."
        assert str(placenode) not in self.items.keys(), errormsg

        # create the item and add it
        item_id = str(placenode)
        self.items[item_id] = Item(placenode)
        self.activateItem(item_id)

    def removeNode(self, placenode_id):
        """ Remove a PlaceNode from the PlacesGraph """
        errormsg = "A PlaceNode with the given id is not present in memory."
        assert placenode_id in self.items.keys(), errormsg

        item_id = placenode_id
        # remove the item
        try:
            item = self.items[item_id]
        except KeyError:
            if DEBUG:
                print "Warning: PlaceNode to be removed " + \
                      "not found in memory."
            return

        if self.isActive(item_id):
            if self.isProtected(item_id):
                # remove protection
                self.items[item_id].keep_active = False
            # deactivate item
            self.deactivateItem(item_id)
        # delete item
        self.items.pop(item_id)

    # The following methods are added as an interface for the world model.
    # They should not be used to access memory directly.

    # adds a fact directly to memory
    def worldAdd(self, fact):
        pass

    # removes a fact directly from memory
    def worldDelete(self, fact):
        pass

    # returns facts that are currently observable
    # (e.g. facts related to the current room)
    def worldObserve(self):
        pass
