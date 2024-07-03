import re
import matplotlib.pyplot as plt
import pandas as pd
import os
from jsonpath import jsonpath
import requests
import json
from matplotlib import rcParams
# 导入数据解析模块
import parsel

# 保存路径
save_path = './fanqie/'
# #要命名的文件名
name = 'data.csv'
filename = save_path + name
# #目标url of 番茄巅峰榜
# url = 'https://fanqienovel.com/api/author/misc/top_book_list/v1/?limit=200&offset=0&a_bogus=QysQfcZTMsm17jVEl7ke9aJm32R0YWR-gZEFKy4r-0Ll'
# headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    'cookie': 'novel_web_id=1314981381011154749; s_v_web_id=verify_ly3rzkf3_glbXpxut_9hSm_427e_9cxM_hEcxmaoJuqYe; ttwid=1%7CsDIlEMBJoRB76T_Q2yHyDBOOUWMjDN3PtU_qF6aGQ2w%7C1719886449%7Cda5b1fbea7af85ea8f52533365a43d32600f0808a4d04475df84212b484f6e5e; csrf_session_id=37b0f1d401c59ee8cc7ce2ef73a1e37e; msToken=_h_FeLwRFmYDcAepCds6yYEGaZNp-8xk7Tikz2abNJpUBxBIdXZg6KLfxiChzQ4tYfNnGIjRdvNWfPvZ-MoLqjacdTgPhtD9h9e3L_wcanb5xrOpzbZsi1_61eJf5NA=; ttwid=1%7CsDIlEMBJoRB76T_Q2yHyDBOOUWMjDN3PtU_qF6aGQ2w%7C1719980712%7C39a71225c57b5c6662a0af77f2c90e7fd9009c486a4092edce9d8bd92dc2a48d'
    , 'Referer': 'https://fanqienovel.com/library?enter_from=menu'
    , 'Priority': 'u=1, i'
}


# 获取书籍数据
def get_book_dict(url):
    r = requests.get(url, headers=headers, timeout=10)
    book_dict = json.loads(r.text)
    return book_dict


# 把数据写入csv文件
def save_csv(book_dict, save_path='./fanqie/', name='data.csv'):
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    try:
        os.remove(save_path + name)
    except:
        pass
    with open(save_path + name, 'a', encoding='utf-8', newline='') as f:
        f.write('书名,作者,类型,ID,评分,封面链接\n')
        for book in jsonpath(book_dict, '$..book_list[*]'):
            f.write(
                book['book_name'] + ',' + book['author'] + ',' + book['category'] + ',' + book['book_id'] + ',' + book[
                    'rank_score'] + ',' + book['thumb_url'] + '\n')
            # print("写入csv文件完成")
    return 1


def save_csv_phb(book_dict, save_path='./fanqie/', name='data.csv'):
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    try:
        os.remove(save_path + name)
    except:
        pass
    with open(save_path + name, 'a', encoding='utf-8', newline='') as f:
        f.write('书名,作者,作品简述,ID,阅读量,封面链接\n')
        for book in jsonpath(book_dict, '$..book_list[*]'):
            f.write(
                book['book_name'] + ',' + book['author'] + ',' + book['abstract'] + ',' + book['book_id'] + ',' + book[
                    'read_count'] + ',' + book['thumb_url'] + '\n')
            # print("写入csv文件完成")
    return 1


def Type_Summary(filename):
    # 导出“类型”一列的数据
    data = pd.read_csv(filename)
    data_Type = data['类型'].values.tolist()
    data_Type_All = list()
    for i in data_Type:
        # 描述小说用了4个字，分为两个类型
        data_Type_Specific = re.findall(r'.{2}', i)
        # 统计所有出现的类型
        data_Type_All.extend(data_Type_Specific)
    # 统计所有类型出现的次数
    counts = {}
    for i in data_Type_All:
        if len(i) > 1:
            counts[i] = counts.get(i, 0) + 1
    # 词频排序
    data_Type_Counts = sorted(counts.items(), key=lambda x: x[1], reverse=False)
    # print(data_Type_Counts)
    return data_Type_Counts


