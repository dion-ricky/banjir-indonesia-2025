from typing import Any, Dict, List, Optional

from bs4 import BeautifulSoup

from news_scraper import NewsScraper


class KompasScraper(NewsScraper):
    """Scraper for Kompas news website."""
    
    def scrape_list_page(self, url=None, limit=10) -> List[str]:
        """Scrape the list page to get article URLs."""
        target_url = url or self.base_url
        response = self.client.get(target_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        article_links = []
        for article in soup.find("div", class_="articleList").find_all("div", class_="articleItem"):
            article_link_element = article.find("a", class_="article-link")
            href = article_link_element.get("href")
            if href and "video.kompas.com" not in href:
                article_links.append(href)

        if len(article_links) < limit:
            next_page_link = soup.find("a", class_="paging__link--next")
            if next_page_link and next_page_link.get("href"):
                next_page_url = next_page_link["href"]
                article_links.extend(
                    self.scrape_list_page(
                        next_page_url,
                        limit - len(article_links),
                    )
                )

        return article_links

    def scrape_article(self, url: str) -> Optional[Dict[str, Any]]:
        """Scrape an individual article page."""
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