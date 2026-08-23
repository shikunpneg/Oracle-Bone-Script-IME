// preload.js — Electron 渲染进程预加载脚本
const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("oracleIme", {
  renderText: (text) => ipcRenderer.invoke("render-text", text),
  ocrClipboard: () => ipcRenderer.invoke("ocr-clipboard"),
  checkServer: () => ipcRenderer.invoke("check-server"),
  onServerStatus: (callback) => ipcRenderer.on("server-status", (_e, data) => callback(data)),
});