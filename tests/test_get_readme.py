import os
from dotenv import load_dotenv
import sys
import json

# 添加父目录到路径，以便导入scraper模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from steps.scraper import get_readme

def test_get_readme():
    """测试get_readme函数能否正确获取README介绍内容"""
    # 加载环境变量
    load_dotenv()
    
    # 确保GITHUB_TOKEN环境变量存在
    if not os.getenv('GITHUB_TOKEN'):
        print("错误: 请确保设置了GITHUB_TOKEN环境变量")
        return
    
    # 测试几个知名的仓库
    repos = [
        "Gen-Verse/MMaDA"
    ]
    
    results = {}
    
    for repo in repos:
        print(f"\n测试仓库: {repo}")
        try:
            introduction = get_readme(repo)
            
            # 打印获取到的介绍内容的前200个字符
            preview = introduction
            print(f"获取到的介绍内容: {preview}")
            
            # 验证获取的内容不为空
            if introduction:
                print(f"✓ 仓库 {repo} 测试通过")
                results[repo] = "通过"
            else:
                print(f"✗ 仓库 {repo} 测试失败: README介绍内容为空")
                results[repo] = "失败 - 内容为空"
        except Exception as e:
            print(f"✗ 仓库 {repo} 测试出错: {str(e)}")
            results[repo] = f"出错 - {str(e)}"
    
    # 输出总结
    print("\n测试结果总结:")
    for repo, result in results.items():
        print(f"{repo}: {result}")
    
    # 保存测试结果到文件
    with open("readme_test_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print("\n测试结果已保存到 readme_test_results.json 文件")

if __name__ == "__main__":
    test_get_readme() 