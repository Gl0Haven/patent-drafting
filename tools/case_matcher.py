#!/usr/bin/env python3
"""
案例匹配脚本
根据技术特征从权威案例库中检索相似案例
"""

import argparse
import json
import sys
import os

# 案例库（基于《专利审查指南》2024官方示例）
POSITIVE_CASES = [
    {
        "id": "CASE-P-001",
        "name": "深度神经网络模型的训练方法",
        "source": "审查指南示例5",
        "decision": "授权",
        "key_features": [
            "深度学习", "训练方法", "硬件内部结构", "单处理器", "多处理器",
            "训练速度", "硬件执行效果", "算法与硬件关联"
        ],
        "tech_attributes": {
            "tech_means": "算法与计算机系统内部结构存在特定技术关联",
            "tech_problem": "解决训练速度慢的问题",
            "tech_effect": "提升模型训练过程中硬件的执行效果"
        },
        "l_level": "L4",
        "g_level": "G3",
        "anchor_result": "成功"
    },
    {
        "id": "CASE-P-002",
        "name": "电子券使用倾向度的分析方法",
        "source": "审查指南示例6",
        "decision": "授权",
        "key_features": [
            "大数据处理", "电子券", "用户行为", "分类", "聚类",
            "模型训练", "内在关联关系", "自然规律", "分析精确性"
        ],
        "tech_attributes": {
            "tech_means": "分类、聚类等算法处理具体应用领域数据",
            "tech_problem": "提升分析用户对电子券使用倾向度的精确性",
            "tech_effect": "挖掘的内在关联关系符合自然规律"
        },
        "l_level": "L4",
        "g_level": "G3",
        "anchor_result": "成功"
    },
    {
        "id": "CASE-P-003",
        "name": "知识图谱推理方法",
        "source": "审查指南示例7",
        "decision": "授权",
        "key_features": [
            "知识图谱", "自然语言处理", "文本数据", "实体识别",
            "关系抽取", "语义搜索", "推理准确性"
        ],
        "tech_attributes": {
            "tech_means": "实体识别、关系抽取等自然语言处理技术",
            "tech_problem": "丰富语义信息和提高推理准确性",
            "tech_effect": "文本嵌入及语义搜索效果提升"
        },
        "l_level": "L4",
        "g_level": "G3",
        "anchor_result": "成功"
    },
    {
        "id": "CASE-P-004",
        "name": "去除图像噪声的方法",
        "source": "审查指南撰写示例",
        "decision": "授权",
        "key_features": [
            "图像处理", "信号处理", "噪声去除", "图像质量",
            "滤波器", "技术效果"
        ],
        "tech_attributes": {
            "tech_means": "滤波器设计、信号处理等技术手段",
            "tech_problem": "去除图像中的噪声",
            "tech_effect": "图像质量提升，符合自然规律"
        },
        "l_level": "L3",
        "g_level": "G3",
        "anchor_result": "成功"
    },
    {
        "id": "CASE-P-005",
        "name": "物流配送方法",
        "source": "审查指南示例13",
        "decision": "授权",
        "key_features": [
            "物流配送", "数据架构", "通信方式", "用户体验",
            "批量通知", "操作便利", "技术特征关联"
        ],
        "tech_attributes": {
            "tech_means": "数据架构和通信方式的调整",
            "tech_problem": "提升配送效率和用户体验",
            "tech_effect": "用户体验提升与技术特征相关"
        },
        "l_level": "L4",
        "g_level": "G3",
        "anchor_result": "成功"
    },
    {
        "id": "CASE-P-006",
        "name": "用于适配神经网络参数的方法",
        "source": "审查指南示例15",
        "decision": "授权",
        "key_features": [
            "神经网络参数", "权重参数", "硬件使用率", "硬件运算效率",
            "算法与硬件关联", "数据尺寸填充"
        ],
        "tech_attributes": {
            "tech_means": "权重参数尺寸填充算法",
            "tech_problem": "提升硬件运算效率",
            "tech_effect": "硬件高效处理数据"
        },
        "l_level": "L4",
        "g_level": "G3",
        "anchor_result": "成功"
    }
]

