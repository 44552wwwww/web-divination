#!/usr/bin/env python3
"""大六壬课传推算"""

TIAN_GAN = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
DI_ZHI = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]

# 月将: 中气后换将 (正月亥, 二月戌, ...)
YUE_JIANG_MAP = {1:"亥",2:"戌",3:"酉",4:"申",5:"未",6:"午",7:"巳",8:"辰",9:"卯",10:"寅",11:"丑",12:"子"}

# 贵人起法
GUI_REN_DAY = {"甲":"丑","戊":"丑","庚":"丑","乙":"子","己":"子","丙":"亥","丁":"亥","辛":"午","壬":"巳","癸":"巳"}

# 十二天将顺序 (贵人→螣蛇→朱雀→六合→勾陈→青龙→天空→白虎→太常→玄武→太阴→天后)
TIAN_JIANG = ["贵人","螣蛇","朱雀","六合","勾陈","青龙","天空","白虎","太常","玄武","太阴","天后"]

# 地支五行
ZHI_WX = {"子":"水","丑":"土","寅":"木","卯":"木","辰":"土","巳":"火","午":"火","未":"土","申":"金","酉":"金","戌":"土","亥":"水"}

def _day_ganzhi(d):
    idx = ((d - __import__('datetime').date(1900,1,1)).days + 10) % 60
    return TIAN_GAN[idx%10], DI_ZHI[idx%12]

def _get_yue_jiang(month):
    return YUE_JIANG_MAP.get(month, "亥")

def _get_gui_ren(ri_gan):
    return GUI_REN_DAY.get(ri_gan, "丑")

