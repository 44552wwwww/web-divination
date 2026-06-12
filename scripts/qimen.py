#!/usr/bin/env python3
"""奇门遁甲时家排盘"""

# 二十四节气 → 阴阳遁局数 [冬至起阳遁, 夏至起阴遁]
DUN_TABLE = {
    "冬至": [1,7,4], "小寒": [2,8,5], "大寒": [3,9,6],
    "立春": [8,5,2], "雨水": [9,6,3], "惊蛰": [1,7,4],
    "春分": [3,9,6], "清明": [4,1,7], "谷雨": [5,2,8],
    "立夏": [4,1,7], "小满": [5,2,8], "芒种": [6,3,9],
    "夏至": [9,3,6], "小暑": [8,2,5], "大暑": [7,1,4],
    "立秋": [2,5,8], "处暑": [1,4,7], "白露": [9,3,6],
    "秋分": [7,1,4], "寒露": [6,9,3], "霜降": [5,8,2],
    "立冬": [6,9,3], "小雪": [5,8,2], "大雪": [4,7,1],
}

# 三奇六仪顺序 (阳遁顺排, 阴遁逆排)
QI_YI = ["戊","己","庚","辛","壬","癸","丁","丙","乙"]

# 九宫八卦
GONG_GUA = {1:"坎",8:"艮",3:"震",4:"巽",9:"离",2:"坤",7:"兑",6:"乾"}

# 八门 (原始宫位: 休1生8伤3杜4景9死2惊7开6)
MEN_YUAN_GONG = {"休":1,"生":8,"伤":3,"杜":4,"景":9,"死":2,"惊":7,"开":6}

# 九星 (原始宫位)
XING_YUAN_GONG = {"蓬":1,"任":8,"冲":3,"辅":4,"英":9,"芮":2,"柱":7,"心":6}

# 八神 (阳遁顺排)
SHEN_YANG = ["值符","螣蛇","太阴","六合","白虎","玄武","九地","九天"]
SHEN_YIN  = ["值符","螣蛇","太阴","六合","白虎","玄武","九地","九天"]  # 阴遁同顺排

# 用神表
YONG_SHEN = {
    "考试": (["丁","景门"], "丁奇主文书，景门主文章考试"),
    "开业": (["开"], "开门主开创、开始、开业"),
    "出行": (["生"], "生门主生机、出行平安"),
    "求职": (["开"], "开门主工作、机会"),
    "谈判": (["惊"], "惊门主口舌、谈判辩论"),
    "求财": (["戊","生"], "戊为资本，生门为财源"),
    "搬家": (["生"], "生门主安居"),
}

# 十干
TIAN_GAN = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
DI_ZHI = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]

# 旬首表 (六甲遁)
XUN_SHOU = {
    "甲子":"戊","甲戌":"己","甲申":"庚","甲午":"辛","甲辰":"壬","甲寅":"癸"
}

# 日上起时干 (五鼠遁)
def _shi_gan(ri_gan, shi_zhi):
    start = {"甲":0,"己":0,"乙":2,"庚":2,"丙":4,"辛":4,"丁":6,"壬":6,"戊":8,"癸":8}
    return TIAN_GAN[(start[ri_gan] + DI_ZHI.index(shi_zhi)) % 10]

# 节气计算 (简化: 每月两个节气)
def _get_jieqi(year):
    """返回 (节气名, 阴阳遁, 元)"""
    # 简化: 按月份近似
    from datetime import date
    # 使用简单日期映射
    jieqi_dates = [
        (date(year,1,6), "小寒"), (date(year,1,21), "大寒"),
        (date(year,2,4), "立春"), (date(year,2,19), "雨水"),
        (date(year,3,6), "惊蛰"), (date(year,3,21), "春分"),
        (date(year,4,5), "清明"), (date(year,4,20), "谷雨"),
        (date(year,5,6), "立夏"), (date(year,5,21), "小满"),
        (date(year,6,6), "芒种"), (date(year,6,21), "夏至"),
        (date(year,7,7), "小暑"), (date(year,7,23), "大暑"),
        (date(year,8,7), "立秋"), (date(year,8,23), "处暑"),
        (date(year,9,8), "白露"), (date(year,9,23), "秋分"),
        (date(year,10,8), "寒露"), (date(year,10,23), "霜降"),
        (date(year,11,7), "立冬"), (date(year,11,22), "小雪"),
        (date(year,12,7), "大雪"), (date(year,12,22), "冬至"),
    ]
    return jieqi_dates