NEGATIVE_CASES = [
    {
        "id": "CASE-N-001",
        "name": "金融产品价格预测方法",
        "source": "审查指南示例10",
        "decision": "不授权",
        "key_features": [
            "金融产品", "价格预测", "神经网络", "历史价格",
            "未来价格", "经济学规律", "无自然规律关联"
        ],
        "tech_attributes": {
            "tech_means": "神经网络模型（通用算法）",
            "tech_problem": "如何预测金融产品价格（非技术问题）",
            "tech_effect": "历史价格不能决定未来价格走势"
        },
        "l_level": "L4",
        "g_level": "G1",
        "anchor_result": "失败"
    },
    {
        "id": "CASE-N-002",
        "name": "抽象算法（不涉及任何技术领域）",
        "source": "审查指南",
        "decision": "不授权",
        "key_features": [
            "抽象算法", "数学模型", "纯算法", "无技术领域",
            "智力活动规则"
        ],
        "tech_attributes": {
            "tech_means": "无技术手段",
            "tech_problem": "无技术问题",
            "tech_effect": "无技术效果"
        },
        "l_level": "L1",
        "g_level": "G0",
        "anchor_result": "失败"
    },
    {
        "id": "CASE-N-003",
        "name": "游戏规则/玩法",
        "source": "审查实践",
        "decision": "不授权",
        "key_features": [
            "游戏规则", "玩法设计", "竞赛评分", "娱乐",
            "主观性", "非技术问题"
        ],
        "tech_attributes": {
            "tech_means": "无技术手段",
            "tech_problem": "不解决技术问题",
            "tech_effect": "不产生技术效果"
        },
        "l_level": "L1",
        "g_level": "G0",
        "anchor_result": "失败"
    },
    {
        "id": "CASE-N-004",
        "name": "商业返利规则",
        "source": "审查指南",
        "decision": "不授权",
        "key_features": [
            "返利规则", "消费额度", "商业规则", "营销策略",
            "无技术特征"
        ],
        "tech_attributes": {
            "tech_means": "商业规则方法",
            "tech_problem": "商业问题",
            "tech_effect": "商业效果"
        },
        "l_level": "L1",
        "g_level": "G0",
        "anchor_result": "失败"
    }
]

def calculate_similarity(input_features, case_features):
    """计算特征相似度"""
    if not input_features or not case_features:
        return 0.0
    
    input_set = set(f.lower() for f in input_features)
    case_set = set(f.lower() for f in case_features)
    
    # Jaccard相似度
    intersection = len(input_set & case_set)
    union = len(input_set | case_set)
    
    return intersection / union if union > 0 else 0.0

def match_cases(input_features, max_results=3):
    """匹配相似案例"""
    all_cases = []
    
    for case in POSITIVE_CASES:
        similarity = calculate_similarity(input_features, case["key_features"])
        all_cases.append({
            **case,
            "similarity": similarity,
            "case_type": "positive"
        })
    
    for case in NEGATIVE_CASES:
        similarity = calculate_similarity(input_features, case["key_features"])
        all_cases.append({
            **case,
            "similarity": similarity,
            "case_type": "negative"
        })
    
    # 按相似度排序
    all_cases.sort(key=lambda x: x["similarity"], reverse=True)
    
    positive_results = [c for c in all_cases if c["case_type"] == "positive"][:max_results]
    negative_results = [c for c in all_cases if c["case_type"] == "negative"][:max_results]
    
    return {
        "positive_cases": positive_results,
        "negative_cases": negative_results
    }

def main():
    parser = argparse.ArgumentParser(description="专利客体适格性案例匹配")
    parser.add_argument("--features", type=str, required=True,
                        help="逗号分隔的技术特征列表")
    parser.add_argument("--format", type=str, default="text",
                        choices=["text", "json"],
                        help="输出格式")
    
    args = parser.parse_args()
    
    # 解析输入特征
    input_features = [f.strip() for f in args.features.split(",")]
    
    # 执行匹配
    result = match_cases(input_features)
    
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("=" * 60)
        print("相似正向案例（授权）")
        print("=" * 60)
        for i, case in enumerate(result["positive_cases"], 1):
            print(f"\n{i}. {case['name']} (相似度: {case['similarity']:.2%})")
            print(f"   来源: {case['source']}")
            print(f"   关键特征: {', '.join(case['key_features'][:5])}...")
            print(f"   L层: {case['l_level']}, G层: {case['g_level']}, 锚定: {case['anchor_result']}")
        
        print("\n" + "=" * 60)
        print("相似反向案例（不授权）")
        print("=" * 60)
        for i, case in enumerate(result["negative_cases"], 1):
            print(f"\n{i}. {case['name']} (相似度: {case['similarity']:.2%})")
            print(f"   来源: {case['source']}")
            print(f"   关键特征: {', '.join(case['key_features'][:5])}...")
            print(f"   不授权理由: {case['tech_attributes']['tech_problem']}")

if __name__ == "__main__":
    main()
