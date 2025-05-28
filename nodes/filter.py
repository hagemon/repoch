import os
from llm.chat import chat
from json_repair import json_repair

FILTER_PROMPT = """我正在做一个每周开源资讯的播客，需要从一些热门项目中，挑选出一些值得详细介绍的项目，返回他们的URL链接。榜单分为总榜和新锐榜，要分别从中选取一些项目。

# 要求
1. 总共选取3-4个项目，倾向于从新锐榜里选
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
"""


def filter_trending(language, date):
    trending_dir = os.path.join(date, "trending")
    rookie_dir = os.path.join(date, "rookies")
    with open(
        os.path.join(trending_dir, f"{language}.json"), "r", encoding="utf-8"
    ) as f:
        trending_list = f.readlines()
    with open(os.path.join(rookie_dir, f"{language}.json"), "r", encoding="utf-8") as f:
        rookie_list = f.readlines()
    prompt = FILTER_PROMPT.format(trending=trending_list, rookie_list=rookie_list)
    filtered = chat(prompt)
    filtered = json_repair.loads(filtered)
    with open(os.path.join(date, "filtered.json"), "w", encoding="utf-8") as f:
        f.write(filtered)
    return filtered
