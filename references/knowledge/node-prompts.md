# 节点Prompt库

本文档包含工作流中所有AI处理节点的Prompt模板。

---

## 阶段一：初步穿透筛查

### 1-1 特征提取与标注

```
## 任务
提取权利要求1的全部技术特征，并进行分类标注。

## 输入
- patent_application: 专利申请文件全文
- claims: 权利要求列表

## 处理要求

1. **完整提取**
   逐一列出权利要求1中的每一个技术特征，包括：
   - 具体技术手段
   - 数据处理步骤
   - 结构描述
   - 方法流程

2. **分类标注**
   对每个特征进行标注：
   - 【技术特征】：利用自然规律解决技术问题的具体措施
   - 【非技术特征】：智力活动规则、数学方法、商业规则
   - 【待定】：特征不明显，需要进一步分析

3. **标注标准**
   - 技术特征：具有物理实现、与硬件耦合、产生技术效果
   - 非技术特征：纯逻辑规则、抽象算法、业务流程
   - 待定：特征描述模糊，需结合上下文判断

## 输出格式
```json
{
  "features": [
    {
      "id": "F1",
      "description": "特征描述",
      "category": "技术特征/非技术特征/待定",
      "confidence": "高/中/低",
      "reasoning": "标注理由"
    }
  ]
}
```
```

### 1-2 名实分离风险识别

```
## 任务
分析技术特征与非技术特征的关联方式，识别"名实分离"风险。

## 输入
- feature_list: 特征提取结果
- claims: 权利要求原文

## 处理要求

1. **关联方式分析**
   识别非技术特征（如算法规则）如何与技术特征（物理实现）关联：
   - 算法作为"运行载体"：方法声称技术，但仅由通用计算机执行
   - 特征叠加无实质交互：技术特征与算法特征简单拼接
   - 问题-手段脱节：声称解决技术问题，但手段是纯算法

2. **风险等级判定**
   - 【高风险】：技术特征仅为算法规则的通用运行载体（如"由计算机执行"）
   - 【中风险】：存在一定技术关联但不够紧密
   - 【低风险】：技术特征与领域深度绑定

3. **关键识别信号**
   以下表述是高风险信号：
   - "由计算机执行"
   - "在处理器上实现"
   - "通过程序代码"
   - "使用算法"
   - "计算得到"

## 输出格式
```json
{
  "risks": [
    {
      "feature_pair": ["特征A", "特征B"],
      "risk_level": "高/中/低",
      "risk_type": "名实分离/关联缺失/其他",
      "description": "风险描述"
    }
  ],
  "overall_risk": "高/中/低"
}
```
```

### 1-3 数据含义初判

```
## 任务
定位核心数据对象，初步判断其L层级。

## 输入
- patent_application: 申请文件
- feature_list: 特征列表

## 处理要求

1. **数据对象定位**
   识别方案中的核心数据：
   - 输入数据：原始观测、用户输入
   - 中间数据：处理结果、特征值
   - 输出数据：预测结果、决策指令

2. **L层级初判**
   - L1-L3（低层次）：原始数据、预处理数据、提取特征
     → 通常不构成技术贡献
   - L4-L5（高层次）：模型输出、决策/控制指令
     → 可能构成技术贡献

3. **判断依据**
   - L1：传感器读数、原始信号、用户输入
   - L2：清洗后的数据、标准化数据
   - L3：统计特征、频域特征、边缘特征
   - L4：分类标签、预测值、聚类结果
   - L5：控制指令、调节参数、设备操作

## 输出格式
```json
{
  "data_objects": [
    {
      "name": "数据名称",
      "type": "输入/中间/输出",
      "level_initial": "L1/L2/L3/L4/L5",
      "physical_unit": "有/无",
      "source": "数据来源"
    }
  ],
  "core_data_summary": "核心数据及L层级汇总"
}
```
```

### 1-4 问题性质初判

