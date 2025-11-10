from bs4 import BeautifulSoup

from news_scraper import NewsScraper


class DetikScraper(NewsScraper):

    def scrape_article(self, url):
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

    def scrape_list_page(self, url=None, limit=10):
        target_url = url or self.base_url
        response = self.client.get(target_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        articles = []

        for list_feed_element in soup.find_all("div", class_="list--feed"):
            for article_element in list_feed_element.find_all("article"):
                link = article_element.find("a")
                if link and link.get("href") and "20.detik.com" not in link["href"]:
                    article_url = link["href"]
                    articles.append(article_url)

        if len(articles) < limit:
            next_page_link = soup.find(
                "div",
                class_="paging",
            ).find_all(
                "a", recursive=False
            )[-1]

            if next_page_link and next_page_link.get("href"):
                next_page_url = next_page_link["href"]
                articles.extend(
                    self.scrape_list_page(
                        next_page_url,
                        limit - len(articles),
                    )
                )

        return articles
