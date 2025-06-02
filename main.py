from nodes.outline import create_outline
from nodes.filter import filter_trending
from nodes.scraper import start_scrape
from nodes.wiki import get_wiki, summarize_wiki
from nodes.conclude import conclude
from nodes.shownotes import generate_shownotes
import datetime
from tqdm import tqdm
import io
from contextlib import redirect_stdout


def main():
    # Workflow
    # lans = ["all", "python", "swift", "typescript", "javascript", "go", "rust"]
    lans = ["all"]
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    overwrite = True
    # date = "2025-06-01"

    # Create main progress bar for languages
    with tqdm(lans, desc="Languages", position=0, colour="blue") as lang_pbar:
        for language in lang_pbar:
            # Define node tasks
            node_tasks = [
                ("Scraping", lambda: start_scrape(language, date, overwrite)),
                ("Creating outline", lambda: create_outline(language, date, overwrite)),
                (
                    "Filtering trending",
                    lambda: filter_trending(language, date, overwrite),
                ),
                ("Getting wiki", lambda: get_wiki(language, date, overwrite)),
                ("Summarizing wiki", lambda: summarize_wiki(language, date, overwrite)),
                ("Concluding", lambda: conclude(language, date, overwrite)),
                (
                    "Generating shownotes",
                    lambda: generate_shownotes(language, date, overwrite),
                ),
            ]

            # Create sub-progress bar for node tasks
            with tqdm(
                node_tasks,
                desc=f"Processing {language}",
                position=1,
                leave=True,
                colour="green",
            ) as node_pbar:
                for task_name, task_func in node_pbar:
                    node_pbar.set_description(f"{task_name}")

                    # Capture the output of the task function
                    captured_output = io.StringIO()
                    with redirect_stdout(captured_output):
                        _ = task_func()

                    # Print captured output in gray color below progress bars
                    output = captured_output.getvalue()
                    if output.strip():  # Only print if there's actual output
                        tqdm.write(f"\033[90m[{task_name}] {output.strip()}\033[0m")

            tqdm.write(
                f"\033[90m✓ Completed processing for language: {language}\033[0m"
            )


if __name__ == "__main__":
    main()
