import requests
import json
from jsonpath import jsonpath
import os
from lxml import etree

#目标url of 番茄巅峰榜
url = 'https://fanqienovel.com/api/author/misc/top_book_list/v1/?limit=200&offset=0&a_bogus=QysQfcZTMsm17jVEl7ke9aJm32R0YWR-gZEFKy4r-0Ll'

#headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'
    ,'cookie':'csrf_session_id=ecc1986ed4e8cdfe3a06dfe01285fa8e; s_v_web_id=verify_ly3qomo2_YbogndOi_P9uK_4NB6_8CYW_FsTfqhp6OoPd; novel_web_id=7386846545851434505; ttwid=1%7C-n-jiMa0TuCOPkCYZwrd8_Xpn9Nc2YovLKk8V4ONXv4%7C1719884402%7Cd4e110824fc3fa733e5b77bb41293daff10fc51e14be1376f440e2bb0ccc9dee; msToken=acpdNP7HJyaV7GUMudUbSdsV5y4n-xa-jGbYWEY6uBw4byUx-XT7UcAgrYzTiJeOeUCboYYpJa5o1geUcUzP-z9U12Hb9rAcP9VgxET_'
    ,'Referer':'https://fanqienovel.com/'
    ,'Priority':'u=1, i'
}

#预处理,获取小说的相关json信息
def get_book_dict(url,headers):
    r = requests.get(url,headers=headers,timeout=10)
    js = json.loads(r.text)
    return js

#写入路径默认fanqie文件夹
save_path = './fanqie/'
#要命名的文件名
name = 'data.csv'
#把数据写入csv文件
def save_csv(book_dict, save_path='./fanqie/',name=name):
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    try:
        os.remove(save_path+name)
    except:
        pass
    with open(save_path+name,'a',encoding='utf-8',newline='') as f:
        f.write('书名,作者,类型,ID,评分,封面链接\n')
        for book in jsonpath(book_dict, '$..book_list[*]'):
            f.write(book['book_name']+','+book['author']+','+book['category']+','+book['book_id']+','+book['rank_score']+','+book['thumb_url']+'\n')
    print("写入csv文件完成")
#调用函数将小说信息储存
save_csv(get_book_dict(url),save_path,name)

#把小说封面爬取下来
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


# 调用函数，传入相应的参数
# download_books_images(get_book_dict(url), headers,save_path)

