import datetime
import codecs
import requests
import os
from pyquery import PyQuery as pq
from tqdm import tqdm
import json
from dotenv import load_dotenv
import re

load_dotenv()
REPO_DIR = 'repos'

def create_date_directory(date):
    """创建以日期命名的目录"""
    target_dir = os.path.join(REPO_DIR, date)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # 在date目录下创建trending和rookies子目录
    trending_dir = os.path.join(target_dir, "trending")
    rookies_dir = os.path.join(target_dir, "rookies")

    if not os.path.exists(trending_dir):
        os.makedirs(trending_dir)

    if not os.path.exists(rookies_dir):
        os.makedirs(rookies_dir)

    return date, trending_dir, rookies_dir


def createMarkdown(date, language, directory):
    """为每种语言创建单独的 Markdown 文件"""
    if not language:
        language = "all"

    filename = os.path.join(directory, f"{language}.md")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"## {date} - {language}\n")

    return filename


def createJson(language, directory):
    if not language:
        language = "all"
    filename = os.path.join(directory, f"{language}.json")
    return filename


def scrape_trending(language, filename):
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip,deflate,sdch",
        "Accept-Language": "zh-CN,zh;q=0.8",
    }

    url = "https://github.com/trending/{language}?since=weekly".format(
        language=language if language != "all" else ""
    )
    r = requests.get(url, headers=HEADERS)
    assert r.status_code == 200

    d = pq(r.content)
    items = d("div.Box article.Box-row")

    # codecs to solve the problem utf-8 codec like chinese
    json_data = []
    with codecs.open(filename, "w", "utf-8") as f:
        for item in items:
            i = pq(item)
            title = i(".lh-condensed a").text().replace(" ", "")
            # owner = i(".lh-condensed span.text-normal").text()
            description = i("p.col-9").text()
            star = (
                i(".d-inline-block.float-sm-right")
                .text()
                .split("stars this")[0]
                .replace(",", "")
                .strip()
            )
            url = i(".lh-condensed a").attr("href")
            url = "https://github.com" + url

            introduction = get_readme(title)
            json_data.append(
                {
                    "title": title,
                    "description": description,
                    "star": int(star),
                    "url": url,
                    "introduction": introduction,
                }
            )
        json.dump(json_data, f, ensure_ascii=False, indent=4)


def scrape_rookie_trending(language, filename, last_week):
    language_flag = f"+language:{language}" if language != "all" else ""
    url = f"https://api.github.com/search/repositories?q=created:>{last_week}{language_flag}&sort=stars&order=desc&per_page=10"

    payload = {}
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
        "X-GitHub-Api-Version": "2022-11-28",
        "Cookie": "_octo=GH1.1.103830472.1747908073; logged_in=no",
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)
    items = data["items"]

    json_data = []
    for item in items:
        introduction = get_readme(item["full_name"].replace(" ", ""))
        obj = {
            "title": item["full_name"],
            "description": item["description"],
            "url": item["html_url"],
            "star": item["stargazers_count"],
            "introduction": introduction,
        }
        json_data.append(obj)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)


def get_readme(repo_name):
    meta_url = f"https://api.github.com/repos/{repo_name}/readme"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}",
        "X-GitHub-Api-Version": "2022-11-28",
        "Cookie": "_octo=GH1.1.103830472.1747908073; logged_in=no",
    }
    response = requests.request("GET", meta_url, headers=headers)
    if response.status_code != 200:
        print(f"获取 README 元数据失败: {response.status_code}, {response.text}")
        return ""

    response_json = response.json()
    readme_url = response_json["download_url"]
    try:
        content_response = requests.request("GET", readme_url, headers=headers)
    except Exception as e:
        print(f"获取 README 内容失败: {e}\n 仓库名称: {repo_name} \n 仓库URL: {readme_url}")
        return ""
    if content_response.status_code != 200:
        print(f"获取 README 内容失败: {content_response.status_code}")
        return ""

    markdown_text = content_response.text
    # 找到第一个和第二个标题
    titles = re.finditer(r"^#+ .*$", markdown_text, re.MULTILINE)
    try:
        first_title = next(titles)
        second_title = next(titles)
        introduction = markdown_text[first_title.end() : second_title.start()]

        if introduction.strip() == "":
            try:
                third_title = next(titles)
                introduction = markdown_text[second_title.end() : third_title.start()]
            except StopIteration:
                introduction = markdown_text[second_title.end() :]

        # 清理HTML标签（包括多行的标签块）
        introduction = re.sub(
            r"<(div|table|pre|details|summary|section|header|footer|nav|article|aside)[\s\S]*?</\1>",
            "",
            introduction,
            flags=re.DOTALL,
        )

        # 清理Markdown链接（整行的链接，而非行内链接）
        introduction = re.sub(r"^\[.*?\]\(.*?\)$", "", introduction, flags=re.MULTILINE)
        introduction = re.sub(
            r"^!\[.*?\]\(.*?\)$", "", introduction, flags=re.MULTILINE
        )

        # 清理空白行并修剪空白字符
        introduction = re.sub(r"\n\s*\n+", "\n\n", introduction)
        introduction = introduction.strip()

    except StopIteration:
        introduction = ""
    return introduction


def start_scrape(lans):
    strdate = datetime.datetime.now().strftime("%Y-%m-%d")
    last_week = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime(
        "%Y-%m-%d"
    )

    # 创建以日期命名的目录
    _, trending_directory, rookies_directory = create_date_directory(strdate)

    
    for lan in tqdm(lans):
        # 为每种语言创建单独的 Markdown 文件
        # lang_filename = createMarkdown(strdate, lan, directory)
        json_filename = createJson(lan, trending_directory)
        scrape_trending(lan, json_filename)

        # 为新兴项目创建json文件
        rookies_json_filename = createJson(lan, rookies_directory)
        scrape_rookie_trending(lan, rookies_json_filename, last_week)

    return strdate


if __name__ == "__main__":
    start_scrape()
