#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小六壬掌诀推算工具
支持：月日时推算、数字推算、六宫断辞查询
"""

import sys
from datetime import datetime

# 六宫信息
LIU_GONG = {
    1: {
        "name": "大安",
        "wuxing": "木（青龙）",
        "jixiong": "大吉",
        "fangwei": "东方",
        "shuli": "1、5、7",
        "zhushi": ["身不动时", "求谋顺利", "行人身未动", "失物去不远"],
        "duanci": "大安事事昌，求谋在东方。失物去不远，宅舍保安康。\n行人身未动，病者主无妨。将军回田野，仔细与推详。",
        "modern": "诸事顺利，适合开启新计划。所求之事成功率较高，但需主动行动。",
        "ganqing": "感情稳定，有进展。单身者有望遇到合适对象。",
        "shiye": "事业顺利，工作稳定。适合求职、升迁。",
        "jiankang": "健康状况良好，无大碍。",
        "chuxing": "出行顺利，平安。",
        "shiwu": "失物未远离，仔细寻找可找回。",
        "kaoshi": "考试顺利，成绩理想。"
    },
    2: {
        "name": "留连",
        "wuxing": "水（玄武）",
        "jixiong": "小凶",
        "fangwei": "北方",
        "shuli": "2、8、10",
        "zhushi": ["卒未归时", "事难成就", "去者未回程", "失物南方见"],
        "duanci": "留连事难成，求谋日未明。官事只宜缓，去者未回程。\n失物南方见，急讨方称心。更须防口舌，人口且平平。",
        "modern": "事情拖延，进展缓慢。需要耐心等待，不宜急躁决策。",
        "ganqing": "感情暧昧不明，进展缓慢。需要更多沟通和耐心。",
        "shiye": "工作进展缓慢，可能有阻碍。宜稳守，不宜冒进。",
        "jiankang": "小病缠身，恢复较慢。注意调理。",
        "chuxing": "出行可能有延误，需多预留时间。",
        "shiwu": "失物在南方，需尽快寻找。",
        "kaoshi": "准备不足，结果可能不理想。需加倍努力。"
    },
    3: {
        "name": "速喜",
        "wuxing": "火（朱雀）",
        "jixiong": "大吉",
        "fangwei": "南方",
        "shuli": "3、6、9",
        "zhushi": ["人便至时", "求财向南行", "失物申午见", "行人立便至"],
        "duanci": "速喜喜来临，求财向南行。失物申午见，行人路上寻。\n官事有福德，病者无祸侵。田宅六畜吉，行人有信音。",
        "modern": "喜事临门，快速见效。适合行动、求财、社交。",
        "ganqing": "感情迅速升温，有喜事。单身者可能很快遇到心动对象。",
        "shiye": "工作有突破，好消息将至。适合主动出击。",
        "jiankang": "疾病恢复快，有望速愈。",
        "chuxing": "出行顺利，可能有好消息。",
        "shiwu": "失物在申、午时（下午3-5点或11-1点）能找到。",
        "kaoshi": "考试顺利，成绩不错。"
    },
    4: {
        "name": "赤口",
        "wuxing": "金（白虎）",
        "jixiong": "大凶",
        "fangwei": "西方",
        "shuli": "4、7、10",
        "zhushi": ["官事凶时", "口舌是非", "失物急去寻", "行人有惊慌"],
        "duanci": "赤口主口舌，官非切要防。失物急去寻，行人有惊慌。\n六畜多作怪，病者出西方。更须防诅咒，诚恐染瘟黄。",
        "modern": "口舌是非，容易与人争执。需谨言慎行，避免冲突。",
        "ganqing": "感情易生口角，注意沟通方式。避免冲动决定。",
        "shiye": "工作中可能有纠纷或小人。谨言慎行，勿与人争。",
        "jiankang": "注意呼吸系统、口腔、喉咙问题。",
        "chuxing": "出行需谨慎，可能有意外。",
        "shiwu": "失物需紧急寻找，可能已被移动。",
        "kaoshi": "考试可能有失误，需仔细检查。"
    },
    5: {
        "name": "小吉",
        "wuxing": "木（六合）",
        "jixiong": "上吉",
        "fangwei": "东方",
        "shuli": "1、5、7",
        "zhushi": ["人来喜时", "最吉昌", "失物在坤方", "交易甚是强"],
        "duanci": "小吉最吉昌，路上好商量。阳人来报喜，失物在坤方。\n行人立便至，交易甚是强。凡事皆和合，病者祷上苍。",
        "modern": "诸事和合，有好消息。适合合作、谈判、交易。",
        "ganqing": "感情和合，关系融洽。适合促进关系发展。",
        "shiye": "合作顺利，谈判成功。有贵人相助。",
        "jiankang": "健康状况良好，但小问题需注意。",
        "chuxing": "出行顺利，路上可能有好消息。",
        "shiwu": "失物在西南方（坤方），能找到。",
        "kaoshi": "考试结果不错，和合顺利。"
    },
    6: {
        "name": "空亡",
        "wuxing": "土（勾陈）",
        "jixiong": "大凶",
        "fangwei": "中央",
        "shuli": "3、6、9",
        "zhushi": ["音信稀时", "谋事落空", "失物寻不见", "阴人小乘张"],
        "duanci": "空亡事不长，阴人多乖张。求财无利益，行人有灾殃。\n失物寻不见，官事主刑伤。病人逢暗鬼，禳解保安康。",
        "modern": "事情落空，计划可能泡汤。需重新评估，不宜强求。",
        "ganqing": "感情不稳定，可能落空。不适合表白或做重大决定。",
        "shiye": "计划可能落空，投资需谨慎。不宜冒险。",
        "jiankang": "病情可能加重，需重视。注意精神压力。",
        "chuxing": "出行可能不顺，建议改期。",
        "shiwu": "失物难找回，可能已丢失。",
        "kaoshi": "考试结果可能不理想，需更加努力。"
    }
}

# 六宫手掌位置（从食指根到无名指根）
GONG_ORDER = [1, 2, 3, 4, 5, 6]  # 大安→留连→速喜→赤口→小吉→空亡

# 农历月份对应数字（正月=1, 二月=2, ...）
# 简化处理，实际需要查农历日历


def xiaoliuren_month_day_hour(month, day, hour_cn=None):
    """
    月日时三轮推算
    month: 农历月（1-12）
    day: 农历日（1-30）
    hour_cn: 时辰（子丑寅卯辰巳午未申酉戌亥）
    """
    # 时辰对应数字
    HOUR_MAP = {
        "子": 1, "丑": 2, "寅": 3, "卯": 4,
        "辰": 5, "巳": 6, "午": 7, "未": 8,
        "申": 9, "酉": 10, "戌": 11, "亥": 12
    }

    if hour_cn is None:
        # 用当前时间推算时辰
        now = datetime.now()
        h = now.hour
        hour_num = (h + 1) // 2  # 简化：每2小时一个时辰
        if hour_num == 0:
            hour_num = 12
        hour_cn = list(HOUR_MAP.keys())[hour_num - 1]
    elif hour_cn in HOUR_MAP:
        hour_num = HOUR_MAP[hour_cn]
    else:
        hour_num = int(hour_cn) if hour_cn.isdigit() else 1

    print(f"\n🔮 小六壬掌诀推算")
    print(f"  农历：{month}月 {day}日 {hour_cn}时")
    print(f"  推算数字：月={month} 日={day} 时={hour_num}")

    # 第一步：月起大安（正月从大安起）
    # 从大安(1)开始，顺数月份
    month_pos = ((month - 1) % 6) + 1
    print(f"\n  第一步：正月起大安，顺数月至{month}月 → 落{LIU_GONG[month_pos]['name']}")

    # 第二步：月上起日
    # 从月落宫开始，顺数日期
    day_pos = ((month_pos - 1 + day - 1) % 6) + 1
    print(f"  第二步：{LIU_GONG[month_pos]['name']}上起日，数至{day}日 → 落{LIU_GONG[day_pos]['name']}")

    # 第三步：日上起时
    # 从日落宫开始，顺数时辰
    time_pos = ((day_pos - 1 + hour_num - 1) % 6) + 1
    print(f"  第三步：{LIU_GONG[day_pos]['name']}上起时，数至{hour_cn}时 → 落{LIU_GONG[time_pos]['name']}")

    gong = LIU_GONG[time_pos]
    print(f"\n  ╔══════════════════════════════════╗")
    print(f"  ║  最终落宫：{gong['name']}（{gong['wuxing']}）{'':>6s}║")
    print(f"  ║  吉凶：{gong['jixiong']}{'':>18s}║")
    print(f"  ╚══════════════════════════════════╝")
    print(f"\n  📜 断辞：")
    print(f"  {gong['duanci']}")
    print(f"\n  📖 现代解读：{gong['modern']}")
    print(f"\n  💡 分类解读：")
    print(f"    感情：{gong['ganqing']}")
    print(f"    事业：{gong['shiye']}")
    print(f"    健康：{gong['jiankang']}")
    print(f"    出行：{gong['chuxing']}")
    print(f"    失物：{gong['shiwu']}")
    print(f"    考试：{gong['kaoshi']}")

    return time_pos, gong


def xiaoliuren_number(n1, n2=None, n3=None):
    """数字推算"""
    if n2 is None:
        # 单数字：从大安起数
        pos = ((n1 - 1) % 6) + 1
        print(f"\n🔮 小六壬数字推算（单数）")
        print(f"  数字：{n1}")
        print(f"  从大安起数{n1}步 → 落{LIU_GONG[pos]['name']}")
    elif n3 is None:
        # 双数字：模拟月日
        month_pos = ((n1 - 1) % 6) + 1
        day_pos = ((month_pos - 1 + n2 - 1) % 6) + 1
        pos = day_pos
        print(f"\n🔮 小六壬数字推算（双数模拟月日）")
        print(f"  数字：{n1}（月）、{n2}（日）")
        print(f"  月数{n1}步 → {LIU_GONG[month_pos]['name']}")
        print(f"  日数{n2}步 → {LIU_GONG[day_pos]['name']}")
    else:
        # 三数字：模拟月日时
        month_pos = ((n1 - 1) % 6) + 1
        day_pos = ((month_pos - 1 + n2 - 1) % 6) + 1
        pos = ((day_pos - 1 + n3 - 1) % 6) + 1
        print(f"\n🔮 小六壬数字推算（三数模拟月日时）")
        print(f"  数字：{n1}（月）、{n2}（日）、{n3}（时）")
        print(f"  月数{n1}步 → {LIU_GONG[month_pos]['name']}")
        print(f"  日数{n2}步 → {LIU_GONG[day_pos]['name']}")
        print(f"  时数{n3}步 → {LIU_GONG[pos]['name']}")

    gong = LIU_GONG[pos]
    print(f"\n  ╔══════════════════════════════════╗")
    print(f"  ║  最终落宫：{gong['name']}（{gong['wuxing']}）{'':>6s}║")
    print(f"  ║  吉凶：{gong['jixiong']}{'':>18s}║")
    print(f"  ╚══════════════════════════════════╝")
    print(f"\n  📜 断辞：{gong['duanci'][:60]}...")
    print(f"  📖 现代解读：{gong['modern']}")

    return pos, gong


def query_gong(name):
    """查询指定宫位信息"""
    for pos, gong in LIU_GONG.items():
        if name in gong["name"]:
            print(f"\n📚 {gong['name']}宫详解")
            print(f"=" * 50)
            print(f"  五行：{gong['wuxing']}")
            print(f"  吉凶：{gong['jixiong']}")
            print(f"  方位：{gong['fangwei']}")
            print(f"  数理：{gong['shuli']}")
            print(f"  主事：{' | '.join(gong['zhushi'])}")
            print(f"\n  断辞原文：")
            print(f"  {gong['duanci']}")
            print(f"\n  现代解读：{gong['modern']}")
            print(f"\n  分类解读：")
            print(f"    感情：{gong['ganqing']}")
            print(f"    事业：{gong['shiye']}")
            print(f"    健康：{gong['jiankang']}")
            print(f"    出行：{gong['chuxing']}")
            print(f"    失物：{gong['shiwu']}")
            print(f"    考试：{gong['kaoshi']}")
            return gong
    print(f"未找到宫位：{name}")
    return None


def list_all():
    """列出所有宫位"""
    print("\n📚 小六壬六宫总览")
    print("=" * 60)
    for pos in range(1, 7):
        g = LIU_GONG[pos]
        print(f"  {pos}. {g['name']:　<4s} | {g['wuxing']:<10s} | {g['jixiong']:<4s} | {g['fangwei']:<4s} | {g['shuli']}")


def print_hand():
    """打印手掌图"""
    print("""
    ╔══════════════════════════════════════════╗
    ║          小六壬掌诀图（左手）            ║
    ╠══════════════════════════════════════════╣
    ║                                          ║
    ║    食指                中指        无名指 ║
    ║   ┌─────┐           ┌─────┐     ┌─────┐ ║
    ║   │     │           │     │     │     │ ║
    ║   │留连  │           │速喜  │     │赤口  │ ║
    ║   │(水)  │           │(火)  │     │(金)  │ ║
    ║   │     │           │     │     │     │ ║
    ║   ├─────┤           ├─────┤     ├─────┤ ║
    ║   │     │           │     │     │     │ ║
    ║   │大安  │           │空亡  │     │小吉  │ ║
    ║   │(木)  │           │(土)  │     │(木)  │ ║
    ║   │     │           │     │     │     │ ║
    ║   └─────┘           └─────┘     └─────┘ ║
    ║                                          ║
    ║   推算顺序：大安(1)→留连(2)→速喜(3)      ║
    ║            →赤口(4)→小吉(5)→空亡(6)      ║
    ║            →回到大安(1)                   ║
    ╚══════════════════════════════════════════╝
    """)


def main():
    if len(sys.argv) < 2:
        print("小六壬掌诀推算工具")
        print("用法：")
        print("  python xiaoliuren_calc.py hand              — 显示手掌图")
        print("  python xiaoliuren_calc.py list              — 列出所有宫位")
        print("  python xiaoliuren_calc.py query <宫名>       — 查询指定宫位")
        print("  python xiaoliuren_calc.py lunar <月> <日> <时辰> — 农历月日时推算")
        print("  python xiaoliuren_calc.py now               — 用当前时间推算")
        print("  python xiaoliuren_calc.py num <n1> [n2] [n3] — 数字推算")
        return

    cmd = sys.argv[1]

    if cmd == "hand":
        print_hand()
    elif cmd == "list":
        list_all()
    elif cmd == "query":
        if len(sys.argv) < 3:
            print("请提供宫名，如：python xiaoliuren_calc.py query 大安")
            return
        query_gong(sys.argv[2])
    elif cmd == "lunar":
        if len(sys.argv) < 5:
            print("请提供月、日、时辰，如：python xiaoliuren_calc.py lunar 3 5 巳")
            print("时辰：子丑寅卯辰巳午未申酉戌亥")
            return
        month = int(sys.argv[2])
        day = int(sys.argv[3])
        hour = sys.argv[4]
        xiaoliuren_month_day_hour(month, day, hour)
    elif cmd == "now":
        now = datetime.now()
        # 简化：用公历月日时模拟
        month = now.month
        day = now.day
        h = now.hour
        hour_map = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        hour_idx = (h + 1) // 2 % 12
        hour_cn = hour_map[hour_idx]
        print(f"当前时间：{now.strftime('%Y-%m-%d %H:%M:%S')}（公历）")
        print(f"模拟农历推算：{month}月{day}日{hour_cn}时")
        print("注意：精确推算需使用农历，此处为公历模拟")
        xiaoliuren_month_day_hour(month, day, hour_cn)
    elif cmd == "num":
        if len(sys.argv) < 3:
            print("请提供至少1个数字，如：python xiaoliuren_calc.py num 3 8 5")
            return
        n1 = int(sys.argv[2])
        n2 = int(sys.argv[3]) if len(sys.argv) > 3 else None
        n3 = int(sys.argv[4]) if len(sys.argv) > 4 else None
        xiaoliuren_number(n1, n2, n3)
    else:
        print(f"未知命令：{cmd}")


if __name__ == "__main__":
    main()