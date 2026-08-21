--[[
oracle_image_trigger.lua — commit 时触发图片输出

注册位置：rime/jiaguwen.schema.yaml 中 engine.processors
监听 commit 事件，当 oracle_image_mode 开启时调用本地渲染服务
]]

local M = {}

-- 检查可选依赖
local http_ok, http = pcall(require, "socket.http")
local ltn12_ok, ltn12 = pcall(require, "ltn12")

function M.commit_handler(commit_text, env)
  -- 检查"图片输出模式"开关
  local image_mode = env.engine.context:get_option("oracle_image_mode")
  if not image_mode then
    return  -- 默认模式，不处理
  end

  if not (http_ok and ltn12_ok) then
    -- 没有 luasocket 时直接降级
    return commit_text
  end

  -- 通过本地 HTTP 调用渲染服务
  local req_body = string.format(
    '{"text": "%s", "mode": "image"}',
    commit_text:gsub('"', '\\"')
  )
  local res_body = {}
  local ok, err = http.request{
    url = "http://127.0.0.1:19840/oracle/render",
    method = "POST",
    headers = { ["Content-Type"] = "application/json" },
    source = ltn12.source.string(req_body),
    sink = ltn12.sink.table(res_body),
  }
  if ok then
    -- 服务端已自动复制图片到剪贴板 + 模拟 Ctrl+V
    -- 返回空字符串避免重复上屏
    return ""  -- 注释掉此行可同时上屏文字（保险）
  end
  return commit_text
end

return M