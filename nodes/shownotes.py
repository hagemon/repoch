import os
import json
from llm.chat import chat


PROMPT = """
你是一个播客内容提取助手，从json文件中提取出各开源项目的名字、链接、介绍，请将介绍翻译为中文，并返回markdown格式，不要有多余的返回

# 项目列表
{projects}

# 格式要求，仅返回markdown
[项目名称](项目链接): 项目介绍（翻译为中文）
[项目名称](项目链接): 项目介绍（翻译为中文）
"""


def generate_shownotes(language, date, overwrite=False):
    shownotes_path = os.path.join("repos", date, "shownotes")
    trendings_path = os.path.join("repos", date, "trending", f"{language}.json")
    rookies_path = os.path.join("repos", date, "rookies", f"{language}.json")
    if not os.path.exists(shownotes_path):
        os.makedirs(shownotes_path)
    if not overwrite and os.path.exists(os.path.join(shownotes_path, f"{language}.md")):
        print(f"{os.path.join(shownotes_path, f'{language}.md')} already exists")
        return
    with open(trendings_path, "r", encoding="utf-8") as f:
        trendings = json.load(f)
    with open(rookies_path, "r", encoding="utf-8") as f:
        rookies = json.load(f)
    projects = trendings + rookies
    # print(PROMPT.format(projects=json.dumps(projects, ensure_ascii=False, indent=4)))
    shownotes = chat(
        PROMPT.format(projects=json.dumps(projects, ensure_ascii=False, indent=4))
    )
    with open(
        os.path.join(shownotes_path, f"{language}.md"), "w", encoding="utf-8"
    ) as f:
        f.write(shownotes)
