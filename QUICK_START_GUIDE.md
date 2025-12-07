# 5分钟快速入门指南

本指南帮助你在5分钟内开始使用CVE爬虫。

## 第1步: 安装（1分钟）

### 方法1: 使用pip（推荐）
```bash
pip install -r requirements.txt
```

### 方法2: 手动安装
```bash
pip install nvdlib
```

## 第2步: 第一次运行（2分钟）

### 最简单的方式 - 交互式模式
```bash
python quick_start.py
```
然后按照提示操作即可！

### 命令行模式
```bash
# 搜索最近1年的Linux内核漏洞
python cve_scraper.py -k "linux kernel" -y 1
```

## 第3步: 查看结果（1分钟）

运行完成后，会生成3个文件：

### Windows
```cmd
type cve_results.json      REM 查看JSON
start cve_results.csv      REM 用Excel打开
notepad cve_results.md     REM 查看Markdown
```

### Linux/Mac
```bash
cat cve_results.json       # 查看JSON
open cve_results.csv       # 用Excel打开
cat cve_results.md         # 查看Markdown
```

## 第4步: 常用命令（1分钟）

### 搜索不同关键词
```bash
# Apache漏洞
python cve_scraper.py -k "apache" -y 2

# Windows提权漏洞
python cve_scraper.py -k "windows privilege escalation" -y 3

# Docker漏洞
python cve_scraper.py -k "docker" -y 1
```

### 指定日期范围
```bash
python cve_scraper.py -k "nginx" -s "2023-01-01 00:00" -e "2023-12-31 23:59"
```

### 使用API密钥（速度快10倍）
```bash
python cve_scraper.py -k "kernel" -y 2 --api-key YOUR_API_KEY
```

## 获取API密钥（可选但推荐）

1. 访问: https://nvd.nist.gov/developers/request-an-api-key
2. 输入邮箱
3. 查收邮件并确认
4. 获取API密钥
5. 使用 `--api-key` 参数

## 常见问题

### Q: 速度很慢怎么办？
A: 申请并使用API密钥，速度提升10倍！

### Q: 如何搜索中文关键词？
A: 直接使用中文即可，但建议使用英文关键词效果更好。

### Q: 如何只保存JSON格式？
A: 添加 `--json-only` 参数

### Q: 出现错误怎么办？
A: 
1. 检查网络连接
2. 确认Python版本 >= 3.7
3. 确认已安装依赖
4. 查看错误信息

## 下一步

### 查看完整文档
```bash
# 查看所有参数
python cve_scraper.py --help

# 阅读README
cat README.md
```

### 运行测试
```bash
python test_scraper.py
```

### 查看示例
```bash
# Windows
examples.bat

# Linux/Mac
bash examples.sh
```

## 实用技巧

### 1. 自定义输出文件名
```bash
python cve_scraper.py -k "apache" -y 1 -o apache_cves
```

### 2. 搜索多个关键词
```bash
# 方法1: 多次运行
python cve_scraper.py -k "linux kernel" -y 1 -o linux_cves
python cve_scraper.py -k "apache" -y 1 -o apache_cves

# 方法2: 使用Python脚本
# 见 DEMO_SCRIPT.md
```

### 3. 定期监控
```bash
# 创建定时任务（Linux/Mac）
# 每周一早上9点运行
0 9 * * 1 cd /path/to/cve-scraper && python cve_scraper.py -k "your keyword" -y 1
```

## 5分钟总结

1. ✅ 安装依赖: `pip install -r requirements.txt`
2. ✅ 运行爬虫: `python cve_scraper.py -k "关键词" -y 1`
3. ✅ 查看结果: 打开生成的文件
4. ✅ 获取API密钥: 提升速度（可选）
5. ✅ 探索更多: 查看文档和示例

## 需要帮助？

- 📖 查看完整文档: [README.md](README.md)
- 🐛 报告问题: [GitHub Issues](https://github.com/yourusername/cve-scraper/issues)
- 💬 讨论交流: [GitHub Discussions](https://github.com/yourusername/cve-scraper/discussions)

---

开始你的CVE搜索之旅吧！🚀
