"""
Defines TS API v1.3 CursorPage model
"""
# ! /usr/local/bin/python3

# internal imports
from .base import ModelBase
from .page import Page
from .constants import TSPaginationKeys


class CursorPage(Page):
    """
    This class models a page of items that would be found in the body of a response
    from an endpoint that uses pagination. Unlike the Page class, it uses cursor-based
    pagination instead of number-based pagination.

    :ivar items: The list of items of the page; i.e. a list of indicators, reports, etc.
    :ivar cursor: A Base64-encoded string that contains information on how to retrieve
        the next page. If no cursor provided, it will default to pageSize: 25, pageNumber: 0
    :ivar total_elements: The total number of elements on the server, e.g. the total number
        of elements across all pages. Note that it is possible for this value to change
        between pages, since data can change between queries.
    """

    def __init__(self, items=None, response_metadata=None):
        """
        Constructs a |CursorPage| object
        """
        super().__init__(items=items)
        self.response_metadata = response_metadata

    def to_dict(self, remove_nones=False):
        """
        Creates a dictionary representation of the page

        :param remove_nones: Whether `None` values should be filtered out of the
        dictionary. Defaults to `False`

        :return: A dictionary representation of the page
        """
        return {
            TSPaginationKeys.ITEMS.value: [n.to_dict(remove_nones) for n in self.items],
            TSPaginationKeys.RESPONSE_METADATA.value: self.response_metadata
        }

    @classmethod
    def from_dict(cls, page:dict=None, content_type=None):
        """
        Creates a |CursorPage| object from a dictionary. This method is intended
        for internal use, to construct a |CursorPage| object from the body of a
        response json from a paginated endpoint.

        :param page: The dictionary
        :param content_type: The class that the contents should be deserialized into

        :return: The resulting |CursorPage| object
        """
        result = CursorPage(items=page.get(TSPaginationKeys.ITEMS.value),
                            response_metadata=page.get(TSPaginationKeys.RESPONSE_METADATA.value))

        if content_type:
            if not issubclass(content_type, ModelBase):
                raise ValueError("'content_type' must be a subclass of ModelBase.")

            result.items = [content_type.from_dict(item) for item in result.items]

        return result

    @classmethod
    def get_cursor_based_page_generator(cls, get_page, cursor=None):
        """
        Creates a page generator that uses cursor-based pagination.

        :param get_page: a function to get the next page, given values for from_time
            and to_time
        :param cursor: A Base64-encoded string that contains information on how to
            retrieve the next page. If no cursor provided, it will default to
            pageSize: 25, pageNumber: 0
        :return: a generator that yields each successive page
        """

        def get_next_cursor(page=None):
            """
            Retrieves the Base-64 encoded cursor string from a page.
            """
            next_cursor = ""
            response_metadata = ""
            page_dict = page.to_dict()
            if page_dict:
                response_metadata = page_dict.get(TSPaginationKeys.RESPONSE_METADATA.value)
            if response_metadata:
                next_cursor = response_metadata.get(TSPaginationKeys.NEXT_CURSOR.value)
            return next_cursor

        finished = False
        while not finished:
            # If cursor is None, no cursor value will be sent with request
            page = get_page(cursor=cursor)
            cursor = get_next_cursor(page)
            # If there are no more pages, cursor == "", therefore -> not "" == True
            finished = not cursor
            yield page
