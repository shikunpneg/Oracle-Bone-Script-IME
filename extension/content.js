// content.js — 在任意网页的输入框中触发甲骨文图片输出
// 监听 Ctrl+Shift+I 快捷键，将输入框内容提交给本地渲染服务

(async function() {
  "use strict";

  // 检查是否已注入（避免重复）
  if (window.__ORACLE_BONE_IME_INSTALLED__) return;
  window.__ORACLE_BONE_IME_INSTALLED__ = true;

  console.log("[甲骨文输入法] 已加载 v0.1.0");

  // === 创建浮动提示框 ===
  const toast = document.createElement("div");
  toast.id = "oracle-bone-toast";
  toast.style.cssText = `
    position: fixed; top: 20px; right: 20px; z-index: 2147483647;
    padding: 12px 20px; background: #2c1810; color: #d4a574;
    border: 2px solid #d4a574; border-radius: 8px;
    font-family: "Microsoft YaHei", sans-serif; font-size: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    display: none; pointer-events: none;
  `;
  document.documentElement.appendChild(toast);

  function showToast(msg, duration = 2000) {
    toast.textContent = msg;
    toast.style.display = "block";
    setTimeout(() => { toast.style.display = "none"; }, duration);
  }

  // === 监听来自 background 的消息 ===
  chrome.runtime.onMessage.addListener((request, _sender, sendResponse) => {
    if (request.action === "render-oracle-image") {
      renderOracleImage().then(sendResponse).catch(sendResponse);
      return true;
    }
    if (request.action === "trigger-oracle-ocr") {
      triggerOCR().then(sendResponse).catch(sendResponse);
      return true;
    }
  });

  // === 监听页面内快捷键（Ctrl+Shift+I） ===
  document.addEventListener("keydown", async (e) => {
    if (e.ctrlKey && e.shiftKey && (e.key === "I" || e.key === "i")) {
      e.preventDefault();
      await renderOracleImage();
    }
    if (e.ctrlKey && e.shiftKey && (e.key === "G" || e.key === "g")) {
      e.preventDefault();
      await triggerOCR();
    }
  });

  // === 字 → 图渲染 ===
  async function renderOracleImage() {
    const el = document.activeElement;
    if (!el) {
      showToast("⚠️ 请先点击输入框");
      return { ok: false, error: "no_focus" };
    }

    let text = "";
    if (el.tagName === "INPUT" || el.tagName === "TEXTAREA") {
      text = el.value;
    } else if (el.isContentEditable) {
      text = el.innerText || el.textContent;
    }

    if (!text || !text.trim()) {
      showToast("⚠️ 输入框为空");
      return { ok: false, error: "empty" };
    }

    showToast(`🐘 渲染中：${text.slice(0, 20)}${text.length > 20 ? "..." : ""}`);

    try {
      // 通过 background 转发跨域请求（避开 CORS）
      const res = await chrome.runtime.sendMessage({
        action: "call-render-server",
        path: "/oracle/render",
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, auto_paste: false }),
      });

      if (!res.ok) {
        showToast(`❌ 渲染失败：${res.error || "未知错误"}`);
        return { ok: false, error: res.error };
      }

      // 把 PNG blob 写入剪贴板
      const blob = new Blob([res.blob], { type: "image/png" });
      await navigator.clipboard.write([
        new ClipboardItem({ "image/png": blob })
      ]);

      // 触发原输入框的粘贴
      el.focus();
      document.execCommand("paste");

      showToast(`✓ 已粘贴甲骨文图片`);
      return { ok: true };
    } catch (err) {
      showToast(`❌ 出错：${err.message}`);
      return { ok: false, error: err.message };
    }
  }

  // === 图 → 字 OCR（截图识别）===
  async function triggerOCR() {
    showToast("📸 请右键粘贴图片或复制图片后再试");
    // 简化：提示用户复制图片后再触发
    try {
      const items = await navigator.clipboard.read();
      for (const item of items) {
        for (const type of item.types) {
          if (type === "image/png") {
            const blob = await item.getType("image/png");
            const formData = new FormData();
            formData.append("image", blob, "clipboard.png");
            const res = await chrome.runtime.sendMessage({
              action: "call-render-server",
              path: "/oracle/ocr",
              method: "POST",
              body: formData,
            });
            if (res.ok && res.data?.candidates?.[0]) {
              const top = res.data.candidates[0];
              showToast(`🔍 识别：${top.chinese} (${(top.conf * 100).toFixed(1)}%)`);
              // 自动填入当前输入框
              const el = document.activeElement;
              if (el && (el.tagName === "INPUT" || el.tagName === "TEXTAREA")) {
                el.value = top.chinese;
                el.dispatchEvent(new Event("input", { bubbles: true }));
              }
              return { ok: true, candidate: top };
            }
          }
        }
      }
    } catch (err) {
      showToast(`❌ OCR 失败：${err.message}`);
      return { ok: false, error: err.message };
    }
  }
})();