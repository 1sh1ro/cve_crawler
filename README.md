# CVE信息爬虫 🔍

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![NVD API](https://img.shields.io/badge/NVD-API%202.0-orange.svg)](https://nvd.nist.gov/developers)

一个基于NVD官方API的CVE漏洞信息爬虫工具，支持按日期范围和关键词搜索，获取完整的CVE详细信息。

## ✨ 特性

- 🎯 **精准搜索**: 支持关键词、日期范围、CPE名称过滤
- 📊 **完整信息**: 获取CVSS评分、CWE类型、受影响产品、参考链接等完整信息
- 🚀 **高性能**: 支持NVD API密钥，速度提升10倍
- 💾 **多格式导出**: 支持JSON、CSV、Markdown三种格式
- 🔄 **自动分段**: 自动处理NVD API的120天限制
- ⚡ **速率控制**: 智能处理API速率限制，避免被封禁
- 🛡️ **稳定可靠**: 基于官方API，数据准确且合规
- 🔗 **参考链接爬虫**: 自动爬取CVE参考链接内容并存储到数据库（新功能！）

## 📋 获取的信息

每个CVE包含以下完整信息：

- CVE编号
- 发布日期和最后修改日期
- 漏洞状态
- 完整的漏洞描述
- CVSS v3/v2评分和严重程度
- CVSS向量字符串
- 可利用性评分和影响评分
- CWE漏洞类型分类
- 受影响的产品和版本（CPE格式）
- 官方参考链接

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 基本使用

```bash
# 爬取最近5年的Linux内核提权漏洞
python cve_scraper.py -k "linux kernel privilege escalation"

# 指定时间范围
python cve_scraper.py -k "apache" -s "2023-01-01 00:00" -e "2023-12-31 23:59"

# 爬取最近3年的Windows漏洞
python cve_scraper.py -k "windows" -y 3
```

### 使用API密钥（强烈推荐）

**方法1: 使用环境变量（推荐）**
```bash
# 创建 .env 文件
echo "NVD_API_KEY=你的API密钥" > .env

# 直接运行，会自动读取
python cve_scraper.py -k "docker" -y 2
```

**方法2: 命令行参数**
```bash
python cve_scraper.py -k "docker" -y 2 --api-key YOUR_API_KEY
```

详细配置说明见：[API_KEY_SETUP.md](API_KEY_SETUP.md)

## 🔑 获取NVD API密钥

**强烈建议申请免费API密钥以提升速度！**

| 模式 | 速率限制 | 速度对比 |
|------|---------|---------|
| 无API密钥 | 5请求/30秒 | 基准速度 |
| 有API密钥 | 50请求/30秒 | **快10倍** |

### 申请步骤

1. 访问 [NVD API密钥申请页面](https://nvd.nist.gov/developers/request-an-api-key)
2. 填写邮箱地址
3. 查收邮件并点击确认链接
4. 在确认页面输入邮箱和UUID
5. 获取API密钥

## 📖 使用说明

### 命令行参数

```
必需参数:
  -k, --keyword KEYWORD        搜索关键词

可选参数:
  -s, --start-date START       开始日期，格式: YYYY-MM-DD HH:MM
  -e, --end-date END           结束日期，格式: YYYY-MM-DD HH:MM
  -y, --years YEARS            最近N年（默认5年）
  --cpe CPE                    CPE名称过滤
  --api-key API_KEY            NVD API密钥
  -o, --output PREFIX          输出文件名前缀（默认: cve_results）
  --json-only                  仅保存JSON格式
  --csv-only                   仅保存CSV格式
  --md-only                    仅保存Markdown格式
```

### 使用示例

#### 1. Linux内核提权漏洞（最近5年）

```bash
python cve_scraper.py -k "linux kernel privilege escalation" -y 5
```

#### 2. Apache漏洞（指定日期范围）

```bash
python cve_scraper.py -k "apache" -s "2023-01-01 00:00" -e "2024-12-31 23:59"
```

#### 3. 使用CPE过滤特定产品

```bash
python cve_scraper.py -k "kernel" -y 2 --cpe "cpe:2.3:o:linux:linux_kernel"
```

#### 4. 自定义输出文件名

```bash
python cve_scraper.py -k "docker" -y 1 -o docker_vulnerabilities
```

#### 5. 仅导出JSON格式

```bash
python cve_scraper.py -k "kubernetes" -y 2 --json-only
```

## 📁 输出格式

### JSON格式
结构化数据，便于程序处理和二次开发：
```json
[
  {
    "CVE ID": "CVE-2024-1234",
    "发布日期": "2024-01-15T10:00:00",
    "严重程度": "HIGH",
    "CVSS评分": 7.8,
    ...
  }
]
```

### CSV格式
表格数据，可直接用Excel打开进行筛选和分析。

### Markdown格式
格式化的报告文档，便于阅读和分享：
```markdown
## CVE-2024-1234

- **发布日期**: 2024-01-15T10:00:00
- **严重程度**: HIGH (CVSS: 7.8)
- **描述**: ...
```

## 🔧 高级用法

### 作为Python模块使用

```python
from cve_scraper import CVEScraper

# 创建爬虫实例
scraper = CVEScraper(api_key='YOUR_API_KEY')

# 执行搜索
results = scraper.scrape(
    keyword='linux kernel',
    start_date='2023-01-01 00:00',
    end_date='2024-12-31 23:59'
)

# 保存结果
scraper.save_all('my_results')
```

### 自定义延迟时间

```python
# 在search_cves方法中指定delay参数
cves = scraper.search_cves(
    keyword='apache',
    start_date='2023-01-01 00:00',
    end_date='2023-12-31 23:59',
    delay=1.0  # 每次请求间隔1秒
)
```

## ⚠️ 注意事项

1. **API限制**: NVD API限制单次查询时间跨度不超过120天，脚本会自动分段处理
2. **速率限制**: 
   - 无API密钥: 每30秒最多5个请求
   - 有API密钥: 每30秒最多50个请求
3. **网络要求**: 需要能够访问 `services.nvd.nist.gov`
4. **数据量**: 大范围查询可能需要较长时间，建议使用API密钥

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🔗 相关链接

- [NVD官网](https://nvd.nist.gov/)
- [NVD API文档](https://nvd.nist.gov/developers)
- [nvdlib库文档](https://nvdlib.com/)
- [CVSS评分标准](https://www.first.org/cvss/)

## 📮 联系方式

如有问题或建议，欢迎提交Issue或联系作者。

---

**免责声明**: 本工具仅用于安全研究和学习目的，请遵守相关法律法规和NVD使用条款。


---

## 🔗 参考链接爬虫（新功能）

### 功能介绍

参考链接爬虫可以从CVE JSON文件中提取所有参考链接，自动爬取这些链接的内容，并保存到SQLite数据库中，方便深度分析。

### 快速开始

#### 1. 安装额外依赖
```bash
pip install beautifulsoup4 requests tabulate lxml
```

或运行：
```bash
install_crawler_deps.bat
```

#### 2. 爬取参考链接
```bash
# 测试模式（只处理前5个CVE）
python reference_crawler.py linux_kernel_privilege_escalation_2020-2025.json --max 5

# 爬取全部
python reference_crawler.py linux_kernel_privilege_escalation_2020-2025.json
```

#### 3. 查询数据库
```bash
# 查看统计信息
python query_references.py stats

# 查询特定CVE的所有参考链接
python query_references.py cve CVE-2020-25221

# 搜索特定域名
python query_references.py domain intel.com

# 查看爬取的内容
python query_references.py content CVE-2020-25221 --url intel.com

# 导出到CSV
python query_references.py export --output analysis.csv
```

### 使用场景

#### 场景1: 深度分析Intel安全公告
```bash
# 1. 爬取CVE数据
python crawl_linux_kernel.py

# 2. 爬取参考链接
python reference_crawler.py linux_kernel_privilege_escalation_2020-2025.json

# 3. 查询Intel相关链接
python query_references.py domain intel.com

# 4. 查看具体内容
python query_references.py content CVE-2021-1052 --url intel.com
```

#### 场景2: 追踪内核补丁
```bash
# 查询所有kernel.org的链接
python query_references.py domain kernel.org

# 导出分析
python query_references.py export --output kernel_patches.csv
```

### 数据库结构

参考链接爬虫使用SQLite数据库存储数据，包含两个主表：

- **cves表**: 存储CVE基本信息
- **reference_links表**: 存储参考链接及其内容

### 详细文档

- [参考链接爬虫README](REFERENCE_CRAWLER_README.md) - 功能介绍和快速开始
- [参考链接爬虫指南](REFERENCE_CRAWLER_GUIDE.md) - 详细使用说明和高级技巧

---