def Draw_BarChrat(data_Type_Counts):
    config = {
        "font.family": 'serif',
        "mathtext.fontset": 'stix',  # matplotlib渲染数学字体时使用的字体，和Times New Roman差别不大
        "font.serif": ['SimSun'],  # 宋体
        'axes.unicode_minus': False  # 处理负号，即-号
    }
    rcParams.update(config)
    # 提取数据
    types = [item[0] for item in data_Type_Counts]
    counts = [item[1] for item in data_Type_Counts]
    # 创建画布和子图
    fig, ax = plt.subplots()

    # 绘制横向条形图
    ax.barh(types, counts, color='skyblue')

    # 设置标题和标签
    plt.xlabel('出现频率')
    plt.ylabel('类型')
    plt.title('巅峰榜小说类型')

    # 显示图形
    plt.show()
    result = round(float(counts[-1]) * 100 / 30, 2)
    print(f"\n当代书友阅读类型最多的是", types[-1], "占比：", result, "%\n")


# 解密排行榜的字典
dict_data_phb = {
    '58544': '0',
    '58703': '1',
    '58599': '2',
    '58628': '3',
    '58526': '4',
    '58614': '5',
    '58710': '6',
    '58684': '7',
    '58490': '8',
    '58484': '9',
    '58381': 'a',
    '58652': 'b',
    '58503': 'c',
    '58422': 'd',
    '58650': 'e',
    '58427': 'f',
    '58501': 'g',
    '58554': 'h',
    '58488': 'i',
    '58437': 'j',
    '58671': 'k',
    '58522': 'l',
    '58405': 'm',
    '58587': 'n',
    '58379': 'o',
    '58367': 'p',
    '58504': 'q',
    '58491': 'r',
    '58375': 's',
    '58712': 't',
    '58475': 'u',
    '58691': 'v',
    '58391': 'w',
    '58511': 'x',
    '58345': 'y',
    '58666': 'z',
    '58408': 'A',
    '58561': 'B',
    '58497': 'C',
    '58430': 'D',
    '58442': 'E',
    '58579': 'F',
    '58428': 'G',
    '58571': 'H',
    '58600': 'I',
    '58384': 'J',
    '58409': 'K',
    '58598': 'L',
    '58711': 'M',
    '58653': 'N',
    '58364': 'O',
    '58453': 'P',
    '58480': 'Q',
    '58546': 'R',
    '58446': 'S',
    '58421': 'T',
    '58395': 'U',
    '58548': 'V',
    '58606': 'W',
    '58555': 'X',
    '58471': 'Y',
    '58553': 'Z',
    '58355': '的',
    '58662': '一',
    '58454': '是',
    '58647': '了',
    '58382': '我',
    '58641': '不',
    '58396': '人',
    '58687': '在',
    '58701': '他',
    '58560': '有',
    '58483': '这',
    '58619': '个',
    '58698': '上',
    '58451': '们',
    '58664': '来',
    '58447': '到',
    '58411': '时',
    '58432': '大',
    '58496': '地',
    '58562': '为',
    '58685': '子',
    '58412': '中',
    '58505': '你',
    '58492': '说',
    '58533': '生',
    '58410': '国',
    '58565': '年',
    '58696': '着',
    '58435': '就',
    '58707': '那',
    '58495': '和',
    '58400': '要',
    '58374': '她',
    '58568': '出',
    '58366': '也',
    '58399': '得',
    '58536': '里',
    '58676': '后',
    '58564': '自',
    '58591': '以',
    '58655': '会',
    '58594': '家',
    '58626': '可',
    '58424': '下',
    '58705': '而',
    '58681': '过',
    '58700': '天',
    '58445': '去',
    '58520': '能',
    '58668': '对',
    '58417': '小',
    '58459': '多',
    '58532': '然',
    '58625': '于',
    '58476': '心',
    '58581': '学',
    '58414': '么',
    '58689': '之',
    '58624': '都',
    '58622': '好',
    '58670': '看',
    '58440': '起',
    '58462': '发',
    '58523': '当',
    '58407': '没',
    '58693': '成',
    '58468': '只',
    '58397': '如',
    '58457': '事',
    '58456': '把',
    '58582': '还',
    '58623': '用',
    '58617': '第',
    '58508': '样',
    '58448': '道',
    '58699': '想',
    '58469': '作',
    '58549': '种',
    '58620': '开',
    '58660': '美',
    '58509': '总',
    '58642': '从',
    '58455': '无',
    '58378': '情',
    '58669': '己',
    '58433': '面',
    '58372': '最',
    '58635': '女',
    '58588': '但',
    '58347': '现',
    '58470': '前',
    '58651': '些',
    '58575': '所',
    '58627': '同',
    '58632': '日',
    '58525': '手',
    '58431': '又',
    '58713': '行',
    '58584': '意',
    '58550': '动',
    '58573': '方',
    '58563': '期',
    '58444': '它',
    '58515': '头',
    '58473': '经',
    '58667': '长',
    '58657': '儿',
    '58538': '回',
    '58616': '位',
    '58583': '分',
    '58358': '爱',
    '58365': '老',
    '58673': '因',
    '58612': '很',
    '58438': '给',
    '58524': '名',
    '58377': '法',
    '58425': '间',
    '58402': '斯',
    '58357': '知',
    '58682': '世',
    '58640': '什',
    '58659': '两',
    '58629': '次',
    '58506': '使',
    '58603': '身',
    '58577': '者',
    '58661': '被',
    '58559': '高',
    '58394': '已',
    '58547': '亲',
    '58586': '其',
    '58694': '进',
    '58645': '此',
    '58350': '话',
    '58368': '常',
    '58634': '与',
    '58465': '活',
    '58572': '正',
    '58574': '感',
    '58613': '见',
    '58576': '明',
    '58419': '问',
    '58530': '力',
    '58363': '理',
    '58472': '尔',
    '58545': '点',
    '58704': '文',
    '58371': '几',
    '58690': '定',
    '58537': '本',
    '58663': '公',
    '58557': '特',
    '58556': '做',
    '58464': '外',
    '58467': '孩',
    '58674': '相',
    '58458': '西',
    '58485': '果',
    '58413': '走',
    '58376': '将',
    '58352': '月',
    '58346': '十',
    '58441': '实',
    '58418': '向',
    '58529': '声',
    '58426': '车',
    '58482': '全',
    '58633': '信',
    '58527': '重',
    '58649': '三',
    '58644': '机',
    '58618': '工',
    '58353': '物',
    '58683': '气',
    '58387': '每',
    '58638': '并',
    '58708': '别',
    '58539': '真',
    '58678': '打',
    '58386': '太',
    '58463': '新',
    '58589': '比',
    '58656': '才',
    '58349': '便',
    '58654': '夫',
    '58607': '再',
    '58688': '书',
    '58639': '部',
    '58354': '水',
    '58502': '像',
    '58658': '眼',
    '58479': '等',
    '58344': '体',
    '58351': '却',
    '58452': '加',
    '58404': '电',
    '58373': '主',
    '58460': '界',
    '58403': '门',
    '58392': '利',
    '58610': '海',
    '58389': '受',
    '58605': '听',
    '58361': '表',
    '58709': '德',
    '58401': '少',
    '58369': '克',
    '58534': '代',
    '58385': '员',
    '58672': '许',
    '58578': '稜',
    '58494': '先',
    '58416': '口',
    '58592': '由',
    '58593': '死',
    '58486': '安',
    '58436': '写',
    '58512': '性',
    '58566': '马',
    '58380': '光',
    '58611': '白',
    '58643': '或',
    '58580': '住',
    '58715': '难',
    '58388': '望',
    '58390': '教',
    '58552': '命',
    '58521': '花',
    '58679': '结',
    '58518': '乐',
    '58675': '色',
    '58585': '更',
    '58692': '拉',
    '58697': '东',
    '58423': '神',
    '58648': '记',
    '58513': '处',
    '58595': '让',
    '58489': '母',
    '58478': '父',
    '58517': '应',
    '58615': '直',
    '58528': '字',
    '58500': '场',
    '58370': '平',
    '58604': '报',
    '58531': '友',
    '58519': '关',
    '58356': '放',
    '58570': '至',
    '58498': '张',
    '58567': '认',
    '58569': '接',
    '58477': '告',
    '58540': '入',
    '58636': '笑',
    '58535': '内',
    '58551': '英',
    '58393': '军',
    '58714': '候',
    '58481': '民',
    '58621': '岁',
    '58677': '往',
    '58415': '何',
    '58429': '度',
    '58609': '山',
    '58590': '觉',
    '58706': '路',
    '58695': '带',
    '58359': '万',
    '58406': '男',
    '58558': '边',
    '58362': '风',
    '58466': '解',
    '58602': '叫',
    '58493': '任',
    '58601': '金',
    '58348': '快',
    '58608': '原',
    '58450': '吃',
    '58702': '妈',
    '58398': '变',
    '58439': '通',
    '58541': '师',
    '58665': '立',
    '58542': '象',
    '58449': '数',
    '58630': '四',
    '58596': '失',
    '58637': '满',
    '58499': '战',
    '58434': '远',
    '58680': '格',
    '58597': '士',
    '58514': '音',
    '58420': '轻',
    '58510': '目',
    '58686': '条',
    '58383': '呢'
}
# 小说解密
dict_data2_xs = {
    '58670': '0',
    '58413': '1',
    '58678': '2',
    '58371': '3',
    '58353': '4',
    '58480': '5',
    '58359': '6',
    '58449': '7',
    '58540': '8',
    '58692': '9',
    '58712': 'a',
    '58542': 'b',
    '58575': 'c',
    '58626': 'd',
    '58691': 'e',
    '58561': 'f',
    '58362': 'g',
    '58619': 'h',
    '58430': 'i',
    '58531': 'j',
    '58588': 'k',
    '58440': 'l',
    '58681': 'm',
    '58631': 'n',
    '58376': 'o',
    '58429': 'p',
    '58555': 'q',
    '58498': 'r',
    '58518': 's',
    '58453': 't',
    '58397': 'u',
    '58356': 'v',
    '58435': 'w',
    '58514': 'x',
    '58482': 'y',
    '58529': 'z',
    '58515': 'A',
    '58688': 'B',
    '58709': 'C',
    '58344': 'D',
    '58656': 'E',
    '58381': 'F',
    '58576': 'G',
    '58516': 'H',
    '58463': 'I',
    '58649': 'J',
    '58571': 'K',
    '58558': 'L',
    '58433': 'M',
    '58517': 'N',
    '58387': 'O',
    '58687': 'P',
    '58537': 'Q',
    '58541': 'R',
    '58458': 'S',
    '58390': 'T',
    '58466': 'U',
    '58386': 'V',
    '58697': 'W',
    '58519': 'X',
    '58511': 'Y',
    '58634': 'Z',
    '58611': '的',
    '58590': '一',
    '58398': '是',
    '58422': '了',
    '58657': '我',
    '58666': '不',
    '58562': '人',
    '58345': '在',
    '58510': '他',
    '58496': '有',
    '58654': '这',
    '58441': '个',
    '58493': '上',
    '58714': '们',
    '58618': '来',
    '58528': '到',
    '58620': '时',
    '58403': '大',
    '58461': '地',
    '58481': '为',
    '58700': '子',
    '58708': '中',
    '58503': '你',
    '58442': '说',
    '58639': '生',
    '58506': '国',
    '58663': '年',
    '58436': '着',
    '58563': '就',
    '58391': '那',
    '58357': '和',
    '58354': '要',
    '58695': '她',
    '58372': '出',
    '58696': '也',
    '58551': '得',
    '58445': '里',
    '58408': '后',
    '58599': '自',
    '58424': '以',
    '58394': '会',
    '58348': '家',
    '58426': '可',
    '58673': '下',
    '58417': '而',
    '58556': '过',
    '58603': '天',
    '58565': '去',
    '58604': '能',
    '58522': '对',
    '58632': '小',
    '58622': '多',
    '58350': '然',
    '58605': '于',
    '58617': '心',
    '58401': '学',
    '58637': '么',
    '58684': '之',
    '58382': '都',
    '58464': '好',
    '58487': '看',
    '58693': '起',
    '58608': '发',
    '58392': '当',
    '58474': '没',
    '58601': '成',
    '58355': '只',
    '58573': '如',
    '58499': '事',
    '58469': '把',
    '58361': '还',
    '58698': '用',
    '58489': '第',
    '58711': '样',
    '58457': '道',
    '58635': '想',
    '58492': '作',
    '58647': '种',
    '58623': '开',
    '58521': '美',
    '58609': '总',
    '58530': '从',
    '58665': '无',
    '58652': '情',
    '58676': '己',
    '58456': '面',
    '58581': '最',
    '58509': '女',
    '58488': '但',
    '58363': '现',
    '58685': '前',
    '58396': '些',
    '58523': '所',
    '58471': '同',
    '58485': '日',
    '58613': '手',
    '58533': '又',
    '58589': '行',
    '58527': '意',
    '58593': '动',
    '58699': '方',
    '58707': '期',
    '58414': '它',
    '58596': '头',
    '58570': '经',
    '58660': '长',
    '58364': '儿',
    '58526': '回',
    '58501': '位',
    '58638': '分',
    '58404': '爱',
    '58677': '老',
    '58535': '因',
    '58629': '很',
    '58577': '给',
    '58606': '名',
    '58497': '法',
    '58662': '间',
    '58479': '斯',
    '58532': '知',
    '58380': '世',
    '58385': '什',
    '58405': '两',
    '58644': '次',
    '58578': '使',
    '58505': '身',
    '58564': '者',
    '58412': '被',
    '58686': '高',
    '58624': '已',
    '58667': '亲',
    '58607': '其',
    '58616': '进',
    '58368': '此',
    '58427': '话',
    '58423': '常',
    '58633': '与',
    '58525': '活',
    '58543': '正',
    '58418': '感',
    '58597': '见',
    '58683': '明',
    '58507': '问',
    '58621': '力',
    '58703': '理',
    '58438': '尔',
    '58536': '点',
    '58384': '文',
    '58484': '几',
    '58539': '定',
    '58554': '本',
    '58421': '公',
    '58347': '特',
    '58569': '做',
    '58710': '外',
    '58574': '孩',
    '58375': '相',
    '58645': '西',
    '58592': '果',
    '58572': '走',
    '58388': '将',
    '58370': '月',
    '58399': '十',
    '58651': '实',
    '58546': '向',
    '58504': '声',
    '58419': '车',
    '58407': '全',
    '58672': '信',
    '58675': '重',
    '58538': '三',
    '58465': '机',
    '58374': '工',
    '58579': '物',
    '58402': '气',
    '58702': '每',
    '58553': '并',
    '58360': '别',
    '58389': '真',
    '58560': '打',
    '58690': '太',
    '58473': '新',
    '58512': '比',
    '58653': '才',
    '58704': '便',
    '58545': '夫',
    '58641': '再',
    '58475': '书',
    '58583': '部',
    '58472': '水',
    '58478': '像',
    '58664': '眼',
    '58586': '等',
    '58568': '体',
    '58674': '却',
    '58490': '加',
    '58476': '电',
    '58346': '主',
    '58630': '界',
    '58595': '门',
    '58502': '利',
    '58713': '海',
    '58587': '受',
    '58548': '听',
    '58351': '表',
    '58547': '德',
    '58443': '少',
    '58460': '克',
    '58636': '代',
    '58585': '员',
    '58625': '许',
    '58694': '稜',
    '58428': '先',
    '58640': '口',
    '58628': '由',
    '58612': '死',
    '58446': '安',
    '58468': '写',
    '58410': '性',
    '58508': '马',
    '58594': '光',
    '58483': '白',
    '58544': '或',
    '58495': '住',
    '58450': '难',
    '58643': '望',
    '58486': '教',
    '58406': '命',
    '58447': '花',
    '58669': '结',
    '58415': '乐',
    '58444': '色',
    '58549': '更',
    '58494': '拉',
    '58409': '东',
    '58658': '神',
    '58557': '记',
    '58602': '处',
    '58559': '让',
    '58610': '母',
    '58513': '父',
    '58500': '应',
    '58378': '直',
    '58680': '字',
    '58352': '场',
    '58383': '平',
    '58454': '报',
    '58671': '友',
    '58668': '关',
    '58452': '放',
    '58627': '至',
    '58400': '张',
    '58455': '认',
    '58416': '接',
    '58552': '告',
    '58614': '入',
    '58582': '笑',
    '58534': '内',
    '58701': '英',
    '58349': '军',
    '58491': '候',
    '58467': '民',
    '58365': '岁',
    '58598': '往',
    '58425': '何',
    '58462': '度',
    '58420': '山',
    '58661': '觉',
    '58615': '路',
    '58648': '带',
    '58470': '万',
    '58377': '男',
    '58520': '边',
    '58646': '风',
    '58600': '解',
    '58431': '叫',
    '58715': '任',
    '58524': '金',
    '58439': '快',
    '58566': '原',
    '58477': '吃',
    '58642': '妈',
    '58437': '变',
    '58411': '通',
    '58451': '师',
    '58395': '立',
    '58369': '象',
    '58706': '数',
    '58705': '四',
    '58379': '失',
    '58567': '满',
    '58373': '战',
    '58448': '远',
    '58659': '格',
    '58434': '士',
    '58679': '音',
    '58432': '轻',
    '58689': '目',
    '58591': '条',
    '58682': '呢'
}


