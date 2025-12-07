# 🔗 CVE参考链接爬虫

## ✨ 新功能介绍

这是一个强大的扩展功能，可以从CVE JSON文件中提取所有参考链接，自动爬取这些链接的内容，并保存到SQLite数据库中，方便后续分析和查询。

---

## 🎯 主要功能

### 1. 自动提取参考链接
- 从CVE JSON文件中提取所有参考链接
- 自动去重，避免重复爬取
- 支持批量处理

### 2. 智能内容爬取
- 自动提取网页标题和正文内容
- 移除JavaScript和CSS，只保留有用信息
- 记录HTTP状态码和错误信息
- 支持自定义请求延迟，避免被封

### 3. 数据库存储
- 使用SQLite数据库存储所有数据
- CVE信息和参考链接分表存储
- 支持重复运行，自动更新已存在的记录
- 完整的外键关联

### 4. 强大的查询功能
- 统计信息查看
- 按CVE ID查询
- 按域名搜索
- 查看爬取的内容
- 导出到CSV

---

## 🚀 快速开始

### 安装依赖
```bash
pip install beautifulsoup4 requests tabulate lxml
```

或者运行：
```bash
install_crawler_deps.bat
```

### 基本使用

#### 1. 爬取参考链接（测试模式）
```bash
python reference_crawler.py linux_kernel_privilege_escalation_2020-2025.json --max 5
```

#### 2. 爬取全部数据
```bash
python reference_crawler.py linux_kernel_privilege_escalation_2020-2025.json
```

#### 3. 查看统计信息
```bash
python query_references.py stats
```

#### 4. 查询特定CVE
```bash
python query_references.py cve CVE-2020-25221
```

#### 5. 搜索特定域名
```bash
python query_references.py domain intel.com
```

#### 6. 查看内容
```bash
python query_references.py content CVE-2020-25221 --url intel.com
```

---

## 📊 测试结果

### 测试数据（前3个CVE）
```
总CVE数: 3
总链接数: 15
成功爬取: 13 (86.7%)
失败数量: 2

前10个域名:
+---------------------+------+
| 域名                  | 数量 |
+=====================+======+
| www.openwall.com    |    3 |
| git.kernel.org      |    3 |
| security.netapp.com |    2 |
| lists.opensuse.org  |    2 |
| lists.debian.org    |    2 |
| bugzilla.redhat.com |    2 |
| cdn.kernel.org      |    1 |
+---------------------+------+
```

### 成功爬取的内容示例
- ✅ Openwall邮件列表归档
- ✅ Git kernel提交记录
- ✅ Debian安全公告
- ✅ Red Hat Bugzilla
- ✅ NetApp安全公告
- ⚠️ 部分网站需要JavaScript（如NetApp）

---

## 💡 使用场景

### 场景1: 深度分析特定漏洞
```bash
# 1. 爬取数据
python reference_crawler.py linux_kernel_privilege_escalation_2020-2025.json

# 2. 查询CVE详情
python query_references.py cve CVE-2023-2163

# 3. 查看所有参考链接的内容
python query_references.py content CVE-2023-2163
```

### 场景2: 分析厂商安全响应
```bash
# 查询Intel的所有安全公告
python query_references.py domain intel.com

# 查询Red Hat的所有Bugzilla
python query_references.py domain bugzilla.redhat.com

# 导出分析
python query_references.py export --output vendor_analysis.csv
```

### 场景3: 追踪补丁信息
```bash
# 查询所有kernel.org的链接
python query_references.py domain kernel.org

# 查看具体补丁内容
python query_references.py content CVE-2020-25221 --url kernel.org
```

---

## 📁 文件说明

### 核心文件
- `reference_crawler.py` - 参考链接爬虫主程序
- `query_references.py` - 数据库查询工具
- `cve_references.db` - SQLite数据库（运行后生成）

### 文档文件
- `REFERENCE_CRAWLER_GUIDE.md` - 详细使用指南
- `REFERENCE_CRAWLER_README.md` - 本文件

### 辅助文件
- `install_crawler_deps.bat` - 依赖安装脚本

---

