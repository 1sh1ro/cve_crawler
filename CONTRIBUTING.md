# 贡献指南

感谢你考虑为CVE信息爬虫项目做出贡献！

## 如何贡献

### 报告Bug

如果你发现了bug，请创建一个Issue并包含以下信息：

- 使用的Python版本
- 使用的操作系统
- 详细的错误信息和堆栈跟踪
- 重现步骤
- 预期行为和实际行为

### 提出新功能

如果你有新功能的想法：

1. 先检查Issue列表，确保没有重复
2. 创建一个新的Issue，描述你的想法
3. 说明这个功能的使用场景和价值
4. 如果可能，提供实现思路

### 提交代码

1. Fork本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建一个Pull Request

### 代码规范

- 遵循PEP 8 Python代码风格
- 添加适当的注释和文档字符串
- 保持代码简洁和可读
- 为新功能添加示例

### 提交信息规范

使用清晰的提交信息：

- `feat: 添加新功能`
- `fix: 修复bug`
- `docs: 更新文档`
- `style: 代码格式调整`
- `refactor: 代码重构`
- `test: 添加测试`
- `chore: 构建或辅助工具变动`

## 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/yourusername/cve-scraper.git
cd cve-scraper

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 运行测试
python cve_scraper.py -k "test" -y 1
```

## 测试

在提交PR之前，请确保：

- 代码能够正常运行
- 没有引入新的bug
- 更新了相关文档
- 添加了必要的注释

## 文档

如果你的更改影响了用户使用方式：

- 更新README.md
- 更新CHANGELOG.md
- 如有必要，添加示例

## 行为准则

- 尊重所有贡献者
- 保持友好和专业
- 接受建设性的批评
- 关注对项目最有利的事情

## 问题和帮助

如果你有任何问题：

- 查看现有的Issue和文档
- 在Issue中提问
- 参与讨论

## 许可证

通过贡献代码，你同意你的贡献将在MIT许可证下发布。

---

再次感谢你的贡献！🎉
