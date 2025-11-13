from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup

from news_scraper import NewsScraper


class KompasScraper(NewsScraper):
    """Scraper for the Kompas website."""
    
    def do_scrape_list_page(self, url=None, limit=10) -> List[str]:
        """Scrape the list page to get article URLs.

        Args:
            url (str|None): List page URL to scrape. Falls back to `self.base_url`.
            limit (int): Maximum number of article URLs to return. If the current page
                doesn't provide enough results, the method will follow pagination.

        Returns:
            List[str]: Collected article URLs.
        """
        target_url = url or self.base_url
        response = self.client.get(target_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        article_links = []
        for item in soup.find("div", class_="articleList").find_all("div", class_="articleItem"):
            link = item.find("a", class_="article-link")
            href = link.get("href")
            if href and "video.kompas.com" not in href:
                article_links.append(href)
                self.prog_bar.update(1)

        if len(article_links) < limit:
            next_page_link = soup.find("a", class_="paging__link--next")
            if next_page_link and next_page_link.get("href"):
                next_page_url = next_page_link["href"]
                article_links.extend(
                    self.do_scrape_list_page(
                        next_page_url,
                        limit - len(article_links),
                    )
                )

        return article_links

    def do_scrape_article(self, url: str) -> Optional[Dict[str, Any]]:
        """Scrape an individual Kompas article page.

        Args:
            url (str): Article URL to scrape.

        Returns:
            Optional[Dict[str, Any]]: A dict with keys `url`, `title`, `content`, `timestamp`.
                Returns the mapping unconditionally (no None for now) but typed as Optional
                to align with the project's broader scraper signatures.
        """
        response = self.client.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        return {
            "url": url,
            "title": soup.find("h1", class_="read__title").text.strip(),
            "content": " ".join(
                [
                    p.text.strip()
                    for p in soup.find(
                        "div",
                        class_="read__content",
                    ).find_all("p")
                ]
            ),
            "timestamp": soup.find("div", class_="read__time").text.strip(),
        }