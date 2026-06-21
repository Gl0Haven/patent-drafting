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

## 安装为 Claude Code 技能

把本目录放到 `~/.claude/skills/patent-drafting/`，在 Claude Code 中即可触发。装到其他位置时，仅需把命令里的根路径相应调整（技能正文用相对路径，命令用 `$HOME/.claude/skills/patent-drafting/`）。

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

## 开源卫生

- 自包含：查新 / 读料 / 类案 / 交底书产出工具、客体自审知识库、交底书全套 prompt 均已并入，不依赖外部插件路径。
- 已脱敏：正文与参考文件只用技能相对路径，运行命令用 `$HOME/.claude/skills/patent-drafting/`，不含用户名等私有信息；不含个人案件信息与实验数据。
- 唯一含本机路径的 `tools/puppeteer-config.json` 由 setup 生成、已被 `.gitignore` 排除，不入库。

## License

[Apache License 2.0](LICENSE)。