def get_request(url, headers, dict_data):
    r = requests.get(url, headers=headers)
    # 解决文字加密问题
    content = r.text
    novel_content = ''
    for index in content:
        try:
            word = dict_data[str(ord(index))]
        except:
            word = index
        novel_content += word
    j1 = json.loads(novel_content)
    return j1


# 展示排行榜上的书籍
def show_books(j1, page_count):
    # print(jsonpath(j1, '$..book_list[*].book_name'))
    print(j1)
    page_count = int(page_count)
    for i in range(0, page_count):
        print("序号：", i + 1)
        print("书名：", jsonpath(j1, '$..book_list[%d].book_name' % i)[0])
        print("作者：", jsonpath(j1, '$..book_list[%d].author' % i)[0])
        if jsonpath(j1, '$..book_list[%d].read_count' % i):
            print("阅读量：", jsonpath(j1, '$..book_list[%d].read_count' % i)[0], "\n")
        elif jsonpath(j1, '$..book_list[%d].rank_score' % i):
            print("巅峰值：", jsonpath(j1, '$..book_list[%d].rank_score' % i)[0], "\n")


# 把小说封面爬取下来
def download_books_images(book_dict, headers, save_path='./fanqie/'):
    # 确保保存目录存在
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for book in jsonpath(book_dict, '$..book_list[*]'):
        try:
            # 构建完整的文件保存路径
            file_path = os.path.join(save_path, f"{book['book_name']}.png")

            # 发起请求获取图片数据
            response = requests.get(book['thumb_url'], headers=headers)
            response.raise_for_status()  # 检查请求是否成功

            # 保存图片到本地
            with open(file_path, 'wb') as f:
                f.write(response.content)

        except requests.RequestException as e:
            print(f"下载{book['book_name']}图片时发生错误: {e}")
        finally:
            # 显式关闭响应对象
            response.close()
            print(f"{book['book_name']}图片下载完成")


