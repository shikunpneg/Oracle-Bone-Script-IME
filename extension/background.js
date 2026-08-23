// background.js — Service Worker（Manifest V3）
// 处理快捷键、跨域消息、调用本地渲染服务

const RENDER_SERVER = "http://127.0.0.1:19840";

// === 快捷键监听 ===
chrome.commands.onCommand.addListener(async (command) => {
  if (command === "trigger-oracle-image") {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab) {
      chrome.tabs.sendMessage(tab.id, { action: "render-oracle-image" });
    }
  } else if (command === "trigger-oracle-ocr") {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (tab) {
      chrome.tabs.sendMessage(tab.id, { action: "trigger-oracle-ocr" });
    }
  }
});

// === 接收 content script 的跨域请求（CORS 绕过） ===
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "call-render-server") {
    fetch(RENDER_SERVER + request.path, {
      method: request.method || "GET",
      headers: request.headers || {},
      body: request.body,
    })
      .then(async (res) => {
        const contentType = res.headers.get("content-type");
        if (contentType && contentType.includes("application/json")) {
          sendResponse({ ok: res.ok, data: await res.json() });
        } else {
          sendResponse({ ok: res.ok, blob: await res.blob() });
        }
      })
      .catch((err) => sendResponse({ ok: false, error: err.message }));
    return true;  // 异步响应
  }
  return false;
});