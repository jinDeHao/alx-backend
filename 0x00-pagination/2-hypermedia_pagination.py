#!/usr/bin/env python3
"""Simple helper function"""
import csv
import math
from typing import List


def index_range(page: int, page_size: int) -> tuple:
    """
    returns a tuple of size two
    containing a start index and an end index
    corresponding to the range of indexes to
    return in a list for those particular
    pagination parameters.
    """
    return (page - 1) * page_size, ((page - 1) * page_size) + page_size


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """get page
        """
        assert isinstance(page, int) and isinstance(page_size, int)
        assert page > 0 and page_size > 0
        start, end = index_range(page, page_size)
        self.dataset()
        return self.__dataset[start: end]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """Hypermedia pagination"""
        data = self.get_page(page, page_size)
        global_len = len(self.__dataset)
        num_of_pages = global_len / page_size
        return {
            "page_size": len(data),
            "page": page,
            "data": data,
            "next_page": page + 1 if global_len > (page * page_size) else None,
            "prev_page": page - 1 if page >= 2 else None,
            "total_pages": int(num_of_pages)
            if num_of_pages <= float(int(num_of_pages))
            else int(num_of_pages) + 1
        }
