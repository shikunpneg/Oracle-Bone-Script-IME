<script setup>
import { ref, computed, watch } from 'vue'

const inputText = ref('我爱甲骨文')
const mode = ref('text')  // text | image
const serverStatus = ref('unknown')
const charCount = computed(() => inputText.value.length)

// 检测本地服务是否启动
async function checkServer() {
  try {
    const res = await fetch('http://127.0.0.1:19840/health')
    const data = await res.json()
    serverStatus.value = data.font_loaded ? 'ok' : 'no-font'
  } catch (e) {
    serverStatus.value = 'offline'
  }
}

// 渲染图片模式
async function renderImage() {
  if (!inputText.value.trim()) return
  try {
    const res = await fetch('http://127.0.0.1:19840/oracle/render', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: inputText.value, auto_paste: false })
    })
    if (!res.ok) throw new Error('服务不可用')
    const blob = await res.blob()
    const url = URL.createObjectURL(blob)
    const img = previewEl.value.querySelector('img') || document.createElement('img')
    img.src = url
    img.alt = inputText.value
    previewEl.value.innerHTML = ''
    previewEl.value.appendChild(img)
    mode.value = 'image'
  } catch (e) {
    alert('渲染失败: ' + e.message + '\n\n请确认已启动本地服务:\ncd server && python -m app.main')
  }
}

const previewEl = ref(null)

// 复制图片到剪贴板
async function copyImage() {
  if (!inputText.value.trim()) return
  try {
    const res = await fetch('http://127.0.0.1:19840/oracle/render', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: inputText.value, auto_paste: false })
    })
    const blob = await res.blob()
    await navigator.clipboard.write([
      new ClipboardItem({ 'image/png': blob })
    ])
    alert('✓ 已复制甲骨文图片到剪贴板，可粘贴到微信/QQ')
  } catch (e) {
    alert('复制失败: ' + e.message)
  }
}

// 加载字体（文字模式）
function ensureFontLoaded() {
  const fontUrl = '/fonts/FZJIAGW-subset.woff2'
  const font = new FontFace('FZJIAGW', `url(${fontUrl})`)
  font.load().then(() => {
    document.fonts.add(font)
    mode.value = 'text'
  }).catch(() => {
    alert('字体加载失败，将使用图片模式')
    mode.value = 'image'
  })
}

checkServer()
</script>

<template>
  <header>
    <h1>🐘 甲骨文输入法 · 在线 Demo</h1>
    <p class="subtitle">「打汉字出甲骨文」开源输入法</p>
  </header>

  <div class="container">
    <div class="card">
      <label for="input">输入汉字</label>
      <textarea id="input" v-model="inputText" rows="3" />
      <p class="char-count">已输入 {{ charCount }} 个字符</p>

      <div class="actions">
        <button @click="renderImage">🐘 生成甲骨文图片</button>
        <button class="secondary" @click="copyImage">📋 复制图片到剪贴板</button>
        <button class="secondary" @click="ensureFontLoaded">🔤 加载字体（文字模式）</button>
      </div>

      <p style="margin-top:16px;font-size:12px;color:var(--color-muted);">
        服务状态：<span :style="{color: serverStatus === 'ok' ? '#2d6e2d' : serverStatus === 'offline' ? '#b22' : '#888'}">
          {{ serverStatus === 'ok' ? '✓ 已连接' : serverStatus === 'no-font' ? '⚠️ 未装字体' : serverStatus === 'offline' ? '❌ 未启动' : '检查中...' }}
        </span>
        <br>
        启动方式：<code>cd server && python -m app.main</code>
      </p>
    </div>

    <div class="card">
      <label>预览</label>
      <div ref="previewEl" class="preview" :class="{ empty: !inputText }">
        <span v-if="mode === 'text'">{{ inputText }}</span>
        <span v-else>点击「生成甲骨文图片」</span>
      </div>
    </div>
  </div>

  <div class="footer">
    <p>
      📦 <a href="https://github.com/shikunpneg/Oracle-Bone-Script-IME" target="_blank">GitHub 仓库</a>
      · 📖 <a href="https://github.com/shikunpneg/Oracle-Bone-Script-IME/blob/main/docs/MANUAL.md">用户手册</a>
    </p>
    <p style="margin-top:8px;font-size:11px;">
      基于方正甲骨文（FZJIAGW.ttf）+ librime + Apache-2.0 License
    </p>
  </div>
</template>