# 交底书写作（patent-drafting · §5·交底书）

> 调用方：patent-drafting/SKILL.md。本文件给出技术交底书撰写的要点与对自带交底书工具页的引用。
> **路径约定**：`references/disclosure-prompts/`、`tools/` 均相对本技能根目录；运行命令以 `$HOME/.claude/skills/patent-drafting/` 为根（`$HOME` 脱敏不含用户名）。权威模板与全套分步指令已并入本技能 `references/disclosure-prompts/`，无外部私有路径依赖。

## 权威模板与分步指令（写前必读，均在 references/disclosure-prompts/）

- 结构、脱敏、符号与公式体例(§7.7)、图示规范、3.4.1 符号表范例：
  `references/disclosure-prompts/disclosure_builder.md`、`references/disclosure-prompts/template_reference.md`
- 全流程分步指令（按需）：`intake.md` / `project_scan.md` / `patent_points_analyzer.md` / `prior_art_search.md` /
  `disclosure_preview.md` / `disclosure_self_check.md`；迭代：`iteration_context.md` / `merger.md` / `correction_handler.md`。

## 与 patent-drafting 主流程的衔接

- §1 关键词与方向、§2 CNIPA 查新、§3 领域写法、§4 创新性补全、§4.5 客体自审的产出，直接喂给交底书：
  - 查新与区别论述 → 写入交底书「现有技术对比 / 区别（1.1）」；
  - 客体自审结论 → 用于校正专利点的技术方案属性，不写入正文。

## 交底书写作要点（概览，细则以上面 prompt 为准）

1. **材料扫描**：含 Office 文档时，先用 `tools/docx_to_md.py`/`tools/pptx_to_md.py` 转 md 再读（命令见下）。
2. **专利点**：候选→融合→选定；每个专利点写清技术问题、技术手段、技术效果（与 §4.5 三要素一致）。
3. **图示**：3.2 系统框图、3.4 流程图用 fenced ```mermaid```，**不要 ASCII 框图**；定稿用 `tools/mermaid_render.py` 转 PNG。
4. **符号与公式**：按 §7.7 体例（维度、下标、无字母多义、分隔符统一），3.4.1 符号表，3.5 符号同形；公式渲染可用 `tools/math_render.py`。
5. **脱敏**：按 template_reference 要求脱敏，正文不出现样例仓库类文末脚注。
6. **产出**：**同时**交付 `.md` 与 `.docx`；定稿用 `tools/mermaid_render.py`（失败回退 `tools/md_to_docx.py`）。
7. **命名**：凡交付（含首次定稿与迭代）一律 `{案件名}_{YYYYMMDDHHmmss}.md/.docx`，不覆盖旧稿（见 disclosure_builder §7.3 第5点）。
8. **自检**：按 `references/disclosure-prompts/disclosure_self_check.md` 内部执行，**自检清单不写入正文**。
9. **权利要求偏向点**：定稿交付对话按 disclosure_builder §7.6 做「权利要求偏向点」引导——**仅对话、不入正文、不捏造未出现的保护取向**。
10. **迭代**：在已有交底书上改时，识别意图走 `merger.md`（增量合并）或 `correction_handler.md`（纠错），另存带时间戳新文件、追加 `交底书修订对话记录.md`（可用 `tools/iteration_dialog_log.py`）。

## 读料工具命令

```bash
conda run --no-capture-output -n patent-drafting python "$HOME/.claude/skills/patent-drafting/tools/docx_to_md.py" --input "<path>.docx" --output "<dir>/<name>.md"
conda run --no-capture-output -n patent-drafting python "$HOME/.claude/skills/patent-drafting/tools/pptx_to_md.py" --input "<path>.pptx" --output "<dir>/<name>.md"
```
（依赖由 `tools/setup_env.sh` 装好，见 SKILL.md「环境」节；旧版 .ppt 不支持，先另存 .pptx。）

## 说明书 vs 交底书

二者技术对象、步骤、公式应同源一致。先有交底书再写说明书时，说明书按 `references/spec-writing.md` 的三级公开结构展开，不与交底书另起一套方案。
