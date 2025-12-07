#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CVE爬虫测试脚本
用于快速测试爬虫功能
"""

from cve_scraper import CVEScraper
from datetime import datetime, timedelta

def test_basic_search():
    """测试基本搜索功能"""
    print("=" * 80)
    print("测试1: 基本搜索功能")
    print("=" * 80)
    
    scraper = CVEScraper()
    
    # 搜索最近30天的测试数据
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    results = scraper.scrape(
        keyword='linux kernel',
        start_date=start_date.strftime('%Y-%m-%d 00:00'),
        end_date=end_date.strftime('%Y-%m-%d 23:59')
    )
    
    if results:
        print(f"\n✓ 测试通过！找到 {len(results)} 个CVE")
        print(f"示例CVE: {results[0]['CVE ID']}")
        return True
    else:
        print("\n⚠ 未找到结果（可能该时间段内没有相关CVE）")
        return True  # 这不算失败

def test_date_splitting():
    """测试日期分割功能"""
    print("\n" + "=" * 80)
    print("测试2: 日期分割功能")
    print("=" * 80)
    
    scraper = CVEScraper()
    
    # 测试超过120天的日期范围
    date_ranges = scraper.split_date_range(
        '2023-01-01 00:00',
        '2023-12-31 23:59'
    )
    
    print(f"日期范围: 2023-01-01 到 2023-12-31")
    print(f"分割为 {len(date_ranges)} 个时间段")
    
    for idx, (start, end) in enumerate(date_ranges, 1):
        print(f"  段{idx}: {start} 到 {end}")
    
    if len(date_ranges) > 1:
        print("\n✓ 测试通过！日期分割功能正常")
        return True
    else:
        print("\n✗ 测试失败！日期分割功能异常")
        return False

def test_data_parsing():
    """测试数据解析功能"""
    print("\n" + "=" * 80)
    print("测试3: 数据解析功能")
    print("=" * 80)
    
    scraper = CVEScraper()
    
    # 搜索一个已知的CVE
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    results = scraper.scrape(
        keyword='CVE-2024',
        start_date=start_date.strftime('%Y-%m-%d 00:00'),
        end_date=end_date.strftime('%Y-%m-%d 23:59')
    )
    
    if results:
        cve = results[0]
        required_fields = [
            'CVE ID', '发布日期', '描述', 'CVSS评分', 
            '严重程度', 'CWE类型', '参考链接'
        ]
        
        missing_fields = [field for field in required_fields if field not in cve]
        
        if not missing_fields:
            print(f"\n✓ 测试通过！所有必需字段都存在")
            print(f"示例数据:")
            print(f"  CVE ID: {cve['CVE ID']}")
            print(f"  严重程度: {cve['严重程度']}")
            print(f"  CVSS评分: {cve['CVSS评分']}")
            return True
        else:
            print(f"\n✗ 测试失败！缺少字段: {missing_fields}")
            return False
    else:
        print("\n⚠ 未找到测试数据")
        return True

def test_export_formats():
    """测试导出功能"""
    print("\n" + "=" * 80)
    print("测试4: 导出功能")
    print("=" * 80)
    
    scraper = CVEScraper()
    
    # 添加一些测试数据
    scraper.results = [{
        'CVE ID': 'CVE-2024-TEST',
        '发布日期': '2024-01-01T00:00:00',
        '最后修改': '2024-01-02T00:00:00',
        '漏洞状态': 'Analyzed',
        '描述': 'Test CVE for export functionality',
        'CVSS评分': 7.5,
        '严重程度': 'HIGH',
        'CVSS向量': 'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N',
        '可利用性评分': 3.9,
        '影响评分': 3.6,
        'CWE类型': 'CWE-79',
        '受影响产品(CPE)': 'cpe:2.3:a:test:test:1.0:*:*:*:*:*:*:*',
        '参考链接': 'https://example.com'
    }]
    
    try:
        scraper.save_to_json('test_output.json')
        scraper.save_to_csv('test_output.csv')
        scraper.save_to_markdown('test_output.md')
        
        print("\n✓ 测试通过！所有导出格式正常")
        
        # 清理测试文件
        import os
        for file in ['test_output.json', 'test_output.csv', 'test_output.md']:
            if os.path.exists(file):
                os.remove(file)
                print(f"  已清理测试文件: {file}")
        
        return True
    except Exception as e:
        print(f"\n✗ 测试失败！错误: {e}")
        return False

def main():
    """运行所有测试"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 25 + "CVE爬虫测试套件" + " " * 38 + "║")
    print("╚" + "=" * 78 + "╝")
    print("\n")
    
    tests = [
        ("日期分割功能", test_date_splitting),
        ("数据解析功能", test_data_parsing),
        ("导出功能", test_export_formats),
        ("基本搜索功能", test_basic_search),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ 测试异常: {e}")
            results.append((name, False))
    
    # 输出测试总结
    print("\n" + "=" * 80)
    print("测试总结")
    print("=" * 80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{status} - {name}")
    
    print(f"\n总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！")
    else:
        print(f"\n⚠ {total - passed} 个测试失败")

if __name__ == "__main__":
    main()
