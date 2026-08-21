--[[
oracle_translator.lua — 在候选词后追加"🐘甲骨文"标签

注册位置：rime/jiaguwen.schema.yaml 中 engine.translators
调用顺序：在默认 lua_translator 之后追加
]]

local M = {}

function M.oracle_translator(input, seg, env)
  -- 复用默认 translator 的候选
  local candidates = env.engine.context:get_candidates() or {}
  for _, cand in ipairs(candidates) do
    -- 检查该字是否有对应甲骨文字形（FZJIAGW.ttf 的 cmap）
    local ch = cand.text
    if #ch == 1 then  -- 单字
      local cp = string.byte(ch)
      -- BMP 汉字 + CJK Ext 区段
      if (cp >= 0x4E and cp <= 0x9F)
         or (string.len(ch) > 1 and utf8.codepoint(ch) >= 0x3400 and utf8.codepoint(ch) <= 0x3134F) then
        yield(Candidate(cand.type, seg.start, seg._end,
          cand.text, cand.comment or "" .. " 🐘"))
      end
    end
  end
end

return M