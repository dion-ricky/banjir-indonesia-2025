# Scrape Indonesia Flood News Coverage from Top News Sites

Supported news site:
- [Kompas](https://www.kompas.com/)
- [Detik](https://www.detik.com/)
- [Tribun News](https://www.tribunnews.com/)

## Project Setup
1. Create python venv
2. `pip install -r requirements.txt`

## How to scrape?
`python3 scrape.py scrape-bulk --output detik --limit 100 "https://www.detik.com/tag/banjir"`
`python3 scrape.py scrape-bulk --output kompas --limit 100 "https://www.kompas.com/tag/banjir"`
`python3 scrape.py scrape-bulk --output tribunnews --limit 100 "https://www.tribunnews.com/tag/banjir"`
