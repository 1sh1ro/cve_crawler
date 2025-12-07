#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CVE信息爬虫 - 基于NVD官方API
支持按日期范围和关键词搜索CVE漏洞信息
"""

import nvdlib
import json
import time
from datetime import datetime, timedelta
import csv
import os
import argparse
from typing import List, Dict, Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class CVEScraper:
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化CVE爬虫
        
        Args:
            api_key: NVD API密钥（可选，但强烈建议使用以提高速度）
        """
        self.api_key = api_key
        self.results = []
        self.has_api_key = api_key is not None
        
        if self.has_api_key:
            print("✓ 使用API密钥模式（速度快10倍）")
        else:
            print("⚠ 未使用API密钥（速度较慢，建议申请免费API Key）")
        
    def split_date_range(self, start_date: str, end_date: str) -> List[tuple]:
        """
        将日期范围分割为120天的小段（NVD API限制）
        
        Args:
            start_date: 开始日期 'YYYY-MM-DD HH:MM'
            end_date: 结束日期 'YYYY-MM-DD HH:MM'
            
        Returns:
            日期范围元组列表
        """
        start = datetime.strptime(start_date, '%Y-%m-%d %H:%M')
        end = datetime.strptime(end_date, '%Y-%m-%d %H:%M')
        
        date_ranges = []
        current = start
        
        while current < end:
            next_date = min(current + timedelta(days=119), end)
            date_ranges.append((
                current.strftime('%Y-%m-%d %H:%M'),
                next_date.strftime('%Y-%m-%d %H:%M')
            ))
            current = next_date + timedelta(seconds=1)
        
        return date_ranges
    
    def search_cves(self, keyword: str, start_date: str, end_date: str, 
                    cpe_name: Optional[str] = None, delay: float = None) -> List:
        """
        搜索CVE漏洞信息
        
        Args:
            keyword: 搜索关键词
            start_date: 开始日期 'YYYY-MM-DD HH:MM'
            end_date: 结束日期 'YYYY-MM-DD HH:MM'
            cpe_name: CPE名称过滤（可选）
            delay: 请求延迟（秒），None则自动根据是否有API Key设置
            
        Returns:
            CVE对象列表
        """
        # 自动设置延迟时间
        if delay is None:
            delay = 0.6 if self.has_api_key else 6
        
        # 分割日期范围
        date_ranges = self.split_date_range(start_date, end_date)
        print(f"\n日期范围被分割为 {len(date_ranges)} 个时间段（NVD API限制每次查询120天）\n")
        
        all_cves = []
        
        for idx, (start, end) in enumerate(date_ranges, 1):
            print(f"[{idx}/{len(date_ranges)}] 正在查询: {start} 到 {end}")
            
            try:
                cves = nvdlib.searchCVE(
                    keywordSearch=keyword,
                    pubStartDate=start,
                    pubEndDate=end,
                    cpeName=cpe_name,
                    key=self.api_key,
                    delay=delay
                )
                
                cve_list = list(cves)
                all_cves.extend(cve_list)
                print(f"  ✓ 找到 {len(cve_list)} 个CVE")
                
                # 避免API限制
                if idx < len(date_ranges):
                    time.sleep(delay)
                    
            except Exception as e:
                print(f"  ✗ 查询失败: {e}")
                continue
        
        print(f"\n总共找到 {len(all_cves)} 个CVE\n")
        return all_cves
    
    def parse_cve_data(self, cve) -> Dict:
        """
        解析nvdlib返回的CVE对象
        
        Args:
            cve: nvdlib.classes.CVE对象
            
        Returns:
            包含完整CVE信息的字典
        """
        # 基本信息
        cve_id = cve.id
        published = cve.published
        last_modified = cve.lastModified
        
        # 描述信息
        description = cve.descriptions[0].value if cve.descriptions else 'N/A'
        
        # CVSS评分 - 优先使用v3，其次v2
        cvss_score = 'N/A'
        cvss_severity = 'N/A'
        cvss_vector = 'N/A'
        exploitability_score = 'N/A'
        impact_score = 'N/A'
        
        if hasattr(cve, 'v31score') and cve.v31score:
            cvss_score = cve.v31score
            cvss_severity = cve.v31severity if hasattr(cve, 'v31severity') else 'N/A'
            cvss_vector = cve.v31vector if hasattr(cve, 'v31vector') else 'N/A'
            exploitability_score = cve.v31exploitability if hasattr(cve, 'v31exploitability') else 'N/A'
            impact_score = cve.v31impactScore if hasattr(cve, 'v31impactScore') else 'N/A'
        elif hasattr(cve, 'v3score') and cve.v3score:
            cvss_score = cve.v3score
            cvss_severity = cve.v3severity if hasattr(cve, 'v3severity') else 'N/A'
            cvss_vector = cve.v3vector if hasattr(cve, 'v3vector') else 'N/A'
            exploitability_score = cve.v3exploitability if hasattr(cve, 'v3exploitability') else 'N/A'
            impact_score = cve.v3impactScore if hasattr(cve, 'v3impactScore') else 'N/A'
        elif hasattr(cve, 'v2score') and cve.v2score:
            cvss_score = cve.v2score
            cvss_severity = cve.v2severity if hasattr(cve, 'v2severity') else 'N/A'
            cvss_vector = cve.v2vector if hasattr(cve, 'v2vector') else 'N/A'
            exploitability_score = cve.v2exploitability if hasattr(cve, 'v2exploitability') else 'N/A'
            impact_score = cve.v2impactScore if hasattr(cve, 'v2impactScore') else 'N/A'
        
        # CWE信息
        cwe_ids = []
        if hasattr(cve, 'cwe') and cve.cwe:
            cwe_ids = [cwe.value for cwe in cve.cwe if hasattr(cwe, 'value')]
        
        # CPE信息（受影响的产品）
        cpe_list = []
        if hasattr(cve, 'cpe'):
            for cpe in cve.cpe[:10]:  # 限制前10个
                if hasattr(cpe, 'criteria'):
                    cpe_list.append(cpe.criteria)
        
        # 参考链接
        ref_urls = []
        if hasattr(cve, 'references'):
            ref_urls = [ref.url for ref in cve.references[:10] if hasattr(ref, 'url')]
        
        # 漏洞状态
        vuln_status = cve.vulnStatus if hasattr(cve, 'vulnStatus') else 'N/A'
        
        return {
            'CVE ID': cve_id,
            '发布日期': published,
            '最后修改': last_modified,
            '漏洞状态': vuln_status,
            '描述': description,
            'CVSS评分': cvss_score,
            '严重程度': cvss_severity,
            'CVSS向量': cvss_vector,
            '可利用性评分': exploitability_score,
            '影响评分': impact_score,
            'CWE类型': ', '.join(cwe_ids) if cwe_ids else 'N/A',
            '受影响产品(CPE)': ' | '.join(cpe_list) if cpe_list else 'N/A',
            '参考链接': ' | '.join(ref_urls) if ref_urls else 'N/A'
        }
    
    def scrape(self, keyword: str, start_date: str, end_date: str, 
               cpe_name: Optional[str] = None) -> List[Dict]:
        """
        执行CVE爬取
        
        Args:
            keyword: 搜索关键词
            start_date: 开始日期 'YYYY-MM-DD HH:MM'
            end_date: 结束日期 'YYYY-MM-DD HH:MM'
            cpe_name: CPE名称过滤（可选）
            
        Returns:
            解析后的CVE信息列表
        """
        print("=" * 80)
        print("CVE信息爬取工具")
        print("=" * 80)
        print(f"关键词: {keyword}")
        print(f"时间范围: {start_date} 到 {end_date}")
        if cpe_name:
            print(f"CPE过滤: {cpe_name}")
        print("=" * 80)
        
        # 搜索CVE
        cves = self.search_cves(keyword, start_date, end_date, cpe_name)
        
        if not cves:
            print("未找到任何CVE")
            return []
        
        # 解析CVE数据
        print("\n正在解析CVE详细信息...")
        for idx, cve in enumerate(cves, 1):
            parsed = self.parse_cve_data(cve)
            self.results.append(parsed)
            print(f"[{idx}/{len(cves)}] {parsed['CVE ID']} - {parsed['严重程度']} ({parsed['CVSS评分']})")
        
        print(f"\n✓ 爬取完成！共获取 {len(self.results)} 个CVE的完整信息")
        return self.results
    
    def save_to_json(self, filename: str = 'cve_results.json'):
        """保存为JSON格式"""
        if not self.results:
            print("⚠ 没有数据可保存")
            return
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"✓ JSON已保存到: {filename}")
    
    def save_to_csv(self, filename: str = 'cve_results.csv'):
        """保存为CSV格式"""
        if not self.results:
            print("⚠ 没有数据可保存")
            return
        
        with open(filename, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.results[0].keys())
            writer.writeheader()
            writer.writerows(self.results)
        print(f"✓ CSV已保存到: {filename}")
    
    def save_to_markdown(self, filename: str = 'cve_results.md', title: str = 'CVE漏洞报告'):
        """保存为Markdown格式"""
        if not self.results:
            print("⚠ 没有数据可保存")
            return
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n")
            f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**CVE数量**: {len(self.results)}\n\n")
            f.write("-" * 80 + "\n\n")
            
            for cve in self.results:
                f.write(f"## {cve['CVE ID']}\n\n")
                f.write(f"- **发布日期**: {cve['发布日期']}\n")
                f.write(f"- **最后修改**: {cve['最后修改']}\n")
                f.write(f"- **漏洞状态**: {cve['漏洞状态']}\n")
                f.write(f"- **严重程度**: {cve['严重程度']} (CVSS: {cve['CVSS评分']})\n")
                f.write(f"- **可利用性评分**: {cve['可利用性评分']}\n")
                f.write(f"- **影响评分**: {cve['影响评分']}\n")
                f.write(f"- **CWE类型**: {cve['CWE类型']}\n")
                f.write(f"- **CVSS向量**: `{cve['CVSS向量']}`\n\n")
                
                f.write(f"**描述**:\n\n{cve['描述']}\n\n")
                
                if cve['受影响产品(CPE)'] != 'N/A':
                    f.write(f"**受影响产品(CPE)**:\n\n")
                    for cpe in cve['受影响产品(CPE)'].split(' | '):
                        if cpe:
                            f.write(f"- `{cpe}`\n")
                    f.write("\n")
                
                if cve['参考链接'] != 'N/A':
                    f.write(f"**参考链接**:\n\n")
                    for url in cve['参考链接'].split(' | '):
                        if url:
                            f.write(f"- {url}\n")
                    f.write("\n")
                
                f.write("-" * 80 + "\n\n")
        
        print(f"✓ Markdown已保存到: {filename}")
    
    def save_all(self, prefix: str = 'cve_results'):
        """保存为所有格式"""
        self.save_to_json(f'{prefix}.json')
        self.save_to_csv(f'{prefix}.csv')
        self.save_to_markdown(f'{prefix}.md')

