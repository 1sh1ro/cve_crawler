# 📚 CVE参考链接爬虫使用指南

## 🎯 功能介绍

这个工具可以从CVE JSON文件中提取参考链接，爬取这些链接的内容，并保存到SQLite数据库中，方便后续查询和分析。

---

## 📦 安装依赖

```bash
pip install beautifulsoup4 requests tabulate
```

---

## 🚀 快速开始

### 1. 爬取参考链接

#### 基本用法
```bash
python reference_crawler.py linux_kernel_privilege_escalation_2020-2025.json
```

#### 测试模式（只处理前5个CVE）
```bash
python reference_crawler.py linux_kernel_privilege_escalation_2020-2025.json --max 5
```

#### 自定义数据库名称
```bash
python reference_crawler.py linux_kernel_privilege_escalation_2020-2025.json --db my_cve.db
```

#### 调整请求延迟（避免被封）
```bash
python reference_crawler.py linux_kernel_privilege_escalation_2020-2025.json --delay 2
```

---

## 🔍 查询数据库

### 1. 查看统计信息
```bash
python query_references.py stats
```

输出示例：
```
================================================================================
数据库统计信息
================================================================================
CVE总数: 96
参考链接总数: 450
成功爬取: 380 (84.4%)
失败数量: 70

前10个域名:
+---------------------------+--------+
| 域名                      | 数量   |
+---------------------------+--------+
| git.kernel.org            | 120    |
| security.netapp.com       | 45     |
| bugzilla.redhat.com       | 38     |
| intel.com                 | 25     |
+---------------------------+--------+
```

### 2. 查询特定CVE的所有参考链接
```bash
python query_references.py cve CVE-2020-25221
```

### 3. 搜索特定域名的所有链接
```bash
python query_references.py domain intel.com
```

### 4. 查看爬取的内容
```bash
# 查看某个CVE的所有内容
python query_references.py content CVE-2020-25221

# 查看某个CVE中特定URL的内容
python query_references.py content CVE-2020-25221 --url intel.com
```

### 5. 导出到CSV
```bash
python query_references.py export --output my_export.csv
```

---

## 📊 数据库结构

### CVE表 (cves)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| cve_id | TEXT | CVE编号 |
| description | TEXT | 漏洞描述 |
| cvss_score | REAL | CVSS评分 |
| severity | TEXT | 严重程度 |
| published_date | TEXT | 发布日期 |
| created_at | TIMESTAMP | 创建时间 |

### 参考链接表 (references)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| cve_id | TEXT | CVE编号（外键） |
| url | TEXT | 参考链接URL |
| domain | TEXT | 域名 |
| title | TEXT | 页面标题 |
| content | TEXT | 页面内容 |
| status_code | INTEGER | HTTP状态码 |
| crawled_at | TIMESTAMP | 爬取时间 |
| error | TEXT | 错误信息 |

---

## 💡 使用场景

### 场景1: 分析Intel安全公告
```bash
# 1. 爬取数据
python reference_crawler.py linux_kernel_privilege_escalation_2020-2025.json

# 2. 查询Intel相关链接
python query_references.py domain intel.com

# 3. 查看具体内容
python query_references.py content CVE-2021-1052 --url intel.com
```

### 场景2: 批量分析漏洞修复补丁
```bash
# 查询所有git.kernel.org的链接
python query_references.py domain git.kernel.org

# 导出到CSV进行进一步分析
python query_references.py export --output kernel_patches.csv
```

### 场景3: 监控特定厂商的安全公告
```bash
# 搜索特定厂商
python query_references.py domain redhat.com
python query_references.py domain debian.org
python query_references.py domain ubuntu.com
```

---

## 🔧 高级用法

### 直接使用Python API

```python
from reference_crawler import ReferenceCrawler

# 创建爬虫实例
crawler = ReferenceCrawler(db_name='my_cve.db')

# 处理JSON文件
crawler.process_json_file(
    'linux_kernel_privilege_escalation_2020-2025.json',
    max_cves=10,  # 只处理前10个
    delay=2       # 每次请求延迟2秒
)
```

### 使用查询API

```python
from query_references import ReferenceQuery

# 创建查询实例
query = ReferenceQuery(db_name='cve_references.db')

# 获取统计信息
query.get_statistics()

# 搜索特定CVE
query.search_by_cve('CVE-2020-25221')

# 搜索特定域名
query.search_by_domain('intel.com')

# 导出数据
query.export_to_csv('my_export.csv')
```

---

## ⚠️ 注意事项

### 1. 爬取速度
- 默认每个请求延迟1秒，避免被目标网站封禁
- 可以通过 `--delay` 参数调整延迟时间
- 建议使用 `--max` 参数先测试少量数据

### 2. 网络问题
- 某些网站可能需要VPN才能访问
- 超时设置为10秒，超时会记录错误
- 失败的链接会在数据库中标记错误信息

### 3. 内容提取
- 自动移除JavaScript和CSS
- 内容限制在10000字符以内
- 某些动态加载的内容可能无法获取

### 4. 数据库管理
- 数据库文件默认为 `cve_references.db`
- 可以使用SQLite工具直接查询数据库
- 支持重复运行，会更新已存在的记录

---

## 📈 性能优化

### 并发爬取（高级）
如果需要更快的爬取速度，可以修改代码使用多线程：

```python
from concurrent.futures import ThreadPoolExecutor

def crawl_references_parallel(self, references, cve_id, max_workers=5):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(self.crawl_url, url): url for url in references}
        for future in futures:
            url = futures[future]
            result = future.result()
            self.save_reference_to_db(cve_id, url, result)
```

---

## 🛠️ 故障排除

### 问题1: 数据库锁定
```bash
# 如果遇到数据库锁定，关闭所有访问数据库的程序
# 或者使用新的数据库文件
python reference_crawler.py data.json --db new_db.db
```

### 问题2: 编码错误
```bash
# 确保JSON文件是UTF-8编码
# 可以使用文本编辑器转换编码
```

### 问题3: 依赖缺失
```bash
# 安装所有依赖
pip install beautifulsoup4 requests tabulate lxml
```

---

## 📝 示例工作流

### 完整的分析流程

```bash
# 1. 爬取CVE数据
python cve_scraper.py --keyword "linux kernel privilege escalation" --start-date 2020-01-01

# 2. 爬取参考链接（先测试5个）
python reference_crawler.py linux_kernel_privilege_escalation_2020-2025.json --max 5

# 3. 查看统计信息
python query_references.py stats

# 4. 如果测试正常，爬取全部
python reference_crawler.py linux_kernel_privilege_escalation_2020-2025.json

# 5. 分析特定厂商
python query_references.py domain intel.com

# 6. 导出结果
python query_references.py export --output analysis_results.csv
```

---

## 🎓 扩展建议

### 1. 添加更多数据源
- 可以扩展爬虫支持特定网站的深度爬取
- 例如：GitHub Issues、邮件列表归档等

### 2. 内容分析
- 使用NLP技术分析漏洞描述
- 提取关键信息（受影响版本、修复方法等）

### 3. 可视化
- 使用matplotlib生成统计图表
- 创建Web界面展示数据

### 4. 自动化监控
- 定期运行爬虫获取最新数据
- 发现新漏洞时发送通知

---

**祝你使用愉快！** 🎉
