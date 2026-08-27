#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
六十四卦查询工具
支持：按卦名/卦序/上下卦查询、金钱卦起卦、数字卦起卦
"""

import sys
import random
from datetime import datetime

# 尽量以 UTF-8 输出，避免 Windows GBK 控制台打印卦符时报错
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

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
        "name": '乾为天',
        "short_name": '乾',
        "pinyin": 'qián',
        "shang": 1,
        "xia": 1,
        "guaci": '元，亨，利，贞。',
        "tuan": '大哉乾元，万物资始，乃统天。云行雨施，品物流形。大明终始，六位时成，时乘六龙以御天。乾道变化，各正性命，保合太和，乃利贞。首出庶物，万国咸宁。',
        "daxiang": '天行健，君子以自强不息。',
        "yaoci": ['初九：潜龙勿用。', '九二：见龙在田，利见大人。', '九三：君子终日乾乾，夕惕若厉，无咎。', '九四：或跃在渊，无咎。', '九五：飞龙在天，利见大人。', '上九：亢龙有悔。', '用九：见群龙无首，吉。'],
        "hexin": '天道刚健，创生万物，君子以自强不息',
        "keywords": ['天', '健', '元', '创造', '刚健', '君子', '龙', '阳', '始']
    },
    2: {
        "name": '坤为地',
        "short_name": '坤',
        "pinyin": 'kūn',
        "shang": 8,
        "xia": 8,
        "guaci": '元，亨，利牝马之贞。君子有攸往，先迷后得主，利。西南得朋，东北丧朋。安贞吉。',
        "tuan": '至哉坤元，万物资生，乃顺承天。坤厚载物，德合无疆。含弘光大，品物咸亨。牝马地类，行地无疆，柔顺利贞。君子攸行，先迷失道，后顺得常。西南得朋，乃与类行；东北丧朋，乃终有庆。安贞之吉，应地无疆。',
        "daxiang": '地势坤，君子以厚德载物。',
        "yaoci": ['初六：履霜，坚冰至。', '六二：直方大，不习无不利。', '六三：含章可贞，或从王事，无成有终。', '六四：括囊，无咎无誉。', '六五：黄裳，元吉。', '上六：龙战于野，其血玄黄。', '用六：利永贞。'],
        "hexin": '地道柔顺，承载万物，君子以厚德载物',
        "keywords": ['地', '顺', '含', '承载', '柔顺', '牝马', '臣道', '阴', '成']
    },
    3: {
        "name": '水雷屯',
        "short_name": '屯',
        "pinyin": 'zhūn',
        "shang": 6,
        "xia": 4,
        "guaci": '元，亨，利，贞。勿用有攸往，利建侯。',
        "tuan": '屯，刚柔始交而难生。动乎险中，大亨贞。雷雨之动满盈，天造草昧，宜建侯而不宁。',
        "daxiang": '云雷，屯。君子以经纶。',
        "yaoci": ['初九：磐桓，利居贞，利建侯。', '六二：屯如邅如，乘马班如。匪寇婚媾，女子贞不字，十年乃字。', '六三：即鹿无虞，惟入于林中，君子几不如舍，往吝。', '六四：乘马班如，求婚媾，往吉，无不利。', '九五：屯其膏，小贞吉，大贞凶。', '上六：乘马班如，泣血涟如。'],
        "hexin": '万物始生，艰难初创，宜建侯而不宁',
        "keywords": ['始生', '艰难', '初创', '建侯', '动乎险中', '经纶', '屯难']
    },
    4: {
        "name": '山水蒙',
        "short_name": '蒙',
        "pinyin": 'méng',
        "shang": 7,
        "xia": 6,
        "guaci": '亨。匪我求童蒙，童蒙求我。初筮告，再三渎，渎则不告。利贞。',
        "tuan": '蒙，山下有险，险而止，蒙。蒙亨，以亨行时中也。匪我求童蒙，童蒙求我，志应也。初筮告，以刚中也。再三渎，渎则不告，渎蒙也。蒙以养正，圣功也。',
        "daxiang": '山下出泉，蒙。君子以果行育德。',
        "yaoci": ['初六：发蒙，利用刑人，用说桎梏，以往吝。', '九二：包蒙，吉。纳妇，吉。子克家。', '六三：勿用取女，见金夫，不有躬，无攸利。', '六四：困蒙，吝。', '六五：童蒙，吉。', '上九：击蒙，不利为寇，利御寇。'],
        "hexin": '启蒙发智，教育之道，童蒙求我，非我求童蒙',
        "keywords": ['启蒙', '教育', '童蒙', '养正', '发蒙', '求教', '果行育德']
    },
    5: {
        "name": '水天需',
        "short_name": '需',
        "pinyin": 'xū',
        "shang": 6,
        "xia": 1,
        "guaci": '有孚，光亨，贞吉。利涉大川。',
        "tuan": '需，须也，险在前也。刚健而不陷，其义不困穷矣。需有孚，光亨，贞吉，位乎天位，以正中也。利涉大川，往有功也。',
        "daxiang": '云上于天，需。君子以饮食宴乐。',
        "yaoci": ['初九：需于郊，利用恒，无咎。', '九二：需于沙，小有言，终吉。', '九三：需于泥，致寇至。', '六四：需于血，出自穴。', '九五：需于酒食，贞吉。', '上六：入于穴，有不速之客三人来，敬之终吉。'],
        "hexin": '等待时机，饮食宴乐，险在前而刚健不陷',
        "keywords": ['等待', '需待', '饮食', '宴乐', '时机', '险在前', '耐心']
    },
    6: {
        "name": '天水讼',
        "short_name": '讼',
        "pinyin": 'sòng',
        "shang": 1,
        "xia": 6,
        "guaci": '有孚，窒惕，中吉，终凶。利见大人，不利涉大川。',
        "tuan": '讼，上刚下险，险而健，讼。讼有孚，窒惕中吉，刚来而得中也。终凶，讼不可成也。利见大人，尚中正也。不利涉大川，入于渊也。',
        "daxiang": '天与水违行，讼。君子以作事谋始。',
        "yaoci": ['初六：不永所事，小有言，终吉。', '九二：不克讼，归而逋，其邑人三百户，无眚。', '六三：食旧德，贞厉，终吉。或从王事，无成。', '九四：不克讼，复即命，渝安贞，吉。', '九五：讼，元吉。', '上九：或锡之鞶带，终朝三褫之。'],
        "hexin": '争讼辩论，宜见大人，不宜涉大川',
        "keywords": ['争讼', '辩论', '冲突', '作事谋始', '天水违行', '中正', '惕']
    },
    7: {
        "name": '地水师',
        "short_name": '师',
        "pinyin": 'shī',
        "shang": 8,
        "xia": 6,
        "guaci": '贞，丈人吉，无咎。',
        "tuan": '师，众也。贞，正也。能以众正，可以王矣。刚中而应，行险而顺，以此毒天下，而民从之，吉又何咎矣。',
        "daxiang": '地中有水，师。君子以容民畜众。',
        "yaoci": ['初六：师出以律，否臧凶。', '九二：在师中，吉无咎，王三锡命。', '六三：师或舆尸，凶。', '六四：师左次，无咎。', '六五：田有禽，利执言，无咎。长子帅师，弟子舆尸，贞凶。', '上六：大君有命，开国承家，小人勿用。'],
        "hexin": '军队出征，师出以律，丈人吉',
        "keywords": ['军队', '出征', '师律', '容民畜众', '战争', '行险', '丈人']
    },
    8: {
        "name": '水地比',
        "short_name": '比',
        "pinyin": 'bǐ',
        "shang": 6,
        "xia": 8,
        "guaci": '吉。原筮，元永贞，无咎。不宁方来，后夫凶。',
        "tuan": '比，吉也。比，辅也，下顺从也。原筮，元永贞，无咎，以刚中也。不宁方来，上下应也。后夫凶，其道穷也。',
        "daxiang": '地上有水，比。先王以建万国，亲诸侯。',
        "yaoci": ['初六：有孚，比之，无咎。有孚盈缶，终来有它，吉。', '六二：比之自内，贞吉。', '六三：比之匪人。', '六四：外比之，贞吉。', '九五：显比，王用三驱，失前禽，邑人不诫，吉。', '上六：比之无首，凶。'],
        "hexin": '亲附团结，建万国亲诸侯，吉',
        "keywords": ['亲比', '团结', '亲附', '建万国', '亲诸侯', '上下应', '辅']
    },
    9: {
        "name": '风天小畜',
        "short_name": '小畜',
        "pinyin": 'xiǎo xù',
        "shang": 5,
        "xia": 1,
        "guaci": '亨。密云不雨，自我西郊。',
        "tuan": '小畜，柔得位而上下应之，曰小畜。健而巽，刚中而志行，乃亨。密云不雨，尚往也。自我西郊，施未行也。',
        "daxiang": '风行天上，小畜。君子以懿文德。',
        "yaoci": ['初九：复自道，何其咎，吉。', '九二：牵复，吉。', '九三：舆说辐，夫妻反目。', '六四：有孚，血去惕出，无咎。', '九五：有孚挛如，富以其邻。', '上九：既雨既处，尚德载，妇贞厉，月几望，君子征凶。'],
        "hexin": '小有蓄积，以懿文德，密云不雨',
        "keywords": ['小蓄', '积蓄', '懿文德', '密云不雨', '等待', '积累', '柔得位']
    },
    10: {
        "name": '天泽履',
        "short_name": '履',
        "pinyin": 'lǚ',
        "shang": 1,
        "xia": 2,
        "guaci": '履虎尾，不咥人，亨。',
        "tuan": '履，柔履刚也。说而应乎乾，是以履虎尾，不咥人，亨。刚中正，履帝位而不疚，光明也。',
        "daxiang": '上天下泽，履。君子以辨上下，定民志。',
        "yaoci": ['初九：素履，往无咎。', '九二：履道坦坦，幽人贞吉。', '六三：眇能视，跛能履，履虎尾，咥人，凶。武人为于大君。', '九四：履虎尾，愬愬，终吉。', '九五：夬履，贞厉。', '上九：视履考祥，其旋元吉。'],
        "hexin": '履行实践，履虎尾不咥人，辨上下定民志',
        "keywords": ['履行', '实践', '礼', '履虎尾', '辨上下', '定民志', '危而安']
    },
    11: {
        "name": '地天泰',
        "short_name": '泰',
        "pinyin": 'tài',
        "shang": 8,
        "xia": 1,
        "guaci": '小往大来，吉，亨。',
        "tuan": '泰，小往大来，吉亨，则是天地交而万物通也，上下交而其志同也。内阳而外阴，内健而外顺，内君子而外小人，君子道长，小人道消也。',
        "daxiang": '天地交，泰。后以财成天地之道，辅相天地之宜，以左右民。',
        "yaoci": ['初九：拔茅茹，以其汇，征吉。', '九二：包荒，用冯河，不遐遗，朋亡，得尚于中行。', '九三：无平不陂，无往不复，艰贞无咎。勿恤其孚，于食有福。', '六四：翩翩，不富以其邻，不戒以孚。', '六五：帝乙归妹，以祉元吉。', '上六：城复于隍，勿用师，自邑告命，贞吝。'],
        "hexin": '天地交泰，万物通，小往大来，吉亨',
        "keywords": ['通泰', '亨通', '天地交', '小往大来', '辅相天地', '安泰']
    },
    12: {
        "name": '天地否',
        "short_name": '否',
        "pinyin": 'pǐ',
        "shang": 1,
        "xia": 8,
        "guaci": '否之匪人，不利君子贞，大往小来。',
        "tuan": '否之匪人，不利君子贞，大往小来，则是天地不交而万物不通也，上下不交而天下无邦也。内阴而外阳，内柔而外刚，内小人而外君子，小人道长，君子道消也。',
        "daxiang": '天地不交，否。君子以俭德辟难，不可荣以禄。',
        "yaoci": ['初六：拔茅茹，以其汇，贞吉，亨。', '六二：包承，小人吉，大人否，亨。', '六三：包羞。', '九四：有命，无咎，畴离祉。', '九五：休否，大人吉。其亡其亡，系于苞桑。', '上九：倾否，先否后喜。'],
        "hexin": '天地闭塞，不利君子贞，大往小来',
        "keywords": ['闭塞', '不通', '否塞', '俭德辟难', '天地不交', '君子退', '小人进']
    },
    13: {
        "name": '天火同人',
        "short_name": '同人',
        "pinyin": 'tóng rén',
        "shang": 1,
        "xia": 3,
        "guaci": '同人于野，亨。利涉大川，利君子贞。',
        "tuan": '',
        "daxiang": '天与火，同人。君子以类族辨物。',
        "yaoci": [],
        "hexin": '与人合同，同人于野，类族辨物',
        "keywords": ['同人', '合同', '大同', '类族辨物', '与人和同', '通志']
    },
    14: {
        "name": '火天大有',
        "short_name": '大有',
        "pinyin": 'dà yǒu',
        "shang": 3,
        "xia": 1,
        "guaci": '元亨。',
        "tuan": '',
        "daxiang": '火在天上，大有。君子以遏恶扬善，顺天休命。',
        "yaoci": [],
        "hexin": '盛大丰有，遏恶扬善，顺天休命',
        "keywords": ['大有', '丰有', '遏恶扬善', '顺天休命', '富有']
    },
    15: {
        "name": '地山谦',
        "short_name": '谦',
        "pinyin": 'qiān',
        "shang": 8,
        "xia": 7,
        "guaci": '亨，君子有终。',
        "tuan": '',
        "daxiang": '地中有山，谦。君子以裒多益寡，称物平施。',
        "yaoci": [],
        "hexin": '谦逊自牧，裒多益寡，称物平施',
        "keywords": ['谦逊', '谦退', '卑以自牧', '裒多益寡', '称物平施', '有终']
    },
    16: {
        "name": '雷地豫',
        "short_name": '豫',
        "pinyin": 'yù',
        "shang": 4,
        "xia": 8,
        "guaci": '利建侯行师。',
        "tuan": '',
        "daxiang": '雷出地奋，豫。先王以作乐崇德，殷荐之上帝，以配祖考。',
        "yaoci": [],
        "hexin": '和乐豫悦，作乐崇德，殷荐之上帝',
        "keywords": ['豫悦', '和乐', '作乐崇德', '利建侯行师', '豫奋']
    },
    17: {
        "name": '泽雷随',
        "short_name": '随',
        "pinyin": 'suí',
        "shang": 2,
        "xia": 4,
        "guaci": '元，亨，利，贞，无咎。',
        "tuan": '',
        "daxiang": '泽中有雷，随。君子以向晦入宴息。',
        "yaoci": [],
        "hexin": '随时随从，向晦入宴息',
        "keywords": ['随从', '随时', '天下随时', '向晦宴息', '元亨利贞']
    },
    18: {
        "name": '山风蛊',
        "short_name": '蛊',
        "pinyin": 'gǔ',
        "shang": 7,
        "xia": 5,
        "guaci": '元亨，利涉大川。先甲三日，后甲三日。',
        "tuan": '',
        "daxiang": '山下有风，蛊。君子以振民育德。',
        "yaoci": [],
        "hexin": '弊坏整治，振民育德',
        "keywords": ['蛊坏', '整治', '振民育德', '先甲三日', '后甲三日', '革新']
    },
    19: {
        "name": '地泽临',
        "short_name": '临',
        "pinyin": 'lín',
        "shang": 8,
        "xia": 2,
        "guaci": '元，亨，利，贞。至于八月有凶。',
        "tuan": '',
        "daxiang": '泽上有地，临。君子以教思无穷，容保民无疆。',
        "yaoci": [],
        "hexin": '临下治民，教思无穷，保民无疆',
        "keywords": ['临下', '治民', '教思无穷', '保民', '八月有凶', '临莅']
    },
    20: {
        "name": '风地观',
        "short_name": '观',
        "pinyin": 'guān',
        "shang": 5,
        "xia": 8,
        "guaci": '盥而不荐，有孚颙若。',
        "tuan": '',
        "daxiang": '风行地上，观。先王以省方观民设教。',
        "yaoci": [],
        "hexin": '观察省视，省方观民设教',
        "keywords": ['观察', '省视', '盥而不荐', '省方观民', '设教', '观仰']
    },
    21: {
        "name": '火雷噬嗑',
        "short_name": '噬嗑',
        "pinyin": 'shì hé',
        "shang": 3,
        "xia": 4,
        "guaci": '亨，利用狱。',
        "tuan": '',
        "daxiang": '雷电，噬嗑。先王以明罚敕法。',
        "yaoci": [],
        "hexin": '咬合决断，明罚敕法',
        "keywords": ['噬嗑', '咬合', '决断', '利用狱', '明罚敕法', '口中有物']
    },
    22: {
        "name": '山火贲',
        "short_name": '贲',
        "pinyin": 'bì',
        "shang": 7,
        "xia": 3,
        "guaci": '亨，小利有攸往。',
        "tuan": '',
        "daxiang": '山下有火，贲。君子以明庶政，无敢折狱。',
        "yaoci": [],
        "hexin": '文饰美化，明庶政，无敢折狱',
        "keywords": ['贲饰', '文饰', '美化', '明庶政', '无敢折狱', '小利有攸往']
    },
    23: {
        "name": '山地剥',
        "short_name": '剥',
        "pinyin": 'bō',
        "shang": 7,
        "xia": 8,
        "guaci": '不利有攸往。',
        "tuan": '',
        "daxiang": '山附于地，剥。上以厚下安宅。',
        "yaoci": [],
        "hexin": '剥落衰败，上以厚下安宅',
        "keywords": ['剥落', '衰败', '顺而止之', '厚下安宅', '小人长', '不利有攸往']
    },
    24: {
        "name": '地雷复',
        "short_name": '复',
        "pinyin": 'fù',
        "shang": 8,
        "xia": 4,
        "guaci": '亨。出入无疾，朋来无咎。反复其道，七日来复。利有攸往。',
        "tuan": '',
        "daxiang": '雷在地中，复。先王以至日闭关，商旅不行，后不省方。',
        "yaoci": [],
        "hexin": '回复复兴，至日闭关，商旅不行',
        "keywords": ['回复', '复归', '一阳来复', '七日来复', '闭关', '天地之心']
    },
    25: {
        "name": '天雷无妄',
        "short_name": '无妄',
        "pinyin": 'wú wàng',
        "shang": 1,
        "xia": 4,
        "guaci": '元，亨，利，贞。其匪正有眚，不利有攸往。',
        "tuan": '',
        "daxiang": '天下雷行，物与无妄。先王以茂对时育万物。',
        "yaoci": [],
        "hexin": '真实无妄，茂对时育万物',
        "keywords": ['无妄', '真实', '不妄为', '天命不佑', '茂对时', '育万物']
    },
    26: {
        "name": '山天大畜',
        "short_name": '大畜',
        "pinyin": 'dà xù',
        "shang": 7,
        "xia": 1,
        "guaci": '利贞。不家食，吉。利涉大川。',
        "tuan": '',
        "daxiang": '天在山中，大畜。君子以多识前言往行，以畜其德。',
        "yaoci": [],
        "hexin": '大蓄积德，多识前言往行，以畜其德',
        "keywords": ['大蓄', '积德', '多识前言', '畜德', '利涉大川', '尚贤']
    },
    27: {
        "name": '山雷颐',
        "short_name": '颐',
        "pinyin": 'yí',
        "shang": 7,
        "xia": 4,
        "guaci": '贞吉。观颐，自求口实。',
        "tuan": '',
        "daxiang": '山下有雷，颐。君子以慎言语，节饮食。',
        "yaoci": [],
        "hexin": '颐养口体，慎言语，节饮食',
        "keywords": ['颐养', '养正', '慎言语', '节饮食', '自求口实', '养身']
    },
    28: {
        "name": '泽风大过',
        "short_name": '大过',
        "pinyin": 'dà guò',
        "shang": 2,
        "xia": 5,
        "guaci": '栋桡，利有攸往，亨。',
        "tuan": '',
        "daxiang": '泽灭木，大过。君子以独立不惧，遁世无闷。',
        "yaoci": [],
        "hexin": '大为过甚，独立不惧，遁世无闷',
        "keywords": ['大过', '过甚', '栋桡', '独立不惧', '遁世无闷', '非常之时']
    },
    29: {
        "name": '坎为水',
        "short_name": '坎',
        "pinyin": 'kǎn',
        "shang": 6,
        "xia": 6,
        "guaci": '有孚，维心亨，行有尚。',
        "tuan": '',
        "daxiang": '水洊至，习坎。君子以常德行，习教事。',
        "yaoci": [],
        "hexin": '重重险陷，常德行，习教事',
        "keywords": ['坎险', '重险', '维心亨', '常德行', '习教事', '水洊至']
    },
    30: {
        "name": '离为火',
        "short_name": '离',
        "pinyin": 'lí',
        "shang": 3,
        "xia": 3,
        "guaci": '利贞，亨。畜牝牛，吉。',
        "tuan": '',
        "daxiang": '明两作，离。大人以继明照于四方。',
        "yaoci": [],
        "hexin": '附丽光明，继明照于四方',
        "keywords": ['离丽', '光明', '柔丽乎中正', '畜牝牛', '继明照四方', '文明']
    },
    31: {
        "name": '泽山咸',
        "short_name": '咸',
        "pinyin": 'xián',
        "shang": 2,
        "xia": 7,
        "guaci": '亨，利贞。取女吉。',
        "tuan": '',
        "daxiang": '山上有泽，咸。君子以虚受人。',
        "yaoci": [],
        "hexin": '男女感应，虚受人',
        "keywords": ['感应', '咸感', '男女', '虚受人', '取女吉']
    },
    32: {
        "name": '雷风恒',
        "short_name": '恒',
        "pinyin": 'héng',
        "shang": 4,
        "xia": 5,
        "guaci": '亨，无咎，利贞，利有攸往。',
        "tuan": '',
        "daxiang": '雷风，恒。君子以立不易方。',
        "yaoci": [],
        "hexin": '恒久不变，立不易方',
        "keywords": ['恒久', '不易', '立不易方', '夫妇', '刚上柔下']
    },
    33: {
        "name": '天山遁',
        "short_name": '遁',
        "pinyin": 'dùn',
        "shang": 1,
        "xia": 7,
        "guaci": '亨，小利贞。',
        "tuan": '',
        "daxiang": '天下有山，遁。君子以远小人，不恶而严。',
        "yaoci": [],
        "hexin": '退避隐遁，远小人不恶而严',
        "keywords": ['退避', '隐遁', '远小人', '不恶而严', '小利贞']
    },
    34: {
        "name": '雷天大壮',
        "short_name": '大壮',
        "pinyin": 'dà zhuàng',
        "shang": 4,
        "xia": 1,
        "guaci": '利贞。',
        "tuan": '',
        "daxiang": '雷在天上，大壮。君子以非礼弗履。',
        "yaoci": [],
        "hexin": '盛大强壮，非礼弗履',
        "keywords": ['大壮', '强壮', '非礼弗履', '利贞', '刚以动']
    },
    35: {
        "name": '火地晋',
        "short_name": '晋',
        "pinyin": 'jìn',
        "shang": 3,
        "xia": 8,
        "guaci": '康侯用锡马蕃庶，昼日三接。',
        "tuan": '',
        "daxiang": '明出地上，晋。君子以自昭明德。',
        "yaoci": [],
        "hexin": '前进晋升，自昭明德',
        "keywords": ['晋进', '晋升', '自昭明德', '康侯', '昼日三接']
    },
    36: {
        "name": '地火明夷',
        "short_name": '明夷',
        "pinyin": 'míng yí',
        "shang": 8,
        "xia": 3,
        "guaci": '利艰贞。',
        "tuan": '',
        "daxiang": '明入地中，明夷。君子以莅众，用晦而明。',
        "yaoci": [],
        "hexin": '光明受伤，用晦而明',
        "keywords": ['明夷', '伤明', '用晦而明', '利艰贞', '暗君在上']
    },
    37: {
        "name": '风火家人',
        "short_name": '家人',
        "pinyin": 'jiā rén',
        "shang": 5,
        "xia": 3,
        "guaci": '利女贞。',
        "tuan": '',
        "daxiang": '风自火出，家人。君子以言有物而行有恒。',
        "yaoci": [],
        "hexin": '家庭伦理，言有物而行有恒',
        "keywords": ['家人', '家庭', '言有物', '行有恒', '利女贞', '正家']
    },
    38: {
        "name": '火泽睽',
        "short_name": '睽',
        "pinyin": 'kuí',
        "shang": 3,
        "xia": 2,
        "guaci": '小事吉。',
        "tuan": '',
        "daxiang": '上火下泽，睽。君子以同而异。',
        "yaoci": [],
        "hexin": '乖离睽异，以同而异',
        "keywords": ['睽乖', '乖离', '以同而异', '小事吉', '二女同居']
    },
    39: {
        "name": '水山蹇',
        "short_name": '蹇',
        "pinyin": 'jiǎn',
        "shang": 6,
        "xia": 7,
        "guaci": '利西南，不利东北。利见大人，贞吉。',
        "tuan": '',
        "daxiang": '山上有水，蹇。君子以反身修德。',
        "yaoci": [],
        "hexin": '艰难蹇涩，反身修德',
        "keywords": ['蹇难', '艰难', '反身修德', '利西南', '见险而止']
    },
    40: {
        "name": '雷水解',
        "short_name": '解',
        "pinyin": 'xiè',
        "shang": 4,
        "xia": 6,
        "guaci": '利西南。无所往，其来复吉。有攸往，夙吉。',
        "tuan": '',
        "daxiang": '雷雨作，解。君子以赦过宥罪。',
        "yaoci": [],
        "hexin": '解除困难，赦过宥罪',
        "keywords": ['解除', '解缓', '赦过宥罪', '利西南', '雷雨作']
    },
    41: {
        "name": '山泽损',
        "short_name": '损',
        "pinyin": 'sǔn',
        "shang": 7,
        "xia": 2,
        "guaci": '有孚，元吉，无咎，可贞，利有攸往。曷之用？二簋可用享。',
        "tuan": '',
        "daxiang": '山下有泽，损。君子以惩忿窒欲。',
        "yaoci": [],
        "hexin": '损下益上，惩忿窒欲',
        "keywords": ['损减', '损下益上', '惩忿窒欲', '二簋可用享', '有孚']
    },
    42: {
        "name": '风雷益',
        "short_name": '益',
        "pinyin": 'yì',
        "shang": 5,
        "xia": 4,
        "guaci": '利有攸往，利涉大川。',
        "tuan": '',
        "daxiang": '风雷，益。君子以见善则迁，有过则改。',
        "yaoci": [],
        "hexin": '增益利民，见善则迁，有过则改',
        "keywords": ['增益', '利民', '见善则迁', '有过则改', '利涉大川']
    },
    43: {
        "name": '泽天夬',
        "short_name": '夬',
        "pinyin": 'guài',
        "shang": 2,
        "xia": 1,
        "guaci": '扬于王庭，孚号有厉。告自邑，不利即戎。利有攸往。',
        "tuan": '',
        "daxiang": '泽上于天，夬。君子以施禄及下，居德则忌。',
        "yaoci": [],
        "hexin": '决断果决，施禄及下',
        "keywords": ['夬决', '决断', '施禄及下', '扬于王庭', '刚决柔']
    },
    44: {
        "name": '天风姤',
        "short_name": '姤',
        "pinyin": 'gòu',
        "shang": 1,
        "xia": 5,
        "guaci": '女壮，勿用取女。',
        "tuan": '',
        "daxiang": '天下有风，姤。后以施命诰四方。',
        "yaoci": [],
        "hexin": '不期而遇，施命诰四方',
        "keywords": ['姤遇', '相遇', '施命诰四方', '女壮勿取', '一阴始生']
    },
    45: {
        "name": '泽地萃',
        "short_name": '萃',
        "pinyin": 'cuì',
        "shang": 2,
        "xia": 8,
        "guaci": '亨，王假有庙。利见大人，亨，利贞。用大牲吉。利有攸往。',
        "tuan": '',
        "daxiang": '泽上于地，萃。君子以除戎器，戒不虞。',
        "yaoci": [],
        "hexin": '聚集会萃，除戎器，戒不虞',
        "keywords": ['萃聚', '聚集', '除戎器', '戒不虞', '王假有庙']
    },
    46: {
        "name": '地风升',
        "short_name": '升',
        "pinyin": 'shēng',
        "shang": 8,
        "xia": 5,
        "guaci": '元亨，用见大人，勿恤。南征吉。',
        "tuan": '',
        "daxiang": '地中生木，升。君子以顺德，积小以高大。',
        "yaoci": [],
        "hexin": '上升渐进，顺德积小以高大',
        "keywords": ['上升', '渐进', '顺德', '积小以高大', '南征吉']
    },
    47: {
        "name": '泽水困',
        "short_name": '困',
        "pinyin": 'kùn',
        "shang": 2,
        "xia": 6,
        "guaci": '亨，贞，大人吉，无咎。有言不信。',
        "tuan": '',
        "daxiang": '泽无水，困。君子以致命遂志。',
        "yaoci": [],
        "hexin": '困穷受困，致命遂志',
        "keywords": ['困穷', '受困', '致命遂志', '有言不信', '刚掩']
    },
    48: {
        "name": '水风井',
        "short_name": '井',
        "pinyin": 'jǐng',
        "shang": 6,
        "xia": 5,
        "guaci": '改邑不改井，无丧无得，往来井井。汔至亦未繘井，羸其瓶，凶。',
        "tuan": '',
        "daxiang": '木上有水，井。君子以劳民劝相。',
        "yaoci": [],
        "hexin": '井养不穷，劳民劝相',
        "keywords": ['井养', '不穷', '劳民劝相', '改邑不改井', '往来井井']
    },
    49: {
        "name": '泽火革',
        "short_name": '革',
        "pinyin": 'gé',
        "shang": 2,
        "xia": 3,
        "guaci": '巳日乃孚。元亨，利贞，悔亡。',
        "tuan": '',
        "daxiang": '泽中有火，革。君子以治历明时。',
        "yaoci": [],
        "hexin": '变革革命，治历明时',
        "keywords": ['变革', '革命', '治历明时', '巳日乃孚', '顺天应人']
    },
    50: {
        "name": '火风鼎',
        "short_name": '鼎',
        "pinyin": 'dǐng',
        "shang": 3,
        "xia": 5,
        "guaci": '元吉，亨。',
        "tuan": '',
        "daxiang": '木上有火，鼎。君子以正位凝命。',
        "yaoci": [],
        "hexin": '鼎新立极，正位凝命',
        "keywords": ['鼎器', '鼎新', '正位凝命', '元吉亨', '烹任']
    },
    51: {
        "name": '震为雷',
        "short_name": '震',
        "pinyin": 'zhèn',
        "shang": 4,
        "xia": 4,
        "guaci": '亨。震来虩虩，笑言哑哑。震惊百里，不丧匕鬯。',
        "tuan": '',
        "daxiang": '洊雷，震。君子以恐惧修省。',
        "yaoci": [],
        "hexin": '震动警戒，恐惧修省',
        "keywords": ['震动', '戒惧', '恐惧修省', '震惊百里', '不丧匕鬯']
    },
    52: {
        "name": '艮为山',
        "short_name": '艮',
        "pinyin": 'gèn',
        "shang": 7,
        "xia": 7,
        "guaci": '艮其背，不获其身；行其庭，不见其人，无咎。',
        "tuan": '',
        "daxiang": '兼山，艮。君子以思不出其位。',
        "yaoci": [],
        "hexin": '止而不动，思不出其位',
        "keywords": ['艮止', '知止', '思不出位', '其道光明', '时止则止']
    },
    53: {
        "name": '风山渐',
        "short_name": '渐',
        "pinyin": 'jiàn',
        "shang": 5,
        "xia": 7,
        "guaci": '女归吉，利贞。',
        "tuan": '',
        "daxiang": '山上有木，渐。君子以居贤德善俗。',
        "yaoci": [],
        "hexin": '渐进有序，居贤德善俗',
        "keywords": ['渐进', '有序', '居贤德', '善俗', '女归吉', '鸿渐']
    },
    54: {
        "name": '雷泽归妹',
        "short_name": '归妹',
        "pinyin": 'guī mèi',
        "shang": 4,
        "xia": 2,
        "guaci": '征凶，无攸利。',
        "tuan": '',
        "daxiang": '泽上有雷，归妹。君子以永终知敝。',
        "yaoci": [],
        "hexin": '少女归嫁，永终知敝',
        "keywords": ['归妹', '嫁娶', '永终知敝', '征凶', '无攸利']
    },
    55: {
        "name": '雷火丰',
        "short_name": '丰',
        "pinyin": 'fēng',
        "shang": 4,
        "xia": 3,
        "guaci": '亨，王假之。勿忧，宜日中。',
        "tuan": '',
        "daxiang": '雷电皆至，丰。君子以折狱致刑。',
        "yaoci": [],
        "hexin": '丰盛盛大，折狱致刑',
        "keywords": ['丰盛', '盛大', '折狱致刑', '日中则昃', '月盈则食']
    },
    56: {
        "name": '火山旅',
        "short_name": '旅',
        "pinyin": 'lǚ',
        "shang": 3,
        "xia": 7,
        "guaci": '小亨，旅贞吉。',
        "tuan": '',
        "daxiang": '山上有火，旅。君子以明慎用刑而不留狱。',
        "yaoci": [],
        "hexin": '旅居在外，明慎用刑而不留狱',
        "keywords": ['旅居', '行旅', '明慎用刑', '不留狱', '小亨', '旅贞吉']
    },
    57: {
        "name": '巽为风',
        "short_name": '巽',
        "pinyin": 'xùn',
        "shang": 5,
        "xia": 5,
        "guaci": '小亨，利有攸往，利见大人。',
        "tuan": '',
        "daxiang": '随风，巽。君子以申命行事。',
        "yaoci": [],
        "hexin": '巽入顺从，申命行事',
        "keywords": ['巽入', '顺从', '申命行事', '小亨', '利有攸往', '利见大人']
    },
    58: {
        "name": '兑为泽',
        "short_name": '兑',
        "pinyin": 'duì',
        "shang": 2,
        "xia": 2,
        "guaci": '亨，利贞。',
        "tuan": '',
        "daxiang": '丽泽，兑。君子以朋友讲习。',
        "yaoci": [],
        "hexin": '和悦欣悦，朋友讲习',
        "keywords": ['兑悦', '欣悦', '朋友讲习', '亨', '利贞', '说以先民']
    },
    59: {
        "name": '风水涣',
        "short_name": '涣',
        "pinyin": 'huàn',
        "shang": 5,
        "xia": 6,
        "guaci": '亨，王假有庙。利涉大川，利贞。',
        "tuan": '',
        "daxiang": '风行水上，涣。先王以享于帝，立庙。',
        "yaoci": [],
        "hexin": '涣散分离，享于帝立庙',
        "keywords": ['涣散', '分离', '享于帝', '立庙', '王假有庙', '利涉大川']
    },
    60: {
        "name": '水泽节',
        "short_name": '节',
        "pinyin": 'jié',
        "shang": 6,
        "xia": 2,
        "guaci": '亨。苦节不可贞。',
        "tuan": '',
        "daxiang": '泽上有水，节。君子以制数度，议德行。',
        "yaoci": [],
        "hexin": '节制节度，制数度议德行',
        "keywords": ['节制', '节度', '制数度', '议德行', '苦节不可贞', '亨']
    },
    61: {
        "name": '风泽中孚',
        "short_name": '中孚',
        "pinyin": 'zhōng fú',
        "shang": 5,
        "xia": 2,
        "guaci": '豚鱼吉，利涉大川，利贞。',
        "tuan": '',
        "daxiang": '泽上有风，中孚。君子以议狱缓死。',
        "yaoci": [],
        "hexin": '中心诚信，议狱缓死',
        "keywords": ['中孚', '诚信', '议狱缓死', '信及豚鱼', '利涉大川']
    },
    62: {
        "name": '雷山小过',
        "short_name": '小过',
        "pinyin": 'xiǎo guò',
        "shang": 4,
        "xia": 7,
        "guaci": '亨，利贞。可小事，不可大事。飞鸟遗之音，不宜上，宜下，大吉。',
        "tuan": '',
        "daxiang": '山上有雷，小过。君子以行过乎恭，丧过乎哀，用过乎俭。',
        "yaoci": [],
        "hexin": '小有过越，行过乎恭，丧过乎哀，用过乎俭',
        "keywords": ['小过', '过越', '救小过', '可小事不可大事', '宜下不宜上']
    },
    63: {
        "name": '水火既济',
        "short_name": '既济',
        "pinyin": 'jì jì',
        "shang": 6,
        "xia": 3,
        "guaci": '亨小，利贞。初吉，终乱。',
        "tuan": '',
        "daxiang": '水在火上，既济。君子以思患而豫防之。',
        "yaoci": [],
        "hexin": '事已成就，思患而豫防之',
        "keywords": ['既济', '已成', '思患预防', '初吉终乱', '亨小']
    },
    64: {
        "name": '火水未济',
        "short_name": '未济',
        "pinyin": 'wèi jì',
        "shang": 3,
        "xia": 6,
        "guaci": '亨。小狐汔济，濡其尾，无攸利。',
        "tuan": '',
        "daxiang": '火在水上，未济。君子以慎辨物居方。',
        "yaoci": [],
        "hexin": '事未完成，慎辨物居方',
        "keywords": ['未济', '未成', '慎辨物居方', '小狐汔济', '濡其尾']
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
    print(f"  卦辞：{gua.get('guaci') or '（待补充）'}")
    if gua.get('tuan'):
        print(f"  彖传：{gua['tuan'][:80]}...")
    else:
        print("  彖传：（待补充）")
    print(f"  大象：{gua.get('daxiang') or '（待补充）'}")
    yaoci = gua.get('yaoci') or []
    if yaoci:
        print("\n  爻辞：")
        for yao in yaoci:
            print(f"    {yao}")
    else:
        print("\n  爻辞：（该卦暂未收录完整爻辞，可参考卦辞/大象传）")
    print(f"\n  核心含义：{gua.get('hexin') or '（待补充）'}")
    keywords = gua.get('keywords') or []
    print(f"  关键词：{' | '.join(keywords) if keywords else '（待补充）'}")
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

        def yao_text(g, idx):
            yaoci = g.get('yaoci') or []
            if 1 <= idx <= len(yaoci):
                return yaoci[idx - 1]
            return None

        n = len(bian_yao)
        if n == 0:
            print("  六爻不变 → 本卦卦辞断之")
        elif n == 1:
            print(f"  一爻变 → 本卦第{bian_yao[0]}爻爻辞断之")
            t = yao_text(gua, bian_yao[0])
            print(f"  → {t}" if t else "  → 该卦暂未收录完整爻辞，建议参考本卦卦辞")
        elif n == 2:
            print(f"  二爻变 → 本卦二变爻爻辞，以上爻（第{bian_yao[1]}爻）为主")
            t1 = yao_text(gua, bian_yao[0])
            t2 = yao_text(gua, bian_yao[1])
            if t1:
                print(f"  → 本卦第{bian_yao[0]}爻：{t1}")
            else:
                print(f"  → 本卦第{bian_yao[0]}爻：暂未收录完整爻辞")
            if t2:
                print(f"  → 本卦第{bian_yao[1]}爻：{t2}（为主）")
            else:
                print(f"  → 本卦第{bian_yao[1]}爻：暂未收录完整爻辞（为主）")
        elif n == 3:
            print(f"  三爻变 → 本卦卦辞（贞）+ 变卦卦辞（悔）")
            print(f"  → 本卦卦辞：{gua.get('guaci') or '（待补充）'}")
            print(f"  → 变卦卦辞：{bgua.get('guaci') or '（待补充）'}")
        elif n == 4:
            no_bian = [y for y in range(1, 7) if y not in bian_yao]
            print(f"  四爻变 → 变卦不变爻爻辞，以下爻（第{no_bian[0]}爻）为主")
            t = yao_text(bgua, no_bian[0])
            print(f"  → 变卦第{no_bian[0]}爻：{t}" if t else f"  → 变卦第{no_bian[0]}爻：暂未收录完整爻辞")
        elif n == 5:
            no_bian = [y for y in range(1, 7) if y not in bian_yao][0]
            print(f"  五爻变 → 变卦唯一不变爻（第{no_bian}爻）爻辞断之")
            t = yao_text(bgua, no_bian)
            print(f"  → 变卦第{no_bian}爻：{t}" if t else f"  → 变卦第{no_bian}爻：暂未收录完整爻辞")
        elif n == 6:
            if seq == 1:
                print("  六爻全变（乾卦）→ 用九：见群龙无首，吉。")
            elif seq == 2:
                print("  六爻全变（坤卦）→ 用六：利永贞。")
            else:
                print("  六爻全变 → 变卦卦辞断之")
                print(f"  → 变卦卦辞：{bgua.get('guaci') or '（待补充）'}")
    else:
        print("📏 六爻皆静 → 本卦卦辞断之")
        print(f"  → 本卦卦辞：{gua.get('guaci') or '（待补充）'}")


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
