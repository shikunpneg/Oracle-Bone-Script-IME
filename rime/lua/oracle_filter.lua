--[[
oracle_filter.lua — 过滤/排序候选词

功能：
  1. 把有甲骨文字形的候选排在前面
  2. 过滤掉非汉字字符（保留可选 emoji）
]]

local M = {}

function M.oracle_filter(translation, env)
  local has_glyph = {}
  local no_glyph = {}
  for i, cand in ipairs(translation:iter()) do
    local ch = cand.text
    local priority = cand.quality or 0
    -- 单字且在 BMP 汉字区
    if #ch == 1 then
      local cp = string.byte(ch)
      if cp >= 0x4E and cp <= 0x9F then
        table.insert(has_glyph, {cand, priority + 10})  -- 加权
      else
        table.insert(no_glyph, {cand, priority})
      end
    else
      table.insert(no_glyph, {cand, priority})
    end
  end
  -- 按权重排序
  table.sort(has_glyph, function(a, b) return a[2] > b[2] end)
  table.sort(no_glyph, function(a, b) return a[2] > b[2] end)
  -- yield 回
  for _, pair in ipairs(has_glyph) do
    yield(pair[1])
  end
  for _, pair in ipairs(no_glyph) do
    yield(pair[1])
  end
end

return M