# 保存小说图片
def save_book_img(book_dict, j, save_path='./fanqie/'):
    j = str(j)
    # 确保保存目录存在
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for book in jsonpath(book_dict, '$..book_list[' + j + ']'):
        # 构建完整的文件保存路径
        file_path = os.path.join(save_path, f"{book['book_name']}.png")

        # 发起请求获取图片数据
        response = requests.get(book['thumb_url'], headers=headers)
        response.raise_for_status()  # 检查请求是否成功

        # 保存图片到本地
        with open(file_path, 'wb') as f:
            f.write(response.content)
            print(f"{book['book_name']}图片下载完成")


# 保存小说内容
def save_book_text(book_dict, j, save_path='./fanqie/'):
    print("正在下载小说内容...")
    j = str(j)
    # url地址(小说主页)
    id = jsonpath(book_dict, '$..book_list[' + j + '].book_id')[0]
    id = str(id)
    urls = 'https://fanqienovel.com/page/' + id + '?enter_from=stack-room'
    # print(urls)
    # 发送请求
    response = requests.get(url=urls, headers=headers, timeout=30)
    # 获取响应的文本数据 (html字符串数据)
    html = response.text
    """解析数据: 提取我们需要的数据内容"""
    # 把html字符串数据转成可解析对象
    selector = parsel.Selector(html)
    # 提取书名
    name = selector.css('.info-name h1::text').get()
    # 提取章节名
    title_list = selector.css('.chapter-item-title::text').getall()
    # 提取章节ID
    href = selector.css('.chapter-item-title::attr(href)').getall()
    # print(name)
    # print(title_list)
    # print(href)
    # for循环遍历, 提取列表里元素
    for title, link in zip(title_list, href):
        # print(title)
        # 完整的小说章节链接
        link_url = 'https://fanqienovel.com' + link
        # 发送请求+获取数据内容
        link_data = requests.get(url=link_url, headers=headers).text
        # print(link_data)
        # 解析数据: 提取小说内容
        link_selector = parsel.Selector(link_data)
        # 提取小说内容
        content_list = link_selector.css('.muye-reader-content-16 p::text').getall()
        # print(content_list)
        # 把列表合并成字符串 \n 换行符
        content = '\n\n'.join(content_list)
        # print(content)
        # print(link_url)
        novel_content = ''
        for index in content:
            try:
                word = dict_data2_xs[str(ord(index))]
            except:
                word = index
            novel_content += word
        with open(save_path + name + '.txt', mode='a', encoding='utf-8') as f:
            f.write(title)
            f.write('\n\n')
            f.write(novel_content)
            f.write('\n\n')
    print(name, "小说下载完成")
    return 1


