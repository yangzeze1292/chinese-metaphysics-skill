# -*- coding: utf-8 -*-
"""
合婚评分计算脚本 · Hehun Scoring Engine
基于九维加权模型，计算双方八字合婚评分
"""

# ============================================================
# 基础数据
# ============================================================
TIAN_GAN = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
DI_ZHI   = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]

GAN_ZHI_60 = [TIAN_GAN[i%10]+DI_ZHI[i%12] for i in range(60)]

WX_TG = {"甲":"木","乙":"木","丙":"火","丁":"火","戊":"土","己":"土","庚":"金","辛":"金","壬":"水","癸":"水"}
WX_ZHI = {"子":"水","丑":"土","寅":"木","卯":"木","辰":"土","巳":"火","午":"火","未":"土","申":"金","酉":"金","戌":"土","亥":"水"}

YIN_YANG = {"甲":"阳","丙":"阳","戊":"阳","庚":"阳","壬":"阳",
            "乙":"阴","丁":"阴","己":"阴","辛":"阴","癸":"阴"}

NAYIN_WX = {
    "甲子":"金","乙丑":"金","丙寅":"火","丁卯":"火","戊辰":"木","己巳":"木",
    "庚午":"土","辛未":"土","壬申":"金","癸酉":"金","甲戌":"火","乙亥":"火",
    "丙子":"水","丁丑":"水","戊寅":"土","己卯":"土","庚辰":"金","辛巳":"金",
    "壬午":"木","癸未":"木","甲申":"水","乙酉":"水","丙戌":"土","丁亥":"土",
    "戊子":"火","己丑":"火","庚寅":"木","辛卯":"木","壬辰":"水","癸巳":"水",
    "甲午":"金","乙未":"金","丙申":"火","丁酉":"火","戊戌":"木","己亥":"木",
    "庚子":"土","辛丑":"土","壬寅":"金","癸卯":"金","甲辰":"火","乙巳":"火",
    "丙午":"水","丁未":"水","戊申":"土","己酉":"土","庚戌":"金","辛亥":"金",
    "壬子":"木","癸丑":"木","甲寅":"水","乙卯":"水","丙辰":"土","丁巳":"土",
    "戊午":"火","己未":"火","庚申":"木","辛酉":"木","壬戌":"水","癸亥":"水",
}

# 六合
LIU_HE = [("子","丑"),("寅","亥"),("卯","戌"),("辰","酉"),("巳","申"),("午","未")]
# 三合
SAN_HE = [("申","子","辰"),("寅","午","戌"),("亥","卯","未"),("巳","酉","丑")]
# 六冲
LIU_CHONG = [("子","午"),("丑","未"),("寅","申"),("卯","酉"),("辰","戌"),("巳","亥")]
# 六害
LIU_HAI = [("子","未"),("丑","午"),("寅","巳"),("卯","辰"),("申","亥"),("酉","戌")]

# 生肖名称
SHENG_XIAO = {"子":"鼠","丑":"牛","寅":"虎","卯":"兔","辰":"龙","巳":"蛇",
              "午":"马","未":"羊","申":"猴","酉":"鸡","戌":"狗","亥":"猪"}

# ============================================================
# 九维评分函数
# ============================================================

def dim1_nayin(m_nian_gz, f_nian_gz):
    """维度一：年柱纳音（权重10%）"""
    m_wx = NAYIN_WX.get(m_nian_gz, "")
    f_wx = NAYIN_WX.get(f_nian_gz, "")
    if not m_wx or not f_wx:
        return 0, "纳音数据缺失"
    
    sheng_chain = {"金":"水","水":"木","木":"火","火":"土","土":"金"}
    ke_chain = {"金":"木","木":"土","土":"水","水":"火","火":"金"}
    
    if sheng_chain.get(m_wx) == f_wx:
        return 3, f"男方{m_wx}生女方{f_wx}，吉"
    elif sheng_chain.get(f_wx) == m_wx:
        return 3, f"女方{f_wx}生男方{m_wx}，吉"
    elif m_wx == f_wx:
        return 2, f"同属{m_wx}，中"
    elif ke_chain.get(m_wx) == f_wx:
        return -1, f"男方{m_wx}克女方{f_wx}，注意"
    elif ke_chain.get(f_wx) == m_wx:
        return -1, f"女方{f_wx}克男方{m_wx}，注意"
    return 0, "无法判断"