```
## 任务
提取背景技术中的问题表述，初步判断问题性质。

## 输入
- patent_application: 申请文件

## 处理要求

1. **问题提取**
   从以下位置提取问题表述：
   - 背景技术
   - 发明内容
   - 权利要求序言
   - 实施例中的问题描述

2. **关键词模式匹配**
   使用预设关键词库进行匹配：

   **算法问题关键词**：
   - 计算复杂度、收敛速度、迭代次数
   - 精度不足、误差大、偏差
   - 特征选择困难、维度灾难

   **商业规则关键词**：
   - 效率低、成本高、管理混乱
   - 用户体验差、转化率低
   - 资源浪费、流程繁琐

   **技术问题关键词**：
   - 噪声干扰、信号衰减
   - 设备故障、性能下降
   - 能耗过高、散热不足

3. **问题性质判定**
   - 算法问题：优化算法本身性能
   - 商业问题：业务流程、管理效率
   - 技术问题：技术领域实际技术问题

## 输出格式
```json
{
  "problem_statements": [
    {
      "source": "问题来源",
      "original_text": "原始表述",
      "keywords_matched": ["匹配的关键词"],
      "problem_nature": "算法问题/商业问题/技术问题",
      "confidence": "高/中/低"
    }
  ],
  "overall_problem_nature": "算法问题/商业问题/技术问题"
}
```
```

### 1-5 风险报告生成

```
## 任务
综合阶段一分析，生成结构化客体风险筛查报告。

## 输入
- feature_list: 特征提取结果
- name_real_separation_risks: 名实分离风险
- data_level_initial: 数据含义初判
- problem_nature: 问题性质初判

## 处理要求

1. **综合风险评估**
   综合四方面分析给出风险等级：
   - 特征标注中高风险特征比例
   - 名实分离风险等级
   - 数据L层级分布
   - 问题性质（算法/商业问题为高风险）

2. **风险点详细说明**
   对每个风险点进行详细描述：
   - 风险位置（具体权利要求/说明书位置）
   - 风险表现
   - 可能的法律后果

3. **结论建议**
   - 低风险：建议通过客体审查
   - 中风险：建议进入深度审查
   - 高风险：强烈建议深度审查

## 输出格式
```json
{
  "report_title": "客体风险筛查报告",
  "risk_level": "低/中/高",
  "risk_summary": "风险概述",
  "risk_points": [
    {
      "id": "R1",
      "location": "位置",
      "type": "风险类型",
      "description": "详细描述",
      "severity": "严重/一般/轻微"
    }
  ],
  "feature_analysis": {
    "total_features": 0,
    "tech_features": 0,
    "non_tech_features": 0,
    "pending_features": 0
  },
  "data_level_distribution": {"L1": 0, "L2": 0, "L3": 0, "L4": 0, "L5": 0},
  "problem_nature_distribution": {"算法问题": 0, "商业问题": 0, "技术问题": 0},
  "recommendation": "建议",
  "next_action": "进入下一阶段/结案"
}
```
```

---

## 阶段二：深度穿透审查

### 2-1 技术问题穿透-删除测试

```
## 任务
执行删除测试，判断问题的本质是算法/商业问题还是技术问题。

## 输入
- screening_report: 阶段一筛查报告
- patent_application: 申请文件全文

## 处理要求

1. **删除测试执行**
   对每个关键技术特征执行删除测试：
   - 模拟删除该特征
   - 观察方案的逻辑内核是否依然完整
   - 判断问题是否仍然存在

2. **问题本质判断**
   - 若删除技术特征后问题消失 → 问题本质是技术问题
   - 若删除技术特征后问题依然存在 → 问题可能是算法/商业问题
   - 若删除非技术特征后问题消失 → 该特征可能是必要技术特征

3. **关键问题识别**
   特别关注：
   - "由计算机执行"类特征删除后方案是否依然成立
   - 算法优化与领域问题的对应关系
   - 商业效率与技术效果的区分

## 输出格式
```json
{
  "deletion_tests": [
    {
      "deleted_feature": "被删除特征",
      "result_after_deletion": "删除后方案状态",
      "problem_still_exists": true/false,
      "problem_essence": "技术问题/算法问题/商业问题",
      "conclusion": "结论"
    }
  ],
  "problem_essence_analysis": {
    "primary_problem_type": "技术问题/算法问题/商业问题",
    "supporting_evidence": "支持证据",
    "confidence": "高/中/低"
  }
}
```
```

