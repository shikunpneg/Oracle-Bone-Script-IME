// electron/main.js — 甲骨文输入法桌面端主进程
// 负责：渲染服务管理、全局快捷键、剪贴板操作

const { app, BrowserWindow, ipcMain, clipboard, globalShortcut, Tray, Menu, nativeImage } = require("electron");
const { spawn } = require("child_process");
const path = require("path");
const fs = require("fs");
const http = require("http");

const ROOT = path.join(__dirname, "..");
const PYTHON_SCRIPT = path.join(ROOT, "server", "app", "main.py");
const FONT_PATH = path.join(ROOT, "assets", "fonts", "FZJIAGW.ttf");
const SERVER_PORT = 19840;
const SERVER_URL = `http://127.0.0.1:${SERVER_PORT}`;

let mainWindow = null;
let tray = null;
let pythonProcess = null;
let isQuitting = false;

// === 检查/启动 Python 渲染服务 ===
function ensureServerRunning() {
  return new Promise((resolve) => {
    const check = () => {
      http.get(SERVER_URL + "/health", (res) => {
        if (res.statusCode === 200) {
          console.log("[Electron] 渲染服务已在运行");
          resolve(true);
        } else {
          setTimeout(check, 1000);
        }
      }).on("error", () => {
        console.log("[Electron] 启动 Python 渲染服务...");
        pythonProcess = spawn("python", ["-m", "app.main"], {
          cwd: path.join(ROOT, "server"),
          stdio: ["ignore", "pipe", "pipe"],
        });
        pythonProcess.stdout.on("data", (d) => process.stdout.write(`[PY] ${d}`));
        pythonProcess.stderr.on("data", (d) => process.stderr.write(`[PY-ERR] ${d}`));
        setTimeout(check, 2000);
      });
    };
    check();
  });
}

// === 主窗口 ===
function createMainWindow() {
  mainWindow = new BrowserWindow({
    width: 480,
    height: 640,
    title: "甲骨文输入法",
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true,
      nodeIntegration: false,
    },
    icon: path.join(__dirname, "icons", "icon.png"),
  });
  mainWindow.loadFile(path.join(__dirname, "renderer", "index.html"));
  if (process.argv.includes("--dev")) {
    mainWindow.webContents.openDevTools();
  }
}

// === 系统托盘 ===
function createTray() {
  const iconPath = path.join(__dirname, "icons", "icon-16.png");
  if (!fs.existsSync(iconPath)) {
    console.warn("[Electron] 托盘图标不存在，跳过托盘创建");
    return;
  }
  const icon = nativeImage.createFromPath(iconPath);
  tray = new Tray(icon);
  tray.setToolTip("甲骨文输入法 v0.1.0");
  tray.setContextMenu(Menu.buildFromTemplate([
    { label: "显示主窗口", click: () => mainWindow?.show() },
    { label: "渲染服务状态", click: () => checkServerStatus() },
    { type: "separator" },
    { label: "退出", click: () => { isQuitting = true; app.quit(); } },
  ]));
}

async function checkServerStatus() {
  try {
    const res = await fetch(SERVER_URL + "/health");
    const data = await res.json();
    if (mainWindow) {
      mainWindow.webContents.send("server-status", data);
    }
  } catch (e) {
    if (mainWindow) {
      mainWindow.webContents.send("server-status", { error: e.message });
    }
  }
}

// === 全局快捷键：Ctrl+Shift+I 触发渲染 ===
function registerShortcuts() {
  const ok = globalShortcut.register("CommandOrControl+Shift+I", async () => {
    await triggerOracleRender();
  });
  if (!ok) console.warn("[Electron] 全局快捷键 Ctrl+Shift+I 注册失败");

  const ok2 = globalShortcut.register("CommandOrControl+Shift+G", async () => {
    await triggerOracleOCR();
  });
  if (!ok2) console.warn("[Electron] 全局快捷键 Ctrl+Shift+G 注册失败");
}

// === 触发渲染流程 ===
async function triggerOracleRender() {
  // 1. 读取剪贴板文本（用户在任意输入框选中的文字）
  const text = clipboard.readText();
  if (!text || !text.trim()) {
    console.log("[Electron] 剪贴板无文本");
    return;
  }

  try {
    // 2. 调用渲染服务
    const res = await fetch(SERVER_URL + "/oracle/render", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, auto_paste: false }),
    });

    if (!res.ok) {
      console.error("[Electron] 渲染失败:", res.status);
      return;
    }

    const arrayBuf = await res.arrayBuffer();
    const buf = Buffer.from(arrayBuf);

    // 3. 写入剪贴板
    const image = nativeImage.createFromBuffer(buf);
    clipboard.writeImage(image);

    // 4. 模拟 Ctrl+V
    const robot = require("robotjs");
    setTimeout(() => {
      robot.keyTap("v", "control");
    }, 50);

    console.log(`[Electron] ✓ 已渲染并粘贴：${text}`);
  } catch (e) {
    console.error("[Electron] 渲染流程失败:", e);
  }
}

async function triggerOracleOCR() {
  const image = clipboard.readImage();
  if (image.isEmpty()) {
    console.log("[Electron] 剪贴板无图片");
    return;
  }

  try {
    const png = image.toPNG();
    const formData = new FormData();
    const blob = new Blob([png], { type: "image/png" });
    formData.append("image", blob, "clipboard.png");

    const res = await fetch(SERVER_URL + "/oracle/ocr", {
      method: "POST",
      body: formData,
    });
    const data = await res.json();

    if (data.candidates?.[0]) {
      const top = data.candidates[0];
      clipboard.writeText(top.chinese);
      console.log(`[Electron] ✓ OCR：${top.chinese} (${(top.conf * 100).toFixed(1)}%)`);
    }
  } catch (e) {
    console.error("[Electron] OCR 失败:", e);
  }
}

// === IPC: 渲染进程调用 ===
ipcMain.handle("render-text", async (_evt, text) => {
  await triggerOracleRender();
  return { ok: true };
});

ipcMain.handle("ocr-clipboard", async () => {
  await triggerOracleOCR();
  return { ok: true };
});

ipcMain.handle("check-server", async () => {
  return checkServerStatus();
});

// === 应用生命周期 ===
app.whenReady().then(async () => {
  await ensureServerRunning();
  createMainWindow();
  createTray();
  registerShortcuts();
  console.log("[Electron] ✓ 甲骨文输入法桌面端已启动");
  console.log("[Electron]   全局快捷键: Ctrl+Shift+I / Ctrl+Shift+G");
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    isQuitting = true;
    app.quit();
  }
});

app.on("before-quit", () => {
  globalShortcut.unregisterAll();
  if (pythonProcess) {
    pythonProcess.kill();
  }
});

app.on("will-quit", () => {
  globalShortcut.unregisterAll();
});