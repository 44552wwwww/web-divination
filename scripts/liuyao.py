#!/usr/bin/env python3
"""六爻/文王卦推算引擎"""

# 八卦: 阳爻=1, 阴爻=0
TRIGRAMS = {
    "乾": (1,1,1), "兑": (0,1,1), "离": (1,0,1), "震": (0,0,1),
    "巽": (1,1,0), "坎": (0,1,0), "艮": (1,0,0), "坤": (0,0,0),
}
TRIGRAM_NAMES = {"乾":"乾","兑":"兑","离":"离","震":"震","巽":"巽","坎":"坎","艮":"艮","坤":"坤"}

# 六十四卦名 (key用上下卦名)
HEX_MAP = {}
for u_name, u_tri in TRIGRAMS.items():
    for l_name, l_tri in TRIGRAMS.items():
        key = u_name + l_name
        HEX_MAP[key] = f"{u_name}{l_name}"

# 八卦纳支 (从初爻到上爻)
NA_ZHI = {
    "乾": ["子","寅","辰","午","申","戌"],
    "坤": ["未","巳","卯","丑","亥","酉"],
    "震": ["子","寅","辰","午","申","戌"],
    "巽": ["丑","亥","酉","未","巳","卯"],
    "坎": ["寅","辰","午","申","戌","子"],
    "离": ["卯","丑","亥","酉","未","巳"],
    "艮": ["辰","午","申","戌","子","寅"],
    "兑": ["巳","卯","丑","亥","酉","未"],
}

# 地支五行
ZHI_WX = {"子":"水","丑":"土","寅":"木","卯":"木","辰":"土","巳":"火",
          "午":"火","未":"土","申":"金","酉":"金","戌":"土","亥":"水"}

# 八卦五行
GUA_WX = {"乾":"金","兑":"金","离":"火","震":"木","巽":"木","坎":"水","艮":"土","坤":"土"}

# 八宫卦: 每宫8卦的本卦名
GONG_GUA = {
    "乾": ["乾","姤","遁","否","观","剥","晋","大有"],
    "坎": ["坎","节","屯","既济","革","丰","明夷","师"],
    "艮": ["艮","贲","大畜","损","睽","履","中孚","渐"],
    "震": ["震","豫","解","恒","升","井","大过","随"],
    "巽": ["巽","小畜","家人","益","无妄","噬嗑","颐","蛊"],
    "离": ["离","旅","鼎","未济","蒙","涣","讼","同人"],
    "坤": ["坤","复","临","泰","大壮","夬","需","比"],
    "兑": ["兑","困","萃","咸","蹇","谦","小过","归妹"],
}

# 世应位置: [世爻位置, 应爻位置]
SHI_YING_POS = [(5,2),(1,4),(2,5),(3,6),(4,1),(5,2),(6,3),(3,6)]

# 六亲
def _liuqin(gong_wx, zhi):
    """以宫五行为我，支五行为他，定六亲"""
    order_s = {"木":"火","火":"土","土":"金","金":"水","水":"木"}
    order_k = {"木":"土","土":"水","水":"火","火":"金","金":"木"}
    if gong_wx == ZHI_WX[zhi]: return "兄弟"
    if order_s.get(ZHI_WX[zhi]) == gong_wx: return "父母"
    if order_s.get(gong_wx) == ZHI_WX[zhi]: return "子孙"
    if order_k.get(ZHI_WX[zhi]) == gong_wx: return "官鬼"
    if order_k.get(gong_wx) == ZHI_WX[zhi]: return "妻财"
    return "?"

SIX_BEASTS = ["青龙","朱雀","勾陈","螣蛇","白虎","玄武"]

YONG_SHEN = {
    "考试": ("父母","代表文书、成绩、录取"),
    "求财": ("妻财","代表财富、收益、回报"),
    "感情": ("妻财","代表配偶、感情、缘分"),
    "健康": ("官鬼","代表病症、健康问题"),
    "寻人": ("父母","代表消息、庇护、下落"),
    "其他": ("妻财","代表所求之事"),
}

# 八卦序数 (用于定宫)
GUA_XU = {"乾":1,"兑":2,"离":3,"震":4,"巽":5,"坎":6,"艮":7,"坤":8}


def _find_trigram(yao_tuple):
    """三元组找对应卦名"""
    for name, tri in TRIGRAMS.items():
        if tri == yao_tuple: return name
    return None


def _find_gong(hex_name):
    """根据卦名找所属宫和世应位置"""
    for gong_name, gua_list in GONG_GUA.items():
        if hex_name in gua_list:
            idx = gua_list.index(hex_name)
            return gong_name, SHI_YING_POS[idx][0], SHI_YING_POS[idx][1]
    # fallback: 八纯卦
    for gong_name in GONG_GUA:
        if hex_name.startswith(gong_name) and len(hex_name)==2:
            return gong_name, 5, 2
    return "乾", 5, 2


