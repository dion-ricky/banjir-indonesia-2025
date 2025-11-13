from typing import List
from bs4 import BeautifulSoup
from news_scraper import NewsScraper


class TribunNewsScraper(NewsScraper):
    """Scraper for Tribunnews."""

    def do_scrape_list_page(self, url=None, limit=10, page=None) -> List[str]:
        """Scrape the list page to get article URLs.

        Args:
            url (str|None): Base list URL to scrape. If None, uses `self.base_url`.
            limit (int): Maximum number of article URLs to collect.
            page (int|None): Page number for pagination; if omitted starts at 1.

        Returns:
            List[str]: A list of article URLs collected from one or more pages.
        """
        page = page or 1
        target_url = url or self.base_url
        target_url = f"{target_url}?page={page}"
        response = self.client.get(target_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        article_links = []
        for item in soup.find_all("li", class_="ptb15"):
            link = item.find("a")
            href = link.get("href")
            article_links.append(href)
            self.prog_bar.update(1)

        if len(article_links) < limit:
            article_links.extend(
                self.do_scrape_list_page(
                    url=url,
                    limit=limit - len(article_links),
                    page=page + 1,
                )
            )

        return article_links

    def do_scrape_article(self, url: str) -> dict:
        """Scrape a single article from Tribunnews.

        Args:
            url (str): Article page URL.

        Returns:
            dict: Mapping with `url`, `title`, `content` (joined paragraphs), and `timestamp`.
        """
        response = self.client.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        return {
            "url": url,
            "title": soup.find("h1", id="arttitle").get_text(strip=True),
            "content": "\n".join(
                p.get_text(strip=True)
                for p in soup.find(
                    "div",
                    class_="txt-article",
                ).find_all("p")
            ),
            "timestamp": soup.find(
                "time",
            )
            .find("span")
            .get_text(strip=True),
        }
