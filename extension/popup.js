// popup.js — 弹出页面状态检查
(async function () {
  const statusEl = document.getElementById("status");
  try {
    const res = await fetch("http://127.0.0.1:19840/health", { method: "GET" });
    if (res.ok) {
      const data = await res.json();
      statusEl.textContent = data.font_loaded
        ? "✓ 服务已连接，字体已加载"
        : "⚠️ 服务已连接，但字体未加载";
      statusEl.className = "status ok";
    } else {
      statusEl.textContent = "⚠️ 服务返回 " + res.status;
      statusEl.className = "status err";
    }
  } catch (e) {
    statusEl.innerHTML = "❌ 服务未启动<br><small>运行 <code>python -m app.main</code></small>";
    statusEl.className = "status err";
  }
})();