def compute(lines: list, question_type: str, sex: str = "男") -> dict:
    if len(lines) != 6:
        return {"success": False, "error": "需要6次摇卦结果"}
    for l in lines:
        if l not in ("少阳","少阴","老阳","老阴"):
            return {"success": False, "error": f"无效的爻: {l}"}
    if question_type not in YONG_SHEN:
        return {"success": False, "error": f"问事类型不支持: {question_type}"}

    # 1. 排爻
    yao_vals = []
    for line in lines:
        yao_vals.append(1 if line in ("少阳","老阳") else 0)

    # 2. 上下卦
    lower_tri = tuple(yao_vals[:3])
    upper_tri = tuple(yao_vals[3:6])
    lower_name = _find_trigram(lower_tri)
    upper_name = _find_trigram(upper_tri)
    if not lower_name or not upper_name:
        return {"success": False, "error": "无法识别卦象"}

    hex_name = upper_name + lower_name

    # 3. 变卦
    changed_yaos = list(yao_vals)
    moving_lines = []
    for i, line in enumerate(lines):
        if line in ("老阳","老阴"):
            changed_yaos[i] = 1 - changed_yaos[i]
            moving_lines.append(i + 1)

    changed_lower = _find_trigram(tuple(changed_yaos[:3]))
    changed_upper = _find_trigram(tuple(changed_yaos[3:6]))
    changed_name = (changed_upper or upper_name) + (changed_lower or lower_name)

    # 4. 定宫和世应
    gong_name, shi_pos, ying_pos = _find_gong(hex_name)
    gong_wx = GUA_WX[gong_name]

    # 5. 装六亲
    yao_detail = []
    for i in range(6):
        zhi = NA_ZHI[lower_name][i]
        lq = _liuqin(gong_wx, zhi)
        beast = SIX_BEASTS[i % 6]
        is_shi = (i + 1 == shi_pos)
        is_ying = (i + 1 == ying_pos)
        is_moving = (i + 1) in moving_lines
        yao_detail.append({
            "position": i + 1,
            "zhi": zhi,
            "wx": ZHI_WX[zhi],
            "liuqin": lq,
            "beast": beast,
            "is_shi": is_shi,
            "is_ying": is_ying,
            "is_moving": is_moving,
            "line_type": lines[i],
        })

    # 6. 用神
    if question_type == "感情" and sex == "女":
        yong_type = "官鬼"
        yong_desc = "代表丈夫、感情"
    else:
        yong_type, yong_desc = YONG_SHEN[question_type]

    # 找用神
    yong_positions = [d for d in yao_detail if d["liuqin"] == yong_type]
    yong_has_moving = any(d["is_moving"] for d in yong_positions)
    yong_has_shi = any(d["is_shi"] for d in yong_positions)

    # 7. 白话解读
    moving_count = len(moving_lines)
    if moving_count == 0:
        analysis = f"占问{question_type}，用神取{yong_type}（{yong_desc}）。静卦——事情不会有太大变化，顺其自然即可。"
        if yong_has_shi:
            analysis += f"用神持世（就是你自己），说明这事主动权在你手上。"
        else:
            analysis += f"用神不持世，可能需要借力或等待时机。"
    elif moving_count == 1:
        moving_detail = yao_detail[moving_lines[0]-1]
        analysis = f"占问{question_type}，用神取{yong_type}（{yong_desc}）。只有一个动爻（第{moving_lines[0]}爻{moving_detail['liuqin']}动）——事情的关键在于{moving_detail['liuqin']}代表的方面。"
        if yong_has_moving:
            analysis += "动爻就是用神，说明事情正在发生变化，要抓住机会。"
    else:
        analysis = f"占问{question_type}，用神取{yong_type}（{yong_desc}）。有{moving_count}个动爻——事情变化多，比较复杂。建议具体分析每个动爻的影响。"
        if yong_has_moving:
            analysis += "用神动了，说明事情有转机。"

    # 世爻信息
    shi_detail = yao_detail[shi_pos-1]
    analysis += f" 世爻（你）在{shi_pos}爻，{shi_detail['liuqin']}临{shi_detail['beast']}——"
    if shi_detail['liuqin'] == "妻财": analysis += "你目前比较看重实际利益。"
    elif shi_detail['liuqin'] == "官鬼": analysis += "你目前有压力或责任感在身。"
    elif shi_detail['liuqin'] == "父母": analysis += "你目前有学习或文书方面的任务。"
    elif shi_detail['liuqin'] == "子孙": analysis += "你目前心态比较放松。"
    elif shi_detail['liuqin'] == "兄弟": analysis += "你目前在竞争或合作中。"

    return {
        "success": True,
        "data": {
            "hexagram": hex_name,
            "changed_hexagram": changed_name if moving_lines else hex_name,
            "gong_name": gong_name,
            "gong_wx": gong_wx,
            "shi_pos": shi_pos,
            "ying_pos": ying_pos,
            "moving_lines": moving_lines,
            "yong_shen_type": yong_type,
            "yong_shen_desc": yong_desc,
            "question_type": question_type,
            "yao_detail": yao_detail,
            "analysis": analysis,
        }
    }


if __name__ == "__main__":
    import json
    # 测试: 火风鼎
    r = compute(["少阳","少阳","少阳","少阴","少阳","少阳"], "考试", "男")
    print(json.dumps(r, ensure_ascii=False, indent=2, default=str))
    # 测试边界
    r2 = compute(["少阳"], "考试")
    print(json.dumps(r2, ensure_ascii=False, indent=2))
