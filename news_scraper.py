from typing import Optional

import click
import httpx
import tenacity


def err_logger(fn):
    """Decorator to log errors during scraping."""
    def wrapper(self, *args, **kwargs):
        try:
            return fn(self, *args, **kwargs)
        except Exception as e:
            click.echo(f"Error in {fn.__name__}: {str(e)}", err=True)
            return None
    return wrapper

class NewsScraper:

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.Client(
            timeout=30.0,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        )

    @err_logger
    @tenacity.retry(stop=tenacity.stop_after_attempt(3), reraise=True)
    def scrape_article(self, url: str) -> dict:
        """Scrape a single article page."""
        pass

    @err_logger
    @tenacity.retry(stop=tenacity.stop_after_attempt(3), reraise=True)
    def scrape_list_page(self, url: Optional[str] = None) -> list:
        """Scrape the list of articles from the main page or category page."""
        pass