import sys
import traceback
from typing import Optional

import httpx
from tqdm import tqdm


def err_logger(fn):
    """Decorator to log errors during scraping."""

    def wrapper(self, *args, **kwargs):
        try:
            return fn(self, *args, **kwargs)
        except Exception as e:
            _, _, tb = sys.exc_info()

            second_to_last_tb = None
            # Get the frame where the exception actually occurred
            # The last frame in the traceback is usually where the error happened
            while tb.tb_next:
                second_to_last_tb = tb
                tb = tb.tb_next

            # Access the local variables of that frame
            local_vars = second_to_last_tb.tb_frame.f_locals

            traceback.print_exc()
            print("Local variables at the point of exception:")
            for var_name, var_value in local_vars.items():
                print(f"  {var_name}: {var_value}")

            return None

    return wrapper


class NewsScraper:

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.Client(
            timeout=30.0,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            },
        )

    @err_logger
    def scrape_article(self, url: str) -> dict:
        """Scrape a single article page."""
        return self.do_scrape_article(url)

    def do_scrape_article(self, url: str) -> dict:
        """Actual implementation of scraping a single article. To be overridden by subclasses."""
        pass

    @err_logger
    def scrape_list_page(self, url: Optional[str] = None, limit: int = 10) -> list:
        """Scrape the list of articles from the main page or category page."""
        self.prog_bar = tqdm(total=limit, desc="Listing articles", unit="article")
        return self.do_scrape_list_page(url=url, limit=limit)

    def do_scrape_list_page(self, url: Optional[str] = None, limit: int = 10) -> list:
        """Actual implementation of scraping the list page. To be overridden by subclasses."""
        pass