### 2-2 技术手段穿透-特定关联检索

```
## 任务
全量检索"特定技术关联"信号。

## 输入
- patent_application: 申请文件全文

## 处理要求

1. **关联信号检索**
   在申请文件中检索以下模式：

   **强绑定信号**（支持客体）：
   - "根据……内存容量……调整"
   - "针对……图像特性……设计"
   - "利用……传感器类型……优化"
   - "结合……信道特性……处理"
   - "适应……硬件架构……实现"

   **弱绑定信号**（不支持客体）：
   - "通过计算机实现"
   - "利用处理器执行"
   - "采用通用算法"
   - "基于云端处理"

2. **关联程度评估**
   - 高：算法与具体物理特性深度耦合
   - 中：算法考虑了某些领域特性
   - 低：算法基本独立于具体领域

3. **证据提取**
   列出每个关联信号的：
   - 具体位置（权利要求/说明书）
   - 原始表述
   - 关联类型

## 输出格式
```json
{
  "correlation_signals": [
    {
      "location": "位置",
      "original_text": "原始表述",
      "signal_type": "强绑定/弱绑定",
      "signal_keyword": "关键词",
      "evidence_strength": "高/中/低"
    }
  ],
  "overall_correlation": {
    "level": "高/中/低",
    "tech_correlation_exists": true/false,
    "key_evidence": "关键证据"
  }
}
```
```

### 2-3 技术效果穿透-指标匹配

```
## 任务
提取实验数据中的性能指标，与效果指标库进行匹配。

## 输入
- patent_application: 申请文件全文

## 处理要求

1. **效果指标提取**
   识别申请中声称的技术效果：
   - 性能指标数值
   - 改善程度
   - 对比数据

2. **指标库匹配**
   使用预设指标库进行匹配：

   **算法效果指标库**（非技术效果）：
   - 准确率(Accuracy)、精确率(Precision)、召回率(Recall)
   - F1值、AUC、ROC
   - 收敛速度、迭代次数
   - 训练时间、推理时间

   **技术效果指标库**（技术效果）：
   - 功耗、能耗、发热量
   - 时延、响应时间、处理速度
   - 信噪比、误码率、传输距离
   - 温度、压力、湿度精度
   - 设备寿命、故障率

3. **效果性质判断**
   - 匹配算法指标 → 非技术效果
   - 匹配技术指标 → 技术效果
   - 两者都有 → 需进一步分析

## 输出格式
```json
{
  "claimed_effects": [
    {
      "effect_description": "效果描述",
      "metric_value": "指标数值",
      "matched_algorithm_indicators": ["匹配的算法指标"],
      "matched_tech_indicators": ["匹配的技术指标"],
      "effect_type": "技术效果/算法效果/混合"
    }
  ],
  "effect_type_distribution": {
    "tech_effects": 0,
    "algo_effects": 0,
    "mixed_effects": 0
  },
  "overall_effect_nature": "技术主导/算法主导/混合"
}
```
```

### 2-4 闭环断层检测

