import os
import sys
import unittest
from dotenv import load_dotenv

# 添加父目录到路径，以便导入scraper模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from nodes.scraper import get_readme

class TestScraper(unittest.TestCase):
    
    def setUp(self):
        # 加载环境变量
        load_dotenv()
        # 确保GITHUB_TOKEN环境变量存在
        self.assertTrue(os.getenv('GITHUB_TOKEN'), "请确保设置了GITHUB_TOKEN环境变量")
    
    def test_get_readme(self):
        """测试get_readme函数能否正确获取README介绍内容"""
        # 测试几个知名的仓库
        repos = [
            "microsoft/vscode",
            "tensorflow/tensorflow",
            "facebook/react",
            "golang/go",
            "rust-lang/rust"
        ]
        
        for repo in repos:
            print(f"\n测试仓库: {repo}")
            introduction = get_readme(repo)
            
            # 打印获取到的介绍内容的前200个字符
            preview = introduction[:200] + "..." if len(introduction) > 200 else introduction
            print(f"获取到的介绍内容: {preview}")
            
            # 验证获取的内容不为空
            self.assertTrue(introduction, f"仓库 {repo} 的README介绍内容不应为空")
            print(f"✓ 仓库 {repo} 测试通过")

if __name__ == "__main__":
    unittest.main() 