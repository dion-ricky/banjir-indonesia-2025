from bs4 import BeautifulSoup

from news_scraper import NewsScraper


class DetikScraper(NewsScraper):
    """Scraper for the Detik website."""

    def do_scrape_list_page(self, url=None, limit=10):
        """Scrape a list/index page and return article URLs.

        Args:
            url (str|None): The URL of the list page to scrape. If None, uses `self.base_url`.
            limit (int): Maximum number of article URLs to return. If the current page
                contains fewer items, the scraper will follow pagination recursively
                until the requested `limit` is reached or no more pages are available.

        Returns:
            List[str]: A list of article URL strings.

        """
        target_url = url or self.base_url
        response = self.client.get(target_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        article_links = []

        for list_feed in soup.find_all("div", class_="list--feed"):
            for item in list_feed.find_all("article"):
                link = item.find("a")
                if (
                    link
                    and link.get("href")
                    and "20.detik.com" not in link["href"]
                    and "news.detik.com/x/" not in link["href"]
                    and "detim.com/pop/" not in link["href"]
                ):
                    href = link["href"]
                    self.prog_bar.update(1)
                    article_links.append(href)

        if len(article_links) < limit:
            next_page_link = soup.find(
                "div",
                class_="paging",
            ).find_all(
                "a", recursive=False
            )[-1]

            if next_page_link and next_page_link.get("href"):
                next_page_url = next_page_link["href"]
                article_links.extend(
                    self.do_scrape_list_page(
                        next_page_url,
                        limit - len(article_links),
                    )
                )

        return article_links

    def do_scrape_article(self, url):
        """Scrape a single Detik article page.

        Args:
            url (str): Article URL to scrape.

        Returns:
            dict: A mapping with keys `url`, `title`, `content`, and `timestamp`.
        """
        response = self.client.get(url, follow_redirects=True)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        if "wolipop.detik.com" in url:
            title = soup.find("h1", class_="itp_title_detail").text.strip()
            timestamp = soup.find("div", class_="text-black-light3").text.strip()
            content = " ".join(
                [
                    p.text.strip()
                    for p in soup.find(
                        "div",
                        class_="itp_bodycontent",
                    ).find_all("p")
                ]
            )
        else:
            title = soup.find("h1", class_="detail__title").text.strip()
            timestamp = soup.find("div", class_="detail__date").text.strip()
            content = " ".join(
                [
                    p.text.strip()
                    for p in soup.find(
                        "div",
                        class_="detail__body-text",
                    ).find_all("p")
                ]
            )

        return {
            "url": url,
            "title": title,
            "content": content,
            "timestamp": timestamp,
        }
