#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CVE参考链接数据库查询工具
"""

import sqlite3
import argparse
from tabulate import tabulate

class ReferenceQuery:
    def __init__(self, db_name='cve_references.db'):
        self.db_name = db_name
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def get_statistics(self):
        """获取统计信息"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # CVE总数
        cursor.execute("SELECT COUNT(*) FROM cves")
        total_cves = cursor.fetchone()[0]
        
        # 参考链接总数
        cursor.execute("SELECT COUNT(*) FROM reference_links")
        total_refs = cursor.fetchone()[0]
        
        # 成功爬取的链接
        cursor.execute("SELECT COUNT(*) FROM reference_links WHERE status_code = 200")
        successful_refs = cursor.fetchone()[0]
        
        # 失败的链接
        cursor.execute("SELECT COUNT(*) FROM reference_links WHERE error IS NOT NULL")
        failed_refs = cursor.fetchone()[0]
        
        # 按域名统计
        cursor.execute("""
            SELECT domain, COUNT(*) as count 
            FROM reference_links 
            GROUP BY domain 
            ORDER BY count DESC 
            LIMIT 10
        """)
        top_domains = cursor.fetchall()
        
        conn.close()
        
        print("\n" + "=" * 80)
        print("数据库统计信息")
        print("=" * 80)
        print(f"CVE总数: {total_cves}")
        print(f"参考链接总数: {total_refs}")
        print(f"成功爬取: {successful_refs} ({successful_refs/total_refs*100:.1f}%)" if total_refs > 0 else "成功爬取: 0")
        print(f"失败数量: {failed_refs}")
        
        print("\n前10个域名:")
        print(tabulate(top_domains, headers=['域名', '数量'], tablefmt='grid'))
        print("=" * 80)
    
    def search_by_cve(self, cve_id):
        """根据CVE ID搜索"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # 获取CVE信息
        cursor.execute("SELECT * FROM cves WHERE cve_id = ?", (cve_id,))
        cve = cursor.fetchone()
        
        if not cve:
            print(f"未找到CVE: {cve_id}")
            conn.close()
            return
        
        print("\n" + "=" * 80)
        print(f"CVE信息: {cve_id}")
        print("=" * 80)
        print(f"描述: {cve[2]}")
        print(f"CVSS评分: {cve[3]}")
        print(f"严重程度: {cve[4]}")
        print(f"发布日期: {cve[5]}")
        
        # 获取参考链接
        cursor.execute("""
            SELECT url, domain, title, status_code, error, crawled_at
            FROM reference_links 
            WHERE cve_id = ?
        """, (cve_id,))
        refs = cursor.fetchall()
        
        print(f"\n参考链接 ({len(refs)} 个):")
        for idx, ref in enumerate(refs, 1):
            print(f"\n[{idx}] {ref[0]}")
            print(f"    域名: {ref[1]}")
            print(f"    标题: {ref[2] if ref[2] else 'N/A'}")
            print(f"    状态: {ref[3] if ref[3] else 'N/A'}")
            if ref[4]:
                print(f"    错误: {ref[4]}")
            print(f"    爬取时间: {ref[5]}")
        
        conn.close()
        print("=" * 80)
    
    def search_by_domain(self, domain):
        """根据域名搜索"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT cve_id, url, title, status_code
            FROM reference_links 
            WHERE domain LIKE ?
            ORDER BY cve_id
        """, (f'%{domain}%',))
        refs = cursor.fetchall()
        
        if not refs:
            print(f"未找到域名包含 '{domain}' 的链接")
            conn.close()
            return
        
        print("\n" + "=" * 80)
        print(f"域名搜索结果: {domain} ({len(refs)} 个)")
        print("=" * 80)
        
        data = [[ref[0], ref[1][:50] + '...', ref[2][:40] if ref[2] else 'N/A', ref[3]] for ref in refs]
        print(tabulate(data, headers=['CVE ID', 'URL', '标题', '状态码'], tablefmt='grid'))
        
        conn.close()
        print("=" * 80)
    
    def get_content(self, cve_id, url_pattern=None):
        """获取爬取的内容"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if url_pattern:
            cursor.execute("""
                SELECT url, title, content, status_code
                FROM reference_links 
                WHERE cve_id = ? AND url LIKE ?
            """, (cve_id, f'%{url_pattern}%'))
        else:
            cursor.execute("""
                SELECT url, title, content, status_code
                FROM reference_links 
                WHERE cve_id = ?
            """, (cve_id,))
        
        refs = cursor.fetchall()
        
        if not refs:
            print(f"未找到内容")
            conn.close()
            return
        
        for ref in refs:
            print("\n" + "=" * 80)
            print(f"URL: {ref[0]}")
            print(f"标题: {ref[1]}")
            print(f"状态码: {ref[3]}")
            print("=" * 80)
            if ref[2]:
                print(ref[2][:1000])  # 只显示前1000字符
                if len(ref[2]) > 1000:
                    print("\n... (内容已截断)")
            else:
                print("(无内容)")
            print("=" * 80)
        
        conn.close()
    
    def export_to_csv(self, output_file='references_export.csv'):
        """导出到CSV"""
        import csv
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT r.cve_id, c.severity, c.cvss_score, r.url, r.domain, 
                   r.title, r.status_code, r.error, r.crawled_at
            FROM reference_links r
            JOIN cves c ON r.cve_id = c.cve_id
            ORDER BY r.cve_id
        """)
        
        rows = cursor.fetchall()
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['CVE ID', '严重程度', 'CVSS评分', 'URL', '域名', 
                           '标题', '状态码', '错误', '爬取时间'])
            writer.writerows(rows)
        
        conn.close()
        print(f"✓ 已导出到: {output_file} ({len(rows)} 条记录)")

def main():
    parser = argparse.ArgumentParser(description='CVE参考链接数据库查询工具')
    parser.add_argument('--db', default='cve_references.db', help='数据库文件名')
    
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # 统计命令
    subparsers.add_parser('stats', help='显示统计信息')
    
    # CVE搜索命令
    cve_parser = subparsers.add_parser('cve', help='根据CVE ID搜索')
    cve_parser.add_argument('cve_id', help='CVE ID')
    
    # 域名搜索命令
    domain_parser = subparsers.add_parser('domain', help='根据域名搜索')
    domain_parser.add_argument('domain', help='域名')
    
    # 内容查看命令
    content_parser = subparsers.add_parser('content', help='查看爬取的内容')
    content_parser.add_argument('cve_id', help='CVE ID')
    content_parser.add_argument('--url', help='URL模式（可选）')
    
    # 导出命令
    export_parser = subparsers.add_parser('export', help='导出到CSV')
    export_parser.add_argument('--output', default='references_export.csv', help='输出文件名')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    query = ReferenceQuery(db_name=args.db)
    
    if args.command == 'stats':
        query.get_statistics()
    elif args.command == 'cve':
        query.search_by_cve(args.cve_id)
    elif args.command == 'domain':
        query.search_by_domain(args.domain)
    elif args.command == 'content':
        query.get_content(args.cve_id, args.url)
    elif args.command == 'export':
        query.export_to_csv(args.output)

if __name__ == "__main__":
    main()
