#!/usr/bin/env python3
"""小六壬掌诀推算"""

PALMS = {
    1: {"name": "大安", "emoji": "🟢", "desc": "大安事事昌，求谋在东方。失物去不远，宅舍保安康。",
        "advice": "适合出行、求财、见贵人。不要太急，稳扎稳打。", "good": True},
    2: {"name": "留连", "emoji": "🟡", "desc": "留连事难成，求谋日不明。官事宜迟缓，去者未回程。",
        "advice": "事有拖延，不要急。先等等看清楚再行动。", "good": False},
    3: {"name": "速喜", "emoji": "🔴", "desc": "速喜喜来临，求财向南行。失物申午见，行人路上寻。",
        "advice": "好事马上到。往南方走走，丢了东西中午前后找。", "good": True},
    4: {"name": "赤口", "emoji": "⚪", "desc": "赤口主口舌，官非切要防。失物急去寻，行人有惊慌。",
        "advice": "小心口舌是非，别跟人吵架。东西丢了赶紧找。", "good": False},
    5: {"name": "小吉", "emoji": "🔵", "desc": "小吉最吉昌，路上好商量。阳人来报喜，失物在坤方。",
        "advice": "路上遇到好事，有人来帮你。适合和人谈事合作。", "good": True},
    6: {"name": "空亡", "emoji": "⚫", "desc": "空亡事不长，阴人多主张。求财无利益，行人有灾殃。",
        "advice": "这事不太靠谱，别抱太大希望。等等再说。", "good": False},
}

HOUR_MAP = {
    "子": 1, "丑": 2, "寅": 3, "卯": 4, "辰": 5, "巳": 6,
    "午": 7, "未": 8, "申": 9, "酉": 10, "戌": 11, "亥": 12,
}

def compute(month: int, day: int, hour_name: str) -> dict:
    """推算小六壬掌诀"""
    if month < 1 or month > 12 or day < 1 or day > 30:
        return {"success": False, "error": "月(1-12)或日(1-30)不合法"}
    if hour_name not in HOUR_MAP:
        return {"success": False, "error": f"时辰必须是: {'/'.join(HOUR_MAP.keys())}"}

    hour = HOUR_MAP[hour_name]

    # 月上起月: 从大安(1)顺数月数次
    step1 = (1 + (month - 1) - 1) % 6 + 1
    step1_name = PALMS[step1]["name"]

    # 月上起日: 从上一步结果顺数日数次
    step2 = (step1 + (day - 1) - 1) % 6 + 1
    step2_name = PALMS[step2]["name"]

    # 日上起时: 从第二步结果顺数时数次
    step3 = (step2 + (hour - 1) - 1) % 6 + 1

    result = PALMS[step3]
    return {
        "success": True,
        "data": {
            "result": result["name"],
            "emoji": result["emoji"],
            "poem": result["desc"],
            "advice": result["advice"],
            "is_good": result["good"],
            "steps": [
                {"action": f"正月起大安 → 顺数{month}个月", "landing": step1_name},
                {"action": f"{step1_name}起初一 → 顺数{day}天", "landing": step2_name},
                {"action": f"{step2_name}起子时 → 顺数{hour}个时辰", "landing": result["name"]},
            ]
        }
    }


if __name__ == "__main__":
    import json
    r = compute(3, 19, "午")
    print(json.dumps(r, ensure_ascii=False, indent=2))
    # 测试边界
    r2 = compute(13, 1, "午")
    print(json.dumps(r2, ensure_ascii=False, indent=2))
