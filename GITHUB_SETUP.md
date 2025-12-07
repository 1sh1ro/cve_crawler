# GitHub仓库设置指南

本文档指导你如何将CVE爬虫项目上传到GitHub。

## 步骤1: 创建GitHub仓库

1. 登录 [GitHub](https://github.com)
2. 点击右上角的 "+" 按钮，选择 "New repository"
3. 填写仓库信息：
   - **Repository name**: `cve-scraper` 或你喜欢的名字
   - **Description**: `A CVE vulnerability information scraper based on NVD official API`
   - **Public/Private**: 选择 Public（公开）
   - **不要**勾选 "Initialize this repository with a README"（我们已经有了）
4. 点击 "Create repository"

## 步骤2: 初始化本地Git仓库

在项目目录下打开终端/命令提示符，执行以下命令：

### Windows (CMD)
```cmd
git init
git add .
git commit -m "Initial commit: CVE scraper v1.0.0"
```

### Linux/Mac (Bash)
```bash
git init
git add .
git commit -m "Initial commit: CVE scraper v1.0.0"
```

## 步骤3: 连接到GitHub仓库

将 `yourusername` 替换为你的GitHub用户名：

```bash
git remote add origin https://github.com/yourusername/cve-scraper.git
git branch -M main
git push -u origin main
```

如果遇到认证问题，可能需要使用Personal Access Token：
1. 访问 GitHub Settings → Developer settings → Personal access tokens
2. 生成新的token（勾选 repo 权限）
3. 使用token作为密码

## 步骤4: 配置GitHub仓库设置

### 添加Topics（标签）
在仓库页面点击 "Add topics"，添加：
- `cve`
- `nvd`
- `security`
- `vulnerability`
- `scraper`
- `python`
- `cybersecurity`

### 设置About（关于）
在仓库页面右侧点击设置图标，填写：
- **Description**: `A CVE vulnerability information scraper based on NVD official API`
- **Website**: 留空或填写你的网站
- **Topics**: 已在上面添加

### 启用GitHub Actions
GitHub Actions会自动启用，它会：
- 在每次push时运行测试
- 支持多平台（Ubuntu, Windows, macOS）
- 支持多Python版本（3.7-3.11）

### 创建Releases（发布版本）
1. 点击仓库页面的 "Releases"
2. 点击 "Create a new release"
3. 填写：
   - **Tag version**: `v1.0.0`
   - **Release title**: `v1.0.0 - Initial Release`
   - **Description**: 从 CHANGELOG.md 复制内容
4. 点击 "Publish release"

## 步骤5: 更新README中的链接

在 `README.md` 和 `setup.py` 中，将以下内容替换为你的实际信息：

- `yourusername` → 你的GitHub用户名
- `your.email@example.com` → 你的邮箱

## 步骤6: 添加Badges（徽章）

在 README.md 顶部已经有了一些徽章，你可以添加更多：

### GitHub Stars
```markdown
[![GitHub stars](https://img.shields.io/github/stars/yourusername/cve-scraper.svg)](https://github.com/yourusername/cve-scraper/stargazers)
```

### GitHub Forks
```markdown
[![GitHub forks](https://img.shields.io/github/forks/yourusername/cve-scraper.svg)](https://github.com/yourusername/cve-scraper/network)
```

### GitHub Issues
```markdown
[![GitHub issues](https://img.shields.io/github/issues/yourusername/cve-scraper.svg)](https://github.com/yourusername/cve-scraper/issues)
```

### Build Status
```markdown
[![Build Status](https://github.com/yourusername/cve-scraper/workflows/Tests/badge.svg)](https://github.com/yourusername/cve-scraper/actions)
```

## 步骤7: 创建GitHub Pages（可选）

如果想要一个项目网站：

1. 在仓库设置中找到 "Pages"
2. Source 选择 "main" 分支
3. 选择 "/ (root)" 或 "/docs" 文件夹
4. 点击 "Save"

## 步骤8: 设置Issue模板（可选）

创建 `.github/ISSUE_TEMPLATE/` 目录，添加：

### Bug报告模板
`.github/ISSUE_TEMPLATE/bug_report.md`

### 功能请求模板
`.github/ISSUE_TEMPLATE/feature_request.md`

## 步骤9: 添加贡献者指南

已经创建了 `CONTRIBUTING.md`，确保它包含：
- 如何报告bug
- 如何提出新功能
- 代码规范
- 提交流程

## 步骤10: 推广你的项目

### 在社交媒体分享
- Twitter
- Reddit (r/netsec, r/python)
- LinkedIn

### 提交到awesome列表
- [awesome-security](https://github.com/sbilly/awesome-security)
- [awesome-python](https://github.com/vinta/awesome-python)

### 在相关论坛发布
- HackerNews
- InfoSec社区

## 常见问题

### Q: 如何更新代码？
```bash
git add .
git commit -m "描述你的更改"
git push
```

### Q: 如何创建新分支？
```bash
git checkout -b feature/new-feature
# 做出更改
git add .
git commit -m "Add new feature"
git push -u origin feature/new-feature
```

然后在GitHub上创建Pull Request。

### Q: 如何处理合并冲突？
```bash
git pull origin main
# 解决冲突
git add .
git commit -m "Resolve conflicts"
git push
```

## 维护建议

1. **定期更新依赖**: 检查 nvdlib 是否有新版本
2. **回复Issues**: 及时回复用户的问题和建议
3. **审查Pull Requests**: 仔细审查贡献者的代码
4. **更新文档**: 保持文档与代码同步
5. **发布新版本**: 有重大更新时发布新版本

## 安全建议

1. **不要提交API密钥**: 已在 .gitignore 中排除
2. **使用Secrets**: GitHub Actions中的敏感信息使用Secrets
3. **定期检查依赖**: 使用 Dependabot 检查安全漏洞
4. **代码审查**: 审查所有Pull Request

## 许可证

确保你的项目使用了合适的开源许可证（已使用MIT）。

---

祝你的项目成功！🎉
