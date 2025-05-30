# tests/test_wiki.py

import unittest
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nodes.wiki import fetch_and_parse_to_markdown


class TestWikiParser(unittest.TestCase):
    def setUp(self):
        self.url = "https://deepwiki.com/saxpjexck/lsix"
        self.output_file = os.path.join(os.path.dirname(__file__), "test_output.md")

    def test_deepwiki_parsing(self):
        # 测试解析功能
        markdown_content = fetch_and_parse_to_markdown(self.url)

        # 基本内容测试
        expected_elements = [
            "# Overview",
            # "## Project Purpose",
            # "### Core Components",
            # "the AI Hedge Fund project",
            # "* Core components handle",
            # "* User Interface",
        ]

        # 保存测试文件
        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        for element in expected_elements:
            self.assertIn(element, markdown_content, f"未找到预期的内容: {element}")

        # 验证文件保存
        self.assertTrue(os.path.exists(self.output_file))

        # 验证保存的内容
        with open(self.output_file, "r", encoding="utf-8") as f:
            saved_content = f.read()
            self.assertEqual(markdown_content, saved_content)

    def tearDown(self):
        # 清理测试文件
        if os.path.exists(self.output_file):
            os.remove(self.output_file)


if __name__ == "__main__":
    unittest.main()