def dim2_shengxiao(m_nian_zhi, f_nian_zhi):
    """维度二：生肖关系（权重10%）"""
    pair = (m_nian_zhi, f_nian_zhi)
    rpair = (f_nian_zhi, m_nian_zhi)
    
    for h in LIU_HE:
        if pair == h or rpair == h:
            return 3, f"六合（{SHENG_XIAO[m_nian_zhi]}与{SHENG_XIAO[f_nian_zhi]}合），大吉"
    
    for sh in SAN_HE:
        if m_nian_zhi in sh and f_nian_zhi in sh:
            return 2, f"三合，吉"
    
    for c in LIU_CHONG:
        if pair == c or rpair == c:
            return -2, f"六冲（{SHENG_XIAO[m_nian_zhi]}与{SHENG_XIAO[f_nian_zhi]}冲），注意"
    
    for h in LIU_HAI:
        if pair == h or rpair == h:
            return -2, f"六害（{SHENG_XIAO[m_nian_zhi]}与{SHENG_XIAO[f_nian_zhi]}害），注意"
    
    return 1, "无害无冲，一般"

def dim3_rizhu(m_ri_gan, m_ri_zhi, f_ri_gan, f_ri_zhi):
    """维度三：日柱关系（权重20%）"""
    # 日干关系
    sheng_chain = {"金":"水","水":"木","木":"火","火":"土","土":"金"}
    ke_chain = {"金":"木","木":"土","土":"水","水":"火","火":"金"}
    m_wx = WX_TG[m_ri_gan]
    f_wx = WX_TG[f_ri_gan]
    
    ri_gan_score = 0
    ri_gan_reason = ""
    if sheng_chain.get(m_wx) == f_wx:
        ri_gan_score = 3
        ri_gan_reason = f"男方{m_wx}生女方{f_wx}"
    elif sheng_chain.get(f_wx) == m_wx:
        ri_gan_score = 3
        ri_gan_reason = f"女方{f_wx}生男方{m_wx}"
    elif m_wx == f_wx:
        ri_gan_score = 2
        ri_gan_reason = f"同属{m_wx}，志趣相投"
    elif ke_chain.get(m_wx) == f_wx:
        ri_gan_score = 0
        ri_gan_reason = f"男方{m_wx}克女方{f_wx}"
    elif ke_chain.get(f_wx) == m_wx:
        ri_gan_score = 0
        ri_gan_reason = f"女方{f_wx}克男方{m_wx}"
    
    # 日支关系
    pair = (m_ri_zhi, f_ri_zhi)
    rpair = (f_ri_zhi, m_ri_zhi)
    ri_zhi_score = 0
    ri_zhi_reason = ""
    
    for h in LIU_HE:
        if pair == h or rpair == h:
            ri_zhi_score = 3
            ri_zhi_reason = "配偶宫六合"
            break
    if ri_zhi_score == 0:
        for sh in SAN_HE:
            if m_ri_zhi in sh and f_ri_zhi in sh:
                ri_zhi_score = 2
                ri_zhi_reason = "配偶宫三合"
                break
    if ri_zhi_score == 0:
        for c in LIU_CHONG:
            if pair == c or rpair == c:
                ri_zhi_score = -2
                ri_zhi_reason = "配偶宫六冲，注意"
                break
    if ri_zhi_score == 0:
        for h in LIU_HAI:
            if pair == h or rpair == h:
                ri_zhi_score = -2
                ri_zhi_reason = "配偶宫六害，注意"
                break
    if ri_zhi_score == 0:
        ri_zhi_score = 1
        ri_zhi_reason = "配偶宫无害"
    
    total = ri_gan_score + ri_zhi_score
    reason = f"日干：{ri_gan_reason}；日支：{ri_zhi_reason}"
    # 映射到 -4 到 +5 的范围
    if total >= 6: return 5, reason
    elif total >= 5: return 4, reason
    elif total >= 4: return 3, reason
    elif total >= 3: return 2, reason
    elif total >= 2: return 1, reason
    elif total >= 1: return 0, reason
    elif total >= 0: return -1, reason
    elif total >= -1: return -2, reason
    elif total >= -2: return -3, reason
    else: return -4, reason

