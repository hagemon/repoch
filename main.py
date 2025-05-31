from nodes.outline import create_outline
from nodes.filter import filter_trending
from nodes.scraper import start_scrape
from nodes.wiki import get_wiki, summarize_wiki


def main():
    # Workflow
    # lans = ["all", "python", "swift", "typescript", "javascript", "go", "rust"]
    lans = ["all"]
    print("start scraping...")
    date = start_scrape(lans)
    print("create outline...")
    create_outline("all", date)
    print("filter trending...")
    filter_trending("all", date, overwrite=True)
    print("get wiki...")
    get_wiki("all", date)
    # print("summarize wiki...")
    # summarize_wiki("all", date)
    

if __name__ == "__main__":
    main()