## 🗄️ 数据库结构

### CVE表 (cves)
```sql
CREATE TABLE cves (
    id INTEGER PRIMARY KEY,
    cve_id TEXT UNIQUE,
    description TEXT,
    cvss_score REAL,
    severity TEXT,
    published_date TEXT,
    created_at TIMESTAMP
)
```

### 参考链接表 (reference_links)
```sql
CREATE TABLE reference_links (
    id INTEGER PRIMARY KEY,
    cve_id TEXT,
    url TEXT,
    domain TEXT,
    title TEXT,
    content TEXT,
    status_code INTEGER,
    crawled_at TIMESTAMP,
    error TEXT,
    UNIQUE(cve_id, url)
)
```

---

## ⚙️ 命令行参数

### reference_crawler.py
```bash
python reference_crawler.py <json_file> [选项]

选项:
  --db DB          数据库文件名（默认: cve_references.db）
  --max MAX        最大处理CVE数量（用于测试）
  --delay DELAY    请求延迟秒数（默认: 1）
```

### query_references.py
```bash
python query_references.py [命令] [选项]

命令:
  stats                    显示统计信息
  cve <cve_id>            查询特定CVE
  domain <domain>         搜索特定域名
  content <cve_id>        查看内容
  export                  导出到CSV

选项:
  --db DB                 数据库文件名
  --url URL               URL模式（用于content命令）
  --output OUTPUT         输出文件名（用于export命令）
```

---

## 🎓 高级技巧

### 1. 并发爬取（提高速度）
修改 `reference_crawler.py`，使用线程池：
```python
from concurrent.futures import ThreadPoolExecutor

# 在process_json_file方法中使用
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(self.crawl_url, url) for url in references]
    results = [f.result() for f in futures]
```

### 2. 使用代理
```python
# 在ReferenceCrawler.__init__中添加
self.session.proxies = {
    'http': 'http://proxy:port',
    'https': 'https://proxy:port'
}
```

### 3. 自定义User-Agent
```python
# 修改session.headers
self.session.headers.update({
    'User-Agent': 'Your Custom User Agent'
})
```

---

## ⚠️ 注意事项

### 1. 爬取速度
- 默认延迟1秒，避免被封
- 建议先用 `--max 5` 测试
- 某些网站可能有反爬虫机制

### 2. 内容限制
- 每个页面内容限制10000字符
- 动态加载的内容可能无法获取
- JavaScript渲染的页面需要特殊处理

### 3. 网络问题
- 超时设置为10秒
- 失败的链接会记录错误信息
- 可以重新运行更新失败的链接

### 4. 法律合规
- 遵守robots.txt
- 尊重网站的使用条款
- 不要过度频繁请求

---

## 🔧 故障排除

### 问题1: 依赖缺失
```bash
pip install beautifulsoup4 requests tabulate lxml
```

### 问题2: 数据库锁定
```bash
# 关闭所有访问数据库的程序
# 或使用新数据库
python reference_crawler.py data.json --db new_db.db
```

### 问题3: 编码错误
确保JSON文件是UTF-8编码

### 问题4: 连接超时
```bash
# 增加延迟时间
python reference_crawler.py data.json --delay 3
```

---

## 📈 性能数据

### 爬取速度
- 无API限制: 约1个链接/秒
- 有延迟保护: 约0.5-2个链接/秒
- 96个CVE，约450个链接: 约7-15分钟

### 数据库大小
- 100个CVE: 约5-10MB
- 1000个CVE: 约50-100MB
- 取决于内容长度

---

## 🎉 总结

这个参考链接爬虫为CVE分析提供了强大的数据收集能力：

✅ **自动化** - 一键爬取所有参考链接
✅ **结构化** - 数据存储在SQLite数据库
✅ **可查询** - 强大的查询和导出功能
✅ **可扩展** - 易于添加新功能
✅ **实用性** - 真实的安全研究场景

配合CVE爬虫使用，可以构建完整的漏洞情报收集系统！

---

**需要帮助？查看 `REFERENCE_CRAWLER_GUIDE.md` 获取详细文档！** 📖
