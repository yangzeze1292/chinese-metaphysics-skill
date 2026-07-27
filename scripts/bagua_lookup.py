#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
六十四卦查询工具
支持：按卦名/卦序/上下卦查询、金钱卦起卦、数字卦起卦
"""

import sys
import random
from datetime import datetime

# 八卦基础：序号、卦名、卦象、五行、方位、人物
BAGUA = {
    1: {"name": "乾", "symbol": "☰", "wuxing": "金", "fangwei": "西北", "renwu": "父", "nature": "天"},
    2: {"name": "兑", "symbol": "☱", "wuxing": "金", "fangwei": "西", "renwu": "少女", "nature": "泽"},
    3: {"name": "离", "symbol": "☲", "wuxing": "火", "fangwei": "南", "renwu": "中女", "nature": "火"},
    4: {"name": "震", "symbol": "☳", "wuxing": "木", "fangwei": "东", "renwu": "长男", "nature": "雷"},
    5: {"name": "巽", "symbol": "☴", "wuxing": "木", "fangwei": "东南", "renwu": "长女", "nature": "风"},
    6: {"name": "坎", "symbol": "☵", "wuxing": "水", "fangwei": "北", "renwu": "中男", "nature": "水"},
    7: {"name": "艮", "symbol": "☶", "wuxing": "土", "fangwei": "东北", "renwu": "少男", "nature": "山"},
    8: {"name": "坤", "symbol": "☷", "wuxing": "土", "fangwei": "西南", "renwu": "母", "nature": "地"},
}

# 数字到八卦的映射（先天八卦数：乾1兑2离3震4巽5坎6艮7坤8）
NUM_TO_GUA = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8}

# 六十四卦完整数据库
LIUSHISI_GUA = {
    1: {
        "name": "乾为天", "pinyin": "qián wéi tiān",
        "shang": 1, "xia": 1,
        "guaci": "元亨利贞。",
        "tuan": "大哉乾元，万物资始，乃统天。云行雨施，品物流形。大明终始，六位时成，时乘六龙以御天。乾道变化，各正性命，保合太和，乃利贞。首出庶物，万国咸宁。",
        "daxiang": "天行健，君子以自强不息。",
        "yaoci": [
            "初九：潜龙勿用。",
            "九二：见龙在田，利见大人。",
            "九三：君子终日乾乾，夕惕若厉，无咎。",
            "九四：或跃在渊，无咎。",
            "九五：飞龙在天，利见大人。",
            "上九：亢龙有悔。",
            "用九：见群龙无首，吉。"
        ],
        "hexin": "刚健中正，自强不息，创始之道",
        "keywords": ["创始", "领导", "刚健", "自强", "天行健"]
    },
    2: {
        "name": "坤为地", "pinyin": "kūn wéi dì",
        "shang": 8, "xia": 8,
        "guaci": "元亨，利牝马之贞。君子有攸往，先迷后得主，利。西南得朋，东北丧朋。安贞吉。",
        "tuan": "至哉坤元，万物资生，乃顺承天。坤厚载物，德合无疆。含弘光大，品物咸亨。牝马地类，行地无疆，柔顺利贞。",
        "daxiang": "地势坤，君子以厚德载物。",
        "yaoci": [
            "初六：履霜，坚冰至。",
            "六二：直方大，不习无不利。",
            "六三：含章可贞，或从王事，无成有终。",
            "六四：括囊，无咎无誉。",
            "六五：黄裳，元吉。",
            "上六：龙战于野，其血玄黄。",
            "用六：利永贞。"
        ],
        "hexin": "柔顺承天，厚德载物，包容之道",
        "keywords": ["柔顺", "包容", "厚德", "承载", "地道"]
    },
    3: {
        "name": "水雷屯", "pinyin": "shuǐ léi zhūn",
        "shang": 6, "xia": 4,
        "guaci": "元亨利贞。勿用有攸往，利建侯。",
        "tuan": "屯，刚柔始交而难生。动乎险中，大亨贞。雷雨之动满盈，天造草昧，宜建侯而不宁。",
        "daxiang": "云雷屯，君子以经纶。",
        "yaoci": [
            "初九：磐桓，利居贞，利建侯。",
            "六二：屯如邅如，乘马班如。匪寇婚媾，女子贞不字，十年乃字。",
            "六三：即鹿无虞，惟入于林中，君子几不如舍，往吝。",
            "六四：乘马班如，求婚媾，往吉，无不利。",
            "九五：屯其膏，小贞吉，大贞凶。",
            "上六：乘马班如，泣血涟如。"
        ],
        "hexin": "始生艰难，创业维艰，需耐心经营",
        "keywords": ["创业", "艰难", "初始", "耐心", "积累"]
    },
    4: {
        "name": "山水蒙", "pinyin": "shān shuǐ méng",
        "shang": 7, "xia": 6,
        "guaci": "亨。匪我求童蒙，童蒙求我。初筮告，再三渎，渎则不告。利贞。",
        "tuan": "蒙，山下有险，险而止蒙。蒙亨，以亨行时中也。匪我求童蒙，童蒙求我，志应也。",
        "daxiang": "山下出泉，蒙。君子以果行育德。",
        "yaoci": [
            "初六：发蒙，利用刑人，用说桎梏，以往吝。",
            "九二：包蒙吉，纳妇吉，子克家。",
            "六三：勿用取女，见金夫，不有躬，无攸利。",
            "六四：困蒙，吝。",
            "六五：童蒙，吉。",
            "上九：击蒙，不利为寇，利御寇。"
        ],
        "hexin": "启蒙教育，求知若渴，师道尊严",
        "keywords": ["启蒙", "教育", "学习", "求知", "引导"]
    },
    5: {
        "name": "水天需", "pinyin": "shuǐ tiān xū",
        "shang": 6, "xia": 1,
        "guaci": "有孚，光亨，贞吉。利涉大川。",
        "tuan": "需，须也，险在前也。刚健而不陷，其义不困穷矣。需有孚光亨贞吉，位乎天位，以正中也。",
        "daxiang": "云上于天，需。君子以饮食宴乐。",
        "yaoci": [
            "初九：需于郊，利用恒，无咎。",
            "九二：需于沙，小有言，终吉。",
            "九三：需于泥，致寇至。",
            "六四：需于血，出自穴。",
            "九五：需于酒食，贞吉。",
            "上六：入于穴，有不速之客三人来，敬之终吉。"
        ],
        "hexin": "等待时机，耐心守候，以静制动",
        "keywords": ["等待", "耐心", "时机", "需求", "饮食"]
    },
    6: {
        "name": "天水讼", "pinyin": "tiān shuǐ sòng",
        "shang": 1, "xia": 6,
        "guaci": "有孚窒惕，中吉，终凶。利见大人，不利涉大川。",
        "tuan": "讼，上刚下险，险而健讼。讼有孚窒惕中吉，刚来而得中也。终凶，讼不可成也。",
        "daxiang": "天与水违行，讼。君子以作事谋始。",
        "yaoci": [
            "初六：不永所事，小有言，终吉。",
            "九二：不克讼，归而逋，其邑人三百户，无眚。",
            "六三：食旧德，贞厉，终吉。或从王事，无成。",
            "九四：不克讼，复即命，渝安贞，吉。",
            "九五：讼，元吉。",
            "上九：或锡之鞶带，终朝三褫之。"
        ],
        "hexin": "争讼纠纷，宜和解不宜久争，慎始谋始",
        "keywords": ["争讼", "纠纷", "官司", "和解", "谋始"]
    },
    7: {
        "name": "地水师", "pinyin": "dì shuǐ shī",
        "shang": 8, "xia": 6,
        "guaci": "贞，丈人吉，无咎。",
        "tuan": "师，众也。贞，正也。能以众正，可以王矣。刚中而应，行险而顺，以此毒天下，而民从之，吉又何咎矣。",
        "daxiang": "地中有水，师。君子以容民畜众。",
        "yaoci": [
            "初六：师出以律，否臧凶。",
            "九二：在师中，吉无咎，王三锡命。",
            "六三：师或舆尸，凶。",
            "六四：师左次，无咎。",
            "六五：田有禽，利执言，无咎。长子帅师，弟子舆尸，贞凶。",
            "上六：大君有命，开国承家，小人勿用。"
        ],
        "hexin": "统兵用众，师出有名，纪律严明",
        "keywords": ["军队", "战争", "统帅", "纪律", "组织"]
    },
    8: {
        "name": "水地比", "pinyin": "shuǐ dì bǐ",
        "shang": 6, "xia": 8,
        "guaci": "吉。原筮，元永贞，无咎。不宁方来，后夫凶。",
        "tuan": "比，吉也。比，辅也，下顺从也。原筮元永贞无咎，以刚中也。不宁方来，上下应也。",
        "daxiang": "地上有水，比。先王以建万国，亲诸侯。",
        "yaoci": [
            "初六：有孚比之，无咎。有孚盈缶，终来有它，吉。",
            "六二：比之自内，贞吉。",
            "六三：比之匪人。",
            "六四：外比之，贞吉。",
            "九五：显比，王用三驱，失前禽。邑人不诫，吉。",
            "上六：比之无首，凶。"
        ],
        "hexin": "亲附团结，择善而比，和谐共处",
        "keywords": ["亲附", "团结", "合作", "人际", "辅助"]
    },
    9: {
        "name": "风天小畜", "pinyin": "fēng tiān xiǎo xù",
        "shang": 5, "xia": 1,
        "guaci": "亨。密云不雨，自我西郊。",
        "tuan": "小畜，柔得位而上下应之，曰小畜。健而巽，刚中而志行，乃亨。密云不雨，尚往也。自我西郊，施未行也。",
        "daxiang": "风行天上，小畜。君子以懿文德。",
        "yaoci": [
            "初九：复自道，何其咎，吉。",
            "九二：牵复，吉。",
            "九三：舆说辐，夫妻反目。",
            "六四：有孚，血去惕出，无咎。",
            "九五：有孚挛如，富以其邻。",
            "上九：既雨既处，尚德载，妇贞厉。月几望，君子征凶。"
        ],
        "hexin": "小有积蓄，蓄势待发，以柔蓄刚",
        "keywords": ["积蓄", "准备", "小成", "蓄力", "文德"]
    },
    10: {
        "name": "天泽履", "pinyin": "tiān zé lǚ",
        "shang": 1, "xia": 2,
        "guaci": "履虎尾，不咥人，亨。",
        "tuan": "履，柔履刚也。说而应乎乾，是以履虎尾不咥人亨。刚中正，履帝位而不疚，光明也。",
        "daxiang": "上天下泽，履。君子以辨上下，定民志。",
        "yaoci": [
            "初九：素履，往无咎。",
            "九二：履道坦坦，幽人贞吉。",
            "九三：眇能视，跛能履，履虎尾，咥人，凶。武人为于大君。",
            "九四：履虎尾，愬愬终吉。",
            "九五：夬履，贞厉。",
            "上九：视履考祥，其旋元吉。"
        ],
        "hexin": "履行实践，如履薄冰，谨慎行事",
        "keywords": ["实践", "履行", "礼仪", "谨慎", "行为"]
    }
}


def get_gua_by_name(name):
    """按卦名查询"""
    name = name.strip()
    for seq, gua in LIUSHISI_GUA.items():
        if name in gua["name"]:
            return seq, gua
    return None, None


def get_gua_by_seq(seq):
    """按卦序查询"""
    return LIUSHISI_GUA.get(seq)


def get_gua_by_shangxia(shang, xia):
    """按上下卦查询"""
    for seq, gua in LIUSHISI_GUA.items():
        if gua["shang"] == shang and gua["xia"] == xia:
            return seq, gua
    return None, None


def print_gua(seq, gua):
    """格式化输出卦象信息"""
    shang_gua = BAGUA[gua["shang"]]
    xia_gua = BAGUA[gua["xia"]]
    print(f"\n{'='*60}")
    print(f"  第{seq}卦：{gua['name']}（{gua['pinyin']}）")
    print(f"{'='*60}")
    print(f"  卦象：{shang_gua['symbol']}{xia_gua['symbol']}  "
          f"上{shang_gua['name']}({shang_gua['wuxing']})下{xia_gua['name']}({xia_gua['wuxing']})")
    print(f"  卦辞：{gua['guaci']}")
    print(f"  彖传：{gua['tuan'][:80]}...")
    print(f"  大象：{gua['daxiang']}")
    print(f"\n  爻辞：")
    for yao in gua["yaoci"]:
        print(f"    {yao}")
    print(f"\n  核心含义：{gua['hexin']}")
    print(f"  关键词：{' | '.join(gua['keywords'])}")
    print(f"{'='*60}\n")


def money_gua():
    """金钱卦起卦法：三枚铜钱摇六次"""
    print("\n🎯 金钱卦起卦")
    print("请准备三枚硬币，每次抛掷后记录结果：")
    print("  三正（字面）  = 少阳 ─── 记为 7")
    print("  两正一反      = 少阴 ─ ─ 记为 8")
    print("  一正两反      = 老阳 ⚊ 记为 9（动爻）")
    print("  三反           = 老阴 ⚋ 记为 6（动爻）")
    print()

    yao_list = []
    yao_symbols = []
    for i in range(6):
        while True:
            try:
                val = int(input(f"第{i+1}次抛掷结果（6/7/8/9）："))
                if val in [6, 7, 8, 9]:
                    yao_list.append(val)
                    if val == 6:
                        yao_symbols.append("⚋ 老阴（动爻）")
                    elif val == 7:
                        yao_symbols.append("─── 少阳")
                    elif val == 8:
                        yao_symbols.append("─ ─ 少阴")
                    elif val == 9:
                        yao_symbols.append("⚊ 老阳（动爻）")
                    break
                else:
                    print("请输入 6、7、8、9 中的一个")
            except ValueError:
                print("请输入数字")

    # 显示卦象
    print("\n从下往上的爻象：")
    for i, s in enumerate(yao_symbols):
        print(f"  第{i+1}爻：{s}")

    # 确定本卦（阴爻=偶数，阳爻=奇数，但爻从下往上排）
    # 6(老阴)和8(少阴)为阴爻，7(少阳)和9(老阳)为阳爻
    ben_gua_xia = 0  # 下卦三爻的二进制
    ben_gua_shang = 0  # 上卦三爻的二进制
    for i in range(3):  # 初爻到三爻 = 下卦
        if yao_list[i] in [7, 9]:  # 阳爻
            ben_gua_xia |= (1 << i)
    for i in range(3, 6):  # 四爻到上爻 = 上卦
        if yao_list[i] in [7, 9]:  # 阳爻
            ben_gua_shang |= (1 << (i - 3))

    # 二进制转八卦序号（乾1兑2离3震4巽5坎6艮7坤8）
    def bin_to_gua(b):
        mapping = {0b111: 1, 0b110: 2, 0b101: 3, 0b100: 4,
                   0b011: 5, 0b010: 6, 0b001: 7, 0b000: 8}
        return mapping.get(b, 8)

    shang = bin_to_gua(ben_gua_shang)
    xia = bin_to_gua(ben_gua_xia)

    seq, gua = get_gua_by_shangxia(shang, xia)
    if gua:
        print(f"\n📖 本卦：{gua['name']}（{BAGUA[shang]['symbol']}{BAGUA[xia]['symbol']}）")
        print_gua(seq, gua)

    # 变爻分析
    bian_yao = []
    for i, val in enumerate(yao_list):
        if val in [6, 9]:  # 老阴或老阳，是动爻
            bian_yao.append(i + 1)

    if bian_yao:
        print(f"🔀 变爻：第{'、'.join(str(y) for y in bian_yao)}爻")

        # 计算变卦
        bian_yao_shang = ben_gua_shang
        bian_yao_xia = ben_gua_xia
        for y in bian_yao:
            idx = y - 1
            if idx < 3:
                bian_yao_xia ^= (1 << idx)  # 翻转该爻
            else:
                bian_yao_shang ^= (1 << (idx - 3))

        bian_shang = bin_to_gua(bian_yao_shang)
        bian_xia = bin_to_gua(bian_yao_xia)
        bseq, bgua = get_gua_by_shangxia(bian_shang, bian_xia)
        if bgua:
            print(f"📖 变卦（之卦）：{bgua['name']}（{BAGUA[bian_shang]['symbol']}{BAGUA[bian_xia]['symbol']}）")
            print_gua(bseq, bgua)

        # 朱熹断卦规则
        print("📏 朱熹《易学启蒙》断卦规则：")
        n = len(bian_yao)
        if n == 0:
            print("  六爻不变 → 本卦卦辞断之")
        elif n == 1:
            print(f"  一爻变 → 本卦第{bian_yao[0]}爻爻辞断之")
            print(f"  → {gua['yaoci'][bian_yao[0]-1]}")
        elif n == 2:
            print(f"  二爻变 → 本卦二变爻爻辞，以上爻（第{bian_yao[1]}爻）为主")
            print(f"  → 本卦第{bian_yao[0]}爻：{gua['yaoci'][bian_yao[0]-1]}")
            print(f"  → 本卦第{bian_yao[1]}爻：{gua['yaoci'][bian_yao[1]-1]}（为主）")
        elif n == 3:
            print(f"  三爻变 → 本卦卦辞（贞）+ 变卦卦辞（悔）")
            print(f"  → 本卦卦辞：{gua['guaci']}")
            print(f"  → 变卦卦辞：{bgua['guaci']}")
        elif n == 4:
            no_bian = [y for y in range(1, 7) if y not in bian_yao]
            print(f"  四爻变 → 变卦不变爻爻辞，以下爻（第{no_bian[0]}爻）为主")
            print(f"  → 变卦第{no_bian[0]}爻：{bgua['yaoci'][no_bian[0]-1]}")
        elif n == 5:
            no_bian = [y for y in range(1, 7) if y not in bian_yao][0]
            print(f"  五爻变 → 变卦唯一不变爻（第{no_bian}爻）爻辞断之")
            print(f"  → 变卦第{no_bian}爻：{bgua['yaoci'][no_bian-1]}")
        elif n == 6:
            if seq == 1:
                print("  六爻全变（乾卦）→ 用九：见群龙无首，吉。")
            elif seq == 2:
                print("  六爻全变（坤卦）→ 用六：利永贞。")
            else:
                print(f"  六爻全变 → 变卦卦辞断之")
                print(f"  → 变卦卦辞：{bgua['guaci']}")
    else:
        print("📏 六爻皆静 → 本卦卦辞断之")
        print(f"  → 本卦卦辞：{gua['guaci']}")


def random_gua():
    """随机模拟金钱卦"""
    yao_list = [random.choice([6, 7, 8, 9]) for _ in range(6)]
    sym_map = {6: "⚋ 老阴", 7: "─── 少阳", 8: "─ ─ 少阴", 9: "⚊ 老阳"}
    print("\n🎲 随机模拟金钱卦：")
    for i, val in enumerate(yao_list):
        print(f"  第{i+1}爻：{sym_map[val]}")

    ben_gua_xia = 0
    ben_gua_shang = 0
    for i in range(3):
        if yao_list[i] in [7, 9]:
            ben_gua_xia |= (1 << i)
    for i in range(3, 6):
        if yao_list[i] in [7, 9]:
            ben_gua_shang |= (1 << (i - 3))

    def bin_to_gua(b):
        mapping = {0b111: 1, 0b110: 2, 0b101: 3, 0b100: 4,
                   0b011: 5, 0b010: 6, 0b001: 7, 0b000: 8}
        return mapping.get(b, 8)

    shang = bin_to_gua(ben_gua_shang)
    xia = bin_to_gua(ben_gua_xia)
    seq, gua = get_gua_by_shangxia(shang, xia)
    if gua:
        print_gua(seq, gua)
    return yao_list


def number_gua(n1, n2, n3=None):
    """数字卦起卦法"""
    # 上卦 = (第一个数 - 1) % 8 + 1
    shang_num = (n1 - 1) % 8 + 1
    # 下卦 = (第二个数 - 1) % 8 + 1
    xia_num = (n2 - 1) % 8 + 1
    # 动爻 = (第三个数 - 1) % 6 + 1
    if n3 is not None:
        dong_yao = (n3 - 1) % 6 + 1
    else:
        dong_yao = 0

    shang = NUM_TO_GUA[shang_num]
    xia = NUM_TO_GUA[xia_num]

    seq, gua = get_gua_by_shangxia(shang, xia)
    if gua:
        print(f"\n🎯 数字卦：{n1}, {n2}" + (f", {n3}" if n3 else ""))
        print(f"  上卦：{BAGUA[shang]['name']}({BAGUA[shang]['symbol']}) | "
              f"下卦：{BAGUA[xia]['name']}({BAGUA[xia]['symbol']})")
        if dong_yao:
            print(f"  动爻：第{dong_yao}爻")
        print_gua(seq, gua)


def time_gua():
    """时间起卦法（农历年月日）"""
    now = datetime.now()
    # 简化：用公历模拟
    year = now.year
    month = now.month
    day = now.day

    # 上卦：年数取余8
    shang_num = (year - 1) % 8 + 1
    # 下卦：月数取余8
    xia_num = (month - 1) % 8 + 1
    # 动爻：日数取余6
    dong_yao = (day - 1) % 6 + 1

    shang = NUM_TO_GUA[shang_num]
    xia = NUM_TO_GUA[xia_num]

    seq, gua = get_gua_by_shangxia(shang, xia)
    if gua:
        print(f"\n🕐 时间卦：{year}年{month}月{day}日")
        print(f"  上卦：{BAGUA[shang]['name']}({BAGUA[shang]['symbol']}) | "
              f"下卦：{BAGUA[xia]['name']}({BAGUA[xia]['symbol']}) | 动爻：第{dong_yao}爻")
        print_gua(seq, gua)


def list_all():
    """列出所有卦名"""
    print("\n📚 六十四卦总览：")
    print("=" * 60)
    for seq in range(1, 65):
        if seq in LIUSHISI_GUA:
            g = LIUSHISI_GUA[seq]
            print(f"  {seq:2d}. {g['name']:　<10s} {g['pinyin']:<30s} {g['hexin']}")
        else:
            print(f"  {seq:2d}. （待补充）")
    print("=" * 60)


def main():
    if len(sys.argv) < 2:
        print("六十四卦查询工具")
        print("用法：")
        print("  python bagua_lookup.py list              — 列出所有卦名")
        print("  python bagua_lookup.py name <卦名>        — 按卦名查询")
        print("  python bagua_lookup.py seq <序号>         — 按卦序查询")
        print("  python bagua_lookup.py money              — 金钱卦起卦（交互）")
        print("  python bagua_lookup.py random             — 随机模拟金钱卦")
        print("  python bagua_lookup.py number <a> <b> [c] — 数字卦起卦")
        print("  python bagua_lookup.py time               — 时间卦起卦")
        return

    cmd = sys.argv[1]

    if cmd == "list":
        list_all()
    elif cmd == "name":
        if len(sys.argv) < 3:
            print("请提供卦名，如：python bagua_lookup.py name 乾为天")
            return
        name = sys.argv[2]
        seq, gua = get_gua_by_name(name)
        if gua:
            print_gua(seq, gua)
        else:
            print(f"未找到卦名含「{name}」的卦，请尝试更精确的名称")
    elif cmd == "seq":
        if len(sys.argv) < 3:
            print("请提供卦序，如：python bagua_lookup.py seq 1")
            return
        seq = int(sys.argv[2])
        gua = get_gua_by_seq(seq)
        if gua:
            print_gua(seq, gua)
        else:
            print(f"未找到第{seq}卦")
    elif cmd == "money":
        money_gua()
    elif cmd == "random":
        random_gua()
    elif cmd == "number":
        if len(sys.argv) < 4:
            print("请提供至少2个数字，如：python bagua_lookup.py number 3 8 5")
            return
        n1 = int(sys.argv[2])
        n2 = int(sys.argv[3])
        n3 = int(sys.argv[4]) if len(sys.argv) > 4 else None
        number_gua(n1, n2, n3)
    elif cmd == "time":
        time_gua()
    else:
        print(f"未知命令：{cmd}")


if __name__ == "__main__":
    main()