def dim4_wuxing(m_wx_count, f_wx_count, m_yongshen, f_yongshen):
    """维度四：五行互补（权重15%）"""
    # 检查男方是否补女方用神
    m_bu_f = any(f_y in m_wx_count and m_wx_count[f_y] > 1.0 for f_y in f_yongshen)
    f_bu_m = any(m_y in f_wx_count and f_wx_count[m_y] > 1.0 for m_y in m_yongshen)
    
    if m_bu_f and f_bu_m:
        return 5, "双方互相补用神，五行互补极佳"
    elif m_bu_f:
        return 3, "男方补女方用神，单方互补"
    elif f_bu_m:
        return 3, "女方补男方用神，单方互补"
    
    # 检查是否冲忌神
    m_bad = any(f_y in m_wx_count and m_wx_count[f_y] > 1.5 for f_y in f_yongshen)
    if m_bad:
        return -2, "男方五行旺女方忌神，注意"
    return 1, "五行互不冲突，一般"

def dim5_shishen(m_ri_gan, f_ri_gan, m_gan_list, f_gan_list):
    """维度五：十神互动（权重10%）"""
    # 简化：以日干互动的生克关系为准
    m_wx = WX_TG[m_ri_gan]
    f_wx = WX_TG[f_ri_gan]
    sheng_chain = {"金":"水","水":"木","木":"火","火":"土","土":"金"}
    
    if sheng_chain.get(f_wx) == m_wx:
        return 3, "女方生日主生男方，滋养关系"
    elif sheng_chain.get(m_wx) == f_wx:
        return 2, "男方日主生女方，付出关系"
    elif m_wx == f_wx:
        return 2, "日主同五行，志趣相投"
    return 1, "十神互动一般"

def dim6_dayun(m_dayun, f_dayun, m_current_age, f_current_age):
    """维度六：大运同步（权重10%）"""
    # 简化判断：对比当前大运五行
    if not m_dayun or not f_dayun:
        return 1, "大运信息不足"
    
    m_dy_wx = WX_TG.get(m_dayun[0], "?")
    f_dy_wx = WX_TG.get(f_dayun[0], "?")
    
    sheng_chain = {"金":"水","水":"木","木":"火","火":"土","土":"金"}
    
    if m_dy_wx == f_dy_wx:
        return 3, "当前大运同为" + m_dy_wx + "，同步"
    elif sheng_chain.get(m_dy_wx) == f_dy_wx:
        return 2, "大运五行相生，节奏协调"
    return 1, "大运走势有差异，一般"

def dim7_shensha(m_shensha, f_shensha):
    """维度七：神煞配合（权重5%）"""
    score = 0
    reasons = []
    
    # 天乙贵人互见
    m_tb = m_shensha.get("天乙贵人", "")
    f_tb = f_shensha.get("天乙贵人", "")
    if m_tb and f_tb:
        score += 1
        reasons.append("双方均带天乙贵人")
    
    # 桃花相冲检查
    m_th = m_shensha.get("桃花", "")
    f_th = f_shensha.get("桃花", "")
    if m_th and f_th:
        for c in LIU_CHONG:
            if (m_th, f_th) == c or (f_th, m_th) == c:
                score -= 2
                reasons.append("桃花相冲，注意")
                break
    
    return max(-3, min(3, score)), "；".join(reasons) if reasons else "神煞无特殊冲突"

def dim8_yongshen(m_yongshen, f_yongshen, m_jishen, f_jishen):
    """维度八：用神配合（权重10%）"""
    m_set = set(m_yongshen)
    f_set = set(f_yongshen)
    common = m_set & f_set
    
    m_ji = set(m_jishen)
    f_ji = set(f_jishen)
    
    # 检查一方用神是否为另一方忌神
    conflict = (m_set & f_ji) or (f_set & m_ji)
    
    if common and not conflict:
        return 5, f"用神一致（{'、'.join(common)}），互相促进"
    elif common:
        return 3, f"用神有交集但部分冲突"
    elif not conflict:
        return 1, "用神不一致但不冲突"
    elif conflict:
        return -2, "用神冲突，需注意"
    return 0, "无法判断"

