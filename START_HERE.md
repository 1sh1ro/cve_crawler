# 🎯 从这里开始

欢迎使用CVE信息爬虫！这是你的起点。

## 📚 文档导航

根据你的需求，选择合适的文档：

### 🚀 我想快速开始
→ [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md) - 5分钟快速入门

### 📖 我想了解详细信息
→ [README.md](README.md) - 完整的中文文档  
→ [README_EN.md](README_EN.md) - 完整的英文文档

### 💻 我想看使用示例
→ [examples.bat](examples.bat) - Windows示例  
→ [examples.sh](examples.sh) - Linux/Mac示例  
→ [DEMO_SCRIPT.md](DEMO_SCRIPT.md) - 详细演示脚本

### 🔧 我想了解项目结构
→ [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - 项目结构说明  
→ [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - 项目总结

### 🤝 我想贡献代码
→ [CONTRIBUTING.md](CONTRIBUTING.md) - 贡献指南  
→ [CHANGELOG.md](CHANGELOG.md) - 更新日志

### 📦 我想发布到GitHub
→ [GITHUB_SETUP.md](GITHUB_SETUP.md) - GitHub设置指南  
→ [CHECKLIST.md](CHECKLIST.md) - 发布前检查清单

## ⚡ 超快速开始（30秒）

```bash
# 1. 安装
pip install -r requirements.txt

# 2. 运行
python quick_start.py

# 3. 完成！
```

## 🎓 学习路径

### 新手路径
1. 阅读 [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)
2. 运行 `python quick_start.py`
3. 查看生成的结果文件
4. 尝试不同的关键词

### 进阶路径
1. 阅读 [README.md](README.md)
2. 学习命令行参数
3. 申请API密钥
4. 尝试高级功能

### 专家路径
1. 阅读 [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
2. 查看源代码 `cve_scraper.py`
3. 作为模块导入使用
4. 二次开发和扩展

## 📋 核心文件说明

### 可执行文件
- `cve_scraper.py` - 主程序（命令行模式）
- `quick_start.py` - 交互式向导（新手友好）
- `test_scraper.py` - 测试脚本

### 配置文件
- `requirements.txt` - Python依赖
- `config.example.ini` - 配置示例
- `.gitignore` - Git忽略规则

### 文档文件
- `README.md` - 主文档（中文）
- `README_EN.md` - 主文档（英文）
- `LICENSE` - MIT许可证

## 🎯 常见任务

### 任务1: 搜索Linux内核漏洞
```bash
python cve_scraper.py -k "linux kernel privilege escalation" -y 5
```

### 任务2: 监控特定产品
```bash
python cve_scraper.py -k "apache" -s "2024-01-01 00:00" -e "2024-12-31 23:59"
```

### 任务3: 使用API密钥加速
```bash
python cve_scraper.py -k "docker" -y 2 --api-key YOUR_API_KEY
```

### 任务4: 导出特定格式
```bash
python cve_scraper.py -k "nginx" -y 1 --json-only
```

## 🆘 遇到问题？

### 安装问题
```bash
# 检查Python版本（需要3.7+）
python --version

# 升级pip
python -m pip install --upgrade pip

# 重新安装依赖
pip install -r requirements.txt --force-reinstall
```

### 运行问题
```bash
# 查看帮助
python cve_scraper.py --help

# 运行测试
python test_scraper.py

# 使用交互模式
python quick_start.py
```

### 网络问题
- 确保能访问 `services.nvd.nist.gov`
- 检查防火墙设置
- 尝试使用代理（如需要）

## 📞 获取帮助

### 文档
- 完整文档: [README.md](README.md)
- 快速入门: [QUICK_START_GUIDE.md](QUICK_START_GUIDE.md)
- 示例脚本: [DEMO_SCRIPT.md](DEMO_SCRIPT.md)

### 社区
- GitHub Issues: 报告bug和提问
- GitHub Discussions: 讨论和交流
- Email: 联系作者

### 资源
- NVD官网: https://nvd.nist.gov/
- NVD API文档: https://nvd.nist.gov/developers
- nvdlib文档: https://nvdlib.com/

## 🎉 开始使用

选择你的方式：

### 方式1: 交互式（推荐新手）
```bash
python quick_start.py
```

### 方式2: 命令行（推荐高级用户）
```bash
python cve_scraper.py -k "your keyword" -y 5
```

### 方式3: 作为模块（推荐开发者）
```python
from cve_scraper import CVEScraper
scraper = CVEScraper()
results = scraper.scrape(...)
```

## 📈 下一步

1. ✅ 完成第一次搜索
2. ✅ 申请API密钥（提速10倍）
3. ✅ 尝试不同的关键词
4. ✅ 探索高级功能
5. ✅ 分享你的经验

## 🌟 项目特色

- ✨ 基于官方NVD API（稳定可靠）
- 🚀 支持API密钥（速度快10倍）
- 📊 完整的CVE信息（CVSS、CWE、CPE等）
- 💾 多格式导出（JSON、CSV、Markdown）
- 🎯 灵活的搜索选项（关键词、日期、CPE）
- 📖 详细的文档和示例
- 🧪 自动化测试
- 🤝 欢迎贡献

## 💡 提示

- 💰 申请免费API密钥可以大幅提升速度
- 📅 大范围搜索会自动分段处理
- 🔍 使用英文关键词效果更好
- 💾 结果会自动保存为3种格式
- 🔄 可以定期运行进行监控

---

**准备好了吗？开始你的CVE搜索之旅！** 🚀

选择一个文档开始，或者直接运行：
```bash
python quick_start.py
```
