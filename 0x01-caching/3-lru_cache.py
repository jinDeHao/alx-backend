#!/usr/bin/env python3
"""Basic dictionary """
BaseCaching = __import__('base_caching').BaseCaching


class LRUCache(BaseCaching):
    """
    inherits from BaseCaching
    """

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
            self.cache_data[key] = item
            return
        keys = list(self.cache_data.keys())
        if len(keys) >= BaseCaching.MAX_ITEMS:
            print("DISCARD: {}".format(keys[0]))
            del self.cache_data[keys[0]]
        self.cache_data[key] = item

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None

        tmp = self.cache_data[key]
        del self.cache_data[key]
        self.cache_data[key] = tmp
        return self.cache_data[key]
