#!/usr/bin/env python3
"""Basic dictionary """
BaseCaching = __import__('base_caching').BaseCaching


class LIFOCache(BaseCaching):
    """
    inherits from BaseCaching
    """
    last_added = ""

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
            self.last_added = key
            return
        keys = list(self.cache_data.keys())
        if len(keys) >= BaseCaching.MAX_ITEMS:
            print("DISCARD: {}".format(self.last_added))
            del self.cache_data[self.last_added]
        self.cache_data[key] = item
        self.last_added = key

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
