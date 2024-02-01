#!/usr/bin/env python3
"""Basic dictionary """
BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    """
    inherits from BaseCaching
    """

    used = {}

    def __init__(self):
        """
        initization"""
        super().__init__()

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is None or item is None:
            return
        if key in self.cache_data:
            self.used[key] += 1
            self.cache_data[key] = item
            return
        keys = list(self.cache_data.keys())
        if len(keys) >= BaseCaching.MAX_ITEMS:
            least = self.LFU_key()
            print("DISCARD: {}".format(least))
            del self.cache_data[least]
            del self.used[least]
        self.used[key] = 0
        self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None

        self.used[key] += 1
        return self.cache_data[key]

    def LFU_key(self):
        """
        find the least frequancy used key
        """
        least = -1
        for key, val in self.used.items():
            if least == -1 or self.used[least] > val:
                least = key
        return least
