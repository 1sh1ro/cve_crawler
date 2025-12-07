#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CVE爬虫快速开始脚本
交互式引导用户使用爬虫
"""

from cve_scraper import CVEScraper, get_recent_years_range
from datetime import datetime
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def print_banner():
    """打印欢迎横幅"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 28 + "CVE信息爬虫" + " " * 39 + "║")
    print("║" + " " * 25 + "快速开始向导" + " " * 40 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n")

def get_user_input():
    """获取用户输入"""
    print("请回答以下问题来配置你的CVE搜索：\n")
    
    # 关键词
    print("1. 请输入搜索关键词")
    print("   示例: linux kernel privilege escalation")
    print("         apache vulnerability")
    print("         windows remote code execution")
    keyword = input("\n   关键词: ").strip()
    
    if not keyword:
        print("   ⚠ 使用默认关键词: linux kernel privilege escalation")
        keyword = "linux kernel privilege escalation"
    
    # 时间范围
    print("\n2. 选择时间范围")
    print("   [1] 最近1年")
    print("   [2] 最近2年")
    print("   [3] 最近3年")
    print("   [4] 最近5年（推荐）")
    print("   [5] 自定义日期范围")
    
    choice = input("\n   选择 [1-5]: ").strip()
    
    if choice == '5':
        print("\n   请输入日期范围（格式: YYYY-MM-DD）")
        start_date = input("   开始日期: ").strip() + " 00:00"
        end_date = input("   结束日期: ").strip() + " 23:59"
    else:
        years_map = {'1': 1, '2': 2, '3': 3, '4': 5}
        years = years_map.get(choice, 5)
        start_date, end_date = get_recent_years_range(years)
        print(f"   ✓ 已选择最近{years}年")
    
    # API密钥
    env_api_key = os.getenv('NVD_API_KEY')
    
    print("\n3. NVD API密钥（可选，但强烈推荐）")
    print("   有API密钥可以提速10倍！")
    print("   申请地址: https://nvd.nist.gov/developers/request-an-api-key")
    
    if env_api_key:
        print(f"   ✓ 检测到环境变量中的API密钥: {env_api_key[:8]}...")
        use_env = input("   使用环境变量中的密钥？[Y/n]: ").strip().lower()
        if use_env != 'n':
            api_key = env_api_key
            print("   ✓ 使用环境变量中的API密钥")
        else:
            api_key = input("   请输入新的API密钥（直接回车跳过）: ").strip()
            if not api_key:
                print("   ⚠ 未使用API密钥，速度会较慢")
                api_key = None
    else:
        print("   如果没有，直接按回车跳过")
        api_key = input("\n   API密钥: ").strip()
        
        if not api_key:
            print("   ⚠ 未使用API密钥，速度会较慢")
            api_key = None
        else:
            print("   ✓ 已配置API密钥")
    
    # 输出格式
    print("\n4. 选择输出格式")
    print("   [1] 所有格式（JSON + CSV + Markdown）")
    print("   [2] 仅JSON")
    print("   [3] 仅CSV")
    print("   [4] 仅Markdown")
    
    format_choice = input("\n   选择 [1-4]: ").strip()
    
    # 输出文件名
    print("\n5. 输出文件名前缀")
    default_name = keyword.replace(' ', '_')[:30]
    print(f"   默认: {default_name}")
    output_name = input("   自定义名称（直接回车使用默认）: ").strip()
    
    if not output_name:
        output_name = default_name
    
    return {
        'keyword': keyword,
        'start_date': start_date,
        'end_date': end_date,
        'api_key': api_key,
        'format_choice': format_choice,
        'output_name': output_name
    }

def confirm_settings(settings):
    """确认设置"""
    print("\n" + "=" * 80)
    print("配置确认")
    print("=" * 80)
    print(f"关键词: {settings['keyword']}")
    print(f"时间范围: {settings['start_date']} 到 {settings['end_date']}")
    print(f"API密钥: {'已配置' if settings['api_key'] else '未配置'}")
    print(f"输出文件: {settings['output_name']}.*")
    print("=" * 80)
    
    confirm = input("\n确认开始爬取？[Y/n]: ").strip().lower()
    return confirm != 'n'

def main():
    """主函数"""
    print_banner()
    
    print("欢迎使用CVE信息爬虫！")
    print("本工具可以帮助你从NVD数据库获取完整的CVE漏洞信息。\n")
    
    # 获取用户输入
    settings = get_user_input()
    
    # 确认设置
    if not confirm_settings(settings):
        print("\n已取消操作")
        return
    
    # 创建爬虫实例
    print("\n正在初始化爬虫...")
    scraper = CVEScraper(api_key=settings['api_key'])
    
    # 执行爬取
    try:
        scraper.scrape(
            keyword=settings['keyword'],
            start_date=settings['start_date'],
            end_date=settings['end_date']
        )
        
        # 保存结果
        if scraper.results:
            print("\n" + "=" * 80)
            print("正在保存结果...")
            print("=" * 80)
            
            format_choice = settings['format_choice']
            output_name = settings['output_name']
            
            if format_choice == '2':
                scraper.save_to_json(f'{output_name}.json')
            elif format_choice == '3':
                scraper.save_to_csv(f'{output_name}.csv')
            elif format_choice == '4':
                scraper.save_to_markdown(f'{output_name}.md')
            else:
                scraper.save_all(output_name)
            
            print("\n" + "=" * 80)
            print("✓ 所有任务完成！")
            print("=" * 80)
            print(f"\n共获取 {len(scraper.results)} 个CVE的完整信息")
            print(f"文件已保存到当前目录\n")
        else:
            print("\n⚠ 未找到任何CVE数据")
    
    except KeyboardInterrupt:
        print("\n\n⚠ 用户中断操作")
    except Exception as e:
        print(f"\n✗ 发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
