import requests
from pyquery import PyQuery as pq
import os
import json


def fetch_and_parse_to_markdown(url):
    # 获取网页内容
    response = requests.get(url)
    if response.status_code != 200:
        return f"获取网页失败，状态码: {response.status_code}"

    # 使用PyQuery解析HTML
    doc = pq(response.text)

    # 找到指定的容器元素
    container = doc(
        ".prose-custom.prose-custom-md.prose-custom-gray.\\!max-w-none.text-neutral-300.\\[overflow-wrap\\:anywhere\\]"
    )

    if not container:
        print(f"{url} may not indexed")
        return None

    # 提取标题和段落元素
    elements = container.find(
        "h1, h2, h3, h4, h5, h6, p, ol, ul, li, table, thead, tbody, tr, th, td"
    )

    markdown = ""
    list_stack = []  # 跟踪列表的嵌套
    number_stack = []  # 跟踪有序列表的数字

    for el in elements.items():
        tag = el[0].tag
        text = el.text().strip()  # 获取并清理文本内容

        # 处理标题
        if tag.startswith("h"):
            level = int(tag[1]) + 1  # 增加一级
            level = min(level, 6)  # 限制最大级别为6
            markdown += "#" * level + " " + text + "\n\n"

        # 处理段落，跳过以Source:开头的内容
        elif tag == "p":
            if not text.startswith("Sources:"):  # 添加这个判断
                markdown += text + "\n\n"
            else:
                markdown += "\n\n"

        # 处理有序列表
        elif tag == "ol":
            list_stack.append("ordered")
            number_stack.append(1)

        # 处理无序列表
        elif tag == "ul":
            list_stack.append("unordered")
            number_stack.append(0)

        # 处理列表项
        elif tag == "li":
            indent = "  " * (len(list_stack) - 1)
            if list_stack and list_stack[-1] == "ordered":
                current_number = number_stack[-1]
                markdown += f"{indent}{current_number}. {el.text()}\n"
                number_stack[-1] = current_number + 1
            else:
                markdown += f"{indent}* {el.text()}\n"

        # 处理表格
        elif tag == "table":
            table = el
            # 处理表头
            headers = []
            header_row = table("thead tr th")  # 直接在table元素中查找
            for th in header_row.items():
                headers.append(th.text().strip())

            if headers:
                # 添加表头行
                markdown += "| " + " | ".join(headers) + " |\n"
                # 添加分隔行
                markdown += "| " + " | ".join(["---" for _ in headers]) + " |\n"

            # 处理表格内容
            tbody_rows = table("tbody tr")  # 直接在table元素中查找
            for tr in tbody_rows.items():
                row_data = []
                for td in tr("td").items():
                    # 检查是否包含code标签
                    code = td.find("code")
                    if code:
                        # 如果有code标签，使用`包裹内容
                        row_data.append(f"`{code.text().strip()}`")
                    else:
                        row_data.append(td.text().strip())
                markdown += "| " + " | ".join(row_data) + " |\n"

            markdown += "\n"

        # 列表结束
        if (
            tag in ["ol", "ul"]
            and el.next()
            and el.next()[0].tag not in ["ol", "ul", "li"]
        ):
            if list_stack:
                list_stack.pop()
                number_stack.pop()
            markdown += "\n"

    return markdown


def get_wiki(language, date):
    filtered_path = os.path.join("repos", date, "filtered")
    wiki_path = os.path.join("repos", date, "wiki")
    if not os.path.exists(wiki_path):
        os.makedirs(wiki_path)
    with open(
        os.path.join(filtered_path, f"{language}.json"), "r", encoding="utf-8"
    ) as f:
        repos = json.load(f)
    for repo in repos:
        wiki_url = repo["url"].replace("github.com", "deepwiki.com")
        markdown = fetch_and_parse_to_markdown(wiki_url)
        if not markdown:
            continue
        markdown = f"# {repo['name']}\n\n" + markdown
        repo_name = repo["name"].split("/")[-1]
        with open(
            os.path.join(wiki_path, f"{repo_name}.md"), "w", encoding="utf-8"
        ) as f:
            f.write(markdown)
    return repos


def summarize_wiki():
    pass
