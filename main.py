from nodes.outline import create_outline
from nodes.filter import filter_trending
from nodes.scraper import start_scrape


def main():
    date = start_scrape()
    create_outline("all", date)
    filter_trending("all", date)


if __name__ == "__main__":
    main()
