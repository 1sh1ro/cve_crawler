# CVE爬虫演示脚本

本文档提供了一个完整的演示脚本，可用于录制演示视频或现场演示。

## 演示场景1: 快速开始（3分钟）

### 准备工作
```bash
# 确保已安装Python 3.7+
python --version

# 克隆或下载项目
cd cve-scraper
```

### 演示步骤

**1. 安装依赖（30秒）**
```bash
pip install -r requirements.txt
```
说明：只需要一个依赖包 nvdlib

**2. 查看帮助（30秒）**
```bash
python cve_scraper.py --help
```
说明：展示所有可用的命令行参数

**3. 运行第一个搜索（2分钟）**
```bash
python cve_scraper.py -k "linux kernel" -y 1
```
说明：
- 搜索最近1年的Linux内核相关CVE
- 展示实时进度
- 自动保存为3种格式

**4. 查看结果**
```bash
# Windows
type cve_results.json
start cve_results.csv
notepad cve_results.md

# Linux/Mac
cat cve_results.json
open cve_results.csv
cat cve_results.md
```

## 演示场景2: 高级功能（5分钟）

### 1. 使用API密钥（1分钟）
```bash
python cve_scraper.py -k "apache" -y 2 --api-key YOUR_API_KEY
```
说明：
- 速度提升10倍
- 展示速度对比

### 2. 指定日期范围（1分钟）
```bash
python cve_scraper.py -k "windows privilege escalation" -s "2023-01-01 00:00" -e "2023-12-31 23:59"
```
说明：
- 精确控制时间范围
- 自动处理120天限制

### 3. 使用CPE过滤（1分钟）
```bash
python cve_scraper.py -k "kernel" -y 1 --cpe "cpe:2.3:o:linux:linux_kernel"
```
说明：
- 过滤特定产品
- 更精准的结果

### 4. 自定义输出（1分钟）
```bash
python cve_scraper.py -k "docker" -y 1 -o docker_cves --json-only
```
说明：
- 自定义文件名
- 选择输出格式

### 5. 交互式模式（1分钟）
```bash
python quick_start.py
```
说明：
- 友好的交互界面
- 逐步引导配置
- 适合新手

## 演示场景3: 实际应用案例（10分钟）

### 案例1: 安全研究员查找提权漏洞

**目标**: 查找最近5年的Linux内核提权漏洞

```bash
python cve_scraper.py -k "linux kernel privilege escalation" -y 5 -o linux_privesc
```

**分析结果**:
1. 打开 `linux_privesc.csv` 用Excel分析
2. 按CVSS评分排序
3. 筛选高危漏洞（CVSS >= 7.0）
4. 查看受影响的内核版本

### 案例2: 企业安全团队监控特定产品

**目标**: 监控Apache相关漏洞

```bash
python cve_scraper.py -k "apache" -s "2024-01-01 00:00" -e "2024-12-31 23:59" -o apache_2024
```

**工作流程**:
1. 定期运行（每周/每月）
2. 对比新增CVE
3. 评估影响范围
4. 制定修复计划

### 案例3: 开发者检查依赖库漏洞

**目标**: 检查Docker相关漏洞

```bash
python cve_scraper.py -k "docker" -y 2 -o docker_vulns
```

**使用场景**:
1. 项目使用Docker
2. 需要了解安全风险
3. 制定升级策略

## 演示场景4: 作为Python模块使用（5分钟）

### 创建自定义脚本

```python
# my_cve_monitor.py
from cve_scraper import CVEScraper
import json

# 创建爬虫
scraper = CVEScraper(api_key='YOUR_API_KEY')

# 搜索多个关键词
keywords = ['linux kernel', 'apache', 'nginx']

all_results = []
for keyword in keywords:
    print(f"搜索: {keyword}")
    results = scraper.scrape(
        keyword=keyword,
        start_date='2024-01-01 00:00',
        end_date='2024-12-31 23:59'
    )
    all_results.extend(results)

# 自定义处理
high_severity = [
    cve for cve in all_results 
    if cve['严重程度'] in ['HIGH', 'CRITICAL']
]

print(f"找到 {len(high_severity)} 个高危漏洞")

# 保存高危漏洞
with open('high_severity_cves.json', 'w', encoding='utf-8') as f:
    json.dump(high_severity, f, ensure_ascii=False, indent=2)
```

运行：
```bash
python my_cve_monitor.py
```

## 演示场景5: 数据分析（5分钟）

### 使用Python分析CVE数据

```python
# analyze_cves.py
import json
import pandas as pd
from collections import Counter

# 读取数据
with open('cve_results.json', 'r', encoding='utf-8') as f:
    cves = json.load(f)

df = pd.DataFrame(cves)

# 统计分析
print("=== CVE统计分析 ===\n")

# 1. 按严重程度统计
print("严重程度分布:")
print(df['严重程度'].value_counts())
print()

# 2. CVSS评分分布
print("CVSS评分统计:")
print(f"平均分: {df['CVSS评分'].mean():.2f}")
print(f"最高分: {df['CVSS评分'].max()}")
print(f"最低分: {df['CVSS评分'].min()}")
print()

# 3. CWE类型统计
cwe_list = []
for cwe in df['CWE类型']:
    if cwe != 'N/A':
        cwe_list.extend(cwe.split(', '))

print("Top 10 CWE类型:")
for cwe, count in Counter(cwe_list).most_common(10):
    print(f"  {cwe}: {count}")
print()

# 4. 时间趋势
df['发布日期'] = pd.to_datetime(df['发布日期'])
df['年月'] = df['发布日期'].dt.to_period('M')
print("每月CVE数量:")
print(df['年月'].value_counts().sort_index())
```

## 演示技巧

### 1. 准备工作
- 提前测试所有命令
- 准备好API密钥
- 清理之前的输出文件
- 确保网络连接正常

### 2. 演示时
- 先展示简单功能
- 逐步增加复杂度
- 解释每个参数的作用
- 展示实际输出结果

### 3. 互动环节
- 询问观众需求
- 现场演示定制搜索
- 回答问题
- 分享使用技巧

### 4. 结束语
- 总结主要功能
- 强调优势（官方API、多格式、易用）
- 提供GitHub链接
- 鼓励贡献和反馈

## 常见问题演示

### Q: 如何加快速度？
A: 使用API密钥
```bash
python cve_scraper.py -k "test" -y 1 --api-key YOUR_KEY
```

### Q: 如何搜索特定时间段？
A: 使用 -s 和 -e 参数
```bash
python cve_scraper.py -k "test" -s "2023-01-01 00:00" -e "2023-12-31 23:59"
```

### Q: 如何只保存JSON？
A: 使用 --json-only
```bash
python cve_scraper.py -k "test" -y 1 --json-only
```

### Q: 如何在Python中使用？
A: 导入模块
```python
from cve_scraper import CVEScraper
scraper = CVEScraper()
results = scraper.scrape(...)
```

## 演示检查清单

- [ ] Python环境正常
- [ ] 依赖已安装
- [ ] 网络连接正常
- [ ] API密钥已准备（可选）
- [ ] 演示脚本已测试
- [ ] 输出目录已清理
- [ ] 演示数据已准备
- [ ] 备用方案已准备

---

祝演示成功！🎬
