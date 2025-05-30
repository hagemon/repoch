import os
from llm.chat import chat
from json_repair import json_repair
import json

FILTER_PROMPT = """我正在做一个每周开源资讯的播客，需要从一些热门项目中，挑选出一些值得详细介绍的项目，返回他们的URL链接。榜单分为总榜和新锐榜，要分别从中选取一些项目。

# 要求
1. 总共选取5-6个项目，倾向于从新锐榜里选
2. 不要选择一些经典项目，他们可能一直在榜上，大家都比较熟悉了
3. 你可以考虑项目的创新性，实用性，有趣性，以及社区活跃度
4. 考虑是否是大模型在某些领域的应用，可能会引起大家的注意
5. 考虑是否会提升生产力
6. 不要把一些templates、awesome-list、collection之类的项目选进来
7. 返回json格式，包含项目名称和URL链接

# 总榜
{trending}

# 新锐榜
{rookie_list}

# 格式要求
不要返回任何解释，直接返回json格式，筛选出url和name字段，只需要5-6个你觉得最值得介绍的项目
{{
    "url": "https://github.com/...",
    "name": "..."
}}
"""


def filter_trending(language, date, overwrite=False):
    trending_dir = os.path.join("repos", date, "trending")
    rookie_dir = os.path.join("repos", date, "rookies")
    filtered_dir = os.path.join("repos", date, "filtered")
    filtered_file = os.path.join(filtered_dir, f"{language}.json")
    if not overwrite and os.path.exists(filtered_file):
        return
    if not os.path.exists(filtered_dir):
        os.makedirs(filtered_dir)
    with open(
        os.path.join(trending_dir, f"{language}.json"), "r", encoding="utf-8"
    ) as f:
        trending_list = f.readlines()
    with open(os.path.join(rookie_dir, f"{language}.json"), "r", encoding="utf-8") as f:
        rookie_list = f.readlines()
    prompt = FILTER_PROMPT.format(trending=trending_list, rookie_list=rookie_list)
    filtered = chat(prompt)
    filtered = json_repair.loads(filtered)
    with open(
        os.path.join(filtered_dir, f"{language}.json"), "w", encoding="utf-8"
    ) as f:
        f.write(json.dumps(filtered))
    return filtered
