---
name: patent-drafting
description: "中国发明专利端到端起草技能——从论文/代码/交底材料出发，提取创新点，去中国专利局(CNIPA)查新核验新颖性，学习领域写法，做客体适格性(技术方案三要素)自审，并按需撰写技术交底书或说明书。按用户意图分发阶段(查新/学习写法/写交底书/写说明书/全流程/快速修订)，只跑所需环节。Use when drafting or revising a Chinese invention patent: prior-art search, novelty/inventiveness, subject-matter eligibility self-review, or writing the 技术交底书 (disclosure) or 说明书 (specification)."
---

# 中国发明专利起草（patent-drafting）

统一编排「查新调研 → 领域写法学习 → 创新性/新颖性补全 → 客体适格性自审 → 撰写交底书或说明书」。本技能并入三份来源：说明书写作规范（原 patent-spec-writing）、交底书写作与查新工具（patent-disclosure-skill）、客体适格性自审（patent-review-skill）。**工具/知识/prompt 已物理并入本技能自带（`tools/`、`references/`），全用技能相对路径、零私有路径**；可执行工具统一在专用 conda 环境中运行（见下「环境」节）。

参考文件（在对应阶段按需通读，不必一次性全读，以省 token）：
- 写说明书 → `references/spec-writing.md`（1–14 节完整规范）
- 写交底书 → `references/disclosure-writing.md`
- 查新与客体自审 → `references/prior-art-and-eligibility.md`
- 画说明书附图 → `references/figure-drafting.md`（选图决策表/画法粒度/线型/子图/合规A4/逐图联动/两层验收）
- 写软著（软件著作权登记材料）→ `references/software-copyright-writing.md`（独立软著流水线：intake/四栈读码启发式/操作-设计说明书模板/源代码60页/申请表字段/截图三级兜底/合规自检）

## 环境（运行任何工具前必读）

本技能所有可执行工具都在**专用 conda 环境 `patent-drafting`（Python 3.11）**中运行，不污染 base/其他环境。

> **路径约定（宿主无关）**：下文 `$SKILL_DIR` 指本技能安装根目录——Claude Code 默认 `~/.claude/skills/patent-drafting`、Codex 默认 `~/.codex/skills/patent-drafting`，装到别处则指向该处。所有命令一律以 `$SKILL_DIR` 为根；执行时把它展开成实际安装路径即可。

需要跑工具（查新、读 docx/pptx、类案匹配、交底书出图/出 Word）时按三步：

1. **自动检测环境是否存在**：
   ```bash
   conda env list | grep -q patent-drafting && echo READY || echo MISSING
   ```
2. **`MISSING` → 一键搭建（幂等，约数分钟，含 chromium/nodejs/mermaid 下载）**；`READY` → 直接用：
   ```bash
   bash "$SKILL_DIR/tools/setup_env.sh"
   ```
3. **每次调用工具一律走该环境且加 `--no-capture-output`**（否则 conda 在 Windows 下用 GBK 重编码子进程输出会崩 `UnicodeEncodeError`）：
   ```bash
   conda run --no-capture-output -n patent-drafting python "$SKILL_DIR/tools/<工具>.py" <参数>
   ```

要点：
- 环境已装：playwright(+chromium)、mammoth、python-pptx、python-docx、matplotlib、nodejs、mermaid-cli。
- mermaid 渲染依赖机器本地 `tools/puppeteer-config.json`（setup 生成、指向本机 chromium、已 `.gitignore`）；缺失则重跑 setup，或 `mermaid_render.py` 自动降级（保留 mermaid 围栏、仍出 .md/.docx）。
- cnipa 首次若报缺浏览器：`conda run --no-capture-output -n patent-drafting python -m playwright install chromium`。
- **conda run 两个坑**：①不要用 `conda run ... python -c "<多行脚本>"`（conda 不支持 argv 含换行，会崩）——调用一律走工具 `.py` 文件；②必须带 `--no-capture-output`（capture 模式既会 GBK 重编码崩溃、又不透传 stdin 使 heredoc 静默失效）。
- 纯检索/纯写作不跑脚本时无需该环境；快速修订可跳过。

