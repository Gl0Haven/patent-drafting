# 查新与客体适格性自审（patent-drafting · §2 / §4.5）

> 调用方：patent-drafting/SKILL.md。本文件给出 CNIPA 查新与客体适格性自审的流程、工具命令与兜底。
> **路径约定**：下列 `tools/`、`references/` 均相对本技能根目录；运行命令以本机安装位置 `$HOME/.claude/skills/patent-drafting/` 为根（`$HOME` 由系统提供，脱敏不含用户名）。工具/知识均已并入本技能自带，无外部私有路径依赖；环境缺失走兜底并标注来源可靠性。

## §A CNIPA 查新（保新颖性）

执行前先通读查新指引：`references/disclosure-prompts/prior_art_search.md`。

### 工具优先：tools/cnipa_epub_search.py（依赖兄弟模块 cnipa_epub_parse.py / cnipa_epub_crawler.py，已一并自带）

环境：由 `tools/setup_env.sh` 一键装好（playwright+chromium 等），见 SKILL.md 顶部「环境」节；本技能工具一律用 `conda run --no-capture-output -n patent-drafting python ...` 调用。

使用铁律（与 prior_art_search.md 一致）：
- **先归纳 2–8 个相关度高的语义词块**，再生成命令；
- **分多次调用、每次只传一个词块**，不要一次 argv 堆多个；
- 自行按 `pub_number` 合并多轮 `EPUB_HITS_JSON`；
- `abstract` 规定必用——拿到摘要充分理解后再概括，不仅凭标题判断；
- **每个技术方向命中 ≥5 篇**。

调用示例：
```bash
conda run --no-capture-output -n patent-drafting python "$HOME/.claude/skills/patent-drafting/tools/cnipa_epub_search.py" "语义词块"
```

### 兜底：WebSearch / WebFetch

cnipa 环境缺失或异常无果时，用 WebSearch/WebFetch 检索 CNIPA 公布公告、Google Patents、Espacenet 等，抓取后转写；**在结果中标注"兜底来源、可靠性较 cnipa 工具低"**。

### token 控制

主线只保留紧凑命中表：`pub_number / 标题 / 申请人 / 摘要要点`；原文/长 HTML 不落主线。需要深读时交给 §3 的 subagent。

## §B 客体适格性自审（保适格性 / 创造性论证）

并入自 patent-review-skill。**只取起草相关的自审核心**，不跑其四阶段审查员人工节点编排、不动其自我进化引擎/版本管理。

### 第一性原理

专利法第二条第二款：技术方案 = 对要解决的**技术问题**所采取的**技术手段**（利用自然规律、与技术特征功能互撑）构成技术特征，并产生符合自然规律的**技术效果**。三要素缺一则有客体风险。

### 自审项

1. **三要素核验**：逐条确认技术问题、技术手段、技术效果，且手段利用自然规律、与特征功能互撑。
2. **删除测试**：逐个假设删除核心步骤/公式/约束/模块——删后效果仍无差别获得 → 该特征可能装饰性；删后数据流/约束/效果断裂 → 记其协同作用。（与 `references/spec-writing.md` §13.2 同源，统一执行。）
3. **闭环断层检测**：技术问题 → 技术手段 → 技术效果链不得断裂。
4. **数据含义 L1–L5 + 领域关联度 G0–G4 锚定**：AI/算法/数据处理类据此判断是否落入「抽象算法 / 智力活动规则 / 商业方法」等不授权客体，并把数据、特征、指标锚定到真实技术含义与具体技术领域。**层级的具体判定标准读知识库，勿臆造**：
   - `references/knowledge/patent-law-basis.md`
   - `references/knowledge/node-prompts.md`
5. **类案对照**：用案例匹配脚本比对授权/不授权案例，定位本案更接近哪类、差异在哪。

### 类案匹配工具（tools/case_matcher.py，纯标准库、自带案例数据）

```bash
conda run --no-capture-output -n patent-drafting python "$HOME/.claude/skills/patent-drafting/tools/case_matcher.py" --features "特征1,特征2,特征3" --format text
```
案例库：`references/knowledge/case-database.md`、关键词库 `references/knowledge/keyword-libraries.json`。
（脚本/环境缺失时，直接 Read `references/knowledge/case-database.md` + `patent-law-basis.md` 人工比对。）

### 产出与边界

- 产出**内部自审结论**（风险点 + 整改建议），把问题回改进稿；**自审过程不写入说明书/交底书正文**。
- 自审结论只支持其判定条件下的结论，不替代正式审查意见，也不直接等同授权结论。