def dim9_zonghe(m_pillars, f_pillars):
    """维度九：综合感应（权重10%）"""
    he_count = 0
    chong_count = 0
    
    # 统计合冲
    m_zhi = [p[1] for p in m_pillars]
    f_zhi = [p[1] for p in f_pillars]
    
    for mz in m_zhi:
        for fz in f_zhi:
            pair = (mz, fz)
            rpair = (fz, mz)
            for h in LIU_HE:
                if pair == h or rpair == h:
                    he_count += 1
            for c in LIU_CHONG:
                if pair == c or rpair == c:
                    chong_count += 1
    
    if he_count > chong_count + 1:
        return 3, f"合多冲少（合{he_count}：冲{chong_count}），气场和谐"
    elif he_count > chong_count:
        return 1, f"合冲相当（合{he_count}：冲{chong_count}），一般"
    else:
        return -2, f"冲多合少（合{he_count}：冲{chong_count}），需磨合"

# ============================================================
# 加权计算
# ============================================================
WEIGHTS = [0.10, 0.10, 0.20, 0.15, 0.10, 0.10, 0.05, 0.10, 0.10]

def calc_hehun_score(scores):
    """计算加权总分，scores为9个维度的原始得分列表（-4到+5）"""
    raw_total = 0
    max_possible = 0
    for i, s in enumerate(scores):
        raw_total += s * WEIGHTS[i]
        max_possible += 5 * WEIGHTS[i]  # 每个维度最高+5
    
    # 映射到百分制
    # 原始分范围: -4*总权重 到 5*总权重, 即 -4 到 5
    # 映射到 0-100
    raw_min = -4 * sum(WEIGHTS)  # = -4
    raw_range = 9 * sum(WEIGHTS)  # 5 - (-4) = 9, 9 * 1.0 = 9
    percentage = (raw_total - raw_min) / raw_range * 100
    return round(percentage, 1)

def get_grade(score):
    """获取等级"""
    if score >= 80: return "上等婚"
    elif score >= 65: return "中上婚"
    elif score >= 50: return "中等婚"
    elif score >= 35: return "中下婚"
    else: return "下等婚"

# ============================================================
# 主函数
# ============================================================
def hehun_pipei(male, female):
    """
    合婚配对主函数
    
    male = {
        'nian_gz': '丙戌', 'yue_gz': '丁酉', 'ri_gz': '庚戌', 'shi_gz': '丁亥',
        'ri_gan': '庚', 'ri_zhi': '戌',
        'yongshen': ['火','木','水'], 'jishen': ['土','金'],
        'dayun': '庚子', 'current_age': 20,
        'wx_count': {'金':3,'木':0.5,'水':1,'火':3,'土':1.5},
        'shensha': {'天乙贵人':'丑','桃花':'卯'}
    }
    female = { ... same structure ... }
    """
    m_yg = male['nian_gz']; f_yg = female['nian_gz']
    m_nz = m_yg[1]; f_nz = f_yg[1]
    
    scores = []
    reasons = []
    
    # 维度一
    s1, r1 = dim1_nayin(m_yg, f_yg)
    scores.append(s1); reasons.append(r1)
    
    # 维度二
    s2, r2 = dim2_shengxiao(m_nz, f_nz)
    scores.append(s2); reasons.append(r2)
    
    # 维度三
    s3, r3 = dim3_rizhu(male['ri_gan'], male['ri_zhi'], female['ri_gan'], female['ri_zhi'])
    scores.append(s3); reasons.append(r3)
    
    # 维度四
    s4, r4 = dim4_wuxing(male['wx_count'], female['wx_count'], male['yongshen'], female['yongshen'])
    scores.append(s4); reasons.append(r4)
    
    # 维度五
    s5, r5 = dim5_shishen(male['ri_gan'], female['ri_gan'], [], [])
    scores.append(s5); reasons.append(r5)
    
    # 维度六
    s6, r6 = dim6_dayun(male['dayun'], female['dayun'], male['current_age'], female['current_age'])
    scores.append(s6); reasons.append(r6)
    
    # 维度七
    s7, r7 = dim7_shensha(male.get('shensha',{}), female.get('shensha',{}))
    scores.append(s7); reasons.append(r7)
    
    # 维度八
    s8, r8 = dim8_yongshen(male['yongshen'], female['yongshen'], male['jishen'], female['jishen'])
    scores.append(s8); reasons.append(r8)
    
    # 维度九
    pillars_m = [(male['nian_gz'][0],male['nian_gz'][1]),
                  (male['yue_gz'][0],male['yue_gz'][1]),
                  (male['ri_gz'][0],male['ri_gz'][1]),
                  (male['shi_gz'][0],male['shi_gz'][1])]
    pillars_f = [(female['nian_gz'][0],female['nian_gz'][1]),
                  (female['yue_gz'][0],female['yue_gz'][1]),
                  (female['ri_gz'][0],female['ri_gz'][1]),
                  (female['shi_gz'][0],female['shi_gz'][1])]
    s9, r9 = dim9_zonghe(pillars_m, pillars_f)
    scores.append(s9); reasons.append(r9)
    
    total = calc_hehun_score(scores)
    grade = get_grade(total)
    
    return {
        'scores': scores,
        'reasons': reasons,
        'total': total,
        'grade': grade,
        'weights': WEIGHTS
    }

