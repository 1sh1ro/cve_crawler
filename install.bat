@echo off
REM CVE爬虫安装脚本 (Windows)

echo.
echo ========================================
echo CVE信息爬虫 - 安装脚本
echo ========================================
echo.

REM 检查Python
echo [1/4] 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python！
    echo 请先安装Python 3.7或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

python --version
echo.

REM 升级pip
echo [2/4] 升级pip...
python -m pip install --upgrade pip
echo.

REM 安装依赖
echo [3/4] 安装依赖包...
pip install -r requirements.txt
if errorlevel 1 (
    echo [错误] 依赖安装失败！
    pause
    exit /b 1
)
echo.

REM 运行测试
echo [4/4] 运行测试...
python test_scraper.py
if errorlevel 1 (
    echo [警告] 测试未完全通过，但可以继续使用
)
echo.

echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 快速开始:
echo   python quick_start.py
echo.
echo 或者使用命令行:
echo   python cve_scraper.py -k "linux kernel" -y 1
echo.
echo 查看帮助:
echo   python cve_scraper.py --help
echo.
echo 查看文档:
echo   type START_HERE.md
echo.
echo 配置API密钥（可选，但推荐）:
echo   1. 复制 .env.example 为 .env
echo   2. 编辑 .env 文件，填入你的API密钥
echo   3. 详见 API_KEY_SETUP.md
echo.
pause
