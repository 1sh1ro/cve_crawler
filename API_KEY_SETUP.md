# API密钥配置指南

本文档说明如何配置和使用NVD API密钥。

## 为什么需要API密钥？

| 模式 | 速率限制 | 速度对比 |
|------|---------|---------|
| 无API密钥 | 5请求/30秒 | 基准速度 |
| 有API密钥 | 50请求/30秒 | **快10倍** 🚀 |

## 获取API密钥

### 步骤1: 申请API密钥

1. 访问 [NVD API密钥申请页面](https://nvd.nist.gov/developers/request-an-api-key)
2. 输入你的邮箱地址
3. 点击提交

### 步骤2: 确认邮箱

1. 查收邮件（来自 nvd-noreply@nist.gov）
2. 邮件中会包含：
   - 确认链接
   - UUID（用于激活）

### 步骤3: 激活API密钥

1. 访问确认链接：https://nvd.nist.gov/developers/confirm-api-key
2. 输入你的邮箱和UUID
3. 点击确认
4. 获取你的API密钥

**你的API密钥**: `10f8632f-3119-4c11-b25c-214e0a9203f2`

## 配置API密钥

### 方法1: 使用环境变量（推荐）✅

这是最安全和方便的方法。

#### 步骤1: 创建 .env 文件

在项目根目录创建 `.env` 文件（已创建）：

```bash
# .env
NVD_API_KEY=10f8632f-3119-4c11-b25c-214e0a9203f2
```

#### 步骤2: 直接使用

```bash
# 无需指定 --api-key 参数，会自动从环境变量读取
python cve_scraper.py -k "linux kernel" -y 1

# 或使用交互式模式
python quick_start.py
```

**优点**：
- ✅ 安全（.env文件不会被提交到Git）
- ✅ 方便（无需每次输入）
- ✅ 统一（所有脚本共享）

### 方法2: 命令行参数

每次运行时指定API密钥：

```bash
python cve_scraper.py -k "linux kernel" -y 1 --api-key 10f8632f-3119-4c11-b25c-214e0a9203f2
```

**优点**：
- ✅ 灵活（可以临时使用不同的密钥）

**缺点**：
- ❌ 每次都要输入
- ❌ 可能被记录在命令历史中

### 方法3: 配置文件

创建 `config.ini` 文件：

```ini
[NVD]
api_key = 10f8632f-3119-4c11-b25c-214e0a9203f2
```

然后在代码中读取（需要自己实现）。

## 验证API密钥

### 测试1: 运行快速测试

```bash
python cve_scraper.py -k "test" -y 1
```

如果看到 `✓ 使用API密钥模式（速度快10倍）`，说明配置成功！

### 测试2: 对比速度

```bash
# 不使用API密钥（慢）
python cve_scraper.py -k "linux" -y 1 --api-key ""

# 使用API密钥（快）
python cve_scraper.py -k "linux" -y 1
```

观察速度差异。

## 使用示例

### 示例1: 自动使用环境变量

```bash
# .env 文件已配置，直接运行
python cve_scraper.py -k "linux kernel privilege escalation" -y 5
```

### 示例2: 交互式模式

```bash
python quick_start.py
# 会自动检测并使用环境变量中的API密钥
```

### 示例3: 临时使用其他密钥

```bash
# 命令行参数优先级高于环境变量
python cve_scraper.py -k "apache" -y 2 --api-key OTHER_KEY
```

## 安全注意事项

### ✅ 应该做的

1. **使用 .env 文件**
   - 已在 .gitignore 中排除
   - 不会被提交到Git

2. **不要分享API密钥**
   - 这是你的个人密钥
   - 不要发布到公开仓库

3. **定期更换密钥**
   - 如果怀疑泄露，立即更换

### ❌ 不应该做的

1. **不要硬编码在代码中**
   ```python
   # ❌ 错误示例
   api_key = "10f8632f-3119-4c11-b25c-214e0a9203f2"
   ```

2. **不要提交到Git**
   ```bash
   # ❌ 不要这样做
   git add .env
   git commit -m "Add API key"
   ```

3. **不要在公开场合展示**
   - 截图时注意遮挡
   - 演示时使用示例密钥

## 环境变量配置（不同系统）

### Windows

#### 临时设置（当前会话）
```cmd
set NVD_API_KEY=10f8632f-3119-4c11-b25c-214e0a9203f2
python cve_scraper.py -k "linux" -y 1
```

#### 永久设置（系统环境变量）
1. 右键"此电脑" → 属性
2. 高级系统设置 → 环境变量
3. 新建用户变量：
   - 变量名: `NVD_API_KEY`
   - 变量值: `10f8632f-3119-4c11-b25c-214e0a9203f2`

### Linux/Mac

#### 临时设置（当前会话）
```bash
export NVD_API_KEY=10f8632f-3119-4c11-b25c-214e0a9203f2
python3 cve_scraper.py -k "linux" -y 1
```

#### 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
```bash
echo 'export NVD_API_KEY=10f8632f-3119-4c11-b25c-214e0a9203f2' >> ~/.bashrc
source ~/.bashrc
```

## 故障排查

### 问题1: 提示未使用API密钥

**原因**: 环境变量未正确加载

**解决**:
```bash
# 检查 .env 文件是否存在
cat .env  # Linux/Mac
type .env  # Windows

# 检查内容是否正确
# 应该包含: NVD_API_KEY=你的密钥

# 重新安装依赖
pip install python-dotenv
```

### 问题2: 速度仍然很慢

**原因**: API密钥可能无效或过期

**解决**:
1. 访问 NVD 网站验证密钥
2. 如果过期，重新申请
3. 更新 .env 文件

### 问题3: 找不到 .env 文件

**原因**: 文件可能被隐藏

**解决**:
```bash
# Linux/Mac
ls -la | grep .env

# Windows
dir /a | findstr .env

# 如果不存在，创建它
echo NVD_API_KEY=10f8632f-3119-4c11-b25c-214e0a9203f2 > .env
```

## 常见问题

### Q: .env 文件会被提交到Git吗？
A: 不会，已在 .gitignore 中排除。

### Q: 可以在多个项目中使用同一个密钥吗？
A: 可以，但建议为不同项目申请不同的密钥。

### Q: API密钥有使用期限吗？
A: 通常没有，但NVD可能会定期要求重新验证。

### Q: 忘记API密钥怎么办？
A: 重新申请一个新的密钥。

### Q: 可以分享API密钥给团队吗？
A: 不建议，每个人应该申请自己的密钥。

## 最佳实践

1. **使用 .env 文件**（已配置）
2. **不要提交 .env 到Git**（已在 .gitignore）
3. **提供 .env.example 作为模板**（已创建）
4. **在文档中说明如何配置**（本文档）
5. **代码中优雅地处理缺失密钥**（已实现）

## 总结

✅ 你的API密钥已配置在 `.env` 文件中  
✅ 代码已更新支持自动读取环境变量  
✅ .gitignore 已配置，不会泄露密钥  
✅ 可以直接使用，无需每次输入  

**现在就可以享受10倍速度提升了！** 🚀

---

**你的API密钥**: `10f8632f-3119-4c11-b25c-214e0a9203f2`  
**配置文件**: `.env`  
**状态**: ✅ 已配置