def get_recent_years_range(years: int = 5) -> tuple:
    """获取最近N年的日期范围"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=years*365)
    return start_date.strftime('%Y-%m-%d 00:00'), end_date.strftime('%Y-%m-%d 23:59')


def main():
    parser = argparse.ArgumentParser(
        description='CVE信息爬虫 - 基于NVD官方API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 爬取最近5年的Linux内核提权漏洞
  python cve_scraper.py -k "linux kernel privilege escalation" -y 5
  
  # 指定日期范围和关键词
  python cve_scraper.py -k "apache" -s "2023-01-01 00:00" -e "2023-12-31 23:59"
  
  # 使用API密钥（推荐）
  python cve_scraper.py -k "windows" -y 3 --api-key YOUR_API_KEY
  
  # 指定CPE过滤
  python cve_scraper.py -k "kernel" -y 2 --cpe "cpe:2.3:o:linux:linux_kernel"
  
  # 自定义输出文件名
  python cve_scraper.py -k "docker" -y 1 -o docker_cves
        """
    )
    
    parser.add_argument('-k', '--keyword', type=str, required=True,
                        help='搜索关键词（必需）')
    parser.add_argument('-s', '--start-date', type=str,
                        help='开始日期，格式: YYYY-MM-DD HH:MM')
    parser.add_argument('-e', '--end-date', type=str,
                        help='结束日期，格式: YYYY-MM-DD HH:MM')
    parser.add_argument('-y', '--years', type=int, default=5,
                        help='最近N年（默认5年，当未指定start-date和end-date时使用）')
    parser.add_argument('--cpe', type=str,
                        help='CPE名称过滤（可选）')
    parser.add_argument('--api-key', type=str,
                        help='NVD API密钥（强烈推荐，可提速10倍）。如未指定，将从环境变量NVD_API_KEY读取')
    parser.add_argument('-o', '--output', type=str, default='cve_results',
                        help='输出文件名前缀（默认: cve_results）')
    parser.add_argument('--json-only', action='store_true',
                        help='仅保存JSON格式')
    parser.add_argument('--csv-only', action='store_true',
                        help='仅保存CSV格式')
    parser.add_argument('--md-only', action='store_true',
                        help='仅保存Markdown格式')
    
    args = parser.parse_args()
    
    # 确定日期范围
    if args.start_date and args.end_date:
        start_date = args.start_date
        end_date = args.end_date
    else:
        start_date, end_date = get_recent_years_range(args.years)
    
    # 获取API密钥（优先级：命令行参数 > 环境变量）
    api_key = args.api_key or os.getenv('NVD_API_KEY')
    
    # 创建爬虫实例
    scraper = CVEScraper(api_key=api_key)
    
    # 执行爬取
    try:
        scraper.scrape(
            keyword=args.keyword,
            start_date=start_date,
            end_date=end_date,
            cpe_name=args.cpe
        )
        
        # 保存结果
        if scraper.results:
            print("\n" + "=" * 80)
            print("正在保存结果...")
            print("=" * 80)
            
            if args.json_only:
                scraper.save_to_json(f'{args.output}.json')
            elif args.csv_only:
                scraper.save_to_csv(f'{args.output}.csv')
            elif args.md_only:
                scraper.save_to_markdown(f'{args.output}.md')
            else:
                scraper.save_all(args.output)
            
            print("\n" + "=" * 80)
            print("✓ 所有任务完成！")
            print("=" * 80)
        else:
            print("\n⚠ 未获取到任何数据")
            
    except KeyboardInterrupt:
        print("\n\n⚠ 用户中断操作")
    except Exception as e:
        print(f"\n✗ 发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
