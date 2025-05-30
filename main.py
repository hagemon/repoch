from nodes.outline import create_outline
from nodes.filter import filter_trending
from nodes.scraper import start_scrape
from nodes.wiki import get_wiki


def main():
    # Workflow
    # lans = ["all", "python", "swift", "typescript", "javascript", "go", "rust"]
    # lans = ["all"]
    # date = start_scrape(lans)
    # create_outline("all", date)
    # filter_trending("all", "2025-05-26")
    get_wiki("all", "2025-05-26")
    

if __name__ == "__main__":
    main()
