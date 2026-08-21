// renderer.js — Electron 渲染进程主逻辑

const inputEl = document.getElementById("inputText");
const previewEl = document.getElementById("preview");
const statusEl = document.getElementById("status");
const btnRender = document.getElementById("btnRender");
const btnOCR = document.getElementById("btnOCR");
const ocrResultEl = document.getElementById("ocrResult");

function setStatus(msg, ok = true) {
  statusEl.textContent = msg;
  statusEl.className = "status " + (ok ? "ok" : "err");
}

btnRender.addEventListener("click", async () => {
  const text = inputEl.value.trim();
  if (!text) {
    setStatus("⚠️ 请输入文字", false);
    return;
  }
  btnRender.disabled = true;
  setStatus("🐘 渲染中…");
  try {
    const res = await fetch("http://127.0.0.1:19840/oracle/render", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, auto_paste: false }),
    });
    if (!res.ok) throw new Error("渲染失败: " + res.status);
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    previewEl.innerHTML = `<img src="${url}" alt="${text}">`;
    setStatus(`✓ 已生成：${text}`);
  } catch (e) {
    setStatus(`❌ ${e.message}`, false);
  } finally {
    btnRender.disabled = false;
  }
});

btnOCR.addEventListener("click", async () => {
  ocrResultEl.textContent = "识别中…";
  try {
    // Electron 环境通过 IPC
    if (window.oracleIme) {
      await window.oracleIme.ocrClipboard();
      setStatus("📷 OCR 已触发，结果写入剪贴板");
      ocrResultEl.textContent = "✓ 已完成，请查看剪贴板";
    } else {
      setStatus("⚠️ OCR 仅在 Electron 桌面端可用", false);
    }
  } catch (e) {
    ocrResultEl.textContent = `❌ ${e.message}`;
  }
});

window.oracleIme?.onServerStatus((data) => {
  if (data.error) {
    setStatus("⚠️ 服务连接失败: " + data.error, false);
  } else {
    setStatus(`✓ 服务已连接（字体: ${data.font_loaded ? "OK" : "未加载"}）`);
  }
});

window.oracleIme?.checkServer();