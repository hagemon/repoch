from llm.chat import chat
import os

OUTLINE_PROMPT = """我正在做一个每周开源资讯的播客，主要分为两部分，一部分是根据描述大致介绍我给你提供的一些开源项目，分为总榜和新锐榜（两周内新创建的仓库），你先帮我完成这部分的内容。

# 要求
1. 有总体梗概，分门别类地描述，本周有哪些类别的开源项目值得关注
2. 每个项目都可以或多或少介绍，尽量有趣，突出亮点，但不要太口语化，不要胡编乱造
3. 对于重复的内容，放到新锐榜介绍
4. 对于一些经典项目（比如vscode）可以少提，重点介绍新锐的项目

# 总榜
{trending}

# 新锐榜
{rookie_list}
"""


def create_outline(language, date, overwrite=False):
    trending_dir = os.path.join("repos", date, "trending")
    rookie_dir = os.path.join("repos", date, "rookies")
    outline_file = os.path.join("repos", date, "outline.md")
    if not overwrite and os.path.exists(outline_file):
        return
    with open(
        os.path.join(trending_dir, f"{language}.json"), "r", encoding="utf-8"
    ) as f:
        trending_list = f.readlines()
    with open(os.path.join(rookie_dir, f"{language}.json"), "r", encoding="utf-8") as f:
        rookie_list = f.readlines()
    prompt = OUTLINE_PROMPT.format(trending=trending_list, rookie_list=rookie_list)
    outline = chat(prompt)
    with open(outline_file, "w", encoding="utf-8") as f:
        f.write(outline)


if __name__ == "__main__":
    print(create_outline("all", "2025-05-25"))
