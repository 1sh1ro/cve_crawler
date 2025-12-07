#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API密钥测试脚本
快速验证API密钥配置是否正确
"""

import os
from dotenv import load_dotenv

def test_api_key():
    """测试API密钥配置"""
    print("=" * 60)
    print("API密钥配置测试")
    print("=" * 60)
    print()
    
    # 加载环境变量
    load_dotenv()
    
    # 检查 .env 文件
    if os.path.exists('.env'):
        print("✓ .env 文件存在")
    else:
        print("✗ .env 文件不存在")
        print("  请创建 .env 文件并添加: NVD_API_KEY=你的密钥")
        return False
    
    # 检查环境变量
    api_key = os.getenv('NVD_API_KEY')
    
    if api_key:
        print(f"✓ 检测到API密钥: {api_key[:8]}...{api_key[-4:]}")
        print(f"  完整密钥长度: {len(api_key)} 字符")
        
        # 验证密钥格式（UUID格式）
        if len(api_key) == 36 and api_key.count('-') == 4:
            print("✓ 密钥格式正确（UUID格式）")
        else:
            print("⚠ 密钥格式可能不正确")
            print("  标准格式: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
        
        print()
        print("=" * 60)
        print("配置成功！")
        print("=" * 60)
        print()
        print("现在可以使用以下命令测试:")
        print("  python cve_scraper.py -k \"test\" -y 1")
        print()
        print("如果看到 '✓ 使用API密钥模式（速度快10倍）'")
        print("说明API密钥正在工作！")
        print()
        return True
        
    else:
        print("✗ 未检测到API密钥")
        print()
        print("请按以下步骤配置:")
        print("1. 编辑 .env 文件")
        print("2. 添加一行: NVD_API_KEY=你的密钥")
        print("3. 保存文件")
        print("4. 重新运行此脚本")
        print()
        print("你的API密钥: 10f8632f-3119-4c11-b25c-214e0a9203f2")
        print()
        return False

if __name__ == "__main__":
    test_api_key()
