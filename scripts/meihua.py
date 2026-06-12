#!/usr/bin/env python3
"""梅花易数起卦推算"""

GUA = {
    1: {"name": "乾", "symbol": "☰", "wx": "金", "nature": "天"},
    2: {"name": "兑", "symbol": "☱", "wx": "金", "nature": "泽"},
    3: {"name": "离", "symbol": "☲", "wx": "火", "nature": "火"},
    4: {"name": "震", "symbol": "☳", "wx": "木", "nature": "雷"},
    5: {"name": "巽", "symbol": "☴", "wx": "木", "nature": "风"},
    6: {"name": "坎", "symbol": "☵", "wx": "水", "nature": "水"},
    7: {"name": "艮", "symbol": "☶", "wx": "土", "nature": "山"},
    8: {"name": "坤", "symbol": "☷", "wx": "土", "nature": "地"},
}

GUA_MEANING = {
    1: "天，代表刚健、领导、权威、父亲、头",
    2: "泽，代表喜悦、口舌、少女、缺憾",
    3: "火，代表光明、美丽、文书、中女、眼睛",
    4: "雷，代表震动、行动、长子、足、愤怒",
    5: "风，代表进入、传播、长女、不决、股",
    6: "水，代表危险、智慧、中男、耳朵、陷阱",
    7: "山，代表停止、阻碍、少男、手、固执",
    8: "地，代表柔顺、包容、母亲、腹部、大众",
}

def _num_to_gua(n: int) -> int:
    return (n - 1) % 8 + 1

def _num_to_yao(n: int) -> int:
    return (n - 1) % 6 + 1

def compute(method: str, values: dict) -> dict:
    if method == "number":
        nums = values.get("numbers", [])
        if not nums or len(nums) < 2:
            return {"success": False, "error": "至少输入2个数字"}
        upper = _num_to_gua(nums[0])
        lower = _num_to_gua(nums[1])
        moving = _num_to_yao(nums[0] if len(nums) < 3 else nums[2])
    elif method == "time":
        y, m, d, h = values.get("year",1), values.get("month",1), values.get("day",1), values.get("hour",0)
        upper = _num_to_gua(y + m + d)
        lower = _num_to_gua(m + d + h)
        moving = _num_to_yao(y + m + d + h)
    elif method == "text":
        text = values.get("text", "")
        if not text:
            return {"success": False, "error": "请输入文字"}
        strokes = len(text) * 3
        upper = _num_to_gua(strokes)
        lower = _num_to_gua(strokes // 2)
        moving = _num_to_yao(strokes)
    else:
        return {"success": False, "error": f"不支持的方式: {method}"}

    # 动爻变卦
    changed_upper, changed_lower = upper, lower
    if moving <= 3:
        changed_lower = ((changed_lower - 1) ^ 1) % 8 + 1
    else:
        changed_upper = ((changed_upper - 1) ^ 1) % 8 + 1

    # 体用
    if moving <= 3:
        body_gua, use_gua, body_is = upper, lower, "上卦"
    else:
        body_gua, use_gua, body_is = lower, upper, "下卦"

    # 体用生克
    wx_body, wx_use = GUA[body_gua]["wx"], GUA[use_gua]["wx"]
    order_s = {"木":"火","火":"土","土":"金","金":"水","水":"木"}
    order_k = {"木":"土","土":"水","水":"火","火":"金","金":"木"}

    if order_s.get(wx_use) == wx_body:
        relation, emoji, verdict = "用生体", "🟢", "大吉！事情主动来找你，不用费力。"
        detail = f"对方（{wx_use}）主动来帮你（{wx_body}），就像水灌溉树木一样自然。事情顺利，等着好消息就行。"
    elif order_k.get(wx_body) == wx_use:
        relation, emoji, verdict = "体克用", "🟡", "能成，但比较累。"
        detail = f"你（{wx_body}）能克制对方（{wx_use}），像斧头能砍树。但砍完自己也会累。事情能成，但要付出努力。"
    elif order_s.get(wx_body) == wx_use:
        relation, emoji, verdict = "体生用", "🔴", "消耗自己，可能不划算。"
        detail = f"你（{wx_body}）在滋养对方（{wx_use}），像木头在喂火。不管成不成，你都会损耗很多精力或钱财。三思。"
    elif order_k.get(wx_use) == wx_body:
        relation, emoji, verdict = "用克体", "⚫", "凶。这事大概率不成，别硬来。"
        detail = f"对方（{wx_use}）克制你（{wx_body}）。硬碰硬会吃亏。建议暂缓或换方向。"
    else:
        relation, emoji, verdict = "体用比和", "🟢", "大吉！双方和谐，顺风顺水。"
        detail = f"你和对方都是{wx_body}属性，互相理解、配合默契。事情会很顺利。"

    return {
        "success": True,
        "data": {
            "method": method,
            "upper_gua": GUA[upper], "lower_gua": GUA[lower],
            "upper_changed": GUA[changed_upper], "lower_changed": GUA[changed_lower],
            "moving_yao": moving,
            "body_gua": GUA[body_gua], "use_gua": GUA[use_gua], "body_is": body_is,
            "relation": relation, "emoji": emoji, "verdict": verdict, "detail": detail,
            "calc_steps": [
                f"上卦: {GUA[upper]['name']}{GUA[upper]['symbol']}（{GUA[upper]['nature']}）",
                f"下卦: {GUA[lower]['name']}{GUA[lower]['symbol']}（{GUA[lower]['nature']}）",
                f"动爻: 第{moving}爻动 → {body_is}变",
                f"体卦({body_is}): {GUA[body_gua]['name']}{GUA[body_gua]['symbol']} {GUA[body_gua]['wx']}",
                f"用卦: {GUA[use_gua]['name']}{GUA[use_gua]['symbol']} {GUA[use_gua]['wx']}",
                f"生克关系: {wx_body} vs {wx_use} → {relation}",
            ]
        }
    }


if __name__ == "__main__":
    import json
    # 测试数字起卦
    r = compute("number", {"numbers": [37, 5]})
    print(json.dumps(r, ensure_ascii=False, indent=2))
    # 测试边界
    r2 = compute("number", {"numbers": [1]})
    print(json.dumps(r2, ensure_ascii=False, indent=2))