def _get_dun(year, month, day):
    """根据日期定阴阳遁和局数"""
    from datetime import date
    d = date(year, month, day)
    jieqi_dates = _get_jieqi(year)
    # 找当前所处的节气
    current_jieqi = "冬至"
    for jd, jn in jieqi_dates:
        if d >= jd:
            current_jieqi = jn
    # 阴阳遁: 冬至到夏至前=阳遁, 夏至到冬至前=阴遁
    yang_dun_jieqi = ["冬至","小寒","大寒","立春","雨水","惊蛰","春分","清明","谷雨","立夏","小满","芒种"]
    is_yang = current_jieqi in yang_dun_jieqi
    # 上中下元 (简化: 按日期三元)
    day_of_jieqi = (d - next(jd for jd,jn in jieqi_dates if jn==current_jieqi)).days
    if day_of_jieqi < 5: yuan = 0  # 上元
    elif day_of_jieqi < 10: yuan = 1  # 中元
    else: yuan = 2  # 下元
    dun_num = DUN_TABLE.get(current_jieqi, [1,7,4])[yuan]
    return dun_num, is_yang

def _day_ganzhi(d):
    """公历日期 → 日干支"""
    idx = ((d - __import__('datetime').date(1900,1,1)).days + 10) % 60
    return TIAN_GAN[idx%10], DI_ZHI[idx%12]