## §0 意图分发（入口，先读 prompt 再决定跑哪些阶段）

不要无脑全跑。按用户 prompt 匹配，只执行所需阶段；阶段可叠加。

| 用户意图（prompt 关键词） | 执行阶段 |
|---|---|
| 查新 / 检索 / 现有技术 / 新颖性 / prior art | §1 → §2 →（§4 汇总差异） |
| 学领域写法 / 看范例 / 这类专利怎么写 | §1 → §2 → §3 |
| 写交底书 / 交底 / disclosure | （按需 §1–§4.5）→ §5·交底书 |
| 写说明书 / spec / 改说明书 | （按需 §1–§4.5）→ §5·说明书 |
| 全流程 / 从头做 / 完整起草 | §1 → §2 → §3 → §4 → §4.5 → §5 |
| 快速修订 / 小改 / 套返修意见 | 直接 §5（跳过 §1–§4.5） |
| 客体审查 / 适格性 / 能不能授权 / 是不是技术方案 | §4.5 |
| 写软著 / 软件著作权 / 软著说明书 / 源代码材料 / 软著申请表 | §SC（独立软著流水线，跳过 §1–§4.5） |

意图含糊且涉及"写"时，先确认两点：写**交底书还是说明书**、**是否需要先查新/学习**；其余低风险默认按上表推断并说明。

> **专利 vs 软著分流**：软著（计算机软件著作权登记）是**版权登记、无实质审查**，与发明专利是两条线。命中软著意图直接进 **§SC**，不跑查新(§2)/客体(§4.5)/创造性(§4)；反之专利意图不进 §SC。

## §1 关键词与技术方向提取

- 有论文：取标题、摘要、keyword、创新点、主要公式名。
- 无论文：从代码、发明人交底、已有材料提取（Office 材料先用 `docx_to_md.py`/`pptx_to_md.py` 转 md 再读，命令见 §6）。
- 产出 **3–6 个技术方向**，每方向归纳 **2–8 个语义检索词块**（沿用 `references/prior-art-and-eligibility.md` 的词块法）。

## §2 CNIPA 查新

详细规则与命令见 `references/prior-art-and-eligibility.md` §A。要点：
- `cnipa_epub_search.py` 优先；一次一词块、多轮调用、按 `pub_number` 合并、`abstract` 必用。
- **每方向≥5 篇**。
- 环境缺失/失败 → WebSearch/WebFetch 兜底，并**标注来源可靠性**。
- 主线只保留紧凑命中表（pub_number / 标题 / 摘要），不堆长 HTML。

## §3 领域写法学习 + 差异化（subagent）

- **每技术方向派 1 个 subagent**（不是每篇 1 个），令其深读该方向 ≥5 篇全文。
- subagent 返回**已消化的详实报告**，含：①与本案的差异点（支撑新颖性/创造性）②该领域说明书/权利要求的写法要素与典型句式 ③可借鉴结构与可引用证据。
- 主线只收报告、不收原文 → 控 token；subagent 并行但限流（≤可用并发）。
- 只有用户要"学写法/全流程"时才跑本阶段。

## §4 创新性 / 新颖性补全

汇总各方向报告，落到对应文本：
- 交底书 → 「现有技术对比 / 区别论述」（disclosure 1.1）。
- 说明书 → 「背景技术分类+缺陷」「穿透式审查」「有益效果」。
- 诚实边界：据实引证、不夸大、不把已知现象写成首创。

## §4.5 客体适格性自审（写前/定稿前的穿透式自审）

