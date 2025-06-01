import os

OPENING = (
    "# 开场\n\nRepoke 是一个每周开源简报，帮助你快速获取近期值得关注的开源项目动态。"
)
ENDING = "# 结束\n\n感谢各位的聆听，如果需要详细了解项目细节，可以查看shownotes中各开源项目的链接，我们下周再见！"


def conclude(language, date):
    outline_path = os.path.join("repos", date, "outline", f"{language}.md")
    summary_path = os.path.join("repos", date, "summary", language)
    conclude_path = os.path.join("repos", date, "conclude", f"{language}.md")
    with open(outline_path, "r", encoding="utf-8") as f:
        outline = f.read()
    outline += "\n\n 接下来介绍本周精选开源项目\n\n"
    for file_name in os.listdir(summary_path):
        with open(os.path.join(summary_path, file_name), "r", encoding="utf-8") as f:
            summary = f.read()
        outline = outline + "\n\n" + summary
    with open(conclude_path, "w", encoding="utf-8") as f:
        f.write(OPENING + "\n\n" + outline + "\n\n" + ENDING)
