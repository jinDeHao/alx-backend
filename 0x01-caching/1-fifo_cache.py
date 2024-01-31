#!/usr/bin/env python3
"""Basic dictionary """
BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
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
        self.cache_data[key] = item
        keys = list(self.cache_data.keys())
        if len(keys) > BaseCaching.MAX_ITEMS:
            print("DISCARD: {}".format(keys[0]))
            del self.cache_data[keys[0]]

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None
        return self.cache_data[key]
