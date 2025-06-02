#!/usr/bin/env python3
"""
Dingo Marketing AI Agent 演示脚本
快速展示系统的主要功能和使用场景
"""

import requests
import json
import time
from typing import Dict, Any

# API 基础配置
BASE_URL = "http://127.0.0.1:8000/api/v1"
HEADERS = {"Content-Type": "application/json"}

def print_section(title: str):
    """打印章节标题"""
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print(f"{'='*60}")

def print_response(response: requests.Response, title: str = "响应结果"):
    """格式化打印API响应"""
    print(f"\n📊 {title}:")
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        try:
            data = response.json()
            print(json.dumps(data, indent=2, ensure_ascii=False))
        except:
            print(response.text)
    else:
        print(f"错误: {response.text}")

def demo_scenario_1():
    """场景1: 用户分析 - 分析知名开发者"""
    print_section("场景1: 分析知名GitHub用户")
    
    print("📝 场景描述:")
    print("- 分析几个知名的GitHub用户")
    print("- 了解他们的技术背景和社区影响力")
    print("- 制定个性化的互动策略")
    
    # 中文分析
    print("\n🔍 执行中文用户分析...")
    payload = {
        "user_list": ["octocat", "defunkt"],
        "analysis_depth": "basic",
        "language": "zh"
    }
    
    response = requests.post(f"{BASE_URL}/analyze/users", 
                           headers=HEADERS, 
                           data=json.dumps(payload))
    print_response(response, "中文分析结果")
    
    time.sleep(2)
    
    # 英文分析
    print("\n🔍 执行英文用户分析...")
    payload["language"] = "en"
    payload["user_list"] = ["gvanrossum"]  # Python之父
    
    response = requests.post(f"{BASE_URL}/analyze/users", 
                           headers=HEADERS, 
                           data=json.dumps(payload))
    print_response(response, "English Analysis Result")

def demo_scenario_2():
    """场景2: 内容营销活动"""
    print_section("场景2: 创建内容营销活动")
    
    print("📝 场景描述:")
    print("- 为Dingo项目创建技术博客内容")
    print("- 针对开发者群体制定内容策略")
    print("- 生成多种类型的营销材料")
    
    print("\n📝 创建内容营销活动...")
    payload = {
        "name": "Dingo数据质量工具推广",
        "target_audience": "Python开发者和数据工程师",
        "topics": ["数据质量评估", "Python数据工具", "开源项目贡献"],
        "content_types": ["blog", "social", "tutorial"],
        "duration": "2周",
        "keywords": ["数据质量", "Python", "开源", "数据验证"],
        "language": "zh"
    }
    
    response = requests.post(f"{BASE_URL}/campaigns/content", 
                           headers=HEADERS, 
                           data=json.dumps(payload))
    print_response(response, "内容营销活动结果")

def demo_scenario_3():
    """场景3: 社区互动"""
    print_section("场景3: 执行社区互动活动")
    
    print("📝 场景描述:")
    print("- 分析目标项目的GitHub社区状态")
    print("- 与活跃用户进行互动")
    print("- 建立长期的社区关系")
    
    print("\n🤝 执行社区互动...")
    payload = {
        "interaction_types": ["comment", "issue"],
        "target_count": 5,
        "engagement_level": "moderate",
        "language": "zh"
    }
    
    response = requests.post(f"{BASE_URL}/engagement/community", 
                           headers=HEADERS, 
                           data=json.dumps(payload))
    print_response(response, "社区互动结果")