详见 `references/prior-art-and-eligibility.md` §B。与 §2 互补：查新保新颖性，本节保**适格性/创造性论证**。核验项：
- 第一性原理：专利法第二条第二款三要素（技术问题 / 技术手段 / 技术效果）。
- 删除测试（与说明书规范 §13.2 统一）+ 闭环断层检测。
- 数据含义 L1–L5 + 领域关联度 G0–G4 锚定（AI/算法类判抽象算法等不授权客体风险；层级定义读 review 知识库，勿臆造）。
- 类案对照：`case_matcher.py` 比对授权/不授权案例。
- 产出内部自审结论，把问题回改进稿；自审不写入正文。

## §5 撰写（按意图二选一或都写）

- **说明书**：通读 `references/spec-writing.md`，按 1–14 节规范写/改（硬规则不挂名词小标题、三级纯文字、公式唯一名称禁式号、网络三段式、迭代终止步骤、整体技术构思段、有益效果方案+效果、具体实施方式重走+阶段小结+图走查、返修联动矩阵、附图（§11：AI/网络类方法流程图与网络结构图各出一张，可用 mermaid_render 生成）、18 项自检）。
- **交底书**：通读 `references/disclosure-writing.md`，并按其指引使用自带的 `references/disclosure-prompts/disclosure_builder.md` + `template_reference.md`；产出 .md + .docx，自检不入正文。

## §SC 软件著作权（软著）分支

软著与专利是两条线：软著是**版权登记、无实质审查**，故本分支**不跑查新/客体/创造性**，自成一条更短流水线。命中 §0 表"写软著"意图时进入本节，**通读 `references/software-copyright-writing.md`** 后按其执行。

一句话流程（详规见参考文档）：

1. **SC-1 Intake**：一次问全——源码仓路径（可多个）、软件全称/简称/版本（默认 V1.0）、著作权人+开发方式（独立/合作/委托）、说明书类型（默认按有无 GUI 自动判，可覆盖）、截图来源。缺项标"待确认"，**不杜撰**。
2. **SC-2 读码梳理**：Glob/Grep 识别技术栈与入口，定位界面定义/控件/事件回调精读（四栈启发式见参考文档 §4），其余采样，产出中间稿（界面区块树 / 逐步操作流程，或无 GUI 时模块-函数-数据流）。**只写代码里有的**。操作流程不直接读码成文，走 **§4.5「抽取+语义读码 → 功能-顺序确认表 → 逐功能确认(粒度 A/B 由用户选) → 装配」**：主线按**代码语义**(I/O 锚点 + 调用图 + 数据依赖的"输入→输出关键路径")判定、**不靠命名/菜单序**(仅作旁证)；无单一主线的多功能工具箱**列候选流程交用户定主线**；最后把顺序与主次锚定到作者，主线与"其他功能"分开。
3. **SC-3 出三样**：①说明书（操作/设计，套 `references/sc-templates/` 文风 → `md_to_docx.py` 出 docx；设计说明书的结构图/流程图走 `mermaid_render.py`）②源代码 60 页材料（`sc_source_doc.py`）③申请表字段表（`sc-templates/申请表字段表.md` + 实测行数）。
4. **SC-4 合规自检（不入正文）+ 交付告知**：名称三处一致、源代码≥50行/页·前30后30·无空行·末页是结尾、说明书≥30行/页·无真实用户数据/他名软件、行数↔源码页数不矛盾、主要功能描述 500–1300 字（2026-03 新规）。不合规回改。**交付时必附草稿声明（不可省略）**——见下。

> **⚠️ 2026-03-15 合规红线（交付必告知）**：CPCC 新版申请表要求申请人**手写实名承诺"未使用 AI 开发编写代码、撰写文档或生成登记申请材料"**，失实将列入失信名单并挂个人征信。故本分支产出一律按"**草稿/素材**"交付，交付时**必须明确告知用户**：本输出不建议直接提交，须自行实质修改、核对真实性后使用，承诺与征信风险用户自负。详见 `references/software-copyright-writing.md` 顶部⚠️块。

截图三级兜底：读码生文（默认）→ playwright 自动截图（Web/Electron，`sc_ui_capture.py`）→ 引导用户补图；无 GUI 直接转设计说明书（免截图）。