```
## 任务
生成三要素关联图，检测技术性断层。

## 输入
- deletion_test_result: 删除测试结果
- tech_correlation_signals: 技术关联信号
- effect_indicators: 效果指标

## 处理要求

1. **三要素关联图生成**
   构建"问题-手段-效果"关联图：
   - 问题节点
   - 手段节点
   - 效果节点
   - 节点间关联线

2. **断层检测**
   检测以下断层类型：
   - 【问题-手段断层】：声称解决A问题，但手段解决的是B问题
   - 【手段-效果断层】：手段是算法优化，效果却声称是物理量提升
   - 【效果-问题断层】：效果改善不能解决声称的问题

3. **典型断层模式**
   - 算法优化 → 物理效果（断层）
   - 业务效率 → 技术性能（断层）
   - 数据处理 → 设备改善（断层）

## 输出格式
```json
{
  "triple_element_graph": {
    "problem_nodes": ["问题节点"],
    "method_nodes": ["手段节点"],
    "effect_nodes": ["效果节点"],
    "connections": [
      {"from": "节点A", "to": "节点B", "type": "关联类型"}
    ]
  },
  "loop_breaks": [
    {
      "break_type": "问题-手段/手段-效果/效果-问题",
      "description": "断层描述",
      "severity": "严重/一般/轻微",
      "example": "具体案例"
    }
  ],
  "loop_integrity": "完整/存在断层"
}
```
```

### 2-5 三要素报告生成

```
## 任务
综合深度分析，生成三要素实质分析报告。

## 输入
- deletion_test_result: 删除测试结果
- tech_correlation_signals: 技术关联信号
- effect_type: 效果性质
- loop_break_points: 断层点

## 处理要求

1. **三要素技术属性判定**
   - 技术手段：是否利用自然规律，是否具有技术性
   - 技术问题：是否技术领域问题，是否可技术手段解决
   - 技术效果：是否基于自然规律，是否可测量验证

2. **综合研判**
   - 三要素均具备 → 具备技术属性
   - 任一不具备 → 不具备技术属性

3. **疑点清单**
   列出所有需要审查员确认的疑点

## 输出格式
```json
{
  "report_title": "三要素实质分析报告",
  "element_analysis": {
    "technical_method": {
      "conclusion": "具备/不具备",
      "evidence": ["证据"],
      "doubt_points": ["疑点"]
    },
    "technical_problem": {
      "conclusion": "具备/不具备",
      "evidence": ["证据"],
      "doubt_points": ["疑点"]
    },
    "technical_effect": {
      "conclusion": "具备/不具备",
      "evidence": ["证据"],
      "doubt_points": ["疑点"]
    }
  },
  "comprehensive_judgment": {
    "element_tech_attr": true/false,
    "confidence": "高/中/低",
    "reasoning": "综合理由"
  },
  "doubt_points_for_reviewer": [
    {
      "point": "疑点描述",
      "requires_confirmation": true/false
    }
  ]
}
```
```

---

## 阶段三：锚定穿透验证

### 3-1 数据含义量化

```
## 任务
精确判断数据的L1-L5层次。

## 输入
- triple_element_report: 三要素报告

## 处理要求

1. **数据对象枚举**
   列出方案中所有数据对象：
   - 名称
   - 类型（输入/中间/输出）
   - 物理单位（有无）
   - 明确来源

2. **L层级精确判断**
   - L1：有物理单位、来自物理测量
   - L2：经过清洗但保留原始含义
   - L3：提取的统计/频域特征
   - L4：模型输出的预测/分类结果
   - L5：控制指令、调节参数

3. **判断依据**
   逐项检查：
   - 是否具有物理单位
   - 是否明确对应物理量
   - 是否具有技术领域含义
   - 是否可作用于外部环境

## 输出格式
```json
{
  "data_quantification": [
    {
      "data_name": "数据名称",
      "level": "L1/L2/L3/L4/L5",
      "has_physical_unit": true/false,
      "has_clear_source": true/false,
      "has_tech_domain_meaning": true/false,
      "quantification_evidence": ["判断依据"]
    }
  ],
  "level_distribution": {"L1": 0, "L2": 0, "L3": 0, "L4": 0, "L5": 0},
  "dominant_level": "L层级"
}
```
```

### 3-2 关联度量化

