# 🚀 发布到GitHub指南

## 仓库信息
- **GitHub用户名**: 1sh1ro
- **仓库名称**: cve_crawler
- **仓库URL**: https://github.com/1sh1ro/cve_crawler

---

## 📋 发布步骤

### 步骤1: 初始化Git仓库
```bash
git init
```

### 步骤2: 配置Git用户信息（如果还没配置）
```bash
git config user.name "1sh1ro"
git config user.email "你的邮箱@example.com"
```

### 步骤3: 添加所有文件
```bash
git add .
```

### 步骤4: 创建首次提交
```bash
git commit -m "Initial commit: CVE Crawler with NVD API integration"
```

### 步骤5: 设置主分支名称
```bash
git branch -M main
```

### 步骤6: 添加远程仓库
```bash
git remote add origin https://github.com/1sh1ro/cve_crawler.git
```

### 步骤7: 推送到GitHub
```bash
git push -u origin main
```

---

## 🔐 如果需要身份验证

### 使用Personal Access Token (推荐)
1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 选择权限: `repo` (完整仓库访问)
4. 生成并复制token
5. 推送时使用token作为密码

### 或使用SSH (更方便)
```bash
# 生成SSH密钥
ssh-keygen -t ed25519 -C "你的邮箱@example.com"

# 添加到GitHub
# 复制公钥内容: cat ~/.ssh/id_ed25519.pub
# 访问 https://github.com/settings/keys 添加

# 修改远程URL为SSH
git remote set-url origin git@github.com:1sh1ro/cve_crawler.git
git push -u origin main
```

---

## 📝 提交信息建议

### 首次提交
```bash
git commit -m "Initial commit: CVE Crawler with NVD API integration

Features:
- NVD API integration with rate limiting
- Keyword search functionality
- Date range filtering
- Multiple export formats (JSON, CSV, Markdown)
- Comprehensive documentation
- Quick start examples"
```

---

## 🎯 发布后的检查清单

- [ ] 访问 https://github.com/1sh1ro/cve_crawler 确认文件已上传
- [ ] 检查 README.md 在仓库首页正确显示
- [ ] 确认 .gitignore 正常工作（api_key.txt 未上传）
- [ ] 测试克隆仓库: `git clone https://github.com/1sh1ro/cve_crawler.git`
- [ ] 添加仓库描述和标签（在GitHub网页上）
- [ ] 考虑添加 GitHub Topics: `python`, `cve`, `security`, `nvd`, `vulnerability`

---

## 🏷️ 推荐的GitHub仓库设置

### 仓库描述
```
A powerful CVE crawler using NVD API with keyword search, date filtering, and multiple export formats
```

### Topics标签
- python
- cve
- security
- nvd
- vulnerability
- cybersecurity
- vulnerability-scanner
- cve-search

### About部分
- ✅ Website: 可以留空或添加文档链接
- ✅ Topics: 添加上述标签
- ✅ Include in the home page: 勾选

---

## 🔄 后续更新流程

### 添加新功能后
```bash
git add .
git commit -m "Add: 新功能描述"
git push
```

### 修复bug后
```bash
git add .
git commit -m "Fix: bug描述"
git push
```

### 更新文档后
```bash
git add .
git commit -m "Docs: 文档更新说明"
git push
```

---

## ⚠️ 重要提醒

1. **API密钥安全**: 确认 `api_key.txt` 在 `.gitignore` 中
2. **测试数据**: `output/` 目录也在 `.gitignore` 中，不会上传
3. **首次推送**: 如果仓库已存在内容，可能需要先 `git pull origin main --allow-unrelated-histories`

---

## 🆘 常见问题

### 问题1: 推送被拒绝
```bash
# 如果远程仓库有内容，先拉取
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### 问题2: 认证失败
- 使用Personal Access Token代替密码
- 或配置SSH密钥

### 问题3: 文件太大
- 检查是否误提交了大文件
- 使用 `git rm --cached 文件名` 移除

---

## 📞 需要帮助？

如果遇到问题，可以：
1. 检查Git状态: `git status`
2. 查看提交历史: `git log`
3. 查看远程仓库: `git remote -v`

---

**准备好了吗？开始发布吧！** 🚀
