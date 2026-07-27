#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大六壬排盘工具
功能：天盘布法、四课起法、三传发传（九宗门）、十二天将
"""

import sys
from datetime import datetime

# 十二地支
DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 天干
TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# 地支五行
DIZHI_WUXING = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木",
    "辰": "土", "巳": "火", "午": "火", "未": "土",
    "申": "金", "酉": "金", "戌": "土", "亥": "水"
}

# 地支方位
DIZHI_FANGWEI = {
    "子": "北", "丑": "东北", "寅": "东北", "卯": "东",
    "辰": "东南", "巳": "东南", "午": "南", "未": "西南",
    "申": "西南", "酉": "西", "戌": "西北", "亥": "西北"
}

# 天干寄宫（日干在地支的寄宫）
GANGAN_JIGONG = {
    "甲": "寅", "乙": "辰", "丙": "巳", "丁": "未",
    "戊": "巳", "己": "未", "庚": "申", "辛": "戌",
    "壬": "亥", "癸": "丑"
}

# 十二月将（中气后换将）
YUEJIANG = {
    1: "大吉丑", 2: "神后子", 3: "登明亥",
    4: "河魁戌", 5: "从魁酉", 6: "传送申",
    7: "小吉未", 8: "胜光午", 9: "太乙巳",
    10: "天罡辰", 11: "太冲卯", 12: "功曹寅"
}

# 十二天将
TIANJIANG = {
    "贵人": {"wuxing": "土", "jixiong": "吉", "zhushi": "官贵、福禄、诏命"},
    "螣蛇": {"wuxing": "火", "jixiong": "凶", "zhushi": "惊恐、怪异、虚诈"},
    "朱雀": {"wuxing": "火", "jixiong": "凶", "zhushi": "文书、口舌、消息"},
    "六合": {"wuxing": "木", "jixiong": "吉", "zhushi": "婚姻、交易、和合"},
    "勾陈": {"wuxing": "土", "jixiong": "凶", "zhushi": "争讼、勾留、田土"},
    "青龙": {"wuxing": "木", "jixiong": "吉", "zhushi": "财帛、喜庆、升迁"},
    "天空": {"wuxing": "土", "jixiong": "凶", "zhushi": "欺诈、虚妄、奏书"},
    "白虎": {"wuxing": "金", "jixiong": "凶", "zhushi": "凶丧、病伤、道路"},
    "太常": {"wuxing": "土", "jixiong": "吉", "zhushi": "衣食、宴会、礼仪"},
    "玄武": {"wuxing": "水", "jixiong": "凶", "zhushi": "盗贼、阴私、遗失"},
    "太阴": {"wuxing": "金", "jixiong": "吉", "zhushi": "妇女、阴私、密谋"},
    "天后": {"wuxing": "水", "jixiong": "吉", "zhushi": "妻妾、恩泽、阴德"},
}


def get_ganzhi_year(year):
    """获取年干支（简化计算）"""
    gan = TIANGAN[(year - 4) % 10]
    zhi = DIZHI[(year - 4) % 12]
    return gan + zhi


def get_ganzhi_month(year, month):
    """获取月干支（五虎遁）"""
    year_gan = TIANGAN.index(get_ganzhi_year(year)[0])
    # 月干起法：甲己之年丙作首
    month_gan_start = (year_gan % 5) * 2 + 2  # 甲己→丙(2), 乙庚→戊(4), 丙辛→庚(6), 丁壬→壬(8), 戊癸→甲(0)
    gan = TIANGAN[(month_gan_start + month - 1) % 10]
    zhi = DIZHI[(month + 1) % 12]  # 正月建寅(2)
    return gan + zhi


def get_ganzhi_day(year, month, day):
    """获取日干支（简化计算，基于1900年1月1日甲戌日）"""
    # 计算从1900-01-01到目标日期的天数
    import datetime
    base = datetime.date(1900, 1, 1)
    target = datetime.date(year, month, day)
    days = (target - base).days

    # 1900-01-01是甲戌日（甲=0, 戌=10）
    gan = TIANGAN[(days + 0) % 10]
    zhi = DIZHI[(days + 10) % 12]
    return gan + zhi


def get_ganzhi_hour(hour, day_gan):
    """获取时干支（五鼠遁）"""
    day_gan_idx = TIANGAN.index(day_gan)
    # 时支
    zhi_idx = (hour + 1) // 2 % 12
    zhi = DIZHI[zhi_idx]
    # 时干起法：甲己还加甲
    hour_gan_start = (day_gan_idx % 5) * 2  # 甲己→甲(0), 乙庚→丙(2), 丙辛→戊(4), 丁壬→庚(6), 戊癸→壬(8)
    gan = TIANGAN[(hour_gan_start + zhi_idx) % 10]
    return gan + zhi


def get_yuejiang(month):
    """获取月将（简化为月份对应）"""
    return YUEJIANG.get(month, "登明亥")


def bu_tianpan(yuejiang_zhi, shichen_zhi):
    """布天盘：月将加时"""
    # 月将所临地支 = 时辰地支
    # 天盘顺时针旋转

    yj_name, yj_zhi = yuejiang_zhi[2:], yuejiang_zhi[-1]  # 提取月将的地支名

    # 找到月将在天盘中的起始位置
    shichen_idx = DIZHI.index(shichen_zhi)

    # 天盘：天盘[地盘位置] = 天盘在该位置的地支
    # 当月将加在时辰上时，天盘顺时针排列
    tianpan = {}
    yj_dizhi = yuejiang_zhi[-1]
    yj_idx = DIZHI.index(yj_dizhi)

    for i in range(12):
        dipan_zhi = DIZHI[(shichen_idx + i) % 12]
        tianpan_zhi = DIZHI[(yj_idx + i) % 12]
        tianpan[dipan_zhi] = tianpan_zhi

    return tianpan


def qi_sike(rigan, rizhi, tianpan):
    """起四课"""
    # 第一课：日干寄宫（天盘+地盘）
    jigong = GANGAN_JIGONG.get(rigan, "寅")
    ke1_shang = tianpan.get(jigong, "?")  # 天盘
    ke1_xia = jigong  # 地盘

    # 第二课：第一课的上神再上一课
    ke2_shang = tianpan.get(ke1_shang, "?")
    ke2_xia = ke1_shang

    # 第三课：日支
    ke3_shang = tianpan.get(rizhi, "?")
    ke3_xia = rizhi

    # 第四课：第三课的上神再上一课
    ke4_shang = tianpan.get(ke3_shang, "?")
    ke4_xia = ke3_shang

    sike = [
        (ke1_xia, ke1_shang),
        (ke2_xia, ke2_shang),
        (ke3_xia, ke3_shang),
        (ke4_xia, ke4_shang),
    ]

    return sike


def fa_sanchuan_zeke(sike, rigan_yinyang):
    """发三传 - 贼克法"""
    # 找到上下相克的课
    ke_list = []

    for i, (xia, shang) in enumerate(sike):
        shang_wx = DIZHI_WUXING.get(shang, "")
        xia_wx = DIZHI_WUXING.get(xia, "")
        if shang_wx and xia_wx:
            # 五行相克关系
            ke_relation = check_wuxing_ke(shang_wx, xia_wx)
            if ke_relation:
                ke_list.append((i + 1, shang, xia, ke_relation))

    if not ke_list:
        return None, "无克，需用其他方法"

    # 贼克：下克上为"贼"（优先），上克下为"克"
    zei_list = [k for k in ke_list if k[3] == "下克上"]
    if zei_list:
        # 如果有多个贼，用比用法
        if len(zei_list) > 1:
            return None, "多贼，需比用法"
        k = zei_list[0]
        chu_chuan = k[1]  # 初传 = 上神
        return [chu_chuan], f"贼克法（下克上，第{k[0]}课）"

    ke_only = [k for k in ke_list if k[3] == "上克下"]
    if len(ke_only) > 1:
        return None, "多克，需比用法"
    k = ke_only[0]
    chu_chuan = k[1]
    return [chu_chuan], f"贼克法（上克下，第{k[0]}课）"


def check_wuxing_ke(wx1, wx2):
    """检查五行相克关系"""
    ke_map = {
        "木": "土", "土": "水", "水": "火",
        "火": "金", "金": "木"
    }
    if ke_map.get(wx1) == wx2:
        return "上克下"  # wx1克wx2 → 上克下
    if ke_map.get(wx2) == wx1:
        return "下克上"  # wx2克wx1 → 下克上
    return None


def get_zhongchuan_mochuan(chuchuan, tianpan):
    """由初传推中传和末传"""
    # 初传的上神为中传，中传的上神为末传
    zhongchuan = tianpan.get(chuchuan, "?")
    mochuan = tianpan.get(zhongchuan, "?")
    return zhongchuan, mochuan


def bu_tianjiang(shichen, rigan):
    """布十二天将（贵人起法）"""
    # 贵人起法：根据昼夜和日干
    # 简化：日干为阳则贵人顺行，阴则逆行
    ri_gan_yang = rigan in ["甲", "丙", "戊", "庚", "壬"]

    guiren_zhi = "丑"  # 简化，实际需查表
    if ri_gan_yang:
        guiren_zhi = "丑"  # 阳贵人
    else:
        guiren_zhi = "未"  # 阴贵人

    # 天将排列
    tianjiang_list = ["贵人", "螣蛇", "朱雀", "六合", "勾陈", "青龙",
                      "天空", "白虎", "太常", "玄武", "太阴", "天后"]

    tianjiang_map = {}
    guiren_idx = DIZHI.index(guiren_zhi)
    for i, tj in enumerate(tianjiang_list):
        if ri_gan_yang:
            zhi = DIZHI[(guiren_idx + i) % 12]
        else:
            zhi = DIZHI[(guiren_idx - i) % 12]
        tianjiang_map[zhi] = tj

    return tianjiang_map


def print_paipan(year, month, day, hour):
    """完整排盘并打印"""
    nian_ganzhi = get_ganzhi_year(year)
    yue_ganzhi = get_ganzhi_month(year, month)
    ri_ganzhi = get_ganzhi_day(year, month, day)
    shi_ganzhi = get_ganzhi_hour(hour, ri_ganzhi[0])

    ri_gan = ri_ganzhi[0]
    ri_zhi = ri_ganzhi[1]
    shi_zhi = shi_ganzhi[1]

    print(f"\n{'='*60}")
    print(f"  大六壬排盘")
    print(f"{'='*60}")
    print(f"  时间：{year}年{month}月{day}日 {hour}时")
    print(f"  四柱：{nian_ganzhi}年 {yue_ganzhi}月 {ri_ganzhi}日 {shi_ganzhi}时")
    print(f"  日干：{ri_gan}（{'阳' if ri_gan in '甲丙戊庚壬' else '阴'}干）")
    print(f"  日支：{ri_zhi}")

    # 月将
    yj = get_yuejiang(month)
    print(f"\n  📌 月将：{yj}（加于{shi_zhi}）")

    # 天盘
    tianpan = bu_tianpan(yj, shi_zhi)
    print(f"\n  📌 天盘（月将加时）：")
    print(f"  {'─' * 50}")
    row = "  "
    for z in DIZHI:
        tp = tianpan.get(z, "?")
        row += f"   {tp}"
    print(row)
    row = "  "
    for z in DIZHI:
        row += f"   {z}({DIZHI_WUXING[z]})"
    print(row)

    # 四课
    sike = qi_sike(ri_gan, ri_zhi, tianpan)
    print(f"\n  📌 四课：")
    for i, (xia, shang) in enumerate(sike):
        print(f"    第{i+1}课：{shang}（上）")
        print(f"            {xia}（下）{' ← 日干寄宫' if i == 0 else ' ← 日支' if i == 2 else ''}")

    # 三传
    is_yang = ri_gan in "甲丙戊庚壬"
    sanchuan, method = fa_sanchuan_zeke(sike, is_yang)
    if sanchuan:
        zhong, mo = get_zhongchuan_mochuan(sanchuan[0], tianpan)
        sanchuan = [sanchuan[0], zhong, mo]
        print(f"\n  📌 三传（{method}）：")
        print(f"    初传：{sanchuan[0]}（{DIZHI_WUXING.get(sanchuan[0], '?')}）")
        print(f"    中传：{sanchuan[1]}（{DIZHI_WUXING.get(sanchuan[1], '?')}）")
        print(f"    末传：{sanchuan[2]}（{DIZHI_WUXING.get(sanchuan[2], '?')}）")
    else:
        print(f"\n  📌 三传：{method}")

    # 十二天将
    tianjiang = bu_tianjiang(shi_zhi, ri_gan)
    print(f"\n  📌 十二天将：")
    row = "  "
    for z in DIZHI:
        tj = tianjiang.get(z, "?")
        row += f"  {tj:　<4s}"
    print(row)
    row = "  "
    for z in DIZHI:
        row += f"  [{z}]"
    print(row)

    # 简要分析
    print(f"\n  📌 简要分析：")
    if sanchuan:
        chu_wx = DIZHI_WUXING.get(sanchuan[0], "")
        ri_wx = DIZHI_WUXING.get(ri_zhi, "")
        if chu_wx and ri_wx:
            print(f"    初传{sanchuan[0]}({chu_wx}) vs 日支{ri_zhi}({ri_wx})")
            if chu_wx == ri_wx:
                print(f"    → 比和，吉")
            elif check_wuxing_ke(chu_wx, ri_wx):
                rel = check_wuxing_ke(chu_wx, ri_wx)
                print(f"    → {rel}，{'吉' if rel == '下克上' else '需注意'}")

    print(f"\n{'='*60}\n")


def main():
    if len(sys.argv) < 2:
        print("大六壬排盘工具")
        print("用法：")
        print("  python liuren_paipan.py now                — 当前时间排盘")
        print("  python liuren_paipan.py date <年> <月> <日> <时> — 指定时间排盘")
        print("  python liuren_paipan.py info               — 天将/地支速查")
        return

    cmd = sys.argv[1]

    if cmd == "now":
        now = datetime.now()
        print_paipan(now.year, now.month, now.day, now.hour)

    elif cmd == "date":
        if len(sys.argv) < 6:
            print("请提供年月日时，如：python liuren_paipan.py date 2024 7 26 10")
            return
        year = int(sys.argv[2])
        month = int(sys.argv[3])
        day = int(sys.argv[4])
        hour = int(sys.argv[5])
        print_paipan(year, month, day, hour)

    elif cmd == "info":
        print("\n📚 大六壬基础知识速查")
        print("\n  📌 十二地支五行方位：")
        for z in DIZHI:
            print(f"    {z}：{DIZHI_WUXING[z]} {DIZHI_FANGWEI[z]}")

        print("\n  📌 天干寄宫：")
        for gan, jigong in GANGAN_JIGONG.items():
            print(f"    {gan} → {jigong}")

        print("\n  📌 十二月将：")
        for m, yj in YUEJIANG.items():
            print(f"    {m}月：{yj}")

        print("\n  📌 十二天将：")
        for name, info in TIANJIANG.items():
            print(f"    {name}：{info['wuxing']} {'吉' if info['jixiong'] == '吉' else '凶'} | {info['zhushi']}")

    else:
        print(f"未知命令：{cmd}")


if __name__ == "__main__":
    main()