```
## 任务
判断算法与领域关联强度G0-G4。

## 输入
- triple_element_report: 三要素报告
- tech_correlation_signals: 技术关联信号

## 处理要求

1. **G层级判断标准**
   - G0：完全领域无关，纯数学/逻辑
   - G1：跨领域通用，如通用优化算法
   - G2：技术领域通用，如图像处理通用方法
   - G3：特定应用领域，如医疗影像诊断
   - G4：具体产品/场景，如某型号设备故障诊断

2. **判断依据**
   - 算法是否因应领域特性进行适应性设计
   - 算法是否与具体硬件/物理环境绑定
   - 算法输出是否直接作用于特定技术系统

3. **证据提取**
   列出支持关联度判断的证据

## 输出格式
```json
{
  "correlation_quantification": {
    "domain_correlation": "G0/G1/G2/G3/G4",
    "evidence": ["证据"],
    "reasoning": "判断理由"
  },
  "adaptation_features": [
    {
      "feature": "适应性设计",
      "evidence": "证据"
    }
  ],
  "overall_association": "领域无关/弱关联/中等关联/强关联/极强关联"
}
```
```

### 3-3 综合矩阵判断

```
## 任务
执行L×G组合矩阵判断。

## 输入
- data_level_quantified: 数据含义量化结果
- domain_correlation_quantified: 关联度量化结果

## 处理要求

1. **组合矩阵**
   | 组合 | 技术可能性 |
   |------|------------|
   | L4-L5 × G3-G4 | 强烈支持客体 |
   | L4-L5 × G2 | 支持客体 |
   | L3 × G3-G4 | 支持客体 |
   | L3 × G2 | 需分析 |
   | L1-L3 × G0-G1 | 排除 |

2. **锚定判断**
   - L4且G3 → 锚定成功
   - L3且G2 → 锚定失败
   - 其他组合 → 存疑

3. **结果输出**
   给出明确的锚定提示

## 输出格式
```json
{
  "combination": {
    "L_level": "L层级",
    "G_level": "G层级",
    "matrix_position": "矩阵位置"
  },
  "matrix_result": {
    "technical_possibility": "排除/需分析/支持/强烈支持",
    "anchor_hint": "成功/失败/存疑",
    "reasoning": "判断理由"
  }
}
```
```

### 3-4 验证报告生成

```
## 任务
生成锚定穿透验证报告。

## 输入
- data_level_quantified: 数据含义量化
- domain_correlation_quantified: 关联度量化
- matrix_result: 矩阵判断结果

## 处理要求

1. **报告结构**
   - L层级定位及依据
   - G层级定位及依据
   - L×G组合判断
   - 锚定成功/失败/存疑

2. **详细说明**
   对每个判断点提供详细说明和证据

3. **结论**
   给出锚定结果和理由

## 输出格式
```json
{
  "report_title": "锚定穿透验证报告",
  "L_level_analysis": {
    "dominant_level": "L层级",
    "evidence": ["证据"],
    "confidence": "高/中/低"
  },
  "G_level_analysis": {
    "domain_correlation": "G层级",
    "evidence": ["证据"],
    "confidence": "高/中/低"
  },
  "combination_analysis": {
    "L": "L层级",
    "G": "G层级",
    "matrix_position": "矩阵位置",
    "technical_possibility": "技术可能性"
  },
  "anchor_result": {
    "result": "成功/失败/存疑",
    "reasoning": "理由",
    "confidence": "高/中/低"
  },
  "recommendation": "建议"
}
```
```

---

## 阶段四：案例穿透与结论生成

### 4-1 类案匹配

