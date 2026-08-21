# Web Demo · 甲骨文输入法在线体验

基于 Vue 3 + Vite，提供在线预览功能。

## 开发

```bash
cd web
npm install
npm run dev
# 访问 http://localhost:5173
```

## 构建

```bash
npm run build
# 产物在 dist/
```

## 部署到 GitHub Pages

```bash
npm run build
# 将 dist/ 内容推送到 gh-pages 分支
```

## 依赖

- Vue 3
- Vite 5
- vite-plugin-svg-icons（SVG sprite 管理）
- 字体：`../dist/fonts/FZJIAGW-subset.woff2`（由 `scripts/build_glyph_assets.py` 生成）

## 功能

| 功能 | 描述 |
|------|------|
| 文字模式 | 加载 FZJIAGW WOFF2 子集字体，输入框直接显示甲骨文 |
| 图片模式 | 调用本地 `http://127.0.0.1:19840` 服务生成 PNG |
| 复制图片 | 把生成的 PNG 写入剪贴板，可粘到微信/QQ |
| 服务状态 | 自动检测本地服务连接状态 |