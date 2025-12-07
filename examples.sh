#!/bin/bash
# CVE爬虫使用示例

echo "CVE信息爬虫 - 使用示例"
echo "====================="
echo ""

# 示例1: Linux内核提权漏洞（最近5年）
echo "示例1: 爬取最近5年的Linux内核提权漏洞"
echo "命令: python cve_scraper.py -k \"linux kernel privilege escalation\" -y 5"
echo ""

# 示例2: Apache漏洞（指定日期）
echo "示例2: 爬取2023年的Apache漏洞"
echo "命令: python cve_scraper.py -k \"apache\" -s \"2023-01-01 00:00\" -e \"2023-12-31 23:59\""
echo ""

# 示例3: Windows提权漏洞
echo "示例3: 爬取最近3年的Windows提权漏洞"
echo "命令: python cve_scraper.py -k \"windows privilege escalation\" -y 3"
echo ""

# 示例4: Docker漏洞（使用API密钥）
echo "示例4: 使用API密钥爬取Docker漏洞"
echo "命令: python cve_scraper.py -k \"docker\" -y 2 --api-key YOUR_API_KEY"
echo ""

# 示例5: Kubernetes漏洞（仅JSON）
echo "示例5: 爬取Kubernetes漏洞并仅保存JSON"
echo "命令: python cve_scraper.py -k \"kubernetes\" -y 1 --json-only -o k8s_cves"
echo ""

# 示例6: 使用CPE过滤
echo "示例6: 使用CPE过滤特定Linux内核版本"
echo "命令: python cve_scraper.py -k \"kernel\" -y 2 --cpe \"cpe:2.3:o:linux:linux_kernel\""
echo ""

echo "====================="
echo "提示: 建议申请NVD API密钥以提升速度10倍！"
echo "申请地址: https://nvd.nist.gov/developers/request-an-api-key"
