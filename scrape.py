#!/usr/bin/env python3
import json
from datetime import datetime
from typing import Optional

import click
from tqdm import tqdm

from detik import DetikScraper
from kompas import KompasScraper
from news_scraper import NewsScraper
from tribunnews import TribunNewsScraper

sites = {
    "detik": "https://www.detik.com",
    "kompas": "https://www.kompas.com",
    "tribunnews": "https://www.tribunnews.com",
}

scraper = {
    "detik": DetikScraper,
    "kompas": KompasScraper,
    "tribunnews": TribunNewsScraper,
}


def get_site(url: str) -> Optional[str]:
    for site_key, site_url in sites.items():
        if site_url in url:
            return site_key
    return None


def get_scraper_instance(base_url: str) -> Optional[NewsScraper]:
    site = get_site(base_url)

    if site is None:
        return None

    scraper_class = scraper.get(site)
    if scraper_class:
        return scraper_class(base_url)
    return None


@click.group()
def cli():
    """News scraping tool for collecting articles from news websites."""
    pass


@cli.command()
@click.argument("url")
@click.option("--output", "-o", type=click.Path(), help="Output file path (JSON)")
def scrape_single(url: str, output: Optional[str]):
    """Scrape a single article from the given URL."""
    scraper = get_scraper_instance(url)

    if not scraper:
        click.echo("Unsupported site or unable to determine site from URL.", err=True)
        return

    result = scraper.scrape_article(url)

    if result:
        if output:
            with open(output, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            click.echo(f"Article saved to {output}")
        else:
            click.echo(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        click.echo("Failed to scrape the article.", err=True)


@cli.command()
@click.argument("base_url")
@click.option(
    "--output", "-o", type=click.Path(), help="Output directory for JSON files"
)
@click.option(
    "--limit", "-l", type=int, default=10, help="Maximum number of articles to scrape"
)
def scrape_bulk(base_url: str, output: Optional[str], limit: int):
    """Scrape multiple articles from the news website."""
    scraper = get_scraper_instance(base_url)

    if not scraper:
        click.echo("Unsupported site or unable to determine site from URL.", err=True)
        return

    article_urls = scraper.scrape_list_page(limit=limit)

    results = []
    for url in tqdm(article_urls[:limit], desc="Scraping articles", unit="article"):
        result = scraper.scrape_article(url)
        if result:
            results.append(result)

    if results:
        if output:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"{output.rstrip('/')}/articles_{timestamp}.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            click.echo(f"Articles saved to {output_file}")
        else:
            click.echo(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        click.echo("No articles were successfully scraped.", err=True)


if __name__ == "__main__":
    cli()
