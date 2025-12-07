#!/bin/bash
# CVE爬虫安装脚本 (Linux/Mac)

echo ""
echo "========================================"
echo "CVE信息爬虫 - 安装脚本"
echo "========================================"
echo ""

# 检查Python
echo "[1/4] 检查Python环境..."
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到Python3！"
    echo "请先安装Python 3.7或更高版本"
    exit 1
fi

python3 --version
echo ""

# 升级pip
echo "[2/4] 升级pip..."
python3 -m pip install --upgrade pip
echo ""

# 安装依赖
echo "[3/4] 安装依赖包..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[错误] 依赖安装失败！"
    exit 1
fi
echo ""

# 运行测试
echo "[4/4] 运行测试..."
python3 test_scraper.py
if [ $? -ne 0 ]; then
    echo "[警告] 测试未完全通过，但可以继续使用"
fi
echo ""

echo "========================================"
echo "安装完成！"
echo "========================================"
echo ""
echo "快速开始:"
echo "  python3 quick_start.py"
echo ""
echo "或者使用命令行:"
echo "  python3 cve_scraper.py -k \"linux kernel\" -y 1"
echo ""
echo "查看帮助:"
echo "  python3 cve_scraper.py --help"
echo ""
echo "查看文档:"
echo "  cat START_HERE.md"
echo ""
echo "配置API密钥（可选，但推荐）:"
echo "  1. 复制 .env.example 为 .env"
echo "  2. 编辑 .env 文件，填入你的API密钥"
echo "  3. 详见 API_KEY_SETUP.md"
echo ""
