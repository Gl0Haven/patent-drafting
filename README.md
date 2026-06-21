# patent-drafting

中国发明专利端到端起草技能（Claude Code Skill）。从论文 / 代码 / 交底材料出发，串联**查新调研 → 领域写法学习 → 创新性·新颖性补全 → 客体适格性自审 → 撰写技术交底书或说明书 → 生成合规说明书附图**全流程，并按用户意图分发阶段，只跑所需环节。

本技能并入三份来源：说明书写作规范、交底书写作与 CNIPA 查新工具、客体适格性自审。**工具 / 知识库 / prompt 全部物理自带于 `tools/` 与 `references/`，零私有路径，可整目录搬移。**

## 能力概览

- **CNIPA 查新**：语义词块多轮检索国家知识产权局公布公告，按 `pub_number` 合并，`abstract` 必核；失败自动降级 WebSearch 并标注来源可靠性。
- **领域写法学习**：每技术方向派 1 个 subagent 深读 ≥5 篇全文，回传消化报告（差异点 / 写法要素 / 可引用证据），省 token。
- **客体适格性自审**：专利法第二条第二款三要素、删除测试、L1–L5 / G0–G4 锚定、授权/不授权类案对照。
- **撰写**：技术交底书（含符号公式体例、mermaid 图）或说明书（三层公开、两种步骤写法、网络三段式、有益效果方案+效果、18 项自检）。
- **说明书附图（A4 合规闭环）**：mermaid `.mmd` 配置 → 严格白底黑线渲染 → A4 DOCX（页脚页码 / 居中 / 一图一页 / 仅排"图N(±a)" / 中性元数据）→ 静态验收 + 图文引用双向核对。

## 环境与安装

所有可执行工具运行在**专用 conda 环境 `patent-drafting`（Python 3.11）**，不污染 base。一键搭建（幂等，含 chromium / nodejs / mermaid-cli 下载）：

```bash
bash tools/setup_env.sh
```

检测是否已装：

```bash
conda env list | grep -q patent-drafting && echo READY || echo MISSING
```

调用任一工具一律走该环境并加 `--no-capture-output`（否则 Windows 下 conda 用 GBK 重编码子进程输出会崩 `UnicodeEncodeError`）：

```bash
conda run --no-capture-output -n patent-drafting python tools/<工具>.py <参数>
```

> mermaid 渲染依赖机器本地 `tools/puppeteer-config.json`（由 `setup_env.sh` 生成、指向本机 chromium、已被 `.gitignore` 排除，不入库）。缺失则重跑 setup，或 `mermaid_render.py` 自动降级（保留 mermaid 围栏、仍出 .md/.docx）。

## 安装为 Claude Code / Codex 技能

| 宿主 | 默认安装目录 |
|---|---|
| Claude Code | `~/.claude/skills/patent-drafting/` |
| OpenAI Codex | `~/.codex/skills/patent-drafting/` |

放置后新开会话或重启宿主，使其重新扫描技能目录。装到其他位置时，需把命令里的技能根路径相应调整；技能正文和引用采用相对路径，README 示例默认使用 Claude Code 路径。

## 目录结构

```
patent-drafting/
├── SKILL.md                     # 编排入口：意图分发 + 各阶段流程（始终加载）
├── references/                  # 按阶段按需通读的规范（省 token）
│   ├── spec-writing.md          # 说明书 1–14 节完整规范
│   ├── disclosure-writing.md    # 交底书写作指引
│   ├── prior-art-and-eligibility.md  # 查新 + 客体适格性自审
│   ├── figure-drafting.md       # 说明书附图规范（选图/粒度/线型/A4/验收）
│   ├── disclosure-prompts/      # 交底书分步 prompt 全套
│   └── knowledge/               # 客体自审知识库 + 关键词库
└── tools/                       # 可执行工具（conda 环境内运行）
    ├── setup_env.sh             # 一键搭建/修复 conda 环境
    ├── cnipa_epub_*.py          # CNIPA 查新
    ├── docx_to_md.py / pptx_to_md.py   # Office 转 Markdown
    ├── mermaid_render.py        # mermaid → PNG（含 --patent 附图严格模式）
    ├── md_to_docx.py / math_render.py  # 交底书产出
    ├── patent_figures.py        # 附图生成：配置 → 渲染 → A4 DOCX
    ├── patent_figures_check.py  # 附图静态验收 + 图文引用核对
    └── case_matcher.py          # 客体自审类案匹配
```

## 致谢与项目关系

本项目在形成过程中参考并整合了以下开源项目的工作，谨向原作者和贡献者致谢：

