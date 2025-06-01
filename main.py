from nodes.outline import create_outline
from nodes.filter import filter_trending
from nodes.scraper import start_scrape
from nodes.wiki import get_wiki, summarize_wiki
from nodes.conclude import conclude
import datetime


def main():
    # Workflow
    # lans = ["all", "python", "swift", "typescript", "javascript", "go", "rust"]
    lans = ["all"]
    # date = datetime.datetime.now().strftime("%Y-%m-%d")
    date = "2025-06-01"
    print("start scraping...")
    start_scrape(lans, date)
    print("create outline...")
    create_outline("all", date)
    print("filter trending...")
    filter_trending("all", date)
    print("get wiki...")
    get_wiki("all", date)
    print("summarize wiki...")
    summarize_wiki("all", date)
    print("conclude...")
    conclude("all", date)


if __name__ == "__main__":
    main()