## §6 工具清单（均自带；统一在 conda 环境 patent-drafting 中运行，见顶部「环境」节）

依赖由 `tools/setup_env.sh` 一次装好；调用一律 `conda run --no-capture-output -n patent-drafting python tools/<工具>.py`。一键环境搭建/修复：`tools/setup_env.sh`。
- 查新：`tools/cnipa_epub_search.py`（+ 自带兄弟模块 cnipa_epub_parse/crawler；需 `pip install -r tools/requirements-cnipa.txt` 且 `python -m playwright install chromium`）。
- 读料：`tools/docx_to_md.py` / `tools/pptx_to_md.py`（需 `tools/requirements.txt`，含 mammoth/python-pptx）。
- 交底书产出：`tools/mermaid_render.py`（mermaid→PNG）、`tools/md_to_docx.py`（→Word）、`tools/math_render.py`（公式→PNG）。
- 说明书附图（A4 合规闭环，规范见 `references/figure-drafting.md`）：`tools/patent_figures.py`（配置 JSON + .mmd → 严格渲染 → A4 DOCX：页脚页码/居中/分页/仅图N/中性元数据）、`tools/patent_figures_check.py`（静态验收+图文引用核对，不改文件）；`mermaid_render.py --patent` 为附图严格渲染模式（白底黑线/无阴影/禁透明/失败或残留即非零/隐含 --no-docx）。
- 客体自审：`tools/case_matcher.py`，知识库 `references/knowledge/*.md`。
- 软著（§SC）：`tools/sc_source_doc.py`（扫码→裁剪前30后30、≥50行/页、去空行、页眉=软件名+版本、右上页码→出"源代码.docx"，并实测总行数回填申请表；**默认排除测试目录与自动生成代码**，`--include-tests`/`--include-generated` 可保留、`--tail-file` 指定末页文件、`--ext` 限定主语言；`--src` 可多次指定代码文件夹，`--dry-run` 仅自检并打印语言分布）、`tools/sc_ui_capture.py`（Web/Electron 走 playwright 自动截图，失败即降级退占位）。说明书与字段表用 `md_to_docx.py`/`mermaid_render.py` 出件，规范见 `references/software-copyright-writing.md`。
- 任一工具环境缺失 → 走兜底（WebSearch/WebFetch 或人工分析）并标注。

## §7 省 token 铁律

- 每方向 1 个 subagent（非每篇）；subagent 回消化报告而非原文。
- cnipa 多调用结果自行合并；只跑意图所需阶段；限并行数。
- 参考文件按阶段按需读，不一次性全读；快速修订跳过 §1–§4.5。

## §8 开源卫生（自包含 + 已脱敏）

- 本技能**自包含**：查新/读料/类案/交底书产出工具、客体自审知识库、交底书全套 prompt 均已并入 `tools/` 与 `references/`，不依赖外部插件路径。
- **全部路径已脱敏**：正文与参考文件只用技能相对路径（`tools/`、`references/`）；运行命令以宿主无关的 `$SKILL_DIR`（见「环境」节定义）为根，不含用户名等私有信息。
- 正文与参考均通用化：不含个人案件信息、实验数据。
- 迁移/开源：整目录可直接搬移（Claude Code、Codex 等宿主通用）；装到任何位置只需让 `$SKILL_DIR` 指向实际安装目录，命令本身无需改。

## §9 自检（交付前）

1. 是否按 §0 仅跑了用户意图所需阶段；
2. 查新每方向是否 ≥5 篇、命中是否经 abstract 核验、来源是否标注可靠性；
3. subagent 报告是否落到创新性/新颖性文本，差异点是否据实；
4. 客体自审三要素/删除测试/类案对照是否通过，问题是否回改；
5. 说明书或交底书是否各按其规范自检（spec 18 项 / 交底书 self_check 不入正文）；
6. 是否触及开源卫生红线（私有案情、私有数据）。
