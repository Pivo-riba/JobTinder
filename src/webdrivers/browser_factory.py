from typing import Union

from selenium import webdriver
from loguru import logger

from config import BROWSER_TYPE_CONFIG
from src.webdrivers.base_browser import BrowserType
from src.webdrivers.chrome import Chrome
from src.webdrivers.firefox import Firefox

class BrowserFactory:
    """Factory class for creating browser instances"""
    _browser_type: BrowserType = BROWSER_TYPE_CONFIG
    _browsers = {
        BrowserType.CHROME: Chrome,
        BrowserType.FIREFOX: Firefox,
    }

    @classmethod
    def get_browser_type(cls) -> BrowserType:
        """Get current browser type"""
        return cls._browser_type

    @classmethod
    def set_browser_type(cls, browser_type: BrowserType) -> None:
        """Set browser type"""
        if browser_type not in BrowserType.__members__:
            raise ValueError(f"Unsupported browser type: {browser_type}")
        cls._browser_type = browser_type
        logger.debug(f"Browser type set to: {browser_type}")

    @classmethod
    def get_browser(cls) -> Union[webdriver.Chrome, webdriver.Firefox]:
        """
        Create and return a WebDriver instance for the specified browser type
        Args:
            browser_type: BrowserType enum value
        Returns:
            WebDriver instance
        Raises:
            RuntimeError: If browser initialization fails
        """
        browser_type = cls._browsers.get(cls._browser_type)
        if browser_type is None:
            raise ValueError(f"Unsupported browser type: {cls._browser_type}")

        browser = browser_type()

        return browser.create_driver()