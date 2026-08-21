# download_fonts.ps1 — Windows PowerShell 版本
# 用法：.\scripts\download_fonts.ps1 或 .\scripts\download_fonts.ps1 -Font fzjiagw

param(
  [string]$Font = "all"
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Root = Split-Path -Parent $ScriptDir
$FontDir = Join-Path $Root "assets\fonts"
New-Item -ItemType Directory -Force -Path $FontDir | Out-Null
Set-Location $FontDir

function Info($msg) { Write-Host "[INFO] $msg" -ForegroundColor Green }
function Warn($msg) { Write-Host "[WARN] $msg" -ForegroundColor Yellow }
function Err($msg)  { Write-Host "[ERR ] $msg" -ForegroundColor Red }

function Download-FZJIAGW {
  if (Test-Path "FZJIAGW.ttf") {
    Info "FZJIAGW.ttf 已存在，跳过"
    return
  }
  $urls = @(
    "https://www.foundertype.com/FZJiaGuWen.ttf",
    "https://cdn1.foundertype.com/Public/Uploads/FZJiaGuWen.ttf",
    "https://www.zishuai.com/fonts/FZJIAGW.ttf",
    "https://m.fontke.com/font/167501847/FZJIAGW.ttf"
  )
  Info "下载方正甲骨文 FZJIAGW.ttf..."
  foreach ($url in $urls) {
    Warn "尝试镜像: $url"
    try {
      Invoke-WebRequest -Uri $url -OutFile "FZJIAGW.ttf" -UseBasicParsing -ErrorAction Stop
      $size = (Get-Item FZJIAGW.ttf).Length
      Info ("✓ 下载成功: FZJIAGW.ttf ({0:N1} KB)" -f ($size/1KB))
      return
    } catch {
      Warn "下载失败: $_"
    }
  }
  Err "所有镜像失败，请手动从方正字库下载并放置到 $FontDir\FZJIAGW.ttf"
  Err "官方地址: https://www.foundertype.com/index.php/Register/index.html"
}

switch ($Font) {
  "fzjiagw" { Download-FZJIAGW }
  "all" {
    Download-FZJIAGW
  }
  default {
    Err "未知字体: $Font。可用: fzjiagw, all"
    exit 1
  }
}

Info "字体下载完成。当前 $FontDir 内容:"
Get-ChildItem $FontDir -Filter *.ttf | ForEach-Object {
  "{0} ({1:N1} KB)" -f $_.Name, ($_.Length/1KB)
} | Write-Host