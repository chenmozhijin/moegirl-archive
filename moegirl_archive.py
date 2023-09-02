# -*- coding: utf-8 -*-
"""Python 3.8.0
对列出的页面进行存档

Jan 7, 2020
Jan 15, 2020
Jan 21, 2020
Feb 18, 2020
Hu Xiangyou
"""

# 导入必要的模块
import requests  # 用于发送HTTP请求
import time  # 用于时间相关操作
import os  # 用于文件系统操作
import socket  # 用于获取主机名
import re

# 打印脚本的文档字符串（注释）
print(__doc__)

# 配置文件路径和文件名
listPath = "PAGELIST.txt"  # 存放页面列表的文件路径
fold = "archive/"  # 存档文件夹路径
fileData = "!.txt"  # 存档数据文件名

file_encoding = 'UTF-8'  # 文件编码

url = "https://zh.moegirl.org/api.php"  # 请求的URL地址

# 请求参数
params1 = {'action': 'query', 'format': 'json', 'prop': 'info', 'curtimestamp': 1, 'indexpageids': 1}
params = {'action': 'query', 'format': 'json', 'prop': 'cirrusdoc', 'curtimestamp': 1, 'indexpageids': 1}

# 打开页面列表文件
f = open(listPath, 'r', encoding=file_encoding)
pagelistfile = f.read().splitlines()
f.close()

pageidlist = []  # 存放页面ID的列表
for pageline in pagelistfile:
    # 如果页面列表行以[M___]、[T___]、[C___]开头，提取页面ID并添加到pageidlist中
    if pageline.split("\t")[0] in ('[M___]', '[T___]', '[C___]'):
        pageidlist.append(int(pageline.split("\t")[1]))

n_all = 0  # 总共处理的页面数
n_new = 0  # 新存档页面数
n_overridden = 0  # 被覆盖的页面数
n_moved = 0  # 被移动的页面数
n_error = 0  # 出错次数

# 打开存档数据文件
f = open(fold + fileData, 'r', encoding=file_encoding)
reviddict = eval(f.read())
f.close()

# 将列表拆分为指定长度的子列表
def devide(l: list, n: int) -> list:
    for i in range(0, len(l), n):
        yield l[i:i + n]

# 将秒数转换为可读时间格式
def second2days(seconds: float = 0.00) -> str:
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    y, d = divmod(d, 365)

    y = str(int(y)) + " 年" if y else ""
    d = str(int(d)) + " 天" if d else ""
    h = str(int(h)) + " 小时" if h else ""
    m = str(int(m)) + " 分钟" if m else ""
    s = str(round(s, 2)) + " 秒" if s else ""

    return " ".join(i for i in (y, d, h, m, s) if i)

# 检查响应是否正常
def isResponceOK(json: dict) -> bool:
    if 'batchcomplete' in json:
        return True
    else:
        print("响应不完整。可能因为请求的数据量过大。请调整请求的数据量。")
        return False

# 保存存档数据到文件
def saveData():
    f = open(fold + fileData, 'w', encoding=file_encoding)
    f.write(str(reviddict))
    f.close()

start_time = time.time()
print("开始于", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time)))

# 将页面ID列表拆分为每组50个ID
for pageidlist_d in devide(pageidlist, 50):
    l_param: str = "|".join(str(i) for i in pageidlist_d)
    while True:
        try:
            # 发送GET请求获取页面信息
            a = requests.get(url, params={**params1, **{'requestid': time.time(), 'pageids': l_param}}, timeout=(10, 30))
            json: dict = a.json()
        except:
            print("[出错]\t网络问题，正在重试")
            n_error += 1
            continue
        else:
            if isResponceOK(json):
                break

    for pageid in pageidlist_d:
        if pageid not in reviddict or \
                reviddict[pageid][0] != json['query']['pages'][str(pageid)]['lastrevid'] or \
                reviddict[pageid][1] != json['query']['pages'][str(pageid)]['title']:
            while True:
                try:
                    # 发送GET请求获取页面内容
                    b = requests.get(url, params={**params, **{'pageids': pageid}}, timeout=(10, 30))
                except:
                    print("[出错]\t网络问题，正在重试")
                    n_error += 1
                    continue
                else:
                    if b.ok:
                        json2: dict = b.json()
                        if isResponceOK(json2):
                            break
            pageJson = json2['query']['pages'][str(pageid)]
            if 'cirrusdoc' in pageJson:
                content = pageJson['cirrusdoc'][0]['source']['text']
                title = pageJson['title']
                revid = pageJson['cirrusdoc'][0]['source']['version']
                content = re.sub(r'萌娘百科欢迎您参与完善本条目☆Kira~   欢迎正在阅读这个条目的您协助编辑本条目。编辑前请阅读Wiki入门或条目编辑规范，并查找相关资料。萌娘百科祝您在本站度过愉快的时光。   ', r'', content)
                data = [{"title": title, "pageid": pageid, "text": content, "source": "moegril"}]
                # 将标题中的特殊字符替换为安全字符，用于构建存档文件名
                title_in_file = title.replace("/", "／").replace(":", "：").replace("\\", "＼").replace("*", "＊").replace("?","？").replace("\"", "＂").replace("<", "＜").replace(">", "＞").replace("|", "｜")
                import json
                if os.path.isfile(fold + title_in_file + ".json"):
                    if pageid in reviddict and reviddict[pageid][0] == revid and reviddict[pageid][1] == title:
                        # print("[－]","\t[P]",pageid,"\t[R]",revid,"\t[标题]",title)
                        pass
                    else:
                        with open(fold + title_in_file + ".json", 'w', encoding=file_encoding) as output_file:
                            json.dump(data, output_file, ensure_ascii=False, indent=4)
                        f.close()
                        print("[覆]","\t[P]",pageid,"\t[R]",revid,"\t[标题]",title)
                        n_overridden += 1
                else:
                    #f = open(fold + title_in_file + ".txt", 'w', encoding=file_encoding)
                    #f.write(content)
                    #f.close()
                    with open(fold + title_in_file + ".json", 'w', encoding=file_encoding) as output_file:
                        json.dump(data, output_file, ensure_ascii=False, indent=4)
                    f.close()
                    print("[新]","\t[P]",pageid,"\t[R]",revid,"\t[标题]",title)
                    n_new += 1
                if pageid in reviddict and title != reviddict[pageid][1]:
                    print("[移]","\t", reviddict[pageid][1], "->", title, "\t[注意] 请手动删除之前的存档。")
                    n_moved += 1
                reviddict[pageid] = (revid, title)
        n_all += 1

# 更新存档数据
reviddict['info'] = "萌娘百科页面存档"
reviddict['time'] = json2['curtimestamp']
reviddict['by'] = socket.getfqdn(socket.gethostname())

saveData()

print()
end_time = time.time()
print("结束于", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(end_time)))
print("耗时", second2days(end_time - start_time))

print(n_all, "个已检查。")
print(n_new, "个新存档。", n_overridden, "个被覆盖。", n_moved, "个被移动。")
print("期间共出错", n_error, "次。")

print("完成。")

