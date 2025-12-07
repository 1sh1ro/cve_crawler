# 项目结构说明

```
cve-scraper/
│
├── cve_scraper.py          # 主程序文件（核心爬虫逻辑）
├── quick_start.py          # 快速开始脚本（交互式向导）
├── test_scraper.py         # 测试脚本
│
├── requirements.txt        # Python依赖包
├── config.example.ini      # 配置文件示例
│
├── README.md              # 项目说明文档
├── LICENSE                # MIT许可证
├── CHANGELOG.md           # 更新日志
├── CONTRIBUTING.md        # 贡献指南
├── PROJECT_STRUCTURE.md   # 本文件
│
├── examples.sh            # Linux/Mac示例脚本
├── examples.bat           # Windows示例脚本
│
├── .gitignore            # Git忽略文件配置
├── .github/
│   └── workflows/
│       └── test.yml      # GitHub Actions CI配置
│
└── output/               # 输出目录（自动生成）
    ├── *.json           # JSON格式输出
    ├── *.csv            # CSV格式输出
    └── *.md             # Markdown格式输出
```

## 文件说明

### 核心文件

#### cve_scraper.py
主程序文件，包含：
- `CVEScraper` 类：核心爬虫逻辑
- 日期范围分割功能
- CVE数据解析功能
- 多格式导出功能
- 命令行参数处理

主要方法：
- `__init__(api_key)`: 初始化爬虫
- `split_date_range()`: 分割日期范围
- `search_cves()`: 搜索CVE
- `parse_cve_data()`: 解析CVE数据
- `scrape()`: 执行爬取
- `save_to_json/csv/markdown()`: 保存结果

#### quick_start.py
交互式快速开始脚本，适合新手使用：
- 友好的用户界面
- 逐步引导配置
- 自动执行爬取和保存

#### test_scraper.py
测试脚本，包含：
- 基本搜索功能测试
- 日期分割功能测试
- 数据解析功能测试
- 导出功能测试

### 配置文件

#### requirements.txt
Python依赖包列表：
- nvdlib: NVD API封装库

#### config.example.ini
配置文件示例，包含：
- API密钥配置
- 默认参数设置
- 高级选项配置

### 文档文件

#### README.md
项目主文档，包含：
- 项目介绍
- 功能特性
- 安装和使用说明
- 示例代码
- 常见问题

#### LICENSE
MIT开源许可证

#### CHANGELOG.md
版本更新日志

#### CONTRIBUTING.md
贡献指南，包含：
- 如何报告Bug
- 如何提出新功能
- 代码规范
- 提交流程

#### PROJECT_STRUCTURE.md
本文件，项目结构说明

### 示例脚本

#### examples.sh
Linux/Mac系统的使用示例脚本

#### examples.bat
Windows系统的使用示例脚本

### 配置文件

#### .gitignore
Git版本控制忽略文件配置，排除：
- Python缓存文件
- 虚拟环境
- 输出文件
- API密钥等敏感信息

#### .github/workflows/test.yml
GitHub Actions CI/CD配置：
- 多平台测试（Ubuntu, Windows, macOS）
- 多Python版本测试（3.7-3.11）
- 自动运行测试

## 使用流程

### 新手用户
1. 安装依赖: `pip install -r requirements.txt`
2. 运行快速开始: `python quick_start.py`
3. 按照提示操作

### 高级用户
1. 安装依赖: `pip install -r requirements.txt`
2. 直接使用命令行: `python cve_scraper.py -k "关键词" -y 5`
3. 查看示例: `examples.sh` 或 `examples.bat`

### 开发者
1. 克隆仓库
2. 安装依赖
3. 运行测试: `python test_scraper.py`
4. 作为模块导入使用

## 输出文件

所有输出文件默认保存在当前目录：

- `cve_results.json`: JSON格式，结构化数据
- `cve_results.csv`: CSV格式，可用Excel打开
- `cve_results.md`: Markdown格式，可读性强

可以通过 `-o` 参数自定义输出文件名前缀。

## 扩展开发

如果你想基于本项目进行二次开发：

1. 导入CVEScraper类
2. 创建实例并调用方法
3. 自定义数据处理逻辑

示例：
```python
from cve_scraper import CVEScraper

scraper = CVEScraper(api_key='YOUR_KEY')
results = scraper.scrape(
    keyword='your keyword',
    start_date='2023-01-01 00:00',
    end_date='2023-12-31 23:59'
)

# 自定义处理
for cve in results:
    # 你的逻辑
    pass
```

## 维护说明

### 添加新功能
1. 在 `cve_scraper.py` 中实现
2. 在 `test_scraper.py` 中添加测试
3. 更新 `README.md` 文档
4. 更新 `CHANGELOG.md`

### 修复Bug
1. 在 `test_scraper.py` 中添加复现测试
2. 修复代码
3. 确保所有测试通过
4. 更新 `CHANGELOG.md`

### 发布新版本
1. 更新版本号
2. 更新 `CHANGELOG.md`
3. 创建Git标签
4. 推送到GitHub
