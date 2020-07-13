import json
from enum import Enum, auto
from typing import Optional

from robotlibcore import keyword  # type: ignore

from ..base import LibraryComponent
from ..generated.playwright_pb2 import Request


class SupportedBrowsers(Enum):
    chromium = auto()
    firefox = auto()
    webkit = auto()


class BrowserState(LibraryComponent):
    """Keywords to manage Playwright side Browsers, Contexts and Pages.
    """

    def __init__(self, library):
        self.library = library

    @property
    def playwright(self):
        return self.library.playwright

    @keyword
    def open_browser(
        self, url=None, browser=SupportedBrowsers.chromium, headless: bool = True
    ):
        """Opens a new browser instance.

        If ``url`` is provided, navigates there.

        The optional ``browser`` argument specifies which browser to use. The
        supported browsers are listed in the table below. The browser names
        are case-sensitive.
        |   = Value =     |        = Name(s) =                                   |
        | firefox         | [https://www.mozilla.org/en-US/firefox/new|Firefox]  |
        | chromium        | [https://www.chromium.org/Home|Chromium]             |
        | webkit          | [https://webkit.org/|webkit]                         |

        """

        with self.playwright.grpc_channel() as stub:
            response = stub.OpenBrowser(
                Request().NewBrowser(
                    url=url or "", browser=browser.name, headless=headless
                )
            )
            self.info(response.log)

    @keyword
    def close_browser(self):
        """Closes the current browser."""
        with self.playwright.grpc_channel() as stub:
            response = stub.CloseBrowser(Request.Empty())
            self.info(response.log)

    @keyword
    def new_browser(
        self, browser_type=SupportedBrowsers.chromium, **kwargs,
    ):
        """Create a new playwright Browser with specified options. A Browser is the Playwright object that controls a single Browser process.

        See [https://github.com/microsoft/playwright/blob/master/docs/api.md#browsertypelaunchoptions |Playwright browserType.launch] for a full list of supported options.
        """

        with self.playwright.grpc_channel() as stub:
            options = json.dumps(kwargs)
            response = stub.NewBrowser(
                Request().NewBrowser(browser=browser_type.name, rawOptions=options)
            )
            self.info(response.log)

    @keyword
    def new_context(
        self, **kwargs,
    ):
        """Create a new BrowserContext with specified options. A BrowserContext is the Playwright object that controls a single browser profile.
            Within a context caches and cookies are shared.

            See [https://github.com/microsoft/playwright/blob/master/docs/api.md#browsernewcontextoptions|Playwright browser.newContext] for a list of supported options.

            If there's no open Browser will open one. Does not create pages.
        """
        with self.playwright.grpc_channel() as stub:
            options = json.dumps(kwargs)
            self.info(options)
            response = stub.NewContext(Request().NewContext(rawOptions=options))
            self.info(response.log)

    @keyword
    def new_page(self, url: Optional[str] = None):
        """Open a new Page. A Page is the Playwright equivalent to a tab.

            If ``url`` parameter is specified will open the new page to the specified URL.
        """

        with self.playwright.grpc_channel() as stub:
            response = stub.NewPage(Request().Url(url=url))
            self.info(response.log)

    @keyword
    def switch_active_page(self, index: int):
        """Switches the active browser page to another open page by ``index``.

            Newly opened pages get appended to the end of the list
        """
        with self.playwright.grpc_channel() as stub:
            response = stub.SwitchActivePage(Request().Index(index=index))
            self.info(response.log)

    @keyword
    def auto_activate_pages(self):
        """Toggles automatically changing active page to latest opened page """
        with self.playwright.grpc_channel() as stub:
            response = stub.AutoActivatePages(Request().Empty())
            self.info(response.log)