- [handsomestWei/patent-disclosure-skill](https://github.com/handsomestWei/patent-disclosure-skill)（MIT，Copyright © 2026 handsomestWei）：本项目的项目扫描、专利点挖掘、CNIPA 查新、技术交底书生成及部分文档处理工具以其公开实现为基础进行整合和扩展。
- [sipopark/Patent-Review-Skill](https://github.com/sipopark/Patent-Review-Skill)（发行包内 MIT，Copyright © 2024 Patent Review Skill Contributors）：本项目参考其四阶段客体适格性审查、L1–L5 / G0–G4 锚定和类案匹配思路，仅抽取起草阶段需要的自审核心。
- [snipp-zha/Paper-to-patent-Skill](https://github.com/snipp-zha/Paper-to-patent-Skill)（截至 2026-06-21，其 `main` 分支未见独立 LICENSE 文件）：本项目参考其论文来源映射、技术特征证据台账、权利要求先行、原生 Office Math 公式和完整申请包质量门槛等结构与方法。

`patent-drafting` 不是上述项目的简单改名或原样打包，而是面向中国发明专利起草场景重新编排的统一技能：

| 维度 | `patent-disclosure-skill` | `patent-review-skill` | `Paper-to-patent-Skill` | `patent-drafting` |
|---|---|---|---|---|
| 核心目标 | 从项目材料挖掘专利点并形成技术交底书 | 对既有申请进行客体适格性审查 | 将论文、学位论文或技术报告转换为证据可追溯的完整申请初稿 | 从主动查新、领域写法学习和创新补全推进到交底书或说明书起草 |
| 主要交付物 | 技术交底书及迭代记录 | 分阶段审查结论、类案比对和审核意见 | 权利要求书、说明书、摘要、摘要附图、审阅稿、结构化 JSON 和校验报告 | 技术交底书、完整说明书及合规说明书附图；当前不以权利要求书和摘要申请包为默认交付 |
| 起草主线 | 先挖掘和讨论专利点，再生成交底书 | 按四阶段审查节点形成结论 | 先建立来源地图和证据台账，再起草权利要求并反向对齐说明书、附图和摘要 | 先给出不带公式的总体说明，再按步骤结合公式细化；允许两种步骤写法按内容混用 |
| 证据追溯 | 保留项目来源并做逻辑、公式和参数一致性自检 | 以法律依据、技术三要素和类案作为审查锚点 | 使用 P/E/F/C 稳定来源 ID，将权利要求实质特征逐项映射到证据状态 | 要求技术事实可回溯且不得虚构，但尚未把稳定来源 ID 和权利要求逐特征映射设为统一硬产物 |
| 查新与差异化 | CNIPA 优先查新并形成现有技术材料 | 不以主动查新为主，重点是客体适格性 | 支持论文与已有专利双向特征映射，但不提供专利性结论 | 主动执行 CNIPA 查新、摘要核验、领域全文写法学习和新颖性/创造性补全 |
| 公式与网络写法 | 关注交底书内公式和参数一致 | 关注数据含义及技术关联 | 保留论文支持的核心公式并输出可编辑 Office Math，围绕权利要求术语组织全文 | 强调公式语义命名、先文字后公式、符号就地解释，以及网络输入输出、训练和推理关系的充分公开 |
| 附图能力 | Mermaid 图及交底书 DOCX 转换 | 以审查工作流可视化为主 | 生成权利要求步骤对齐的主流程图、方法论附图和摘要附图，输出 SVG/PNG/DOCX | 增加图集选型、训练/推理线型、A4 附图 DOCX、缩小可读性和图文双向引用验收 |
| 运行与组织 | 按工具分别安装 Python / Node.js 依赖 | Python 工作流、测试和自我进化目录 | 通过 manifest 三轴路由、按需片段、结构化草稿、脚本和单元测试组织 | 通过意图路由和分阶段 references 组织，统一使用隔离 conda 环境并提供失败降级和静态验收 |

本项目整体采用 Apache License 2.0；整合自前两个 MIT 项目的相应内容仍保留其原有许可和版权归属。`Paper-to-patent-Skill` 当前仓库未声明许可证，本致谢仅说明结构与方法参考关系，不据此推定其代码或文本可以按 Apache License 2.0 再许可；如存在直接复制内容，应另行取得许可或替换为独立实现。

## 开源卫生

- 自包含：查新 / 读料 / 类案 / 交底书产出工具、客体自审知识库、交底书全套 prompt 均已并入，不依赖外部插件路径。
- 已脱敏：正文与参考文件只用技能相对路径，运行命令用 `$HOME/.claude/skills/patent-drafting/`，不含用户名等私有信息；不含个人案件信息与实验数据。
- 唯一含本机路径的 `tools/puppeteer-config.json` 由 setup 生成、已被 `.gitignore` 排除，不入库。

## License

[Apache License 2.0](LICENSE)。