def compute(year, month, day, hour, q_type):
    from datetime import date
    d = date(year, month, day)

    # 1. 定时柱
    shi_zhi = DI_ZHI[((hour+1)//2)%12]
    ri_gan, ri_zhi = _day_ganzhi(d)
    shi_gan = _shi_gan(ri_gan, shi_zhi)
    shi_gz = shi_gan + shi_zhi

    # 2. 定局
    dun_num, is_yang = _get_dun(year, month, day)
    dun_type = "阳遁" if is_yang else "阴遁"

    # 3. 排地盘三奇六仪
    di_pan = {}
    if is_yang:
        gong_order = [1,2,3,4,5,6,7,8,9]  # 阳遁顺排
        start_gong = dun_num
    else:
        gong_order = [1,9,8,7,6,5,4,3,2]  # 阴遁逆排
        start_gong = dun_num

    start_idx = gong_order.index(start_gong)
    for i in range(9):
        gong = gong_order[(start_idx + i) % 9]
        di_pan[gong] = QI_YI[i]

    # 4. 找旬首→值符值使
    xun_shou_gan = None
    xun_shou_zhi = None
    for xun_key, xun_val in XUN_SHOU.items():
        xun_gan = xun_key[0]
        xun_zhi = xun_key[1]
        gan_idx = TIAN_GAN.index(shi_gan)
        xun_gan_idx = TIAN_GAN.index(xun_gan)
        zhi_idx = DI_ZHI.index(shi_zhi)
        xun_zhi_idx = DI_ZHI.index(xun_zhi)
        # 简化: 找时柱所在的旬
        if (gan_idx - xun_gan_idx) % 10 < 5 and (zhi_idx - xun_zhi_idx) % 12 < 6:
            xun_shou_gan = xun_val
            xun_shou_zhi = xun_key[2:]
            break

    if not xun_shou_gan:
        xun_shou_gan = "戊"
        xun_shou_zhi = "子"

    # 找值符星和值使门
    zhi_fu_xing = None
    zhi_shi_men = None
    zhi_fu_gong = None
    for gong, qi in di_pan.items():
        if qi == xun_shou_gan:
            zhi_fu_gong = gong
            for xing, xing_gong in XING_YUAN_GONG.items():
                if xing_gong == gong:
                    zhi_fu_xing = xing
            for men, men_gong in MEN_YUAN_GONG.items():
                if men_gong == gong:
                    zhi_shi_men = men
            break

    if not zhi_fu_gong:
        zhi_fu_gong = 1
        zhi_fu_xing = "蓬"
        zhi_shi_men = "休"

    # 5. 排天盘九星 (值符随时干落宫)
    shi_gan_gong = None
    for gong, qi in di_pan.items():
        if qi == shi_gan:
            shi_gan_gong = gong
            break
    if not shi_gan_gong:
        shi_gan_gong = dun_num

    tian_pan_xing = {}
    zhi_fu_offset = (shi_gan_gong - zhi_fu_gong) % 9
    for xing, yuan_gong in XING_YUAN_GONG.items():
        new_gong = yuan_gong + zhi_fu_offset
        if new_gong > 9: new_gong -= 9
        elif new_gong < 1: new_gong += 9
        tian_pan_xing[new_gong] = xing

    # 6. 排人盘八门 (值使随时支)
    shi_zhi_idx = DI_ZHI.index(shi_zhi)
    xun_zhi_idx = DI_ZHI.index(xun_shou_zhi) if xun_shou_zhi in DI_ZHI else 0
    men_offset = shi_zhi_idx - xun_zhi_idx
    if men_offset < 0: men_offset += 12

    ren_pan_men = {}
    zhi_shi_yuan_gong = MEN_YUAN_GONG.get(zhi_shi_men, 1)
    for men, yuan_gong in MEN_YUAN_GONG.items():
        # 每个时辰门移动
        rel_offset = (yuan_gong - zhi_shi_yuan_gong) % 9
        new_gong = zhi_fu_gong + men_offset + rel_offset
        while new_gong > 9: new_gong -= 9
        while new_gong < 1: new_gong += 9
        ren_pan_men[new_gong] = men

    # 7. 排神盘八神
    shen_pan = {}
    shen_list = SHEN_YANG if is_yang else SHEN_YIN
    for i in range(8):
        gong = (shi_gan_gong + i - 1) % 9 + 1
        shen_pan[gong] = shen_list[i]

    # 8. 九宫汇总
    grid = []
    for gong_num in range(1, 10):
        gong_name = GONG_GUA.get(gong_num, f"中{gong_num}")
        grid.append({
            "宫位": gong_num,
            "八卦": gong_name,
            "地盘": di_pan.get(gong_num, ""),
            "天盘星": tian_pan_xing.get(gong_num, ""),
            "人盘门": ren_pan_men.get(gong_num, ""),
            "神盘": shen_pan.get(gong_num, ""),
        })

    # 9. 用神落宫
    yong_info = YONG_SHEN.get(q_type, (["开"], "开门主开创"))
    yong_men = yong_info[0][0] if isinstance(yong_info[0], list) else yong_info[0]
    yong_gong = None
    for g in grid:
        if g["人盘门"] == yong_men:
            yong_gong = g; break
    if not yong_gong:
        yong_gong = grid[0]

    # 10. 白话解读
    analysis = f"起局：{dun_type}{dun_num}局。时柱{shi_gz}。\n"
    analysis += f"用神「{yong_men}」落{yong_gong['宫位']}宫({yong_gong['八卦']})，"
    analysis += f"逢天盘{yong_gong['天盘星']}星，神盘{yong_gong['神盘']}。\n"
    if q_type == "考试":
        analysis += "占考试——用神看景门和丁奇。景门主文章，丁奇主文书。"
    elif q_type == "开业":
        analysis += "占开业——用神看开门。开门在吉宫逢吉星吉神为良辰吉时。"
    elif q_type == "求职":
        analysis += "占求职——用神看开门。开门落宫好则机会多，落宫差则需等待。"
    elif q_type == "求财":
        analysis += "占求财——用神看戊(资金)和生门(财源)。"
    analysis += f"\n总体：{'吉' if yong_gong['宫位'] in [1,8,3,4] else '平'}。"

    return {
        "success": True,
        "data": {
            "dun_type": dun_type,
            "dun_num": dun_num,
            "shi_gz": shi_gz,
            "ri_gz": ri_gan + ri_zhi,
            "grid": grid,
            "yong_gong": yong_gong,
            "yong_men": yong_men,
            "q_type": q_type,
            "yong_desc": yong_info[1],
            "analysis": analysis,
        }
    }


if __name__ == "__main__":
    import json
    r = compute(2026, 6, 13, 10, "考试")
    print(json.dumps(r, ensure_ascii=False, indent=2, default=str))
