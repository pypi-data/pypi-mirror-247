"""
Defines TS API v1.3 NumberedPage model
"""
# ! /usr/local/bin/python3

# external imports
import math

# internal imports
from .base import ModelBase
from .constants import TSPaginationKeys
from .page import Page
from ..utils import Utils


class NumberedPage(Page):
    """
    This class models a page of items that would be found in the body of a response
    from an endpoint that uses number-based pagination. Not all paginated endpoints
    will use `page_number`. For instance, the |get_reports_page| method requires
    pagination to be performed by continuously adjusting the `from` and `to`
    parameters.

    :ivar items: The list of items of the page; i.e. a list of indicators, reports, etc.
    :ivar page_number: The number of the page out of all total pages, indexed from 0. 
        i.e. if there are 4 total pages of size 25, then page 0 will contain the first
        25 elements, page 1 will contain the next 25, etc
    :ivar page_size: The size of the page that was request. Note that, if this is the
        last page, then this might not equal len(items). For instance, if pages of size
        25 were requested, there are 107 total elements, and this is the last page, then
        `page_size` will be 25 even though the page only contains 7 elements
    :ivar total_elements: The total number of elements on the server, e.g. the total
        number of elements across all pages.  Note that it is possible for this value to
        change between pages, since data can change between queries
    """

    def __init__(self,
                 items=None,
                 page_number=None,
                 page_size=None,
                 total_elements=None,
                 has_next=None):
        """
        Constructs an |NumberedPage| object
        """
        super().__init__(items=items)
        self.page_number = page_number
        self.page_size = page_size
        self.total_elements = total_elements
        self.has_next = has_next

    def get_total_pages(self):
        """
        Returns the number of pages

        :return: The total number of pages on the server.
        """
        if not (self.total_elements and self.page_size):
            return None

        return math.ceil(float(self.total_elements) / float(self.page_size))

    def has_more_pages(self):
        """
        Returns a truthy value if the NumberedPage has next page

        :return: ``True`` if there are more pages available on the server.
        """
        # if has_next property exists, it represents whether more pages exist
        if self.has_next:
            return self.has_next

        # otherwise, try to compute whether or not more pages exist
        total_pages = self.get_total_pages()
        if not (self.page_number and total_pages):
            return False

        return self.page_number + 1 < total_pages

    def to_dict(self, remove_nones=False):
        """
        Creates a dictionary representation of the page

        :param remove_nones: Whether `None` values should be filtered out of
            the dictionary. Defaults to `False`

        :return: A dictionary representation of the page
        """
        items = []

        # attempt to replace each item with its dictionary representation if possible
        for item in self.items:
            if hasattr(item, 'to_dict'):
                items.append(item.to_dict(remove_nones=remove_nones))
            else:
                items.append(item)

        return {
            TSPaginationKeys.ITEMS.value: items,
            TSPaginationKeys.PAGE_NUMBER.value: self.page_number,
            TSPaginationKeys.PAGE_SIZE.value: self.page_size,
            TSPaginationKeys.TOTAL_ELEMENTS.value: self.total_elements,
            TSPaginationKeys.HAS_NEXT.value: self.has_next
        }

    @classmethod
    def from_dict(cls, page:dict=None, content_type=None):
        """
        Creates a |NumberedPage| object from a dictionary. This method is intended
        for internal use, to construct a |NumberedPage| object from the body of a
        response json from a paginated endpoint

        :param page: The page dictionary
        :param content_type: The class that the contents should be deserialized into.

        :return: A |NumberedPage| object
        """
        result = NumberedPage(
            items=page.get(TSPaginationKeys.ITEMS.value),
            page_number=page.get(TSPaginationKeys.PAGE_NUMBER.value),
            page_size=page.get(TSPaginationKeys.PAGE_SIZE.value),
            total_elements=page.get(TSPaginationKeys.TOTAL_ELEMENTS.value),
            has_next=page.get(TSPaginationKeys.HAS_NEXT.value)
        )

        if content_type:
            if not issubclass(content_type, ModelBase):
                raise ValueError("'content_type' must be a subclass of ModelBase.")

            result.items = [content_type.from_dict(item) for item in result.items]

        return result

    @classmethod
    def get_page_generator(cls, func, start_page=0, page_size=None):
        """
        Constructs a generator for retrieving pages from a paginated endpoint.
        This method is intended for internal use.

        :param func: Should take parameters `page_number` and `page_size` and
            return the corresponding |NumberedPage| object.
        :param start_page: The page to start on.
        :param page_size: The size of each page.
        :return: A generator that generates each successive page.
        """
        # initialize starting values
        page_number = start_page
        more_pages = True

        # continuously request the next page as long as more pages exist
        while more_pages:

            # get next page
            page = func(page_number=page_number, page_size=page_size)

            yield page

            # determine whether more pages exist
            more_pages = page.has_more_pages()
            page_number += 1

    @classmethod
    def get_time_based_page_generator(cls,
                                      get_page,
                                      get_next_to_time,
                                      from_time=None,
                                      to_time=None):
        """
        Façade for utils.get_time_based_page_generator

        :param get_page: a function to get the next page, given values for
            from_time and to_time
        :param get_next_to_time: get the to_time for the next query, given
            the result set and to_time for the previous query
        :param from_time: the initial from_time
        :param to_time: the initial to_time

        :return: generator that yields successive pages
        """
        get_next_to_fn = lambda page, to_time: get_next_to_time(page.items, to_time)
        return Utils.get_time_based_page_generator(get_page_fn=get_page,
                                                   get_next_to_time=get_next_to_fn,
                                                   from_time=from_time,
                                                   to_time=to_time)
