#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CVE参考链接爬虫
从JSON文件中提取参考链接，爬取内容并保存到数据库
"""

import json
import sqlite3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
from datetime import datetime
import re

class ReferenceCrawler:
    def __init__(self, db_name='cve_references.db'):
        """初始化爬虫"""
        self.db_name = db_name
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.init_database()
    
    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # 创建CVE表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cves (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cve_id TEXT UNIQUE NOT NULL,
                description TEXT,
                cvss_score REAL,
                severity TEXT,
                published_date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 创建参考链接表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reference_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cve_id TEXT NOT NULL,
                url TEXT NOT NULL,
                domain TEXT,
                title TEXT,
                content TEXT,
                status_code INTEGER,
                crawled_at TIMESTAMP,
                error TEXT,
                FOREIGN KEY (cve_id) REFERENCES cves(cve_id),
                UNIQUE(cve_id, url)
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"✓ 数据库初始化完成: {self.db_name}")
    
    def load_json(self, json_file):
        """加载JSON文件"""
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✓ 加载了 {len(data)} 个CVE记录")
        return data
    
    def extract_references(self, cve_data):
        """从CVE数据中提取参考链接"""
        references = []
        ref_string = cve_data.get('参考链接', '')
        
        if ref_string:
            # 分割链接（用 | 分隔）
            urls = [url.strip() for url in ref_string.split('|') if url.strip()]
            # 去重
            urls = list(set(urls))
            references.extend(urls)
        
        return references
    
    def save_cve_to_db(self, cve_data):
        """保存CVE信息到数据库"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO cves (cve_id, description, cvss_score, severity, published_date)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                cve_data.get('CVE ID'),
                cve_data.get('描述'),
                cve_data.get('CVSS评分'),
                cve_data.get('严重程度'),
                cve_data.get('发布日期')
            ))
            conn.commit()
        except Exception as e:
            print(f"  ⚠ 保存CVE失败: {e}")
        finally:
            conn.close()
    
    def crawl_url(self, url):
        """爬取单个URL的内容"""
        try:
            response = self.session.get(url, timeout=10, allow_redirects=True)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 提取标题
                title = soup.find('title')
                title = title.get_text().strip() if title else ''
                
                # 移除脚本和样式
                for script in soup(['script', 'style']):
                    script.decompose()
                
                # 提取文本内容
                text = soup.get_text()
                # 清理空白
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)
                
                # 限制内容长度
                if len(text) > 10000:
                    text = text[:10000] + '...'
                
                return {
                    'title': title,
                    'content': text,
                    'status_code': response.status_code,
                    'error': None
                }
            else:
                return {
                    'title': None,
                    'content': None,
                    'status_code': response.status_code,
                    'error': f'HTTP {response.status_code}'
                }
        
        except requests.exceptions.Timeout:
            return {'title': None, 'content': None, 'status_code': None, 'error': 'Timeout'}
        except requests.exceptions.ConnectionError:
            return {'title': None, 'content': None, 'status_code': None, 'error': 'Connection Error'}
        except Exception as e:
            return {'title': None, 'content': None, 'status_code': None, 'error': str(e)}
    
    def save_reference_to_db(self, cve_id, url, crawl_result):
        """保存参考链接信息到数据库"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        domain = urlparse(url).netloc
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO reference_links 
                (cve_id, url, domain, title, content, status_code, crawled_at, error)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                cve_id,
                url,
                domain,
                crawl_result.get('title'),
                crawl_result.get('content'),
                crawl_result.get('status_code'),
                datetime.now().isoformat(),
                crawl_result.get('error')
            ))
            conn.commit()
        except Exception as e:
            print(f"    ⚠ 保存失败: {e}")
        finally:
            conn.close()
    
    def process_json_file(self, json_file, max_cves=None, delay=1):
        """处理JSON文件中的所有CVE"""
        print("\n" + "=" * 80)
        print("开始处理CVE参考链接")
        print("=" * 80)
        
        data = self.load_json(json_file)
        
        if max_cves:
            data = data[:max_cves]
            print(f"⚠ 限制处理前 {max_cves} 个CVE")
        
        total_refs = 0
        successful_refs = 0
        
        for idx, cve_data in enumerate(data, 1):
            cve_id = cve_data.get('CVE ID')
            print(f"\n[{idx}/{len(data)}] 处理 {cve_id}")
            
            # 保存CVE信息
            self.save_cve_to_db(cve_data)
            
            # 提取参考链接
            references = self.extract_references(cve_data)
            print(f"  找到 {len(references)} 个参考链接")
            
            # 爬取每个链接
            for ref_idx, url in enumerate(references, 1):
                total_refs += 1
                print(f"  [{ref_idx}/{len(references)}] {url[:60]}...")
                
                # 爬取内容
                result = self.crawl_url(url)
                
                if result['error']:
                    print(f"    ✗ 失败: {result['error']}")
                else:
                    print(f"    ✓ 成功: {result['title'][:50] if result['title'] else 'No title'}")
                    successful_refs += 1
                
                # 保存到数据库
                self.save_reference_to_db(cve_id, url, result)
                
                # 延迟避免被封
                time.sleep(delay)
        
        print("\n" + "=" * 80)
        print("处理完成")
        print("=" * 80)
        print(f"总CVE数: {len(data)}")
        print(f"总链接数: {total_refs}")
        print(f"成功爬取: {successful_refs}")
        print(f"失败数量: {total_refs - successful_refs}")
        print(f"数据库: {self.db_name}")
        print("=" * 80)

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='CVE参考链接爬虫')
    parser.add_argument('json_file', help='CVE JSON文件路径')
    parser.add_argument('--db', default='cve_references.db', help='数据库文件名')
    parser.add_argument('--max', type=int, help='最大处理CVE数量（用于测试）')
    parser.add_argument('--delay', type=float, default=1, help='请求延迟（秒）')
    
    args = parser.parse_args()
    
    crawler = ReferenceCrawler(db_name=args.db)
    crawler.process_json_file(args.json_file, max_cves=args.max, delay=args.delay)

if __name__ == "__main__":
    main()