def compute(year, month, day, hour, q_type):
    from datetime import date
    d = date(year, month, day)

    # 1. 月将+日干支
    yue_jiang = _get_yue_jiang(month)
    ri_gan, ri_zhi = _day_ganzhi(d)
    shi_zhi = DI_ZHI[((hour+1)//2)%12]

    # 2. 天盘 (月将加时)
    yj_idx = DI_ZHI.index(yue_jiang)
    sz_idx = DI_ZHI.index(shi_zhi)
    tian_pan = {}  # 地盘地支 → 天盘地支
    for i, dz in enumerate(DI_ZHI):
        tian_idx = (yj_idx + i) % 12
        tian_pan[dz] = DI_ZHI[(sz_idx + i) % 12]

    # 3. 四课
    # 第1课: 日干寄宫
    gan_ji_gong = {"甲":"寅","乙":"辰","丙":"巳","丁":"未","戊":"巳","己":"未","庚":"申","辛":"戌","壬":"亥","癸":"丑"}
    ri_gan_gong = gan_ji_gong[ri_gan]
    ke1_shang = tian_pan[ri_gan_gong]
    ke1 = f"日干{ri_gan}寄{ri_gan_gong}→上神{ke1_shang}"

    # 第2课
    ke2_shang = tian_pan[ke1_shang]
    ke2 = f"{ke1_shang}→上神{ke2_shang}"

    # 第3课: 日支
    ke3_shang = tian_pan[ri_zhi]
    ke3 = f"日支{ri_zhi}→上神{ke3_shang}"

    # 第4课
    ke4_shang = tian_pan[ke3_shang]
    ke4 = f"{ke3_shang}→上神{ke4_shang}"

    # 4. 三传 (简化: 元首课)
    # 四课上神克下神(贼)或下神克上神(克)
    ke_list = [(ke1_shang, ri_gan_gong, 1), (ke2_shang, ke1_shang, 2), (ke3_shang, ri_zhi, 3), (ke4_shang, ke3_shang, 4)]
    chu_chuan = zhong_chuan = mo_chuan = "?"

    # 找贼克
    zekes = []
    for shang, xia, ke_num in ke_list:
        shang_wx = ZHI_WX[shang]
        xia_wx = ZHI_WX[xia]
        order_k = {"木":"土","土":"水","水":"火","火":"金","金":"木"}
        if order_k.get(shang_wx) == xia_wx:
            zekes.append((ke_num, shang, "贼", xia))
        elif order_k.get(xia_wx) == shang_wx:
            zekes.append((ke_num, shang, "克", xia))

    if zekes:
        # 取第一课为初传
        chu_ke = zekes[0]
        chu_chuan = chu_ke[1]
        chuan_idx = DI_ZHI.index(chu_chuan)
        zhong_chuan = DI_ZHI[(chuan_idx + 1) % 12]  # 简化: 取中末传
        mo_chuan = DI_ZHI[(chuan_idx + 2) % 12]
    else:
        # 遥克: 取日干上神
        chu_chuan = ke1_shang
        chuan_idx = DI_ZHI.index(chu_chuan)
        zhong_chuan = DI_ZHI[(chuan_idx + 2) % 12]
        mo_chuan = DI_ZHI[(chuan_idx + 4) % 12]

    ke_shi = "元首课" if zekes else "遥克课"

    # 5. 十二天将
    gui_ren_zhi = _get_gui_ren(ri_gan)
    gui_idx = DI_ZHI.index(gui_ren_zhi)
    # 贵人顺逆 (昼顺夜逆, 简化: 顺排)
    tian_jiang_map = {}
    for i in range(12):
        dz = DI_ZHI[(gui_idx + i) % 12]
        tian_jiang_map[dz] = TIAN_JIANG[i]

    # 三传天将
    chu_jiang = tian_jiang_map.get(chu_chuan, "?")
    zhong_jiang = tian_jiang_map.get(zhong_chuan, "?")
    mo_jiang = tian_jiang_map.get(mo_chuan, "?")

    # 6. 白话解读
    analysis = f"课式：{ke_shi}。月将{yue_jiang}加时{shi_zhi}。\n"
    analysis += f"初传{chu_chuan}({chu_jiang}) → 中传{zhong_chuan}({zhong_jiang}) → 末传{mo_chuan}({mo_jiang})。\n"

    if q_type == "纠纷":
        analysis += "占纠纷——看朱雀(口舌)和贵人(调解)。"
        if "朱雀" in [chu_jiang, zhong_jiang, mo_jiang]:
            analysis += "三传见朱雀，中间会有口舌争执，但要注意传话容易走样。"
    elif q_type == "感情":
        analysis += "占感情——看六合(姻缘)和青龙(喜庆)。"
    elif q_type == "合作":
        analysis += "占合作——看六合(合伙)和勾陈(合同)。"
    elif q_type == "寻人":
        analysis += "占寻人——看白虎(动向)和玄武(隐匿)。"
    elif q_type == "官司":
        analysis += "占官司——看勾陈(诉讼)和白虎(裁判)。"

    analysis += f"\n初传代表事情的开始，中传代表中间发展，末传代表最终结果。"
    analysis += f"\n{'三传见贵人→有贵人相助。' if '贵人' in [chu_jiang,zhong_jiang,mo_jiang] else ''}"
    analysis += f"\n{'注意：三传见白虎→过程中可能有冲突。' if '白虎' in [chu_jiang,zhong_jiang,mo_jiang] else ''}"

    return {
        "success": True,
        "data": {
            "yue_jiang": yue_jiang,
            "shi_zhi": shi_zhi,
            "ri_gan": ri_gan,
            "ri_zhi": ri_zhi,
            "ke_shi": ke_shi,
            "four_lessons": [ke1, ke2, ke3, ke4],
            "chu_chuan": chu_chuan,
            "zhong_chuan": zhong_chuan,
            "mo_chuan": mo_chuan,
            "chu_jiang": chu_jiang,
            "zhong_jiang": zhong_jiang,
            "mo_jiang": mo_jiang,
            "tian_jiang_map": tian_jiang_map,
            "q_type": q_type,
            "analysis": analysis,
        }
    }


if __name__ == "__main__":
    import json
    r = compute(2026, 6, 13, 10, "纠纷")
    print(json.dumps(r, ensure_ascii=False, indent=2, default=str))
