from typing import Type, TypeVar

from typing_extensions import Protocol

InteractiveItemTypeT = TypeVar("InteractiveItemTypeT")


class WebDriver(Protocol[InteractiveItemTypeT]):
    @property
    def interactive_item_type(self) -> Type[InteractiveItemTypeT]:
        """
        A type of interactive web element this web driver returns. Each web driver has their own implementation of handling interactive web elements,
        so this is a way to tell what type of interactive web element the web driver is returning.

        This is needed, so interactive elements in the WebQL response can leverage APIs provided by the underlying web driver.

        Property itself is not used and needed for type checking only.
        """

    def locate_interactive_element(self, response_data: dict) -> InteractiveItemTypeT:
        """
        Locates an interactive element in the web page.

        Parameters:

        response_data (dict): The data of the interactive element from the WebQL response.

        Returns:

        InteractiveItemTypeT: The interactive element.
        """

    def start_browser(self, user_session_extras: dict = None):
        """Start the browser.

        Parameters:

        user_session_extras (optional): the JSON object that holds user session information
        """

    def stop_browser(self):
        """Stops/closes the browser."""

    def open_url(self, url: str):
        """Open URL in the browser."""

    def get_accessiblity_tree(self) -> dict:
        """Gets the accessibility tree for the current page.

        Returns:
        dict: AT of the page
        """

    def preprocess_dom(self, lazy_load_pages_count: int = 3):
        """Scroll the page and Modifies the dom by assigning a unique ID to every node in the document.

        Parameters:
        lazy_load_pages_count (int): The number of pages to scroll down and up to load lazy loaded content.
        """

    def get_html(self) -> dict:
        """Returns the original HTML (i.e. without any WebQL modifications) fetched from the most recently loaded page".

        Returns:

        string: The HTML content of the web page.
        """
