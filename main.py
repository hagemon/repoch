from nodes.outline import create_outline
from nodes.filter import filter_trending
from nodes.scraper import start_scrape
from nodes.wiki import get_wiki, summarize_wiki
from nodes.conclude import conclude
from nodes.shownotes import generate_shownotes
import datetime
from tqdm import tqdm


def main():
    # Workflow
    # lans = ["all", "python", "swift", "typescript", "javascript", "go", "rust"]
    lans = ["all"]
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    # date = "2025-06-01"
    for language in tqdm(lans):
        print(f"start scraping {language}...")
        start_scrape(language, date)
        print(f"create outline {language}...")
        create_outline(language, date)
        print("filter trending...")
        filter_trending(language, date)
        print("get wiki...")
        get_wiki(language, date)
        print("summarize wiki...")
        summarize_wiki(language, date)
        print("conclude...")
        conclude(language, date)
        print("generate shownotes...")
        generate_shownotes(language, date, overwrite=True)
        print("done")


if __name__ == "__main__":
    main()
