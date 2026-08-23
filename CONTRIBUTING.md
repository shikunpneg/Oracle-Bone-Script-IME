# 贡献指南

> 感谢你考虑为甲骨文输入法做贡献！

## 行为准则

- 尊重所有贡献者
- 接受建设性批评
- 关注对社区最有利的事情

## 如何贡献

### 报告 Bug

- 在 [Issues](https://github.com/shikunpneg/Oracle-Bone-Script-IME/issues) 中创建 bug 报告
- 包含：复现步骤、期望结果、实际结果、操作系统、输入法版本
- 如果可能，附上截图或日志

### 提出新功能

- 先在 [Discussions](https://github.com/shikunpneg/Oracle-Bone-Script-IME/discussions) 讨论
- 描述：动机、用户故事、可能的实现方案
- 等待 maintainer 反馈后再开 PR

### 提交代码

1. Fork 仓库
2. 创建功能分支：`git checkout -b feat/my-feature`
3. 编写代码 + 测试
4. 遵循代码规范（见下）
5. 提交：`git commit -m "feat: my feature"`
6. 推送到 fork：`git push origin feat/my-feature`
7. 创建 Pull Request

## 代码规范

### Python（服务端）

- 遵循 PEP 8
- 使用 type hints
- 重要函数加 docstring
- 测试覆盖率 > 80%

```bash
# 格式化
black server/
isort server/

# 类型检查
mypy server/

# 测试
pytest server/tests/
```

### JavaScript（扩展 + Electron）

- ES2022+ 语法
- 2 空格缩进
- 使用 const/let，禁用 var

```bash
# 格式化
npx prettier --write extension/ electron/

# Lint
npx eslint extension/ electron/
```

### Lua（RIME 扩展）

- 遵循 [Lua Style Guide](https://github.com/Olivine-Labs/lua-style-guide)
- 2 空格缩进

### YAML（schema 配置）

- 2 空格缩进
- 引号统一使用双引号

## 提交信息规范

```
<type>(<scope>): <subject>

<body>

<footer>
```

类型：
- `feat`：新功能
- `fix`：Bug 修复
- `docs`：仅文档变更
- `style`：代码风格（不影响功能）
- `refactor`：重构（既不修复 bug 也不增加功能）
- `test`：增加测试
- `chore`：杂项（构建、CI 等）

示例：
```
feat(server): add /oracle/ocr endpoint

Add new endpoint to recognize oracle bone script from uploaded image.
Uses ONNX Runtime with HUST-OBS ResNet50 model.

Closes #42
```

## 测试指南

- 新功能必须包含测试
- Bug 修复必须包含回归测试
- 测试覆盖率不能降低

### Python 测试

```python
# server/tests/test_render.py
from app.render_service import RenderService

def test_render_chinese():
    service = RenderService(font_path="tests/fixtures/FZJIAGW.ttf")
    png, _ = service.render("中", font_size=120, canvas=128)
    assert len(png) > 100  # 至少有一些字节
```

## 文档规范

- 用户文档放 `docs/`
- API 文档用 docstring（Python）或 JSDoc（JS）
- 重大变更更新 README.md 和 CHANGELOG.md

## 发布流程

1. 更新 `CHANGELOG.md`
2. 提升版本号（语义化版本）
3. 创建 Git tag：`git tag -a v0.2.0 -m "Release 0.2.0"`
4. 推送 tag：`git push origin v0.2.0`
5. GitHub Actions 自动构建
6. 在 GitHub Releases 撰写说明

## 社区

- 💬 Discussions：https://github.com/shikunpneg/Oracle-Bone-Script-IME/discussions
- 🐛 Issues：https://github.com/shikunpneg/Oracle-Bone-Script-IME/issues

## 致谢

所有贡献者都会在 [README.md](README.md) 和发布说明中致谢。