#
if __name__ == '__main__':

    urli = 'https://fanqienovel.com/api/author/misc/top_book_list/v1/?limit=200&offset=0&a_bogus=QysQfcZTMsm17jVEl7ke9aJm32R0YWR-gZEFKy4r-0Ll'
    while True:
        n1 = int(input("功能列表：\n"
                       "1.分析当代书友的阅读风格\n"
                       "2.查看书库排行榜\n"
                       "3.一键爬取功能\n"
                       "其他数字.退出\n"
                       "请输入功能序号："))
        if n1 == 1:
            urli = 'https://fanqienovel.com/api/author/misc/top_book_list/v1/?limit=200&offset=0&a_bogus=QysQfcZTMsm17jVEl7ke9aJm32R0YWR-gZEFKy4r-0Ll'
            book_dict = get_book_dict(urli)
            save_path = './fanqie/'
            name = 'data.csv'
            filename = save_path + name
            save_csv(book_dict, save_path, name)
            data_Type_Counts = Type_Summary(filename)
            Draw_BarChrat(data_Type_Counts)
        elif n1 == 2:
            n2 = input("\n排行榜类型：\n"
                       "1.番茄巅峰榜\n"
                       "2.番茄最热榜\n"
                       "3.番茄最新榜\n"
                       "4.番茄字数榜\n"
                       "0.退出\n"
                       "请输入要查看的排行榜类型：")
            page_count = input("请输入要查看的书籍数量：")
            if n2 == '1':
                # 番茄巅峰榜
                urli = 'https://fanqienovel.com/api/author/misc/top_book_list/v1/?limit=' + page_count + '&offset=0&a_bogus=QysQfcZTMsm17jVEl7ke9aJm32R0YWR-gZEFKy4r-0Ll'
                j1 = json.loads(requests.get(urli, headers=headers).text)
                # print(urli)
            elif n2 == '2':
                # 最热榜
                urli = 'https://fanqienovel.com/api/author/library/book_list/v0/?page_count=' + page_count + '&page_index=0&gender=-1&category_id=-1&creation_status=-1&word_count=-1&book_type=-1&sort=0&a_bogus=EJBQfcZOMsm1uf3kUhke9GUmD%2FR0YW-EgZENKgHrw0wj'
                # print(urli)
                j1 = get_request(urli, headers, dict_data_phb)
            elif n2 == '3':
                # 最新榜
                urli = 'https://fanqienovel.com/api/author/library/book_list/v0/?page_count=' + page_count + '&page_index=0&gender=-1&category_id=-1&creation_status=-1&word_count=-1&book_type=-1&sort=1&a_bogus=dyBDfcZOMsm1Rf3kYXke9b4mD%2Fj0YWRagZENKsNG30on'
                # print(urli)
                j1 = get_request(urli, headers, dict_data_phb)
            elif n2 == '4':
                # 字数榜
                urli = 'https://fanqienovel.com/api/author/library/book_list/v0/?page_count=' + page_count + '&page_index=0&gender=-1&category_id=-1&creation_status=-1&word_count=-1&book_type=-1&sort=2&a_bogus=my4O6cZOMsm1vE3kYhke9CUmDhR0YWR6gZENKswpR0qH'
                # print(urli)
                j1 = get_request(urli, headers, dict_data_phb)
            elif n2 == 0:
                exit()

            show_books(j1, page_count)
            j = input("请输入要下载的书籍序号：")
            k1 = input("请输入存储路径回车键默认：")
            if k1 != '':
                save_path = k1
            jc = int(j)
            if jc > 0 and jc <= int(page_count):
                save_book_img(j1, jc - 1, save_path)
                # print(j1)
                save_book_text(j1, jc - 1, save_path)
            elif int(j) == '0':
                continue
            else:
                print("输入错误！")
            continue
        elif n1 == 3:

            n4 = input("\n请输入要爬取的榜单\n"
                       "1.番茄巅峰榜\n"
                       "2.番茄最热榜\n"
                       "3.番茄最新榜\n"
                       "4.番茄字数榜\n"
                       "其他数字退出\n")
            k2 = input("请输入存储路径回车键默认：")
            if k2 != '':
                save_path = k2
            if n4 == '1':
                urli = 'https://fanqienovel.com/api/author/misc/top_book_list/v1/?limit=200&offset=0&a_bogus=QysQfcZTMsm17jVEl7ke9aJm32R0YWR-gZEFKy4r-0Ll'
                j1 = json.loads(requests.get(urli, headers=headers).text)
                download_books_images(j1, headers, save_path)
                save_csv(j1, save_path, '番茄巅峰榜.csv')
            if n4 == '2':
                urli = 'https://fanqienovel.com/api/author/library/book_list/v0/?page_count=30&page_index=0&gender=-1&category_id=-1&creation_status=-1&word_count=-1&book_type=-1&sort=0&a_bogus=EJBQfcZOMsm1uf3kUhke9GUmD%2FR0YW-EgZENKgHrw0wj'
                j1 = get_request(urli, headers, dict_data_phb)
                download_books_images(j1, headers, save_path)
                save_csv_phb(j1, save_path, '番茄最热.csv')
            if n4 == '3':
                urli = 'https://fanqienovel.com/api/author/library/book_list/v0/?page_count=30&page_index=0&gender=-1&category_id=-1&creation_status=-1&word_count=-1&book_type=-1&sort=1&a_bogus=dyBDfcZOMsm1Rf3kYXke9b4mD%2Fj0YWRagZENKsNG30on'
                j1 = get_request(urli, headers, dict_data_phb)
                download_books_images(j1, headers, save_path)
                save_csv_phb(j1, save_path, '番茄最新榜.csv')
            if n4 == '4':
                urli = 'https://fanqienovel.com/api/author/library/book_list/v0/?page_count=30&page_index=0&gender=-1&category_id=-1&creation_status=-1&word_count=-1&book_type=-1&sort=2&a_bogus=my4O6cZOMsm1vE3kYhke9CUmDhR0YWR6gZENKswpR0qH'
                j1 = get_request(urli, headers, dict_data_phb)
                download_books_images(j1, headers, save_path)
                save_csv_phb(j1, save_path, '番茄字数榜.csv')
            else:
                continue
        else:
            exit()
