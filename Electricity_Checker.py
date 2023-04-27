import os
import requests


# 获取电费
def get_electricity(bark_url, dyid, pid):
    url = 'https://hqpay.ctbu.edu.cn/weixin/ashx/frmuser.ashx'
    # 设置自定义的User-Agent头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.39'
    }

    params = {
        'test': 'lastlist',
        'pid': pid,
        'dyid': dyid
    }
    # 发送请求并获取响应
    response = requests.get(url, headers=headers, params=params)
    # 输出响应内容
    result = eval(response.text)
    value = result[0][1]
    date = result[0][2]
    electricity = result[0][3]

    # 调用Bark_notification函数推送电费信息到手机
    Bark_notification(bark_url, value, date, electricity)
    # 调用Bark_notification函数推送电费信息到手机
    Server_notification(sckey, value, date, electricity)


# Bark推送电费信息到手机
def Bark_notification(bark_url, value, date, electricity):
    title = '电费查询结果'
    message = f'当前余额：{value}\n扣费日期：{date}\n当月电费：{electricity}'
    if float(value) < 10:
        message += '\n余额不足10元，请及时充值！'
    params = {
        'title': title,
        'body': message
    }
    requests.get(bark_url, params=params)


# Server酱推送
def Server_notification(sckey, value, date, electricity):
    url = 'https://sc.ftqq.com/{}.send'.format(sckey)
    title = '电费查询结果'
    message = f'当前余额：{value}\n扣费日期：{date}\n当月电费：{electricity}'
    if float(value) < 10:
        message += '\n余额不足10元，请及时充值！'
    data = {
        'text': title,
        'desp': message
    }
    response = requests.post(url, data=data)


# 从环境变量中获取参数
bark_url = os.environ['BARK_URL']
sckey = os.environ['SCKEY']
dyid = os.environ['DYID']
pid = os.environ['PID']


# 运行脚本
get_electricity(bark_url, sckey, dyid, pid)