# ============================================================
# 演示
# ============================================================
if __name__ == "__main__":
    print("=" * 70)
    print("  合婚评分引擎 · Hehun Scoring Engine")
    print("=" * 70)
    print()
    print("  九维模型：")
    print("  维度一：年柱纳音（10%）")
    print("  维度二：生肖关系（10%）")
    print("  维度三：日柱关系（20%）★ 权重最高")
    print("  维度四：五行互补（15%）")
    print("  维度五：十神互动（10%）")
    print("  维度六：大运同步（10%）")
    print("  维度七：神煞配合（5%）")
    print("  维度八：用神配合（10%）")
    print("  维度九：综合感应（10%）")
    print()
    print("  等级标准：")
    print("  80-100：上等婚  65-79：中上婚  50-64：中等婚")
    print("  35-49：中下婚  0-34：下等婚")
    print()
    print("  使用方法：")
    print("  result = hehun_pipei(male_dict, female_dict)")
    print("  male_dict = {nian_gz, yue_gz, ri_gz, shi_gz, ri_gan, ri_zhi,")
    print("              yongshen, jishen, dayun, current_age, wx_count, shensha}")
    print()
    
    # 演示：丙戌+丁亥 配对
    male = {
        'nian_gz': '丙戌', 'yue_gz': '丁酉', 'ri_gz': '庚戌', 'shi_gz': '丁亥',
        'ri_gan': '庚', 'ri_zhi': '戌',
        'yongshen': ['火','木','水'], 'jishen': ['土','金'],
        'dayun': '庚子', 'current_age': 20,
        'wx_count': {'金':3,'木':0.5,'水':1,'火':3,'土':1.5},
        'shensha': {'天乙贵人':'丑','桃花':'卯'}
    }
    female = {
        'nian_gz': '丁亥', 'yue_gz': '戊申', 'ri_gz': '己亥', 'shi_gz': '丁卯',
        'ri_gan': '己', 'ri_zhi': '亥',
        'yongshen': ['火','土'], 'jishen': ['水','木','金'],
        'dayun': '庚戌', 'current_age': 19,
        'wx_count': {'金':0.5,'木':1.5,'水':1.5,'火':2,'土':2.5},
        'shensha': {'天乙贵人':'申','桃花':''}
    }
    
    result = hehun_pipei(male, female)
    
    dim_names = ["年柱纳音","生肖关系","日柱关系","五行互补","十神互动","大运同步","神煞配合","用神配合","综合感应"]
    
    print("=" * 70)
    print("  演示：男方 丙戌 丁酉 庚戌 丁亥 × 女方 丁亥 戊申 己亥 丁卯")
    print("=" * 70)
    print()
    for i, (name, s, r) in enumerate(zip(dim_names, result['scores'], result['reasons'])):
        pct = result['weights'][i] * 100
        print(f"  {name}（{pct:.0f}%）：得分 {s:+d}  —  {r}")
    print(f"\n  ★ 加权总分：{result['total']:.1f} / 100  →  {result['grade']}")
    print()