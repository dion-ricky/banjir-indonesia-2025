from typing import List
from bs4 import BeautifulSoup
from news_scraper import NewsScraper


class TribunNewsScraper(NewsScraper):
    """Scraper for Tribunnews articles."""

    def scrape_list_page(self, url=None, limit=10, page=None) -> List[str]:
        """Scrape the list page to get article URLs."""
        page = page or 1

        target_url = url or self.base_url
        target_url = f"{target_url}?page={page}"

        response = self.client.get(target_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        article_links = []
        for item_element in soup.find_all("li", class_="ptb15"):
            link = item_element.find("a")
            href = link.get("href")
            article_links.append(href)

        if len(article_links) < limit:
            article_links.extend(
                self.scrape_list_page(
                    url=url,
                    limit=limit - len(article_links),
                    page=page + 1,
                )
            )

        return article_links

    def scrape_article(self, url: str) -> dict:
        """Scrape a single article from Tribunnews."""
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