def demo_scenario_4():
    """场景4: 内容生成"""
    print_section("场景4: AI内容生成")
    
    print("📝 场景描述:")
    print("- 使用AI生成技术博客文章")
    print("- 创建社交媒体内容")
    print("- 支持中英文内容生成")
    
    # 中文博客生成
    print("\n✍️ 生成中文技术博客...")
    payload = {
        "content_type": "blog",
        "topic": "如何使用Dingo提升数据质量",
        "target_audience": "数据工程师",
        "tone": "professional",
        "length": "medium",
        "language": "zh",
        "keywords": ["数据质量", "Dingo", "最佳实践"]
    }
    
    response = requests.post(f"{BASE_URL}/content/generate", 
                           headers=HEADERS, 
                           data=json.dumps(payload))
    print_response(response, "中文博客生成结果")
    
    time.sleep(2)
    
    # 英文社交媒体内容
    print("\n📱 生成英文社交媒体内容...")
    payload.update({
        "content_type": "social",
        "topic": "Introducing Dingo: A Python Data Quality Tool",
        "target_audience": "developers",
        "language": "en",
        "keywords": ["data quality", "Python", "open source"]
    })
    
    response = requests.post(f"{BASE_URL}/content/generate", 
                           headers=HEADERS, 
                           data=json.dumps(payload))
    print_response(response, "English Social Media Content")

def demo_scenario_5():
    """场景5: 系统状态和配置"""
    print_section("场景5: 系统状态检查和配置")
    
    print("📝 场景描述:")
    print("- 检查系统运行状态")
    print("- 查看和配置目标仓库")
    print("- 了解可用的工具和Agent")
    
    # 系统状态
    print("\n🔍 检查系统状态...")
    response = requests.get(f"{BASE_URL}/status")
    print_response(response, "系统状态")
    
    time.sleep(1)
    
    # 当前仓库配置
    print("\n📂 查看当前目标仓库...")
    response = requests.get(f"{BASE_URL}/repository")
    print_response(response, "当前仓库配置")
    
    time.sleep(1)
    
    # 工具状态
    print("\n🛠️ 查看工具状态...")
    response = requests.get(f"{BASE_URL}/tools/status")
    print_response(response, "工具状态")

def demo_comprehensive():
    """综合演示场景"""
    print_section("综合演示: 完整营销工作流")
    
    print("📝 场景描述:")
    print("- 执行完整的营销工作流程")
    print("- 包含用户分析、内容创作、社区互动等环节")
    print("- 展示多Agent协作能力")
    
    print("\n🚀 启动综合营销活动...")
    payload = {
        "name": "Dingo项目推广计划",
        "objectives": ["提高项目知名度", "吸引贡献者", "建立技术社区"],
        "target_audience": "Python开发者和数据科学家",
        "duration": "1个月",
        "budget_level": "medium",
        "priority_channels": ["github", "social", "blog"],
        "language": "zh"
    }
    
    response = requests.post(f"{BASE_URL}/campaigns/comprehensive", 
                           headers=HEADERS, 
                           data=json.dumps(payload))
    print_response(response, "综合营销活动结果")

def main():
    """主演示函数"""
    print("🎉 欢迎使用 Dingo Marketing AI Agent 系统!")
    print("本演示将展示系统的主要功能和使用场景")
    
    scenarios = [
        ("用户分析", demo_scenario_1),
        ("内容营销", demo_scenario_2),
        ("社区互动", demo_scenario_3),
        ("内容生成", demo_scenario_4),
        ("系统状态", demo_scenario_5),
        ("综合演示", demo_comprehensive)
    ]
    
    print(f"\n📋 可用演示场景:")
    for i, (name, _) in enumerate(scenarios, 1):
        print(f"  {i}. {name}")
    print(f"  0. 全部演示")
    
    try:
        choice = input(f"\n请选择要演示的场景 (0-{len(scenarios)}): ").strip()
        
        if choice == "0":
            # 全部演示
            for name, func in scenarios:
                func()
                input("\n按回车键继续下一个演示...")
        elif choice.isdigit() and 1 <= int(choice) <= len(scenarios):
            # 单个演示
            name, func = scenarios[int(choice) - 1]
            func()
        else:
            print("❌ 无效选择")
            return
            
    except KeyboardInterrupt:
        print("\n\n👋 演示已取消")
    except Exception as e:
        print(f"\n❌ 演示过程中出现错误: {e}")
    
    print(f"\n🎯 演示完成!")
    print(f"💡 提示: 你可以查看API文档了解更多功能: http://127.0.0.1:8000/docs")

if __name__ == "__main__":
    main() 