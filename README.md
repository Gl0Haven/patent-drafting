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

`patent-drafting` 不是上述项目的简单改名或原样打包，而是面向中国发明专利起草场景重新编排的统一技能：

| 维度 | `patent-disclosure-skill` | `patent-review-skill` | `patent-drafting` |
|---|---|---|---|
| 核心目标 | 从项目材料挖掘专利点并形成技术交底书 | 对既有申请进行客体适格性审查 | 从查新、领域写法学习和创新补全推进到交底书或说明书起草 |
| 主要交付物 | 技术交底书及迭代记录 | 分阶段审查结论、类案比对和审核意见 | 技术交底书、完整说明书及合规说明书附图 |
| 说明书写作 | 不以完整说明书起草为主 | 不负责说明书成稿 | 提供三层公开、先总述后公式细化、两种步骤写法混用、公式语义命名、网络训练/推理分离等专门规则 |
| 查新与差异化 | CNIPA 优先查新并形成现有技术材料 | 重点是技术方案三要素与类案锚定 | 在 CNIPA 查新之外增加领域全文写法学习、差异点提炼和新颖性/创造性补全 |
| 客体自审 | 以交底书逻辑闭环和一致性自检为主 | 完整四阶段审查并含人工节点、自我进化和版本管理 | 只保留定稿前需要的客体适格性自审，不引入审查员人工编排和自我进化引擎 |
| 附图能力 | Mermaid 图及交底书 DOCX 转换 | 以审查工作流可视化为主 | 增加图集选型规则、训练/推理线型约定、A4 附图 DOCX 生成及图文双向引用验收 |
| 运行方式 | 按工具分别安装 Python / Node.js 依赖 | Python 工作流与测试脚本 | 统一使用隔离的 `patent-drafting` conda 环境，并保留失败降级和静态验收路径 |

本项目整体采用 Apache License 2.0；整合自上述项目的相应内容仍保留其原有 MIT 许可和版权归属。

## 开源卫生

- 自包含：查新 / 读料 / 类案 / 交底书产出工具、客体自审知识库、交底书全套 prompt 均已并入，不依赖外部插件路径。
- 已脱敏：正文与参考文件只用技能相对路径，运行命令用 `$HOME/.claude/skills/patent-drafting/`，不含用户名等私有信息；不含个人案件信息与实验数据。
- 唯一含本机路径的 `tools/puppeteer-config.json` 由 setup 生成、已被 `.gitignore` 排除，不入库。

## License

[Apache License 2.0](LICENSE)。
