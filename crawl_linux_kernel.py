#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
爬取近5年的Linux内核提权漏洞
"""

from cve_scraper import CVEScraper
from datetime import datetime
import os
from dotenv import load_dotenv

def main():
    print("\n" + "=" * 80)
    print("开始爬取近5年的Linux内核提权漏洞")
    print("=" * 80)
    
    # 加载环境变量
    load_dotenv()
    
    # 读取API密钥
    api_key = os.getenv('NVD_API_KEY')
    
    if api_key:
        print(f"✓ 已加载API密钥: {api_key[:8]}...")
    else:
        print("⚠ 未找到API密钥，将使用较慢的速度")
    
    # 创建爬虫实例
    scraper = CVEScraper(api_key=api_key)
    
    # 设置搜索参数
    keyword = "linux kernel privilege escalation"
    start_date = "2020-01-01 00:00"
    end_date = "2025-12-07 23:59"
    
    print(f"\n搜索参数:")
    print(f"  关键词: {keyword}")
    print(f"  时间范围: {start_date} 到 {end_date}")
    print(f"  API密钥: {'已配置' if api_key else '未配置'}")
    print("\n" + "=" * 80)
    
    # 执行爬取
    try:
        scraper.scrape(
            keyword=keyword,
            start_date=start_date,
            end_date=end_date
        )
        
        # 保存结果
        if scraper.results:
            output_name = "linux_kernel_privilege_escalation_2020-2025"
            
            print("\n" + "=" * 80)
            print("正在保存结果...")
            print("=" * 80)
            
            scraper.save_all(output_name)
            
            print("\n" + "=" * 80)
            print("✓ 爬取完成！")
            print("=" * 80)
            print(f"\n共获取 {len(scraper.results)} 个Linux内核提权漏洞")
            print(f"\n输出文件:")
            print(f"  - {output_name}.json")
            print(f"  - {output_name}.csv")
            print(f"  - {output_name}.md")
            print(f"\n文件保存在 output/ 目录\n")
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