```
## 任务
与知识库案例进行语义相似度计算。

## 输入
- triple_element_report: 三要素报告
- verification_report: 锚定验证报告

## 处理要求

1. **特征提取**
   提取用于匹配的方案特征：
   - 技术领域
   - 问题类型
   - 手段类型
   - 效果类型
   - L/G层级

2. **案例库检索**
   在正反案例库中检索相似案例：
   - 正向案例（客体合格）
   - 反向案例（客体不合格）
   - 边界案例（需具体分析）

3. **相似度计算**
   基于以下维度计算相似度：
   - 问题相似度
   - 手段相似度
   - 效果相似度
   - L/G组合相似度

## 输出格式
```json
{
  "positive_cases": [
    {
      "case_id": "案例ID",
      "case_name": "案例名称",
      "features": ["特征"],
      "conclusion": "结论",
      "similarity_scores": {
        "problem": 0.0,
        "method": 0.0,
        "effect": 0.0,
        "overall": 0.0
      }
    }
  ],
  "negative_cases": [
    {
      "case_id": "案例ID",
      "case_name": "案例名称",
      "features": ["特征"],
      "conclusion": "结论",
      "similarity_scores": {
        "problem": 0.0,
        "method": 0.0,
        "effect": 0.0,
        "overall": 0.0
      }
    }
  ],
  "boundary_cases": [],
  "most_similar_positive": "案例ID",
  "most_similar_negative": "案例ID"
}
```
```

### 4-2 比对分析

```
## 任务
生成五维度比对表。

## 输入
- similar_cases: 相似案例
- triple_element_report: 三要素报告
- verification_report: 锚定验证报告

## 处理要求

1. **五维度分析**
   - 问题维度：问题的性质和表述
   - 手段维度：技术手段的类型和特征
   - 效果维度：声称的技术效果
   - 数据维度：数据L层级
   - 关联维度：领域关联G层级

2. **对比表生成**
   | 维度 | 本案 | 参照案例 | 对比结论 |
   |------|------|----------|----------|
   | 问题 | ... | ... | ... |
   | 手段 | ... | ... | ... |

3. **差异分析**
   识别本案与参照案例的关键差异点

## 输出格式
```json
{
  "comparison_table": [
    {
      "dimension": "维度",
      "current_case": "本案情况",
      "reference_case": "参照案例",
      "comparison_conclusion": "对比结论",
      "key_difference": "关键差异"
    }
  ],
  "overall_similarity": {
    "positive_case": 0.0,
    "negative_case": 0.0,
    "closer_to": "正向/反向"
  }
}
```
```

### 4-3 意见生成

```
## 任务
生成格式完整的审查意见通知书初稿。

## 输入
- comparison_table: 比对分析表
- triple_element_report: 三要素报告
- verification_report: 锚定验证报告
- similar_cases: 相似案例

## 处理要求

1. **通知书结构**
   一、申请概述
   二、审查过程
   三、技术方案分析
   四、三要素审查
   五、锚定验证
   六、案例比对
   七、结论与建议

2. **内容要求**
   - 完整引用分析报告内容
   - 客观陈述技术方案
   - 清晰说明审查理由
   - 提供明确的审查结论

3. **结论类型**
   - 授权：客体合格，建议授权
   - 不授权：客体不合格，不建议授权
   - 补正：需进一步说明或修改

## 输出格式
```json
{
  "opinion_title": "发明专利客体适格性审查意见",
  "sections": {
    "application_overview": "申请概述",
    "review_process": "审查过程",
    "technical_analysis": "技术方案分析",
    "triple_element_review": "三要素审查",
    "anchor_verification": "锚定验证",
    "case_comparison": "案例比对",
    "conclusion": "结论与建议"
  },
  "final_decision": "授权/不授权/待定",
  "reasoning": "理由"
}
```
```

---

## 节点类型说明

| 类型 | 标识 | 说明 |
|------|------|------|
| AI处理节点 | `ai_process` | 执行大模型任务 |
| 人工干预节点 | `human_review` | 审查员操作 |

## Prompt使用指南

1. **调用方式**：在AI节点中引用 `prompt_ref`
2. **输入准备**：确保所有输入变量已正确传入
3. **输出解析**：按照指定的JSON格式解析输出
4. **异常处理**：输出格式不符时，提示重新生成
